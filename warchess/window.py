import imutils
import pygame
import numpy as np
import cv2
import time
import sys
import os


from abstracts import InvalidMove
from classes import ClassicGame
from pygame import mixer

pygame.init()

size = width, height = 900, 500

screen = pygame.display.set_mode(size)

t0 = time.time()
duration = 120

game = ClassicGame()
game.new_game()
game.ignore_turn = True

offset = 50
box = 50
board_blend = 60

# pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
snd_move = pygame.mixer.Sound(f"sounds{os.sep}wood_move_1.mp3")
snd_hit = pygame.mixer.Sound(f"sounds{os.sep}wood_hit_1.mp3")


# snd_move.set_volume(0.2)


def get_box_pos(mouse_pos):
    out = np.array(mouse_pos) - offset - box // 2
    out = np.round(out / box)
    return out


class BoardScene:
    def __init__(self, width, height, board, margin=0.1, box=None,
                 flip_image=True, flip_board=False):
        self.width = width
        self.height = height
        self.board = board
        self.margin = margin
        self.flip_image = flip_image
        self.flip_board = flip_board
        # self.game = game
        # self.board = board
        if type(box) == int:
            self.offset = self.get_offsets()
            self.box = box
        else:
            self.offset, self.box = self.auto_adjust_box_to_margin()

    def auto_adjust_box_to_margin(self):
        is_height_shorter = self.width >= self.height
        operating_dist = self.height if is_height_shorter else self.width

        box = operating_dist * (1 - 2 * self.margin) / 8

        offset1 = (self.width - box * 8) / 2
        offset2 = (self.height - box * 8) / 2

        return (offset1, offset2), int(box)

    def get_offsets(self):
        off_left = self.width * self.margin
        off_top = self.height * self.margin
        return off_left, off_top

    def get_field_position(self, pos):
        x, y = pos
        if self.flip_image:
            y = self.board.height - y - 1

        if self.flip_board:
            x = self.board.width - x - 1
            y = self.board.height - y - 1

        x = x * self.box + self.offset[0]  # + self.box // 2
        y = y * self.box + self.offset[1]  # + self.box // 2

        return x, y

    def locate_field(self, pos):
        x, y = pos
        x = (x - self.offset[0]) / self.box
        y = (y - self.offset[1]) / self.box

        if self.flip_image:
            y = self.board.height - y
        if self.flip_board:
            y = self.board.height - y
            x = self.board.width - x

        return tuple(np.floor([x, y]).astype(int))


scene = BoardScene(width, height, game.board)

activ = None

while True and (time.time() - t0) < duration:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sys.exit()

            if event.key == pygame.K_SPACE:
                scene.flip_board = not scene.flip_board

        if event.type == pygame.MOUSEBUTTONDOWN:
            left, middle, right = pygame.mouse.get_pressed()
            pos = pygame.mouse.get_pos()
            field = scene.locate_field(pos)
            # txt = game.ints_to_strings(field)
            # print(f"Clicked: {txt}")
            if left and not activ:
                activ = field

            elif left and activ:
                try:
                    hit = game.make_move(activ, field)
                except InvalidMove:
                    hit= None

                if hit:
                    snd_hit.play()
                else:
                    snd_move.play()
                activ = None

            if right:
                activ = None

    frac = (duration - (time.time() - t0)) / duration
    col = (0, int(frac * 124), int((1 - frac) * 230))
    screen.fill(col)

    "Draw fields"
    for pos, color in game.board.fields:
        if color:
            col = (255 - board_blend, 255 - board_blend, 255 - board_blend)
        else:
            col = (board_blend, board_blend, board_blend)

        x, y = scene.get_field_position(pos)
        pygame.draw.rect(screen, col, (x, y, scene.box, scene.box))

    "Draw figures"
    for pos, fig in game.board:
        color = fig.color
        if color == 0:
            col = (255, 255, 255)
        else:
            col = (0, 0, 0)

        x, y = scene.get_field_position(pos)
        x += 10
        my_font = pygame.font.SysFont('Arial', scene.box, bold=True)
        text_surface = my_font.render(fig.symbol, False, col)

        screen.blit(text_surface, (x, y))

    if activ:
        tile = pygame.Surface((scene.box, scene.box))
        tile.fill((0, 170, 0))
        tile.set_alpha(150)
        pos = scene.get_field_position(activ)
        screen.blit(tile, pos)

    col = pygame.color.Color(250, 200, 0)
    surf2 = pygame.Surface((50, 50), pygame.SRCALPHA)
    pygame.draw.circle(surf2, col, (box // 2, box // 2), 10)
    surf2.set_alpha(200)

    mouse_pos = pygame.mouse.get_pos()
    field = scene.locate_field(mouse_pos)
    # print(f"Field: {field}")
    pos = scene.get_field_position(field)
    screen.blit(surf2, pos, )

    pygame.display.update()
    pygame.time.wait(10)

    # time.sleep(0.01)
