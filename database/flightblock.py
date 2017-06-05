from config import *
from utils import *

class FlightBlock(object):
    """class to make flight block"""

    def __init__(self, name, block_id, ac_id):
        self.name = name
        self.block_id = block_id
        self.ac_id = ac_id

    def gen_change_block_msg(self):
        msg = pprzmsg("ground", "JUMP_TO_BLOCK")
        msg['ac_id'] = self.ac_id
        msg['block_id'] = self.block_id
        return msg

class FlightBlockList(list):
    """Class of List of Flight Blocks"""
    def add(self, block):
        self.append((block.name, block))

    def getFlightBlockByName(self, FlightBlockName):
        for block in self:
            if (str(block[0]) == str(FlightBlockName)):
                return block[1]

    def getFlightBlockByID(self, flightBlockID):

        return self[int(flightBlockID)][1]
