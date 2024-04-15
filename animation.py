import pygame
from displayPuzzle import *
from copy import deepcopy

animation_wait_time = 1000
animation_reset_wait_time = 1500


class Animation:
    def __init__(self, moves: list[str], init_state: list[list[int]], puzzle: DisplayPuzzle) -> None:
        self.__moves = moves
        self.__init_state = init_state
        self.__puzzle = puzzle
        self.__animation_size = len(moves)
        self.__animation_step = 0
        self.__time_since_last_step = 200
        self.__previous_update_time = pygame.time.get_ticks()
        self.__puzzle.setState(deepcopy(self.__init_state))

    def update(self, deltaTime: int) -> None:
        current_time = pygame.time.get_ticks()
        self.__time_since_last_step += current_time - self.__previous_update_time
        self.__previous_update_time = current_time

        if self.__animation_step == self.__animation_size and self.__time_since_last_step > animation_reset_wait_time:
            self.__puzzle.setState(deepcopy(self.__init_state))
            self.__animation_step = 0
            self.__time_since_last_step = 200
            self.__puzzle.update(None, deltaTime)

        elif self.__time_since_last_step > animation_wait_time and self.__animation_step < self.__animation_size:
            self.__puzzle.update(self.__moves[self.__animation_step], deltaTime)
            self.__animation_step += 1
            self.__time_since_last_step = 0

        else:
            self.__puzzle.update(None, deltaTime)
