import math
import pygame as pg
from socket_creation import make_sockets
class Tile:
    def __init__(self, img, color_lookup):
        self.img = img
        self.img_copy = self.img.copy()

        self.edges = make_sockets(self.img, color_lookup)
        self.up = []
        self.right = []
        self.down = []
        self.left = []
        self.color_lookup =  color_lookup


    def rotate(self, num):
        # rotate the image
        img = pg.transform.rotate(self.img_copy, math.degrees(math.pi/2) * num)

        # rotate edges
        # new_edges = []
        # length = len(self.edges)
        # for i in range(length):
        #     new_edges.append(self.edges[(i - num + length) % length])


        return Tile(img, self.color_lookup)

    def compare(self, edge1, edge2):
        return edge1 == edge2

    def analyze(self, tiles):

        for i in range(len(tiles)):
            # UP
            if self.compare(tiles[i].edges[2], self.edges[0]):
                self.up.append(i)
            # RIGHT
            if self.compare(tiles[i].edges[3], self.edges[1]):
                self.left.append(i)
            # DOWN
            if self.compare(tiles[i].edges[0], self.edges[2]):
                self.down.append(i)
            # LEFT
            if self.compare(tiles[i].edges[1], self.edges[3]):
                self.right.append(i)



class Cell:
    def __init__(self, num):
        self.collapsed = False
        self.options = []
        if type(num) == list:
            self.options = num
        else:
            for i in range(num):
                self.options.append(i)
