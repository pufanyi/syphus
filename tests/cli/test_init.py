import os
import filecmp
import subprocess


def same_file(file1, file2):
    assert os.path.isfile(file1) and os.path.isfile(
        file2
    ), f"One of {file1} and {file2} is not a file"
    with open(file1, "r") as f1, open(file2, "r") as f2:
        assert f1.read() == f2.read(), f"{file1} and {file2} are not the same"


def same_folder(folder1, folder2):
    if os.path.isfile(folder1) or os.path.isfile(folder2):
        same_file(folder1, folder2)
        return

    assert os.path.isdir(folder1) and os.path.isdir(
        folder2
    ), f"One of {folder1} and {folder2} is not both a folder or a file"

    comparison = filecmp.dircmp(folder1, folder2)
    assert (
        not comparison.left_only
        and not comparison.right_only
        and not comparison.diff_files
    ), f"{folder1} and {folder2} are not the same"

    for common_dir in comparison.common_dirs:
        same_folder(
            os.path.join(folder1, common_dir), os.path.join(folder2, common_dir)
        )


def test_init():
    subprocess.run(["syphus", "init", "tests/test_output/init"])
    same_folder("tests/test_output/init", "src/syphus/resources/template")
