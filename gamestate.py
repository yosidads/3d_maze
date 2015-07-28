# coding: utf-8

from gameutil import *
import pygame
import random


class GameState:    

    def __init__(self):

        self.MAZE_X=21
        self.MAZE_Y=13
             
        self._status = GameConstUtil.get_game_status("START")

        self._my_locx = 1
        self._my_locy = 1
        self._my_direction = GameConstUtil.get_direction("RIGHT")
        self._starttime = 0
                
        self._load_sounds()
        self._sound_to_play = None
        self._create_maze()
        
    def _create_maze(self):
        # 0:Road 1:Wall 2:Current Loc 3:Road passed 9:Goal 
        ROAD = GameConstUtil.get_map_obj("ROAD")
        WALL = GameConstUtil.get_map_obj("WALL")
        self._maze =  [[WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL],
                       [WALL,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,WALL],
                       [WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL],
                       [WALL,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,WALL],
                       [WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL],
                       [WALL,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,WALL],
                       [WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL],
                       [WALL,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,WALL],
                       [WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL],
                       [WALL,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,WALL],
                       [WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL,ROAD,WALL],
                       [WALL,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,ROAD,WALL],
                       [WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL]]

        #Create a maze with Bo-Taoshi logic
        for y in range(2, self.MAZE_Y-1, 2):
            for x in range(2, self.MAZE_X-1, 2):
                while True:
                    #Only the Bo in the first row can go down upwards
                    if y == 2:
                        direction = random.randint(0, 3)
                    else:
                        direction = random.randint(1, 3)

                    if direction == 0:
                        if self._maze[y-1][x] == 0:
                            self._maze[y-1][x] = 1
                            break
                    elif direction == 1:
                        if self._maze[y][x+1] == 0:
                            self._maze[y][x+1] = 1
                            break
                    elif direction == 2:
                        if self._maze[y+1][x] == 0:
                            self._maze[y+1][x] = 1
                            break
                    elif direction == 3:
                        if self._maze[y][x-1] == 0:
                            self._maze[y][x-1] = 1
                            break
        
        #set starting location            
        self._maze[self._my_locy][self._my_locx] = GameConstUtil.get_map_obj("HERE")                       
        #set Goal            
        self._maze[self.MAZE_Y-2][self.MAZE_X-2] = GameConstUtil.get_map_obj("GOAL")                       

        #print "###Maze"
        #print self._maze
                        
    def _load_sounds(self):
        pass
        self._sounds = {"WALK": pygame.mixer.Sound("./sound/walk1.wav"), "TURN": pygame.mixer.Sound("./sound/walk2.wav")}

    def _get_object(self, x, y):
        if x >= self.MAZE_X or y >= self.MAZE_Y:
            return 1
        else:
            return self._maze[y][x]
 
    def _process_gameover(self):
        self._final_elapsedtime = self.get_elapsedtime()
        self._status = GameConstUtil.get_game_status("GAMEOVER")
                                 
    def set_status(self, status):
        self._status = status    
    
    def get_status(self):
        return self._status
        
    def get_sounds(self):
        return self._sounds
    
    def set_sound_to_play(self, sound_to_play):
        self._sound_to_play = sound_to_play
        
    def get_sound_to_play(self):
        return self._sound_to_play

    def set_starttime(self, starttime):
        self._statrtime = starttime

    def get_elapsedtime(self):
        current_time = pygame.time.get_ticks()
        
        elapsed_min = int((current_time - self._statrtime) / 1000 / 60)
        elapsed_sec = round(((current_time - self._statrtime) - (elapsed_min * 60 * 1000)) / 1000.00, 2)
        #elapsed_sec = (current_time - self._statrtime) / 
        return {"MIN":elapsed_min, "SEC":elapsed_sec}    
    
    def get_final_elapsedtime(self):
        return self._final_elapsedtime
            
    def update_location(self):
        #print "my_locx=%d my_locy=%d" % (self._my_locx, self._my_locy)
        if self._my_direction == GameConstUtil.get_direction("UP"):
            my_next_locx = self._my_locx
            my_next_locy = self._my_locy - 1
        elif self._my_direction == GameConstUtil.get_direction("RIGHT"):     
            my_next_locx = self._my_locx + 1
            my_next_locy = self._my_locy
        elif self._my_direction == GameConstUtil.get_direction("DOWN"):     
            my_next_locx = self._my_locx
            my_next_locy = self._my_locy + 1
        elif self._my_direction == GameConstUtil.get_direction("LEFT"):     
            my_next_locx = self._my_locx - 1
            my_next_locy = self._my_locy
        #print "my_next_locx=%d my_next_locy=%d" % (my_next_locx, my_next_locy)
        
        #if it is not a wall, you can advance there.
        if self._get_object(my_next_locx, my_next_locy) != GameConstUtil.get_map_obj("WALL"):
            self._maze[self._my_locy][self._my_locx] = GameConstUtil.get_map_obj("PASSED")
            self._my_locx = my_next_locx
            self._my_locy = my_next_locy
            #print "my_locx=%d my_locy=%d AFTER ADVANCED" % (self._my_locx, self._my_locy)
            #Goal!
            if self._get_object(my_next_locx, my_next_locy) == GameConstUtil.get_map_obj("GOAL"):
                self._process_gameover()
            #Move the current location
            else:
                self._maze[self._my_locy][self._my_locx] = GameConstUtil.get_map_obj("HERE")        
            
    def update_direction(self, direction):
        if direction == "RIGHT":
            if self._my_direction == GameConstUtil.get_direction("UP"):
                self._my_direction = GameConstUtil.get_direction("RIGHT")
            elif self._my_direction == GameConstUtil.get_direction("RIGHT"):
                self._my_direction = GameConstUtil.get_direction("DOWN")
            elif self._my_direction == GameConstUtil.get_direction("DOWN"):
                self._my_direction = GameConstUtil.get_direction("LEFT")
            elif self._my_direction == GameConstUtil.get_direction("LEFT"):
                self._my_direction = GameConstUtil.get_direction("UP")
        elif direction == "BACKWARD":
            if self._my_direction == GameConstUtil.get_direction("UP"):
                self._my_direction = GameConstUtil.get_direction("DOWN")
            elif self._my_direction == GameConstUtil.get_direction("RIGHT"):
                self._my_direction = GameConstUtil.get_direction("LEFT")
            elif self._my_direction == GameConstUtil.get_direction("DOWN"):
                self._my_direction = GameConstUtil.get_direction("UP")
            elif self._my_direction == GameConstUtil.get_direction("LEFT"):
                self._my_direction = GameConstUtil.get_direction("RIGHT")
        elif direction == "LEFT":
            if self._my_direction == GameConstUtil.get_direction("UP"):
                self._my_direction = GameConstUtil.get_direction("LEFT")
            elif self._my_direction == GameConstUtil.get_direction("RIGHT"):
                self._my_direction = GameConstUtil.get_direction("UP")
            elif self._my_direction == GameConstUtil.get_direction("DOWN"):
                self._my_direction = GameConstUtil.get_direction("RIGHT")
            elif self._my_direction == GameConstUtil.get_direction("LEFT"):
                self._my_direction = GameConstUtil.get_direction("DOWN")
    
    def get_maze(self):
        return self._maze
    
    def get_path(self):
        if self._my_direction == GameConstUtil.get_direction("UP"):
            my_path_c = [self._get_object(self._my_locx, self._my_locy), 
                         self._get_object(self._my_locx, self._my_locy - 1), 
                         self._get_object(self._my_locx, self._my_locy - 2), 
                         self._get_object(self._my_locx, self._my_locy - 3), 
                         self._get_object(self._my_locx, self._my_locy - 4)]

            my_path_r = [self._get_object(self._my_locx + 1, self._my_locy), 
                         self._get_object(self._my_locx + 1, self._my_locy - 1), 
                         self._get_object(self._my_locx + 1, self._my_locy - 2), 
                         self._get_object(self._my_locx + 1, self._my_locy - 3), 
                         self._get_object(self._my_locx + 1, self._my_locy - 4)]

            my_path_l = [self._get_object(self._my_locx - 1, self._my_locy), 
                         self._get_object(self._my_locx - 1, self._my_locy - 1), 
                         self._get_object(self._my_locx - 1, self._my_locy - 2), 
                         self._get_object(self._my_locx - 1, self._my_locy - 3), 
                         self._get_object(self._my_locx - 1, self._my_locy - 4)]
            
        elif self._my_direction == GameConstUtil.get_direction("RIGHT"):
            my_path_c = [self._get_object(self._my_locx,        self._my_locy), 
                         self._get_object(self._my_locx + 1,    self._my_locy), 
                         self._get_object(self._my_locx + 2,    self._my_locy), 
                         self._get_object(self._my_locx + 3,    self._my_locy), 
                         self._get_object(self._my_locx + 4,    self._my_locy)]

            my_path_r = [self._get_object(self._my_locx,        self._my_locy+1), 
                         self._get_object(self._my_locx + 1,    self._my_locy+1), 
                         self._get_object(self._my_locx + 2,    self._my_locy+1), 
                         self._get_object(self._my_locx + 3,    self._my_locy+1), 
                         self._get_object(self._my_locx + 4,    self._my_locy+1)]

            my_path_l = [self._get_object(self._my_locx,        self._my_locy-1), 
                         self._get_object(self._my_locx + 1,    self._my_locy-1), 
                         self._get_object(self._my_locx + 2,    self._my_locy-1), 
                         self._get_object(self._my_locx + 3,    self._my_locy-1), 
                         self._get_object(self._my_locx + 4,    self._my_locy-1)]
            
        elif self._my_direction == GameConstUtil.get_direction("DOWN"):
            my_path_c = [self._get_object(self._my_locx, self._my_locy), 
                         self._get_object(self._my_locx, self._my_locy + 1), 
                         self._get_object(self._my_locx, self._my_locy + 2), 
                         self._get_object(self._my_locx, self._my_locy + 3), 
                         self._get_object(self._my_locx, self._my_locy + 4)]

            my_path_r = [self._get_object(self._my_locx - 1, self._my_locy), 
                         self._get_object(self._my_locx - 1, self._my_locy + 1), 
                         self._get_object(self._my_locx - 1, self._my_locy + 2), 
                         self._get_object(self._my_locx - 1, self._my_locy + 3), 
                         self._get_object(self._my_locx - 1, self._my_locy + 4)]

            my_path_l = [self._get_object(self._my_locx + 1, self._my_locy), 
                         self._get_object(self._my_locx + 1, self._my_locy + 1), 
                         self._get_object(self._my_locx + 1, self._my_locy + 2), 
                         self._get_object(self._my_locx + 1, self._my_locy + 3), 
                         self._get_object(self._my_locx + 1, self._my_locy + 4)]
            
        elif self._my_direction == GameConstUtil.get_direction("LEFT"):
            my_path_c = [self._get_object(self._my_locx,        self._my_locy), 
                         self._get_object(self._my_locx - 1,    self._my_locy), 
                         self._get_object(self._my_locx - 2,    self._my_locy), 
                         self._get_object(self._my_locx - 3,    self._my_locy), 
                         self._get_object(self._my_locx - 4,    self._my_locy)]

            my_path_r = [self._get_object(self._my_locx,        self._my_locy - 1), 
                         self._get_object(self._my_locx - 1,    self._my_locy - 1), 
                         self._get_object(self._my_locx - 2,    self._my_locy - 1), 
                         self._get_object(self._my_locx - 3,    self._my_locy - 1), 
                         self._get_object(self._my_locx - 4,    self._my_locy - 1)]

            my_path_l = [self._get_object(self._my_locx,        self._my_locy + 1), 
                         self._get_object(self._my_locx - 1,    self._my_locy + 1), 
                         self._get_object(self._my_locx - 2,    self._my_locy + 1), 
                         self._get_object(self._my_locx - 3,    self._my_locy + 1), 
                         self._get_object(self._my_locx - 4,    self._my_locy + 1)]
            
            
        #print "---------------------------"
        #print "###my_path_c"
        #print my_path_c
        #print "###my_path_l"
        #print my_path_l
        #print "###my_path_r"
        #print my_path_r
        my_path_dic = {"CENTER": my_path_c, "RIGHT": my_path_r, "LEFT": my_path_l}
        return my_path_dic
        
