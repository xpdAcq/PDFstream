import os
import typing as tp
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyperclip
from diffpy.srfit.fitbase import FitContribution, FitResults
from diffpy.srfit.pdf import PDFGenerator, DebyePDFGenerator

from pdfstream.modeling.fitobjs import MyRecipe

__all__ = [
    'summarize',
    'gen_fs_save'
]


def _make_df(recipe: MyRecipe) -> tp.Tuple[pd.DataFrame, FitResults]:
    """Make the fitting result data frame."""
    df = pd.DataFrame()
    res = FitResults(recipe)
    df["name"] = ["Rw", "half_chi2", "penalty"] + res.varnames
    df["val"] = [res.rw, res.chi2 / 2, res.penalty] + res.varvals.tolist()
    df["std"] = [np.nan, np.nan, np.nan] + res.varunc
    df = df.set_index("name")
    return df, res


def save_csv(recipe: MyRecipe, base_name: str) -> tp.Tuple[str, dict]:
    """Save fitting results to a csv file.

    Parameters
    ----------
    recipe : MyRecipe
        The fit recipe.

    base_name : str
        The base name for saving. The saving name will be "{base_name}.csv"

    Returns
    -------
    csv_file : str
        The path to the csv file.

    goodness : dict
        The metric of the goodness of the fit.
    """
    df, res = _make_df(recipe)
    csv_file = rf"{base_name}.csv"
    df.to_csv(csv_file)

    goodness = {
        'rw': res.rw,
        'half_chi2': res.chi2 / 2,
        'penalty': res.penalty
    }
    return csv_file, goodness


def save_fgr(contribution: FitContribution, base_name: str, rw: float) -> str:
    """Save fitted PDFs to a four columns txt files with Rw as header.

    Parameters
    ----------
    contribution
        arbitrary number of Fitcontributions.

    base_name
        base name for saving. The saving name will be "{base_name}_{contribution.name}.fgr"

    rw
        value of Rw. It will be in the header as "Rw = {rw}".

    Returns
    -------
    fgr_file : str
        the path to the fgr file.
    """
    fgr_file = rf"{base_name}_{contribution.name}.fgr"
    contribution.profile.savetxt(fgr_file, header=f"Rw = {rw}\nx ycalc y dy")
    return fgr_file


def calc_pgar(contribution: FitContribution, base_name: str, partial_eqs: tp.Dict[str, str] = None) -> str:
    """Calculate the partial PDF.

    Parameters
    ----------
    contribution
        The FitContribution to calculate the partial PDF.
    base_name
        The base name for the saving file.
    partial_eqs
        The mapping from the phase name to their equation.

    Returns
    -------
    pgr_file
        The path to the partial pdf data file. It is a multi-column data file with header.
    """
    data = [contribution.profile.x]
    columns = ["r"]
    for phase_name, equation in partial_eqs.items():
        ycalc = contribution.evaluateEquation(equation)
        data.append(ycalc)
        columns.append(phase_name)
    data_array = np.column_stack(data)
    header = " ".join(columns)
    pgr_file = f"{base_name}_{contribution.name}.pgr"
    np.savetxt(pgr_file, data_array, fmt="%.8e", header=header)
    return pgr_file


def save_cif(generator: tp.Union[PDFGenerator, DebyePDFGenerator], base_name: str, con_name: str,
             ext: str = "cif") -> str:
    """Save refined structure.

    Parameters
    ----------
    generator
        a ProfileGenerator. The structure is inside the "stru" attribute in it.
    base_name
        base name for saving. The saving name will be "{base_name}_{con_name}_{generator.name}."
    con_name
        name of the contribution that the generators belong to.
    ext
        extension of the structure file. It will also determine the structure file type. Default "cif". Only works
        for diffpy structure.
    Returns
    -------
        the path to the cif or xyz files.
    """
    stru_file = rf"{base_name}_{con_name}_{generator.name}.{ext}"
    stru = generator.stru
    try:
        stru.write(stru_file, ext)
    except AttributeError:
        try:
            with open(stru_file, "w") as f:
                stru.CIFOutput(f)
        except AttributeError:
            raise Warning("Fail to save the structure.")
    return stru_file


