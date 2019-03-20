from setuptools import setup, find_packages


with open("README.rst", "r") as f:
    long_description = f.read()

VERSION = "1.5.3"


setup(name="AnkiVim",
      version=VERSION,
      url="https://github.com/MFreidank/VimForAnki",
      download_url="https://github.com/MFreidank/VimForAnki/tarball/{}".format(VERSION),
      description="Use vim to rapidly write textfiles immediately importable into anki(1).",
      scripts=['script/anki-vim'],
      long_description=long_description,
      author="Moritz Freidank",
      author_email="freidankm@yahoo.de",
      maintainer="Moritz Freidank",
      maintainer_email="freidankm@yahoo.de",
      license="MIT",
      packages=find_packages(exclude=("tests", "tests.*")),
      include_package_data=True,
      zip_safe=False,
      package=["ankivim"],
      package_dir={"ankivim": "ankivim"},
      package_data={"ankivim": ["UltiSnips/anki_vim.snippets", ]},
      )
