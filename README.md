Mission Commander
===

Installation
---
```
sudo apt-get install python3-pip
sudo pip3 install utm requests
sudo apt-get install qtdeclarative5-dev qtmultimedia5-dev python3-pyqt5 pyqt5-dev-tools
```

Add Paparazzi to your system path. To make this automatic on startup, copy the following lines to ~/.bashrc
```
export PAPARAZZI_HOME=''your paparazzi software directory''
export PAPARAZZI_SRC=''your paparazzi software directory''
```


You must also install a copy of the AUVSI SUAS Competition Interoperability server. The instructions for this can be found in the documentation for the server: https://auvsi-suas-competition-interoperability-system.readthedocs.io/en/latest/

Running
---
Turn on a paparazzi and choose Microjet under A/C.
This configuration has the lexington park flight plan enabled by default and is garunteed to work.

Run via: `python3 main.py`