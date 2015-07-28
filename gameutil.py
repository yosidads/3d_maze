# coding: utf-8

from pygame.locals import * 

class GameConstUtil():

    @classmethod
    def get_game_title(cls):        
        return "THE 3D Maze"

    @classmethod
    def get_game_status(cls, status):        
        game_status_dic = {"START":0, "BIG_MAP":1, "3D_MAZE":2, "GAMEOVER":3}
        
        return game_status_dic[status]

    @classmethod
    def get_scr_rect(cls):        
        return Rect(0, 0, 640, 480)

    @classmethod
    def get_color(cls, color_desc):        
        game_color_dic = {"BLACK":(0, 0, 0), "WHITE":(255, 255, 255), "BLUE":(0, 0, 255), "GREEN":(0, 255, 0) \
                           , "RED":(255, 0, 0), "YELLOW":(255, 255, 0), "PURPLE":(255, 0, 255), "CYAN":(0, 255, 255)}
        
        return game_color_dic[color_desc]            
   
    @classmethod
    def get_direction(cls, direction_desc):
        direction_dic = {"UP":0, "RIGHT":1, "DOWN":2, "LEFT":3}
        
        return direction_dic[direction_desc]        

    @classmethod
    def get_map_obj(cls, obj_type):
        obj_dic = {"ROAD":0, "WALL":1, "HERE":2, "PASSED":3, "GOAL":9}
        
        return obj_dic[obj_type]        
 