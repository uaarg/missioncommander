from config import *

    def add_shape(self, status, obstacle_id, obmsg):
        msg = pprzmsg("ground", "SHAPE")
        msg['id'] = int(obstacle_id)

        if obstacle_id >= (maxTargets/2 -1 ):
            msg['fillcolor'] = "blue"
            msg['linecolor'] = "blue"
            msg['opacity'] = 2
        elif obstacle_id >= (maxTargets -1):
            msg['fillcolor'] = "red"
            msg['linecolor'] = "red"
            msg['opacity'] = 1
        elif obstacle_id >= (3*maxTargets/2 -1):
            msg['fillcolor'] = "orange"
            msg['linecolor'] = "orange"
            msg['opacity'] = 2
        elif obstacle_id >= (2*maxTargets -1):
            msg['fillcolor'] = "red"
            msg['linecolor'] = "red"
            msg['opacity'] = 1
        else:
            if (self.tooManyTargets< maxTargets):
                print("TOO MANY OBSTACLES, things are failing")
                self.tooManyTargets = self.tooManyTargets +1

        msg['status'] = 0 if status=="create" else 1
        msg['shape'] = 0
        msg['latarr'] = [int(obmsg.get("latitude")*10000000.),int(obmsg.get("latitude")*10000000.)]
        msg['lonarr'] = [int(obmsg.get("longitude")*10000000.),int(obmsg.get("longitude")*10000000.)]
        msg['radius'] = int(obmsg.get("sphere_radius") if "sphere_radius" in obmsg else obmsg.get("cylinder_radius"))
        msg['text'] = "NULL"

        return msg