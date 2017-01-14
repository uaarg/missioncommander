from config import *

def gen_mission_msg(self, ac_id, insert = "APPEND"):
        msg = pprzmsg("datalink", msg_id)

        msg['ac_id'] = ac_id
        msg['insert'] = insert
        msg['duration'] = msgs.get('duration')

        if msg_id == 'MISSION_GOTO_WP_LLA':
            msg['wp_lat'] = msgs.get('wp_lat')
            msg['wp_lon'] = msgs.get('wp_lon')
            msg['wp_alt'] = msgs.get('wp_alt')

        elif msg_id == 'MISSION_CIRCLE_LLA':
            msg['center_lat'] = msgs.get('center_lat')
            msg['center_lon'] = msgs.get('center_lon')
            msg['center_alt'] = msgs.get('center_alt')
            msg['radius'] = msgs.get('radius')

        elif msg_id == 'MISSION_SEGMENT_LLA':
            msg['segment_lat_1'] = msgs.get('segment_lat_1')
            msg['segment_lon_1'] = msgs.get('segment_lon_1')
            msg['segment_lat_2'] = msgs.get('segment_lat_2')
            msg['segment_lon_2'] = msgs.get('segment_lon_2')

        elif msg_id == 'MISSION_PATH_LLA':
            msg['point_lat_1'] = msgs.get('point_lat_1')
            msg['point_lon_1'] = msgs.get('point_lon_1')
            msg['point_lat_2'] = msgs.get('point_lat_2')
            msg['point_lon_2'] = msgs.get('point_lon_2')
            msg['point_lat_3'] = msgs.get('point_lat_3')
            msg['point_lon_3'] = msgs.get('point_lon_3')
            msg['point_lat_4'] = msgs.get('point_lat_4')
            msg['point_lon_4'] = msgs.get('point_lon_4')
            msg['point_lat_5'] = msgs.get('point_lat_5')
            msg['point_lon_5'] = msgs.get('point_lon_5')
            msg['path_alt'] = msgs.get('path_alt')
            msg['nb'] = msgs.get('nb')

        elif msg_id == 'MISSION_SURVEY_LLA':
            msg['survey_lat_1'] = msgs.get('survey_lat_1')
            msg['survey_lon_1'] = msgs.get('survey_lon_1')
            msg['survey_lat_2'] = msgs.get('survey_lat_2')
            msg['survey_lon_2'] = msgs.get('survey_lon_2')
            msg['survey_alt'] = msgs.get('survey_alt')
        
        return msg
