import sys
import os
import shutil


sys.path = [
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
] + sys.path

if os.path.exists("tests/test_output"):
    shutil.rmtree("tests/test_output")
os.makedirs("tests/test_output")
