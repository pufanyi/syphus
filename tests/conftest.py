import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

if not os.path.exists("tests/test_output"):
    os.makedirs("tests/test_output")
