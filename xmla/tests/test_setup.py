"""
testing this setup
"""

from docutils.core import publish_string
import os.path

def test_rst_readme():
    rst2html("README.rst")

def test_rst_changes():
    rst2html("CHANGES.rst")

def rst2html(what):
    fname = os.path.join(os.path.split(__file__)[0], "..", what)
    with open(fname, "r") as f:
        rst=f.read()
    erg=publish_string(rst, writer_name='html', settings_overrides={"halt_level":2})
    assert(erg != "")

