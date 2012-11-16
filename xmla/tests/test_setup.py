"""
testing this setup
"""

from docutils.core import publish_string
import os.path

def test_rst_readme():
    rst2html("README.md")

def test_rst_changes():
    rst2html("CHANGES.md")

def rst2html(what):
    fname = os.path.join(os.path.split(__file__)[0], "..", what)
    rst=open(fname, "r").read()
    erg=publish_string(rst, writer_name='html', settings_overrides={"halt_level":2})
    assert(erg != "")
