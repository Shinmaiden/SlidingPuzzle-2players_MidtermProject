from setting import *
import pygame

pygame.init()

KNOB_COLOR = (59, 59, 59)
RAIL_COLOR = (115, 115, 115)
BORDER_COLOR = (255, 255, 255)


class Slider:
    def __init__(self,
                 window: pygame.display,
                 lower_bound: float,
                 upper_bound: float,
                 slider_center: tuple[int, int],
                 rail_length: int,
                 rail_height: int,
                 knob_length: int,
                 knob_height: int,
                 border_size: int,
                 starting_value: float) -> None:

        self.__window = window
        self.__lower_bound = lower_bound
        self.__upper_bound = upper_bound
        self.__slider_center = slider_center
        self.__rail_length = rail_length
        self.__rail_height = rail_height
        self.__knob_length = knob_length
        self.__knob_height = knob_height
        self.__border_size = border_size

        self.__rail = pygame.Rect(self.__slider_center[0] - self.__rail_length / 2,
                                  self.__slider_center[1] - self.__rail_height / 2,
                                  self.__rail_length,
                                  self.__rail_height)

        self.__rail_bg = pygame.Rect(self.__slider_center[0] - self.__rail_length / 2 - self.__border_size,
                                     self.__slider_center[1] - self.__rail_height / 2 - self.__border_size,
                                     self.__rail_length + 2 * self.__border_size,
                                     self.__rail_height + 2 * self.__border_size)

        self.__knob = pygame.Rect(self.__slider_center[0] - self.__rail_length / 2 + starting_value / (
                self.__upper_bound - self.__lower_bound) * self.__rail_length,
                                  self.__slider_center[1] - self.__knob_height / 2,
                                  self.__knob_length,
                                  self.__knob_height)

        self.__knob_bg = pygame.Rect(self.__slider_center[0] - self.__rail_length / 2 + starting_value / (
                self.__upper_bound - self.__lower_bound) * self.__rail_length - self.__border_size,
                                     self.__slider_center[1] - self.__knob_height / 2 - self.__border_size,
                                     self.__knob_length + 2 * self.__border_size,
                                     self.__knob_height + 2 * self.__border_size)

        self.__dragging = False
        self.__original_x = None

    def mouseOnKnob(self, mouse: tuple[int, int]) -> bool:
        if self.__knob.collidepoint(mouse):
            self.__original_x = mouse[0]
            return True
        return False

    def drag(self, mouse_x: int) -> None:
        displacement = mouse_x - self.__original_x
        knobPos = self.__knob.x + displacement
        if knobPos < self.__rail.x:
            knobPos = self.__rail.x
        elif knobPos > self.__rail.x + self.__rail.width - self.__knob_length:
            knobPos = self.__rail.x + self.__rail.width - self.__knob_length
        self.__knob.update((knobPos, self.__knob.y), (self.__knob_length, self.__knob_height))
        self.__knob_bg.update((knobPos - self.__border_size, self.__knob.y - self.__border_size), (
            self.__knob_length + 2 * self.__border_size, self.__knob_height + 2 * self.__border_size))
        self.__original_x = self.__knob.x + self.__knob_length / 2

    def getValue(self) -> float:
        knob_x_pos = (self.__knob.centerx - self.__rail.x - self.__knob_length / 2)
        rail_length = (self.__rail.width - self.__knob.width)
        bounds_difference = (self.__upper_bound - self.__lower_bound)
        return self.__lower_bound + knob_x_pos / rail_length * bounds_difference

    def draw(self) -> None:
        # draws the slider on screen
        pygame.draw.rect(self.__window, BORDER_COLOR, self.__rail_bg)
        pygame.draw.rect(self.__window, RAIL_COLOR, self.__rail)
        pygame.draw.rect(self.__window, BORDER_COLOR, self.__knob_bg)
        pygame.draw.rect(self.__window, KNOB_COLOR, self.__knob)

    # getters and setters
    def getDragging(self) -> bool:
        return self.__dragging

    def setDragging(self, dragging: bool) -> None:
        self.__dragging = dragging
