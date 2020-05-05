"""Some useful functions when using jupyter lab."""
from pathlib import Path
from typing import List, Union, Callable

import matplotlib.pyplot as plt
import pandas as pd
import pyperclip
from matplotlib.ticker import AutoMinorLocator

LATEX_REF = (
    "\\begin{{figure}}[hptb]\n"
    "\\includegraphics[width=\\columnwidth]{{{}}}\n"
    "\\caption{{{}}}\n"
    "\\label{{fig:{}}}\n"
    "\\end{{figure}}\n"
)


def savefig_factory(figure_dir):
    """
    Create function 'savefig' to save the current figure in the directory.

    Parameters
    ----------
    figure_dir
        The directory to save the figure.

    Returns
    -------
    save_fig
        A function to save current figure.
    """
    figure_dir = Path(figure_dir)
    if not figure_dir.is_dir():
        figure_dir.mkdir()

    def savefig(fname: str,
                dpi=240,
                facecolor=None,
                edgecolor=None,
                orientation='portrait',
                papertype=None,
                fmt='pdf',
                transparent=True,
                bbox_inches=None,
                pad_inches=0.1,
                metadata=None,
                latex=True,
                caption=""):
        """
        The output formats available depend on the backend being used.
        The latex reference will be copied to clipboard.

        Parameters
        ----------

        fname : str or PathLike or file-like object
            A path, or a Python file-like object, or
            possibly some backend-dependent object such as
            `matplotlib.backends.backend_pdf.PdfPages`.

            If *format* is not set, then the output format is inferred from
            the extension of *fname*, if any, and from :rc:`savefig.format`
            otherwise.  If *format* is set, it determines the output format.

            Hence, if *fname* is not a path or has no extension, remember to
            specify *format* to ensure that the correct backend is used.

        dpi : [ *None* | scalar > 0 | 'figure' ]
            The resolution in dots per inch.  If *None*, defaults to
            :rc:`savefig.dpi`.  If 'figure', uses the figure's dpi value.

        facecolor : color spec or None, optional
            The facecolor of the figure; if *None*, defaults to
            :rc:`savefig.facecolor`.

        edgecolor : color spec or None, optional
            The edgecolor of the figure; if *None*, defaults to
            :rc:`savefig.edgecolor`

        orientation : {'landscape', 'portrait'}
            Currently only supported by the postscript backend.

        papertype : str
            One of 'letter', 'legal', 'executive', 'ledger', 'a0' through
            'a10', 'b0' through 'b10'. Only supported for postscript
            output.

        fmt : str
            The file format, e.g. 'png', 'pdf', 'svg', ... The behavior when
            this is unset is documented under *fname*.

        transparent : bool
            If *True*, the axes patches will all be transparent; the
            figure patch will also be transparent unless facecolor
            and/or edgecolor are specified via kwargs.
            This is useful, for example, for displaying
            a plot on top of a colored background on a web page.  The
            transparency of these patches will be restored to their
            original values upon exit of this function.

        bbox_inches : str or `~matplotlib.transforms.Bbox`, optional
            Bbox in inches. Only the given portion of the figure is
            saved. If 'tight', try to figure out the tight bbox of
            the figure. If None, use savefig.bbox

        pad_inches : scalar, optional
            Amount of padding around the figure when bbox_inches is
            'tight'. If None, use savefig.pad_inches

        metadata : dict, optional
            Key/value pairs to store in the image metadata. The supported keys
            and defaults depend on the image format and backend:

            - 'png' with Agg backend: See the parameter ``metadata`` of
              `~.FigureCanvasAgg.print_png`.
            - 'pdf' with pdf backend: See the parameter ``metadata`` of
              `~.backend_pdf.PdfPages`.
            - 'eps' and 'ps' with PS backend: Only 'Creator' is supported.

        latex : bool, optional
            Whether to copy the latex reference into clipboard. The template is in the LATEX_REF.

        caption : str, optional
            The caption for the figure in the latex.
        """
        fname = figure_dir.joinpath(fname)
        plt.savefig(
            fname,
            dpi=dpi,
            facecolor=facecolor,
            edgecolor=edgecolor,
            orientation=orientation,
            papertype=papertype,
            format=fmt,
            transparent=transparent,
            bbox_inches=bbox_inches,
            pad_inches=pad_inches,
            metadata=metadata
        )
        if latex:
            latex_ref = LATEX_REF.format(fname.name, caption, fname.stem)
            pyperclip.copy(latex_ref)
        return

    return savefig


def summarize(csv_df: pd.DataFrame, phases_col: str = "phases", file_col: str = 'csv_file', data_col: str = 'val',
              name_col: str = None, exclude: List[str] = None, map_phase: dict = None,
              phase_del: str = ', ', escape: bool = False, processing: Callable[[pd.DataFrame], None] = None,
              printout: bool = False, cbcopy: bool = False, output: bool = False) -> Union[None, pd.DataFrame]:
    """
    Group the results by phases. For each group data frame, read .csv files according to the csv_df. Each .csv file
    contains fitting results from a fit. Join the results into one large data frame. The index are the parameters and
    the columns are the fits. Print the data frame out to use in the report. It can also copy to clip board or return
    a list of data frame.

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
        The mapping from the phase name to a new name. If None, the phase name will be striped of '_' and capitalized.
         Default None.
    phase_del
        The delimiter of the phase in the string of phases. Dafault ', '.
    escape
        By default, the value will be read from the pandas config module. When set to False prevents from escaping
        latex special characters in column names. Default False.
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
    Get .csv files information from csv_df. Read multiple csv files. Each .csv file contains fitting results from a fit.
    Join the results into one large data frame. The index are the parameters and the columns are the fits.

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


def to_report(res_df: pd.DataFrame, phases_str: str, exclude: List[str] = None, map_phase: dict = None,
              phase_del: str = ', ', escape: bool = False, processing: Callable[[pd.DataFrame], pd.DataFrame] = None) \
        -> str:
    """
    Split the data frame of results by the phases and make a dictionary mapping from phase to data frame of results.

    Parameters
    ----------
    res_df
        The data frame of Results.
    phases_str
        The a string of phases used in fitting.
    exclude
        The phases not to show results. If None, all phases will be included. Default None.
    map_phase
        The mapping from the phase name to a new name. If None, the phase name will be striped of '_' and capitalized.
         Default None.
    phase_del
        The delimiter of the phase in the string of phases. Dafault ', '.
    escape
        By default, the value will be read from the pandas config module. When set to False prevents from escaping
        latex special characters in column names. Default False.
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
        df.rename(index=convert_index, inplace=True)
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


def to_lines(df: pd.DataFrame, del_head=True, del_tail=True, escape=False) -> List[str]:
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
        By default, the value will be read from the pandas config module. When set to False prevents from escaping
        latex special characters in column names. Default False.

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
