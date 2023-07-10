# HCT-GUI
GUI Developments for the Helmholtz Cage Toolkit.

## What is this?
For the foreseeable future, this repository will hold development files for the creation of a software GUI tool, part of space-related, engineering thesis work. This software uses Qt6 as its primary UI framework, and the author is still learning new things about it. As a result, this repository *for the time being* will contain a mixture of development files relevant to the HCT GUI, and practice/experimental files, which the author used to learn about the software used.

## Dependencies
This software uses the following dependencies:
 * [PySide6](https://pypi.org/project/PySide6/)
 * [PyQtGraph 0.13.3](https://www.pyqtgraph.org/)
 * [Qt-Material](https://qt-material.readthedocs.io/en/latest/)
 * [Numpy](https://numpy.org/)
as well a number of other dependencies, all of which can be found in `requirements.txt`.

## Usage
This repository is best cloned into an instantiated `venv`:

```bash
python -m venv .venv
source .venv/bin/activate
```

Then clone the repository and install the requirements:
```bash
git clone https://github.com/Hans-Bananendans/HCT-GUI.git
pip install -r .\requirements.txt
```

## License
<a rel="license" href="https://creativecommons.org/licenses/by-nc-sa/3.0/"><img alt="Creative Commons License" style="border-width:0" src="https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png" /></a><br />
Software in this repository is licensed under [CC BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/) unless otherwise indicated.
