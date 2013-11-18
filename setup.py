from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("sniffer",
                             ["compare.pyx"
                              , "lang_ctype.pyx"
                              , "lang_vhdl.pyx"
                              , "lang_verilog.pyx"
                              , "lang_pdf.pyx"
                              , "lcs.pyx"
                              , "save_email.pyx"
                              , "algorithm.pyx"
                              ])]
)
