import pygame as pg
import sys
from settings import *
from objects import *
from os import path
import numpy as np
from PIL import Image

def Surf_to_PIL(surf):
        raw_str = pg.image.tostring(surf, 'RGBA', False)
        image = Image.frombytes('RGBA', surf.get_size(), raw_str)
        return image

def classify_colors(surf):
    image = Surf_to_PIL(surf)
    np_image = np.asarray(image)
    shape = np_image.shape
    edge_pixels = []
    color_socket = {}
    num = 0
    for y in range(shape[0]):
        for x in range(shape[1]):
            if y == 0 or x == 0 or y == shape[0] - 1 or x == shape[1] - 1:
                if not tuple(np_image[y][x]) in edge_pixels :

                    edge_pixels.append(tuple(np_image[y][x]))
                    color_socket[tuple(np_image[y][x])] = num
                    num += 1
    return color_socket

def make_sockets(surf, lookups):
    image = Surf_to_PIL(surf)
    np_image = np.asarray(image)
    shape = np_image.shape
    sockets = []
    top = []
    right = []
    bottom = []
    left = []
    # TOP
    current_color = (0, 0, 0, 0)
    for x in range(len(np_image[0])):
        if current_color != tuple(np_image[0][x]):
            current_color = tuple(np_image[0][x])
            top.append(lookups[current_color])
    # BOTTOM
    current_color = (0, 0, 0, 0)
    for x in range(len(np_image[-1])):
        if current_color != tuple(np_image[-1][x]):
            current_color = tuple(np_image[-1][x])
            bottom.append(lookups[current_color])
    # RIGHT
    current_color = (0, 0, 0, 0)
    for y in range(shape[0]):
        for x in range(shape[1]):
            if x == shape[1] - 1:
                if current_color != tuple(np_image[y][x]):
                    current_color = tuple(np_image[y][x])
                    right.append(lookups[current_color])
    # LEFT
    current_color = (0, 0, 0, 0)
    for y in range(shape[0]):
        for x in range(shape[1]):
            if x == 0:
                if current_color != tuple(np_image[y][x]):
                    current_color = tuple(np_image[y][x])
                    left.append(lookups[current_color])
    bottom.reverse()
    left.reverse()

    sockets.append(top)
    sockets.append(left)
    sockets.append(bottom)
    sockets.append(right)

    return sockets


