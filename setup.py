from distutils.sysconfig import get_python_lib
from os.path import join
from glob import glob
from cx_Freeze import setup, Executable

cefPath = join(get_python_lib(), 'cefpython3')
CEF_INCLUDES = glob(join(cefPath, '*'))
CEF_INCLUDES.remove(join(cefPath, 'examples'))

setup(
    name = 'wallet',
    version = '0.0.1',
    description = 'Wallet',
    options = {
        'build_exe': {
        'packages': ['os', 'sys', 'ctypes', 'json'],
        'include_files': CEF_INCLUDES + ['data', 'site', 'backendutils.py'],
        'include_msvcr': True,
    }},
    executables = [Executable(script='wallet.py', icon='icon.ico')]
)