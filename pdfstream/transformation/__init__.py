# check if diffpy.pdfgetx is installed
try:
    import diffpy.pdfgetx
    __PDFGETX_AVAL__ = True
except ImportError:
    __PDFGETX_AVAL__ = False
    print("diffpy.pdfgetx not installed. The data transformations functionality will be not available.")
