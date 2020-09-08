import subprocess
from shutil import which
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', "r") as fh:
    requirements = fh.read().split("\n")

print("requirements: ", requirements)

if which('conda') is not None:
    print('CONDA was found. attempting to install requirements using conda')
    subprocess.run(
        ['conda', 'install', '-y', '-c', 'conda-forge', '-c', 'aciacs'] + requirements,
        shell=True
    )
else:
    print('WARNING: conda command was not found. '
          'Pip installer might not be able to install all the required packages, '
          'such as Fiona on Windows')

print("setuptools.find_packages(): ", setuptools.find_packages())

from transpy import __version__

setuptools.setup(
    name="transpy",
    version=__version__,
    author="",
    author_email="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/coderepocenter/TransPy.git",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)