def _save_all(recipe: MyRecipe, folder: str, csv: str, fgr: str, cif: str) -> None:
    """Save fitting results, fitted PDFs and refined structures to files in one folder and save information in
    DataFrames. The DataFrame will contain columns: 'file' (file paths), 'rw' (Rw value) and other information
    in info.

    Parameters
    ----------
    recipe
        Refined recipe to save.
    folder
        Folder to save the files.
    csv
        The path to the csv file containing fitting results information.
    fgr
        The path to the csv file containing fitted PDFs information.
    cif
        The path to the csv file containing refined structure information.
    """
    print(f"Save {recipe.name} ...\n")
    uid = str(uuid4())[:4]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    name = os.path.join(folder, f"{timestamp}_{uid}")

    csv_file, goodness = save_csv(recipe, name)
    params = ", ".join(recipe.getNames())
    csv_info = dict(recipe_name=recipe.name, **goodness, timestamp=timestamp, csv_file=csv_file,
                    params=params)
    recipe_id = update(csv, csv_info, id_col='recipe_id')

    for con_config in recipe.configs:
        con = getattr(recipe, con_config.name)
        fgr_file = save_fgr(con, base_name=name, rw=goodness.get('rw', 'unknown'))
        config_info = con_config.to_dict()
        if con_config.partial_eqs is not None:
            pgr_file = calc_pgar(con, name, con_config.partial_eqs)
        else:
            pgr_file = None
        fgr_info = dict(recipe_id=recipe_id, **config_info, fgr_file=fgr_file, pgr_file=pgr_file)
        con_id = update(fgr, fgr_info, id_col='con_id')

        for gen_config in con_config.genconfigs:
            gen = getattr(con, gen_config.name)
            cif_file = save_cif(gen, base_name=name, con_name=con_config.name)
            gconfig_info = gen_config.to_dict()
            cif_info = dict(con_id=con_id, recipe_id=recipe_id, **gconfig_info, cif_file=cif_file)
            update(cif, cif_info, id_col='gen_id')
    return


def update(file_path: str, info_dct: dict, id_col: str) -> int:
    """Update the database file (a csv file) by appending the information as a row at the end of the dataframe
    and return a serial id of for the piece of information.

    Parameters
    ----------
    file_path
        The path to the csv file that stores the information.
    info_dct
        The dictionary of information.
    id_col
        The column name of the id.

    Returns
    -------
    id_val
        An id for the information.
    """
    df = pd.read_csv(file_path)
    row_dct = {id_col: df.shape[0]}
    row_dct.update(**info_dct)
    if df.empty:
        newdf = pd.DataFrame([row_dct])
    else:
        newdf = df.append(row_dct, ignore_index=True, sort=False)
    newdf.to_csv(file_path, index=False)
    return row_dct[id_col]


def gen_fs_save(db_folder: str, storage_folder: str):
    """
    Generate the function save_all to save results of recipes. The database of csv, fgr and cif will be passed
    to the "_save_all" function. If there is no such file, it will be created as an empty csv file.

    Parameters
    ----------
    db_folder
        The folder where the database collection files are saved. If not exists, create one.

    storage_folder
        The folder where the data files are saved. If not exists, create one.

    Returns
    -------
    save_all
        A function to save results.

    """
    db_path = Path(db_folder)
    if not db_path.is_dir():
        db_path.mkdir()
    coll_paths = []
    for f in ('recipe.csv', 'contribution.csv', 'generator.csv'):
        coll_path = db_path.joinpath(f)
        if not coll_path.is_file():
            pd.DataFrame().to_csv(str(coll_path))
        coll_paths.append(str(coll_path))

    storage_path = Path(storage_folder)
    if not storage_path.is_dir():
        storage_path.mkdir()

    def save_all(recipe: MyRecipe):
        """
        Save fitting results, fitted PDFs and refined structures to files in one folder and save information in
        DataFrames. The DataFrame will contain columns: 'file' (file paths), 'rw' (Rw value) and other
        information in info.

        Parameters
        ----------
        recipe
            The FitRecipe.
        """
        return _save_all(recipe, str(storage_folder), *coll_paths)

    return save_all


