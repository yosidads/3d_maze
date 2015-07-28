# coding: utf-8

from pygame.locals import * 
import sys
#from FontFile import WIDTH
from gamescreen import *
#from gamecontroller import *
from gameutil import *
from gamestate import *

################################################################################
class GameLauncher: 
    
    def __init__(self):
        pygame.init()
        #self.screen = gamesprite.display.set_mode(GameConstUtil.get_scr_rect().size, FULLSCREEN)
        self.screen = pygame.display.set_mode(GameConstUtil.get_scr_rect().size)
        pygame.display.set_caption(GameConstUtil.get_game_title())
        
        self._init_game()
        ########################################################################
        #Main Loop
        ########################################################################
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self._update()
            self._draw()
            pygame.display.update()
            if self.game_state.get_sound_to_play() != None:
                self.game_state.get_sound_to_play().play()
            self.game_state.set_sound_to_play(None)
            self._setup_key_handlers()
    
    def _init_game(self):
        self.game_state = GameState()
        #Game Screens
        self._start_screen = StartScreen()
        self._big_map_screen = BigMapScreen()
        self._3d_screen = ThreeDScreen()
        self._gameover_screen = GameOverScreen()
        #Game Controllers           
        #self._game_controller = GameController()

    def _get_screen(self):
        status = self.game_state.get_status()
        if status == GameConstUtil.get_game_status("START"):
            return self._start_screen
        elif status == GameConstUtil.get_game_status("BIG_MAP"):
            return self._big_map_screen
        elif status == GameConstUtil.get_game_status("3D_MAZE"):
            return self._3d_screen        
        elif status == GameConstUtil.get_game_status("GAMEOVER"):
            return self._gameover_screen        

    def _update(self):
        pass
                                    
    def _draw(self):
        self.screen.fill(GameConstUtil.get_color("BLACK"))
        self._get_screen().draw(self.screen, self.game_state)
            
    def _setup_key_handlers(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                if self.game_state.get_status() == GameConstUtil.get_game_status("START"):
                    self.game_state.set_status(GameConstUtil.get_game_status("3D_MAZE"))
                    self.game_state.set_starttime(pygame.time.get_ticks())
                elif self.game_state.get_status() == GameConstUtil.get_game_status("BIG_MAP"):
                    self.game_state.set_status(GameConstUtil.get_game_status("3D_MAZE"))
                elif self.game_state.get_status() == GameConstUtil.get_game_status("3D_MAZE"):
                    self.game_state.set_status(GameConstUtil.get_game_status("BIG_MAP"))
                elif self.game_state.get_status() == GameConstUtil.get_game_status("GAMEOVER"):
                    self._init_game()            
            elif event.type == KEYDOWN and event.key == K_UP:
                if self.game_state.get_status() == GameConstUtil.get_game_status("3D_MAZE"):
                    self.game_state.update_location()
                    self.game_state.set_sound_to_play(self.game_state.get_sounds()["WALK"])    
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                if self.game_state.get_status() == GameConstUtil.get_game_status("3D_MAZE"):                
                    self.game_state.update_direction("RIGHT")
                    self.game_state.set_sound_to_play(self.game_state.get_sounds()["TURN"])    
            elif event.type == KEYDOWN and event.key == K_DOWN:
                if self.game_state.get_status() == GameConstUtil.get_game_status("3D_MAZE"):
                    self.game_state.update_direction("BACKWARD")
                    self.game_state.set_sound_to_play(self.game_state.get_sounds()["TURN"])    
            elif event.type == KEYDOWN and event.key == K_LEFT:
                if self.game_state.get_status() == GameConstUtil.get_game_status("3D_MAZE"):
                    self.game_state.update_direction("LEFT")
                    self.game_state.set_sound_to_play(self.game_state.get_sounds()["TURN"])    

                                        
################################################################################
# Kick the program
################################################################################
if __name__ == "__main__":
    GameLauncher()
    
