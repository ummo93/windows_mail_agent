from cx_Freeze import setup,Executable
import sys
 
base=None
if sys.platform=='win32':
    base='Win32GUI'
    
setup(name='FirstScript',
      version='0.18',
      executables=[Executable(script='init.pyw',base=base)])
