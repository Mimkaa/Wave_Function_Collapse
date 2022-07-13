import getpass
import random

import pygame as pg
import sys
from settings import *
from objects import *
from os import path
from socket_creation import classify_colors

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
        #self.tiles = [pg.image.load(f"tiles/tile_{i}.png").convert_alpha() for i in range(len(os.listdir("tiles")))]
        self.tile_images = [pg.image.load(f"tiles1/tile_{i}.png").convert_alpha() for i in (0, 1)]
        dif = TILESIZE // self.tile_images[0].get_width()
        self.tile_images = [pg.transform.scale(t, (t.get_width() * dif, t.get_height() * dif)) for t in self.tile_images]

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
        # build tiles
        self.color_lookups = {}
        for img in self.tile_images:
            self.color_lookups.update(classify_colors(img))

        up_tile = Tile(self.tile_images[0],self.color_lookups)
        self.tiles = [Tile(self.tile_images[1],self.color_lookups), up_tile, up_tile.rotate(3), up_tile.rotate(2), up_tile.rotate(1)]



        # generate adjacency rules based on the edges
        for t in self.tiles:
            t.analyze(self.tiles)

        # fill the grid with cells
        self.grid = []
        for i in range(GWIDTH * GHEIGHT):
            self.grid.append(Cell(len(self.tiles)))


        #
        # self.grid[0]['collapsed'] = True
        # self.grid[0]['options'] = [LEFT]



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


        # pick a cell with the least entropy
        grid_copy = self.grid.copy()
        grid_copy.sort(key= lambda x : len(x.options))

        # filtering out collapsed cells
        grid_copy = [c for c in grid_copy if not c.collapsed]

        # finding repetitions of the smallest entropy
        if grid_copy:
            smallest_entropy_cell = grid_copy[0]
            grid_copy = [c for c in grid_copy if len(c.options) == len(smallest_entropy_cell.options)]

            # collapsing a random cell
            cell = random.choice(grid_copy)
            cell.collapsed = True
            pick = random.choice(cell.options)
            cell.options = [pick]

            # next generation of tiles
            next_cells = self.grid.copy()
            for i in range(DIM):
                for j in range(DIM):
                    index = i + j * DIM
                    if self.grid[index].collapsed:
                        next_cells[index] = self.grid[index]
                    else:
                        options_or = [BLANK, UP, DOWN, RIGHT, LEFT]
                        options = [i for i in range(len(options_or))]
                        up = self.grid[i + ((j - 1 + GHEIGHT) % GHEIGHT) * GWIDTH]
                        right = self.grid[((i + 1 + GWIDTH) % GWIDTH) + j * GWIDTH]
                        down = self.grid[i + ((j + 1 + GHEIGHT) % GHEIGHT) * GWIDTH]
                        left = self.grid[((i - 1 + GWIDTH) % GWIDTH) + j * GWIDTH]

                        all_valid = []
                        for option in up.options:
                            # accumulate bottom variants for every possible facing direction recorded in the tile above
                            all_valid += self.tiles[option].down
                        self.check_valid(all_valid, options)
                        if len(options) < 1:
                            options = [i for i in range(len(options_or))]



                        all_valid = []
                        for option in right.options:
                            all_valid += self.tiles[option].left
                        self.check_valid(all_valid, options)
                        if len(options) < 1:
                            options = [i for i in range(len(options_or))]



                        all_valid = []
                        for option in down.options:
                            all_valid += self.tiles[option].up
                        self.check_valid(all_valid, options)
                        if len(options) < 1:
                            options = [i for i in range(len(options_or))]



                        all_valid = []
                        for option in left.options:
                            all_valid += self.tiles[option].right
                        self.check_valid(all_valid, options)
                        if len(options) < 1:
                            options = [i for i in range(len(options_or))]



                        next_cells[index] = Cell(options)


            self.grid = next_cells



    def draw(self):
        self.screen.fill(WHITE)
        for i in range(DIM):
            for j in range(DIM):
                cell = self.grid[i + j * DIM]
                if cell.collapsed:
                    # assuming that we have popped every other option
                    index = cell.options[0]
                    self.screen.blit(self.tiles[index].img, (i * TILESIZE, j * TILESIZE))
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
