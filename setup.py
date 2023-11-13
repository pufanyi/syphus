from setuptools import setup, find_packages


setup(
    name="syphus",
    version="0.0.6.2",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "ruamel.yaml==0.17.32",
        "PyYAML==6.0.1",
        "openai==0.27.8",
        "orjson==3.9.4",
        "opencv-python==4.8.0.76",
        "Pillow==10.0.1",
        "pandas==2.1.0",
        "requests==2.31.0",
    ],
    package_data={
        "syphus": ["resources/**/*"],
    },
    include_package_data=True,
    author="Fanyi Pu",
    author_email="FPU001@e.ntu.edu.sg",
    description="Syphus: Automatic Instruction-Response Generation Pipeline",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pufanyi/syphus",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points={
        "console_scripts": [
            "syphus = syphus.cli.syphus_cli:main",
        ],
    },
)
