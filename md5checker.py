from config import *
import os

def findMD5(airMD5, logging):
    foundpath = None
    aircraftFolder = os.path.join(*[PPRZ_SRC, 'var/aircrafts'])
    aircrafts = os.listdir(aircraftFolder)

    airMD5 = airMD5.split(",")
    airMD5 = convert2Hex(airMD5)

    for aircraft in aircrafts:
        md5File = os.path.join(*[aircraftFolder, aircraft, 'conf/aircraft.md5'])
        if os.path.isfile(md5File):
             md5 = open(md5File, 'r').readline().rstrip()
             if md5 == airMD5:
                 foundpath = os.path.join(*[aircraftFolder, aircraft])
                 print("Found MD5 code.")
                 break
        else:
            logging.warning('There is a problem with the Paparazzi Configuration. A generated aricraft is missing an md5 file')
    if foundpath == None:
        logging.critical('MD5 Checksum Error. Reupload to autopilot or ////YET TO IMPLEMENT ===> rerun with no_md5_checksum')
    return foundpath


def convert2Hex(md5):
    md5str = ''
    for b in md5:
        if b != None and b != '':
            md5str = md5str + format(int(b), '02x')
    return md5str
