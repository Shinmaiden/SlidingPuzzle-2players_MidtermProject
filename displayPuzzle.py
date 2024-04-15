from setting import *
from puzzle import Puzzle
import pygame, random


class DisplayPuzzle(Puzzle):
    def __init__(self, difficulty: int, size: int, window: pygame.display, position: tuple[int, int], mode: str,
                 scramble=True, ai=False) -> None:
        # initialise attributes
        super().__init__(difficulty, scramble)
        self.__size = size
        self.__window = window
        self.__position = position
        self.__moves = 0
        self.__mode = mode
        self.__race_finished = False

        self.__previous_demo_move = None
        self.__creation_time = pygame.time.get_ticks()
        self.__checked_against_best_time = False

        self.__animating = False
        self.__animating_piece_coordinate = None
        self.__animating_piece = None
        self.__animating_direction = None
        self.__accumulated_movement = 0

        self.__tile_size = (1 - PUZZLE_BORDER_SIZE) * self.__size / self._difficulty
        self.__tile_offset = PUZZLE_BORDER_SIZE / 2 * self.__size
        self.__textures = {
            1: pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile1.png')),
                                      (self.__tile_size, self.__tile_size)),
            2: pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile2.png')),
                                      (self.__tile_size, self.__tile_size)),
            3: pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile3.png')),
                                      (self.__tile_size, self.__tile_size)),
            4: pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile4.png')),
                                      (self.__tile_size, self.__tile_size)),
            5: pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile5.png')),
                                      (self.__tile_size, self.__tile_size)),
            6: pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile6.png')),
                                      (self.__tile_size, self.__tile_size)),
            7: pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile7.png')),
                                      (self.__tile_size, self.__tile_size)),
            8: pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile8.png')),
                                      (self.__tile_size, self.__tile_size)),
            9: pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile9.png')),
                                      (self.__tile_size, self.__tile_size)),
            10: pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile10.png')),
                                       (self.__tile_size, self.__tile_size)),
            11: pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile11.png')),
                                       (self.__tile_size, self.__tile_size)),
            12: pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile12.png')),
                                       (self.__tile_size, self.__tile_size)),
            13: pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile13.png')),
                                       (self.__tile_size, self.__tile_size)),
            14: pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile14.png')),
                                       (self.__tile_size, self.__tile_size)),
            15: pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile15.png')),
                                       (self.__tile_size, self.__tile_size)),
            16: pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile16.png')),
                                       (self.__tile_size, self.__tile_size)),
            17: pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile17.png')),
                                       (self.__tile_size, self.__tile_size)),
            18: pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile18.png')),
                                       (self.__tile_size, self.__tile_size)),
            19: pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile19.png')),
                                       (self.__tile_size, self.__tile_size)),
            20: pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile20.png')),
                                       (self.__tile_size, self.__tile_size)),
            21: pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile21.png')),
                                       (self.__tile_size, self.__tile_size)),
            22: pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile22.png')),
                                       (self.__tile_size, self.__tile_size)),
            23: pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile23.png')),
                                       (self.__tile_size, self.__tile_size)),
            24: pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Tile24.png')),
                                       (self.__tile_size, self.__tile_size)),
            'board': pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/boardBackground.png')),
                                            (self.__size, self.__size)),
        }

        self.__finished_backgrond = pygame.Surface((self.__size, self.__size))
        self.__board_rect = self.__finished_backgrond.get_rect()
        self.__finished_backgrond.set_alpha(150)
        self.__finished_backgrond.fill(BLACK)
        self.__finished_msg = big_font.render('Puzzle Solved!', False, WHITE)
        self.__finished_msg_rect = self.__finished_msg.get_rect(
            center=(self.__position[0] + self.__size / 2, self.__position[1] + self.__size / 2 - 25))
        self.__restart_msg = small_font.render('click on me to restart the game!', False, WHITE)
        self.__restart_msg_rect = self.__restart_msg.get_rect(
            center=(self.__position[0] + self.__size / 2, self.__position[1] + self.__size / 2 + 25))
        self.__won_msg = medium_font.render('You Won!', False, WHITE)
        self.__won_msg_rect = self.__won_msg.get_rect(
            center=(self.__position[0] + self.__size / 2, self.__position[1] + self.__size / 2 - 25))
        self.__lost_msg = medium_font.render('Tough Luck!', False, WHITE)
        self.__lost_msg_rect = self.__lost_msg.get_rect(
            center=(self.__position[0] + self.__size / 2, self.__position[1] + self.__size / 2 - 25))
        self.__two_player_restart_msg = small_font.render('click the restart button to restart!', False, WHITE)
        self.__two_player_restart_msg_rect = self.__two_player_restart_msg.get_rect(
            center=(self.__position[0] + self.__size / 2, self.__position[1] + self.__size / 2 + 25))
        self.__tutorial_finished_msg = big_font.render('Congratulations!', False, WHITE)
        self.__tutorial_finished_msg_rect = self.__tutorial_finished_msg.get_rect(
            center=(self.__position[0] + self.__size / 2, self.__position[1] + self.__size / 2 - 25))
        self.__tutorial_solved_msg = small_font.render('You solved the puzzle!', False, WHITE)
        self.__tutorial_solved_msg_rect = self.__tutorial_solved_msg.get_rect(
            center=(self.__position[0] + self.__size / 2, self.__position[1] + self.__size / 2 + 25))

    def displayMove(self, direction: str) -> bool:
        direction_moved, (row, column) = self.move(direction)
        if not direction_moved:
            return False

        self.isSolved()
        self.__moves += 1
        if direction == 'up':
            self.__animating_piece_coordinate = [self.__position[0] + self.__tile_offset + column * self.__tile_size,
                                                 self.__position[1] + self.__tile_offset + (row + 1) * self.__tile_size]
            self.__animating_direction = (0, -1)
            self.__animating_piece = self._state[row][column]
            return True

        elif direction == 'down':
            self.__animating_piece_coordinate = [self.__position[0] + self.__tile_offset + column * self.__tile_size,
                                                 self.__position[1] + self.__tile_offset + (row - 1) * self.__tile_size]
            self.__animating_direction = (0, 1)
            self.__animating_piece = self._state[row][column]
            return True

        elif direction == 'left':
            self.__animating_piece_coordinate = [
                self.__position[0] + self.__tile_offset + (column + 1) * self.__tile_size,
                self.__position[1] + self.__tile_offset + row * self.__tile_size]
            self.__animating_direction = (-1, 0)
            self.__animating_piece = self._state[row][column]
            return True

        else:
            self.__animating_piece_coordinate = [
                self.__position[0] + self.__tile_offset + (column - 1) * self.__tile_size,
                self.__position[1] + self.__tile_offset + row * self.__tile_size]
            self.__animating_direction = (1, 0)
            self.__animating_piece = self._state[row][column]
            return True

    def draw(self) -> None:
        self.__window.blit(self.__textures['board'], self.__position)
        for row in range(self._difficulty):
            for column in range(self._difficulty):
                element = self._state[row][column]
                if element == 0:
                    continue
                texture = self.__textures[element]
                coordinate = (self.__position[0] + self.__tile_offset + column * self.__tile_size,
                              self.__position[1] + self.__tile_offset + row * self.__tile_size)
                self.__window.blit(texture, coordinate)

    def animate(self, deltaTime: int) -> None:
        self.__window.blit(self.__textures['board'], self.__position)
        for row in range(self._difficulty):
            for column in range(self._difficulty):
                element = self._state[row][column]
                if element == 0 or element == self.__animating_piece:
                    continue
                texture = self.__textures[self._state[row][column]]
                coordinate = (self.__position[0] + self.__tile_offset + column * self.__tile_size,
                              self.__position[1] + self.__tile_offset + row * self.__tile_size)
                self.__window.blit(texture, coordinate)

        movement = self.__tile_size * deltaTime / ANIMATION_TIME
        self.__accumulated_movement += movement
        if self.__accumulated_movement < self.__tile_size:
            self.__animating_piece_coordinate = [
                self.__animating_piece_coordinate[0] + movement * self.__animating_direction[0],
                self.__animating_piece_coordinate[1] + movement * self.__animating_direction[1]]
            self.__window.blit(self.__textures[self.__animating_piece], self.__animating_piece_coordinate)
        else:
            self.draw()
            self.__animating = False

    def update(self, direction: str, deltaTime: int) -> None:
        if self.__mode == 'two-players' and self.__race_finished:
            self.draw()
            self.displayRaceEndCard()

        else:
            if direction != None:
                if not self.__animating:
                    moved = self.displayMove(direction)
                    if not moved:
                        self.draw()
                        return

                    self.__animating = True
                    self.__accumulated_movement = 0

                self.animate(deltaTime)
            else:
                self.draw() if not self.__animating else self.animate(deltaTime)

    def getDemoMove(self) -> str:
        choices = []
        flag = False
        for row in range(self._difficulty):
            if flag:
                break
            for column in range(self._difficulty):
                if self._state[row][column] == 0:
                    flag = True
                    if row != self._difficulty - 1 and self.__previous_demo_move != opposites['up']:
                        choices.append('up')

                    if row != 0 and self.__previous_demo_move != opposites["down"]:
                        choices.append('down')

                    if column != self._difficulty - 1 and self.__previous_demo_move != opposites['left']:
                        choices.append('left')

                    if column != 0 and self.__previous_demo_move != opposites['right']:
                        choices.append('right')
                    break

        new_demo_move = random.choice(choices)
        self.__previous_demo_move = new_demo_move
        return new_demo_move

    def displayEndCard(self) -> None:
        # victory screen for time trial mode
        self.__window.blit(self.__finished_backgrond, self.__position)
        self.__window.blit(self.__finished_msg, self.__finished_msg_rect)
        self.__window.blit(self.__restart_msg, self.__restart_msg_rect)

    def displayRaceEndCard(self) -> None:
        self.__window.blit(self.__finished_backgrond, self.__position)
        if self._game_won:
            self.__window.blit(self.__won_msg, self.__won_msg_rect)
            self.__window.blit(self.__two_player_restart_msg, self.__two_player_restart_msg_rect)
        else:
            self.__window.blit(self.__lost_msg, self.__lost_msg_rect)

    def getCreationTime(self) -> int:
        return self.__creation_time

    def getCheckedAgainstBestTime(self) -> bool:
        return self.__checked_against_best_time

    def setCheckedAgainstBestTime(self, checked_against_best_time: bool) -> None:
        self.__checked_against_best_time = checked_against_best_time

    def getBoardRect(self) -> pygame.Rect:
        return self.__board_rect

    def setRaceFinished(self, race_finished: bool) -> None:
        self.__race_finished = race_finished

    def getMoves(self) -> int:
        return self.__moves

    def getAnimating(self) -> bool:
        return self.__animating