def summarize(csv_df: pd.DataFrame, phases_col: str = "phases", file_col: str = 'csv_file', data_col: str = 'val',
              name_col: str = None, exclude: tp.List[str] = None, map_phase: dict = None,
              phase_del: str = ', ', escape: bool = False, processing: tp.Callable[[pd.DataFrame], None] = None,
              printout: bool = True, cbcopy: bool = False, output: bool = False) -> tp.Union[None, pd.DataFrame]:
    """
    Group the results by phases. For each group data frame, read .csv files according to the csv_df. Each .csv
    file contains fitting results from a fit. Join the results into one large data frame. The index are the
    parameters and the columns are the fits. Print the data frame out to use in the report. It can also copy to
    clip board or return a list of data frame.

    Parameters
    ----------
    csv_df
        The data frame of the csv files and its meta data, including phases and other information.
    file_col
        The column name of the .csv file.
    data_col
        The column name of values of the fitting parameters.
    name_col
        The column name for the names of columns in the result data frame.
    phases_col
        The a string of phases used in fitting.
    exclude
        The phases not to show results. If None, all phases will be included. Default None.
    map_phase
        The mapping from the phase name to a new name. If None, the phase name will be striped of '_' and
        capitalized.
         Default None.
    phase_del
        The delimiter of the phase in the string of phases. Dafault ', '.
    escape
        By default, the value will be read from the pandas config module. When set to False prevents from
        escaping latex special characters in column names. Default False.
    processing
        A function to modify the result data frame for each phase in each sample. If None, no modification.
        Default None.
    printout
        If True, printout the result string. Default False.
    cbcopy
        If True, copy result string to the clip board. Default False.
    output
        If True, return a list of the results data_frames. Default False.

    Returns
    -------
    None or list of data frame.
    """
    if not printout and not cbcopy and not output:
        raise Warning("printout, cbcopy and output are all None. Do nothing.")

    def gen_latex_str():
        for phases_str, group in csv_df.groupby(phases_col):
            _res_df = get_result(group, file_col=file_col, data_col=data_col, name_col=name_col)
            _res_df.drop(index=['Rw', 'half_chi2'], inplace=True)
            latex_str = to_report(_res_df, phases_str=phases_str, exclude=exclude, map_phase=map_phase,
                                  phase_del=phase_del, escape=escape, processing=processing)
            yield _res_df, latex_str

    res_dfs = []
    all_lstr = ''
    for res_df, lstr in gen_latex_str():
        res_dfs.append(res_df)
        all_lstr += lstr

    if printout:
        print(all_lstr)
    if cbcopy:
        pyperclip.copy(all_lstr)

    return res_dfs if output else None


def get_result(csv_df: pd.DataFrame, file_col: str = 'csv_file', data_col: str = 'val', name_col: str = None) \
        -> pd.DataFrame:
    """
    Get .csv files information from csv_df. Read multiple csv files. Each .csv file contains fitting results
    from a fit. Join the results into one large data frame. The index are the parameters and the columns are
    the fits.

    Parameters
    ----------
    csv_df
        The data frame of the csv files and its meta data, including phases and other information.
    file_col
        The column name of the .csv file.
    data_col
        The column name of values of the fitting parameters.
    name_col
        If specified, assign the names of columns in the result data frame.

    Returns
    -------
    res_df
        The results data frame.
    """
    dfs = (pd.read_csv(f, index_col=0)[data_col] for f in csv_df[file_col])
    res_df: pd.DataFrame = pd.concat(dfs, axis=1, ignore_index=True, sort=False).rename_axis(None)
    if name_col is not None:
        mapping = dict(zip(res_df.columns, csv_df[name_col]))
        res_df.rename(columns=mapping, inplace=True)

    return res_df


def to_report(res_df: pd.DataFrame, phases_str: str, exclude: tp.List[str] = None, map_phase: dict = None,
              phase_del: str = ', ', escape: bool = False,
              processing: tp.Callable[[pd.DataFrame], pd.DataFrame] = None) -> str:
    """
    Split the data frame of results by the phases and make a dictionary mapping from phase to data frame of
    results.

    Parameters
    ----------
    res_df
        The data frame of Results.
    phases_str
        The a string of phases used in fitting.
    exclude
        The phases not to show results. If None, all phases will be included. Default None.
    map_phase
        The mapping from the phase name to a new name. If None, the phase name will be striped of '_' and
        capitalized. Default None.
    phase_del
        The delimiter of the phase in the string of phases. Dafault ', '.
    escape
        By default, the value will be read from the pandas config module. When set to False prevents from
        escaping latex special characters in column names. Default False.
    processing


    Returns
    -------
    latex_str
        A string of latex table.
    """

    def default_change(s):
        s = ' '.join(s.split('_'))
        s = s.capitalize()
        return s

    total_lines = []
    map_phase = {} if map_phase is None else map_phase
    exclude = {} if exclude is None else exclude
    phases = [phase for phase in phases_str.split(phase_del) if phase not in exclude]
    num_col = res_df.shape[1] + 1

    for n, phase in enumerate(phases):
        df = res_df.filter(like=phase, axis=0).copy()
        df.rename(index=lambda x: convert_index(x), inplace=True)
        if processing is not None:
            df = processing(df)
        phase = map_phase.get(phase, default_change(phase))
        phase_row = rf"\multicolumn{{{num_col}}}{{l}}{{{phase}}}\\"
        if n == 0 and len(phases) == 1:
            lines = to_lines(df, del_head=False, del_tail=False, escape=escape)
            # plug in the row of the name of the phase and not take the last line '\n'
            lines = lines[:4] + [phase_row, r'\hline'] + lines[4:-1]
        elif n == 0 and len(phases) > 1:
            lines = to_lines(df, del_head=False, escape=escape)
            lines = lines[:4] + [phase_row, r'\hline'] + lines[4:]
        elif n == len(phases) - 1:
            lines = to_lines(df, del_tail=False, escape=escape)
            lines = [r'\hline', phase_row, r'\hline'] + lines[:-1]
        else:
            lines = to_lines(df, escape=escape)
            lines = [r'\hline', phase_row, r'\hline'] + lines
        total_lines += lines

    tabular_str = '\n'.join(total_lines)
    table_str = convert_str(tabular_str)
    return table_str


