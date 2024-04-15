import random
from setting import *


class Puzzle:
    def __init__(self, difficulty: int, scramble: bool) -> None:
        self._game_won = False
        self._difficulty = difficulty

        self._state = [[0 for x in range(difficulty)] for y in range(difficulty)]
        current_number = 1
        for y in range(difficulty):
            for x in range(difficulty):
                if current_number == difficulty ** 2:
                    break
                self._state[y][x] = current_number
                current_number += 1

        if scramble:
            for i in range(1000):
                self.move(random.choice(['up', 'down', 'left', 'right']))

    def move(self, direction: str) -> tuple[str, tuple[int]]:
        if not direction:
            return None, (None, None)

        for row in range(self._difficulty):
            for column in range(self._difficulty):
                element = self._state[row][column]
                if element == 0:
                    if direction == 'up':
                        if row == self._difficulty - 1:
                            return None, (None, None)
                        self._state[row][column] = self._state[row + 1][column]
                        self._state[row + 1][column] = 0
                        return 'up', (row, column)

                    elif direction == 'down':
                        if row == 0:
                            return None, (None, None)
                        self._state[row][column] = self._state[row - 1][column]
                        self._state[row - 1][column] = 0
                        return 'down', (row, column)

                    elif direction == 'left':
                        if column == self._difficulty - 1:
                            return None, (None, None)
                        self._state[row][column] = self._state[row][column + 1]
                        self._state[row][column + 1] = 0
                        return 'left', (row, column)

                    else:
                        if column == 0:
                            return None, (None, None)
                        self._state[row][column] = self._state[row][column - 1]
                        self._state[row][column - 1] = 0
                        return 'right', (row, column)

    def __str__(self) -> None:
        string = ""
        for row in self._state:
            for num in row:
                if num < 10:
                    string += f"{num}  "
                else:
                    string += f"{num} "
            string += "\n"
        return string

    def isSolved(self) -> bool:
        counter = 1
        for row in range(self._difficulty):
            for column in range(self._difficulty):
                element = self._state[row][column]
                if element != counter:
                    self._game_won = False
                    return False
                if counter == self._difficulty ** 2 - 1:
                    self._game_won = True
                    return True

                counter += 1

    def layerOnePatternMade(self) -> bool:
        return self._state[0][0] == 2 and self._state[0][1] == 3 and self._state[1][0] == 1

    def firstLayerSolved(self) -> bool:
        counter = 1
        for row in range(self._difficulty):
            for column in range(self._difficulty):
                element = self._state[row][column]
                if element != counter:
                    return False
                if counter == self._difficulty:
                    return True

                counter += 1

    def secondLayerSolved(self) -> bool:
        counter = 1
        for row in range(self._difficulty):
            for column in range(self._difficulty):
                element = self._state[row][column]
                if element != counter:
                    return False
                if counter == self._difficulty * 2:
                    return True

                counter += 1

    # getters and setters
    def getGameWon(self) -> bool:
        return self._game_won

    def getDifficulty(self) -> int:
        return self._difficulty

    def getState(self) -> list[list[int]]:
        return self._state

    def setState(self, state: list[list[int]]) -> None:
        self._state = state
