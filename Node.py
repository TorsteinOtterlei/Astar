import numpy as np
np.set_printoptions(threshold=np.inf, linewidth=300)
import pandas as pd
import time
from PIL import Image

class node():

    def __init__(self, pos):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]

        self.g = None
        self.h = None
        self.f = None

        self.parent = None
        self.children = []


    def set_g(self,val):
        self.g = val
        if not(self.g is None or self.h is None):
            self.f = self.g + self.h

    
    def set_h(self, val):
        self.h = val
        if not(self.g is None or self.h is None):
            self.f = self.g + self.h
        