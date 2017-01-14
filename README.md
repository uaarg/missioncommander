Mission Commander
===

Installation
---
sudo apt-get install python-pip
sudo pip install pyproj requests


set paparazzi path
sudo gedit /etc/environment
```
PAPARAZZI_SRC="/home/rijesh/paparazzi"
PAPARAZZI_HOME="/home/rijesh/paparazzi"

```

You must also install a copy of the AUVSI SUAS Competition Interoperability server. The instructions for this can be found in the documentation for the server: https://auvsi-suas-competition-interoperability-system.readthedocs.io/en/latest/

Running
---
Turn on a paparazzi and choose Microjet under A/C.
This configuration has the lexington park flight plan enabled by default and is garunteed to work.

go to mission commander and run via:
python missioncommander