def convert_str(tabular_str: str) -> str:
    """
    Convert the tabular string to the table by adding the head and tail. Change the 'rule' to 'hline'.

    Parameters
    ----------
    tabular_str
        The string of tabular.

    Returns
    -------
    table_str
        The string for latex table.
    """
    str_map = {r"\toprule": r"\hline\hline",
               r"\midrule": r"\hline",
               r"\bottomrule": r"\hline\hline"}
    for old, new in str_map.items():
        tabular_str = tabular_str.replace(old, new)
    tabular_str += "\n"

    table_str = "\\begin{table}[htpb]\n" + \
                "\\caption{}\n" + \
                "\\label{tab:}\n" + \
                tabular_str + \
                "\\end{table}"

    return table_str


def convert_index(index: str) -> str:
    """
    Map an index value to the report format.

    Parameters
    ----------
    index
        The name of the index.

    Returns
    -------
    new_index
        The new index in report format
    """
    usymbols = ['Uiso', 'U11', 'U12', 'U13', 'U21', 'U22', 'U23', 'U31', 'U32', 'U33']
    xyzsymbols = ['x', 'y', 'z']
    dsymbols = ['delta2', 'delta1']
    words = index.split('_')  # the last one is phase, don't need it
    if words[0] in ('a', 'b', 'c'):
        new_index = r'{} (\AA)'.format(words[0])
    elif words[0] in ('alpha', 'beta', 'gamma'):
        new_index = r'$\{}$ (deg)'.format(words[0])
    elif words[0] in usymbols:
        new_index = r'{}$_{{{}}}$({}) (\AA$^2$)'.format(words[0][0], words[0][1:], words[1])
    elif words[0] in xyzsymbols:
        new_index = r'{}$_{{{}}}$ (\AA)'.format(words[0], words[1])
    elif words[0] in dsymbols:
        new_index = r'$\{}_{}$ (\AA$^2$)'.format(words[0][:-1], words[0][-1])
    elif words[0] == 'psize':
        new_index = r'D (\AA)'
    else:
        new_index = words[0]
    return new_index


def to_lines(df: pd.DataFrame, del_head=True, del_tail=True, escape=False) -> tp.List[str]:
    """
    Convert the results data frame to a list of lines in the string of latex table.

    Parameters
    ----------
    df
        The data frame of the results. Index are the parameters and columns are the samples.
    del_head
        Whether to delete the first four lines in latex string. Default True.
    del_tail
        Whether to delete the last two lines in latex string. Default True.
    escape
        By default, the value will be read from the pandas config module. When set to False prevents from
        escaping latex special characters in column names. Default False.

    Returns
    -------
    lines
        A list of lines in the latex table.
    """
    origin_str = df.to_latex(escape=escape)
    lines = origin_str.split('\n')
    if del_head:
        lines = lines[4:]
    if del_tail:
        lines = lines[:-3]
    return lines


def label_and_tick(data_type: str = None, minor_n: int = 2):
    """
    Decorate the plot.

    Parameters
    ----------
    data_type
        The type of data. Determine label for the plot.

    minor_n
        The number of minor tick between major ticks.
    """
    ax = plt.gca()
    if minor_n is not None:
        from matplotlib.ticker import AutoMinorLocator
        ax.xaxis.set_minor_locator(AutoMinorLocator(minor_n))
        ax.yaxis.set_minor_locator(AutoMinorLocator(minor_n))
    labels = {
        "iq": (r"Q ($\mathrm{\AA^{-2}}$)", r"I (A. U.)"),
        "sq": (r"Q ($\mathrm{\AA^{-2}}$)", r"S"),
        "fq": (r"Q ($\mathrm{\AA^{-2}}$)", r"F ($\mathrm{\AA^{-1}}$)"),
        "gr": (r"r ($\mathrm{\AA}$)", r"G ($\mathrm{\AA}^{-2}$)")
    }
    if data_type in labels:
        xlabel, ylabel = labels[data_type]
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
    return
