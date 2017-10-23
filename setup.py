from setuptools import setup, find_packages


with open("README.rst", "r") as f:
    long_description = f.read()

VERSION = "1.0"


setup(name="VimForAnki",
      version=VERSION,
      url="https://github.com/MFreidank/VimForAnki",
      download_url="https://github.com/MFreidank/VimForAnki/tarball/{}".format(VERSION),
      description="Use vim to rapidly write textfiles immediately importable into anki(1).",
      long_description=long_description,
      author="Moritz Freidank",
      maintainer="Moritz Freidank",
      maintainer_email="freidankm@yahoo.de",
      license="MIT",
      packages=find_packages(exclude=("tests", "tests.*")),
      include_package_data=True,
      zip_safe=False,
      )
