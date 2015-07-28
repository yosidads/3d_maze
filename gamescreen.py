# coding: utf-8

import pygame
from pygame.locals import *
from lib.word_wrapped_text_display_module import *
from gameutil import *
from telnetlib import theNULL

class GameScreen:
    
    def __init__(self):
        pass
    
    def draw(self, screen, game_state):
        pass
    
class StartScreen(GameScreen):
    
    def draw(self, screen, game_state):
        #TITLE
        title_font = pygame.font.SysFont(None, 80)
        title = title_font.render(GameConstUtil.get_game_title(), False, GameConstUtil.get_color("YELLOW"))
        screen.blit(title, ((GameConstUtil.get_scr_rect().width-title.get_width())/2, 100))
        #PUSH START
        push_font = pygame.font.SysFont(None, 40)
        push_space = push_font.render("PUSH SPACE KEY", False, GameConstUtil.get_color("WHITE"))
        screen.blit(push_space, ((GameConstUtil.get_scr_rect().width-push_space.get_width())/2, 250))
        #CREDIT
        credit_font = pygame.font.SysFont(None, 20)
        credit = credit_font.render("Programmed by Daisuke Y. in 2015", False, GameConstUtil.get_color("WHITE"))
        screen.blit(credit, ((GameConstUtil.get_scr_rect().width-credit.get_width())/2, 320))
        #SPECIAL THANKS TO
        special_thanks_font = pygame.font.SysFont(None, 20)
        special_thanks = credit_font.render("Special Thanks To:", False, GameConstUtil.get_color("CYAN"))
        screen.blit(special_thanks, ((GameConstUtil.get_scr_rect().width-special_thanks.get_width())/2, 350))

        sp_thanks_to_txt = "Somebody who taught me this game 30yrs ago\n"
                            #"Z.Yoshida\n" \
                            #"J.M.Yoshida"
        sp_thanks_to_font = pygame.font.SysFont(None, 20)                    
        sp_thanks_to_rect = pygame.Rect((0, 0, 320, 80))
        sp_thanks_to_rendered_text = \
                render_textrect(sp_thanks_to_txt, sp_thanks_to_font, sp_thanks_to_rect, GameConstUtil.get_color("CYAN"), GameConstUtil.get_color("BLACK"), 1)        
        screen.blit(sp_thanks_to_rendered_text, ((GameConstUtil.get_scr_rect().width-sp_thanks_to_rendered_text.get_width())/2, 365))   
        
        #special_thanks_zy_font = gamesprite.font.SysFont(None, 20)
        #special_thanks_zy = credit_font.render("Z.Yoshida", False, GameConstUtil.get_color("WHITE"))
        #screen.blit(special_thanks_zy, ((GameConstUtil.get_scr_rect().width-special_thanks_zy.get_width())/2, 380))
        #special_thanks_jy_font = gamesprite.font.SysFont(None, 20)
        #special_thanks_jy = credit_font.render("J.M.Yoshida", False, GameConstUtil.get_color("WHITE"))
        #screen.blit(special_thanks_jy, ((GameConstUtil.get_scr_rect().width-special_thanks_jy.get_width())/2, 410))


            
class BigMapScreen(GameScreen):
    
    def draw(self, screen, game_state):
        #ELAPSED_TIME
        elapsedtime = game_state.get_elapsedtime()
        elapsedtime_font = pygame.font.SysFont(None, 20)
        elapsedtime_rect = elapsedtime_font.render(str(elapsedtime["MIN"]) + "mins " + str(elapsedtime["SEC"]) + "secs", False, GameConstUtil.get_color("WHITE"))
        screen.blit(elapsedtime_rect, ((270, 20)))
        #screen.blit(elapsedtime_rect, ((GameConstUtil.get_scr_rect().width-elapsedtime_rect.get_width())/2, 20))
                
        my_maze = game_state.get_maze()
        for y in range(len(my_maze)):
            for x in range(len(my_maze[y])):
                rect = pygame.Rect(0 + (10 * x), 40 + (10 * y), 10, 10)
                if my_maze[y][x] == GameConstUtil.get_map_obj("ROAD"):
                    color = GameConstUtil.get_color("BLACK")
                elif my_maze[y][x] == GameConstUtil.get_map_obj("WALL"):
                    color = GameConstUtil.get_color("GREEN")
                elif my_maze[y][x] == GameConstUtil.get_map_obj("HERE"):
                    color = GameConstUtil.get_color("YELLOW")
                elif my_maze[y][x] == GameConstUtil.get_map_obj("PASSED"):
                    color = GameConstUtil.get_color("RED")
                elif my_maze[y][x] == GameConstUtil.get_map_obj("GOAL"):
                    color = GameConstUtil.get_color("PURPLE")
                pygame.draw.rect(screen, color, rect, 0)    

