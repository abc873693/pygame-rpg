import itertools
import sys
import time
import random
import math
import pygame
import colors
from utils import *

def enterMenu(pygame,screen,font,timer):
    print_text(font,100,100,'100',colors.white)
    while True:
        timer.tick(30)
        ticks = pygame.time.get_ticks()