"""Modeling of the PDF of Ni."""
import pdfstream.io as io
import pdfstream.modeling as M

# load the data and meta data from data file to a data parser
data = io.load_parser(
    "Ni_damped.gr",
    {"qbroad": 0.04, "qdamp": 0.02}
)
# create a crystal object using the cif file
crystal = io.load_crystal("Ni.cif")
# create a recipe whose "name" is "nickel"
# the fitting target is the data we loaded from the data file
# the fitting range is from 2.2 A to 22.2 A with 0.01 A as step
# the equation is "f * G"
# "f" is the spherical characteristic function
# "G" is the PDF calculated from the Ni crystal we loaded from the cif file
recipe = M.create(
    "nickel",
    data,
    (2.2, 22.2, 0.01),
    "f * G",
    {"f": M.F.sphericalCF},
    {"G": crystal}
)
# initialize the recipe with the fitting parameters
# different initialization mode can be chosen using the key words in the function
M.initialize(recipe)
# set the initial value of "psize" parameter in "f"
recipe.f_psize.setValue(25.)
# set the lower bound of "psize"
recipe.f_psize.boundRange(lb=0.)
# define what parameter to refine in each step
# the parameters will be freed and refined one by one according to the order in the list
STEPS = [
    ("G_scale", "f_psize"),
    "G_lat",
    ("G_adp", "G_delta2")
]
# start optimization
M.optimize(recipe, STEPS)
# view the fitted data
M.view_fits(recipe)
# report the fitting results
M.report(recipe)
# uncomment the following line to save the recipe
# >>> M.save(recipe, "Ni_refined", ".")
# fitting result will be saved in .res file
# the fitted data will be saved in .fgr file
# the refined structure will be saved in .cif file