class ThreeDScreen(GameScreen):
    
    def _draw_wall(self, screen, game_state):
        my_path_dic = game_state.get_path()
        my_path_c = my_path_dic["CENTER"]
        my_path_r = my_path_dic["RIGHT"]
        my_path_l = my_path_dic["LEFT"]

        #If there is a goal before a wall, do not draw the wall.
        goal_loc_idx_c = 100
        goal_loc_idx_r = 100
        goal_loc_idx_l = 100
        wall_loc_idx_c = 100
        wall_loc_idx_r = 100
        wall_loc_idx_l = 100
        check_flag_c = True
        check_flag_r = True
        check_flag_l = True
        for i in range(len(my_path_c)):
            if my_path_c[i] == GameConstUtil.get_map_obj("GOAL"):
                goal_loc_idx_c = i
            if my_path_c[i] == GameConstUtil.get_map_obj("WALL") and check_flag_c:
                wall_loc_idx_c = i
                check_flag_c = False
            if my_path_r[i] == GameConstUtil.get_map_obj("GOAL"):
                goal_loc_idx_r = i
            if my_path_r[i] == GameConstUtil.get_map_obj("WALL") and check_flag_r:
                wall_loc_idx_r = i
                check_flag_r = False
            if my_path_l[i] == GameConstUtil.get_map_obj("GOAL"):
                goal_loc_idx_l = i
            if my_path_l[i] == GameConstUtil.get_map_obj("WALL") and check_flag_l:
                wall_loc_idx_l = i
                check_flag_l = False

        #Draw Right-side        
        n = len(my_path_r) - 1    
        for m in range(len(my_path_r)):
            if (my_path_r[m] == GameConstUtil.get_map_obj("GOAL") and m < wall_loc_idx_r) or \
                (my_path_r[m] == GameConstUtil.get_map_obj("WALL") and m < goal_loc_idx_r):
                
                color = GameConstUtil.get_color("PURPLE") if my_path_r[m] == GameConstUtil.get_map_obj("GOAL") else GameConstUtil.get_color("CYAN")
                move_dist = (350 + (n * 55)) - (290 + (n * -55))
                rect = pygame.Rect(290 + (n * -55) + move_dist, 210 + (n * -55), (350 + (n * 55)) - (290 + (n * -55)), (270 + (n * 55)) - (210 + (n * -55)))
                pygame.draw.rect(screen, color, rect, 0)
                if n > 0:
                    for j in range(55):
                        pygame.draw.line(screen, color, ( 350 + (n * 55) - j, 210 + (n * -55) + j), ( 350 + (n * 55) - j, 270 + (n * 55) - j)) 
                            
            n -= 1

        #Draw Left-side        
        n = len(my_path_l) - 1    
        for m in range(len(my_path_l)):
            if (my_path_l[m] == GameConstUtil.get_map_obj("GOAL") and m < wall_loc_idx_l) or \
                (my_path_l[m] == GameConstUtil.get_map_obj("WALL") and m < goal_loc_idx_l):

                color = GameConstUtil.get_color("PURPLE") if my_path_l[m] == GameConstUtil.get_map_obj("GOAL") else GameConstUtil.get_color("CYAN")
                move_dist = ((350 + (n * 55)) - (290 + (n * -55))) * -1
                rect = pygame.Rect(290 + (n * -55) + move_dist, 210 + (n * -55), (350 + (n * 55)) - (290 + (n * -55)), (270 + (n * 55)) - (210 + (n * -55)))
                pygame.draw.rect(screen, color, rect, 0)
                if n > 0:
                    for j in range(55):
                        pygame.draw.line(screen, color, ( 290 + (n * -55) + j, 210 + (n * -55) + j), ( 290 + (n * -55) + j, 270 + (n * 55) - j)) 
            n -= 1
        
        #Draw Center    
        n = len(my_path_c) - 1    
        for m in range(len(my_path_c)):
            if (my_path_c[m] == GameConstUtil.get_map_obj("GOAL") and m < wall_loc_idx_c) or \
                (my_path_c[m] == GameConstUtil.get_map_obj("WALL") and m < goal_loc_idx_c):

                color = GameConstUtil.get_color("PURPLE") if my_path_c[m] == GameConstUtil.get_map_obj("GOAL") else GameConstUtil.get_color("CYAN")
                rect = pygame.Rect(290 + (n * -55), 210 + (n * -55), (350 + (n * 55)) - (290 + (n * -55)), (270 + (n * 55)) - (210 + (n * -55)))
                pygame.draw.rect(screen, color, rect, 0)
                                
            n -= 1

    def draw(self, screen, game_state):

        #ELAPSED_TIME
        elapsedtime = game_state.get_elapsedtime()
        elapsedtime_font = pygame.font.SysFont(None, 20)
        elapsedtime_rect = elapsedtime_font.render(str(elapsedtime["MIN"]) + "mins " + str(elapsedtime["SEC"]) + "secs", False, GameConstUtil.get_color("WHITE"))
        screen.blit(elapsedtime_rect, ((270, 20)))
 
        #Diagonal Lines
        pygame.draw.line(screen, GameConstUtil.get_color("WHITE"), (120, 40),   (290, 210))
        pygame.draw.line(screen, GameConstUtil.get_color("WHITE"), (520, 40),   (350, 210))
        pygame.draw.line(screen, GameConstUtil.get_color("WHITE"), (120, 440),  (290, 270))
        pygame.draw.line(screen, GameConstUtil.get_color("WHITE"), (520, 440),  (350, 270))
        
        for n in range(4):
            #Horizontal Lines
            pygame.draw.line(screen, GameConstUtil.get_color("WHITE"), (290 + (n * -55), 270 + (n * 55)),   (350 + (n * 55), 270 + (n * 55)))
            pygame.draw.line(screen, GameConstUtil.get_color("WHITE"), (290 + (n * -55), 210 + (n * -55)),  (350 + (n * 55), 210 + (n * -55)))
            #Vertical Lines
            pygame.draw.line(screen, GameConstUtil.get_color("WHITE"), (290 + (n * -55),    210 + (n * -55)), (290 + (n * -55), 270 + (n * 55)))
            pygame.draw.line(screen, GameConstUtil.get_color("WHITE"), (350 + (n * 55),     210 + (n * -55)), (350 + (n * 55),  270 + (n * 55)))
        
        #Wall drawing
        self._draw_wall(screen, game_state)
        
class GameOverScreen(GameScreen):
    
    def draw(self, screen, game_state):
        elapsedtime = game_state.get_final_elapsedtime()
        #Result
        result_font = pygame.font.SysFont(None, 40)
        result = result_font.render("Your time is " + str(elapsedtime["MIN"]) + "mins " + str(elapsedtime["SEC"]) + "secs", False, GameConstUtil.get_color("CYAN"))
        screen.blit(result, ((GameConstUtil.get_scr_rect().width-result.get_width())/2, 100))
        #PUSH START
        push_font = pygame.font.SysFont(None, 40)
        push_space = push_font.render("PUSH SPACE KEY", False, GameConstUtil.get_color("WHITE"))
        screen.blit(push_space, ((GameConstUtil.get_scr_rect().width-push_space.get_width())/2, 250))

