# -*- coding: utf-8 -*-
"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

import os
from distutils.sysconfig import get_python_inc
#from distutils import setup, find_packages, Extension
from setuptools import setup, Extension
import platform
import sys
from importlib.machinery import SourceFileLoader

def system(cmd):
	print("Executing: ", cmd)
	ret = os.system(cmd)
	if ret != 0:
		print("error, return code is", ret)
		sys.exit(ret)

path_version_file = "vaex/version.py"
if not os.path.exists(path_version_file):
	system("version=`git describe --tags --long`; vaex/setversion.py ${version}")

version = SourceFileLoader('version', path_version_file).load_module()
#system("version=`git describe --tags --long`; vaex/vaex/setversion.py ${version}")


has_py2app = False
#import vaex
try:
	import py2app.build_app
	has_py2app = True
except:
	pass

if has_py2app:
	import py2app.recipes
	class astropy(object):
		def check(self, cmd, graph):
			return dict(packages=["astropy"])
	py2app.recipes.astropy = astropy()
	# see http://stackoverflow.com/questions/31240052/py2app-typeerror-dyld-find-got-an-unexpected-keyword-argument-loader
	"""
	Monkey-patch macholib to fix "dyld_find() got an unexpected keyword argument 'loader'".

	Add 'import macholib_patch' to the top of set_py2app.py
	"""

	import macholib
	if macholib.__version__ <= "1.7":
		print("Applying macholib patch...")
		import macholib.dyld
		import macholib.MachOGraph
		dyld_find_1_7 = macholib.dyld.dyld_find
		def dyld_find(name, loader=None, **kwargs):
			#print("~"*60 + "calling alternate dyld_find")
			if loader is not None:
				kwargs['loader_path'] = loader
			return dyld_find_1_7(name, **kwargs)
		macholib.MachOGraph.dyld_find = dyld_find
#full_name = vaex.__full_name__
cmdclass = {}

if has_py2app and sys.argv[1] == "py2app":
	import vaex.ui
	class my_py2app(py2app.build_app.py2app):
		"""hooks in post script to add in missing libraries and zip the content"""
		def run(self):
			py2app.build_app.py2app.run(self)
			#libQtWebKit.4.dylib
			#libQtNetwork.4.dylib
			if 0:
				libs = [line.strip() for line in """
				libLLVM-3.3.dylib
				libQtGui.4.dylib
				libQtCore.4.dylib
				libQtOpenGL.4.dylib
				libcrypto.1.0.0.dylib
				libssl.1.0.0.dylib
				libpng15.15.dylib
				libfreetype.6.dylib
				libjpeg.8.dylib
				libhdf5_hl.9.dylib
				libhdf5.9.dylib
				""".strip().splitlines()]

				libpath = "/Users/maartenbreddels/anaconda/lib"
				targetdir = 'dist/vaex.app/Contents/Resources/lib/'
				for filename in libs:
					path = os.path.join(libpath, filename)
					cmd = "cp %s %s" % (path, targetdir)
					print(cmd)
					os.system(cmd)

				libs = [line.strip() for line in """
				libpng15.15.dylib
				""".strip().splitlines()]
				targetdir = 'dist/vaex.app/Contents/Resources/'
				for filename in libs:
					#path = os.path.join(libpath, filename)
					cmd = "cp %s %s" % (path, targetdir)
					print(cmd)
					os.system(cmd)

			os.system("cp data/helmi-dezeeuw-2000-10p.hdf5 dist/vaex.app/Contents/Resources/")
			os.system("cd dist")
			zipname = "%s.zip" % vaex.__build_name__
			os.system("cd dist;rm %s" % zipname)
			os.system("cd dist;zip -q -r %s %s.app" % (zipname, vaex.__program_name__))
			retvalue = os.system("git diff --quiet")
			if retvalue != 0:
				print("WARNING UNCOMMITED CHANGES, VERSION NUMBER WILL NOT MATCH")
	cmdclass['py2app'] = my_py2app
			
#from distutils.core import setup, Extension
try:
	import numpy
	numdir = os.path.dirname(numpy.__file__)
except:
	numdir = None

if numdir is None:
	print("numpy not found, cannot install")
import sys 
import glob
sys.setrecursionlimit(10000)

APP = ["vaex_app.py"]
DATA_FILES = []
if has_py2app:
	pass
	#DATA_FILES.append(["data", ["data/disk-galaxy.hdf5"]]) #, "data/Aq-A-2-999-shuffled-1percent.hdf5"]])
	DATA_FILES.append(["data/", glob.glob("data/dist/*")] )


#print glob.glob("doc/*")
if 0:
	DATA_FILES.append(["doc/", glob.glob("docs/build/html/*.html") + glob.glob("docs/build/html/*.js")] )
	for sub in "_static _images _sources".split():
		DATA_FILES.append(["doc/" + sub, glob.glob("docs/build/html/" +sub +"/*")] )
