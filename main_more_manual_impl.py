import getpass
import random

import pygame as pg
import sys
from settings import *
from objects import *
from os import path
import copy
import os
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        self.font=path.join("PixelatedRegular-aLKm.ttf")
        self.tiles = [pg.image.load(f"tiles/tile_{i}.png").convert_alpha() for i in range(len(os.listdir("tiles")))]
        dif = TILESIZE // self.tiles[0].get_width()
        self.tiles_scaled = [pg.transform.scale(t, (t.get_width() * dif, t.get_height() * dif)) for t in self.tiles]

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.grid = []
        for i in range(GWIDTH * GHEIGHT):
            self.grid.append({"collapsed": False, "options": [BLANK, UP, RIGHT, DOWN, LEFT]})

        # self.grid[0]['collapsed'] = True
        # self.grid[0]['options'] = [DOWN]



    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def check_valid(self, valid, arr):

        for i in range(len(arr)-1, -1, -1):
            if arr[i] not in valid:
                arr.pop(i)





    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

        # pick a cell with the least entropy
        grid_copy = self.grid.copy()
        grid_copy.sort(key= lambda x : len(x["options"]))

        # filtering out collapsed cells
        grid_copy = [c for c in grid_copy if not c['collapsed']]

        # finding repetitions on the smallest entropy
        if grid_copy:
            smallest_entropy_cell = grid_copy[0]
            grid_copy = [c for c in grid_copy if len(c['options']) == len(smallest_entropy_cell["options"])]

            # collapsing a random cell
            cell = random.choice(grid_copy)
            cell["collapsed"] = True
            pick = random.choice(cell["options"])
            cell["options"] = [pick]

            # next generation of tiles
            next_cells = self.grid.copy()
            for i in range(DIM):
                for j in range(DIM):
                    index = i + j * DIM
                    if self.grid[index]["collapsed"]:
                        next_cells[index] = self.grid[index]
                    else:
                        options = [BLANK, UP, DOWN, RIGHT, LEFT]
                        up = self.grid[i + ((j - 1 + GHEIGHT) % GHEIGHT) * GWIDTH]
                        right = self.grid[((i + 1 + GWIDTH) % GWIDTH) + j * GWIDTH]
                        down = self.grid[i + ((j + 1 + GHEIGHT) % GHEIGHT) * GWIDTH]
                        left = self.grid[((i - 1 + GWIDTH) % GWIDTH) + j * GWIDTH]

                        all_valid = []
                        for option in up["options"]:
                            # accumulate bottom variants for every possible facing direction recorded in the tile above
                            all_valid += RULES[option][2]
                        if len(options) < 1:
                            options = [BLANK, UP, DOWN, RIGHT, LEFT]
                        self.check_valid(all_valid, options)



                        all_valid = []
                        for option in right["options"]:
                            all_valid += RULES[option][3]
                        if len(options) < 1:
                            options = [BLANK, UP, DOWN, RIGHT, LEFT]
                        self.check_valid(all_valid, options)



                        all_valid = []
                        for option in down["options"]:
                            all_valid += RULES[option][0]
                        if len(options) < 1:
                            options = [BLANK, UP, DOWN, RIGHT, LEFT]
                        self.check_valid(all_valid, options)



                        all_valid = []
                        for option in left["options"]:
                            all_valid += RULES[option][1]
                        self.check_valid(all_valid, options)
                        if len(options) < 1:
                            options = [BLANK, UP, DOWN, RIGHT, LEFT]


                        next_cells[index] = {"collapsed": False, "options": options}


            self.grid = next_cells



    def draw(self):
        self.screen.fill(WHITE)
        for i in range(DIM):
            for j in range(DIM):
                tile = self.grid[i + j * DIM]
                if tile['collapsed']:
                    # assuming that we have popped every other option
                    index = tile['options'][0]
                    self.screen.blit(self.tiles_scaled[index], (i * TILESIZE, j * TILESIZE))
                else:
                    pg.draw.rect(self.screen, BLACK, (i * TILESIZE, j * TILESIZE, TILESIZE, TILESIZE))
                    pg.draw.rect(self.screen, WHITE, (i * TILESIZE, j * TILESIZE, TILESIZE, TILESIZE), 1)


        # fps
        self.draw_text(str(int(self.clock.get_fps())), self.font, 40, WHITE, 50, 50, align="center")
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                



# create the game object
g = Game()
g.new()
g.run()
