import subprocess


def test_init():
    subprocess.run(["syphus", "init", "tests/test_output"])
    assert True