#print DATA_FILES
OPTIONS = {'argv_emulation': False, 'excludes':[], 'resources':['vaex/ui/icons'],
           'matplotlib_backends':'-',
           'no_chdir':True,
		   'includes': ['h5py',
                 'h5py.defs',
                 'h5py.h5ac',
                 'h5py._errors',
                 'h5py._objects',
                 'h5py.defs',
                 'h5py.utils',
                 'h5py._proxy',
				 'six',
				 'aplus',
				 "astropy.extern.bundled",
				 ],
		   "frameworks": [sys.prefix + "/lib/libmkl_avx2.dylib"],
           'iconfile': 'vaex/ui/icons/vaex.icns'

} #, 'debug_modulegraph':True}
#, 'app':True


include_dirs = []
library_dirs = []
libraries = []
defines = []
if "darwin" in platform.system().lower():
	extra_compile_args = ["-mfpmath=sse", "-O3", "-funroll-loops"]
else:
	extra_compile_args = []
	#extra_compile_args = ["-mfpmath=sse", "-msse4", "-Ofast", "-flto", "-march=native", "-funroll-loops"]
	#extra_compile_args = ["-mfpmath=sse", "-msse4", "-Ofast", "-flto", "-funroll-loops"]
	#extra_compile_args = ["-mfpmath=sse", "-O3", "-funroll-loops"]
	#extra_compile_args = ["-mfpmath=sse", "-mavx", "-O3", "-funroll-loops"]
	extra_compile_args = ["-mfpmath=sse", "-msse4a", "-O3", "-funroll-loops"]
extra_compile_args.extend(["-std=c++0x"])

include_dirs.append(os.path.join(get_python_inc(plat_specific=1), "numpy"))
if numdir is not None:
	include_dirs.append(os.path.join(numdir, "core", "include"))

extensions = [
	Extension("vaex.vaexfast", ["src/vaex/vaexfast.cpp"],
                include_dirs=include_dirs,
                library_dirs=library_dirs,
                libraries=libraries,
                define_macros=defines,
                extra_compile_args=extra_compile_args
                )
] if numdir is not None else []

from pip.req import parse_requirements
import pip.download

# older versions of pip don't use the pipsession..?
try:
	session = pip.download.PipSession()
except:
	session = None
# parse_requirements() returns generator of pip.req.InstallRequirement objects
if session:
	install_reqs = parse_requirements("requirements.txt", session=session)
else:
	install_reqs = parse_requirements("requirements.txt")

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
	reqs = [] # we do this with requirements-rtd.txt
else:
	reqs = [str(ir.req) for ir in install_reqs]

if sys.version_info >= (3,0):
	# remove future for py3
	reqs.remove("futures>=2.2.0")

#print "requirements", reqs
#print "ver#sion", vaex.__release__
setup(
	entry_points={
		'console_scripts': ['vaex = vaex.__main__:main'],
		'gui_scripts': ['vaexgui = vaex.__main__:main'] # sometimes in osx, you need to run with this
  	},
	app=["bin/vaex"],
	name="vaex", #vaex.__program_name__,
	author="Maarten A. Breddels",
	author_email="maartenbreddels@gmail.com",
    version = version.versionstring, #"%d.%d.%d" % version.versiontuple,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
	license='MIT',
    #setup_requires=['py2app'],
    #setup_requires=["sphinx"],
    includes=["vaex", "md5", "astropy", "aplus", "six"],
    packages=["vaex", "vaex.ui", "vaex.test", "vaex.misc", "vaex.notebook", "vaex.file", "vaex.ui.plugin", "vaex.ui.icons", "vaex.ext"],
    install_requires=reqs,
    #entry_points={ 'console_scripts': [ 'vaex=vaex.ui.main:main']  },
    #scripts=[os.path.join("bin", "vaex")],
    ext_modules=extensions,
    package_data={'vaex': ['ui/icons/*.png', 'ui/icons/*.icns', 'ext/*.js']},
    package_dir={'vaex':'vaex'},
    cmdclass=cmdclass,
    description="Vaex is a graphical tool to visualize and explore large tabular datasets.",
    long_description=open("README.rst").read(),
    url="https://www.astro.rug.nl/~breddels/vaex",
	classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',

		'Operating System :: MacOS',
		'Operating System :: POSIX',
		'Operating System :: Unix',

		'Topic :: Scientific/Engineering :: Visualization',
		'Topic :: Scientific/Engineering :: Information Analysis',

		'Intended Audience :: Science/Research',

		'Environment :: MacOS X',
		'Environment :: X11 Applications'

    ],
	keywords="visualization exploration data analysis "
)
