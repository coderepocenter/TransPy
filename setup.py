import subprocess
import setuptools
from shutil import which

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', "r") as fh:
    requirements = fh.read().split("\n")

if which('conda') is not None:
    print('CONDA was found. attempting to install requirements using conda')
    for e in requirements:
        print(f'\t- {e}')
    subprocess.run(
        ['conda', 'install', '-y', '-c', 'conda-forge', '-c', 'aciacs'] + requirements,
        shell=True
    )
else:
    print('WARNING: conda command was not found. '
          'pip installer might not be able to install all the required packages.')

packages = setuptools.find_packages(exclude=['tests'])
print("setuptools.find_packages(): ", packages)

from transpy import __version__

setuptools.setup(
    name="transpy",
    version=__version__,
    author="",
    author_email="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/coderepocenter/TransPy.git",
    packages=packages,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            'split_linestring = cli.split_linestring:split_linestring'
        ]
    }
)
