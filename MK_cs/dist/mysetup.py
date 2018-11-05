# mysetup.py
from distutils.core import setup
import py2exe

setup(windows=[{"script":"MartKay.py"}], options={"py2exe":{"includes":["sip"]}})