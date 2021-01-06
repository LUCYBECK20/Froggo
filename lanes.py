"""
Lanes module for Froggo

Author: Lucy Beck
Date: January 2, 2021
"""
from kivy.graphics import *
from models import *
from constants import *
from PIL import Image
import os


class Lane(object):
    """
    Parent class for a lane.
    """
    # Attribute _width: the width of the window to animate in
    # Invariant: _width is a float > 0
    #
    # Attribute _tiles: a list of tiles for each lane
    # Invariant: _tile is a list of kivy.graphics Rectangles
    #
    # Attribute _objs: a list of all of the objects in the lanes
    # Invariant: _objs is a list of kivy.graphics Rectangles
    #
    # Attribute _speed: the speed of the objects in the lanes
    # Invariant: _speed is a number (int or float)
    #
    # Attribute _buffer: how far (in grid squares) that any image must be
    #                    offscreen before it is time to wrap it back around
    # Invariant: _buffer is an int
    #
    # Attribute _animator: A coroutine for performing an animation
    # Invariant: _animator is a generator-based coroutine (or None)
    #

    def __init__(self,width,leveldict,imagespath,pos):
        """
        Initializes the lanes.

        Parameter width: The width of the window to animate in
        Precondition : width is a number (int or float) > 0

        Parameter leveldict: A dictionary containing level information
        Precondition: leveldict is a dictionary

        Parameter imagespath: The path to the Images folder
        Precondition: imagespath is a valid path

        Parameter pos: the position in the leveldict['lanes'] list
        Precondition: pos is an int
        """
        self._width = width
        dict = leveldict['lanes'][pos]
        image = dict['type'] + '.png'
        self._tiles = []
        for col in range(leveldict['size'][0]):
            x = col*GRID_SIZE
            y = pos*GRID_SIZE
            tile = Rectangle(source=image, size=(GRID_SIZE, GRID_SIZE), pos=(x,y))
            self._tiles.append(tile)
        self._objs = []
        if 'objects' in dict:
            for dict2 in dict['objects']:
                x = dict2['position']*GRID_SIZE
                y = pos*GRID_SIZE
                if dict2['type'] == 'turtle_east':
                    obstacle = Turtle('east',x,y)
                elif dict2['type'] == 'turtle_west':
                    obstacle = Turtle('west',x,y)
                else:
                    image = dict2['type'] + '.png'
                    im = Image.open(os.path.join(imagespath,image))
                    multiplier = GRID_SIZE / im.size[1]
                    width = im.size[0] * multiplier
                    if 'speed' in dict and dict['speed']<0:
                        rotated = im.rotate(180)
                        rotated.save(imagespath+'/temp'+image)
                        image = 'temp'+image
                    obstacle = Rectangle(source=image, size=(width,GRID_SIZE), pos=(x,y))
                self._objs.append(obstacle)
        if 'speed' in dict:
            self._speed = dict['speed']
        else:
            self._speed = None
        self._buffer = leveldict['offscreen']
        self._animator = None

    def update(self,dt):
        """
        Updates the game objects each frame.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        for obj in self._objs:
            if isinstance(obj,Turtle):
                obj.x += dt*self._speed
                if self._speed > 0 and obj.x > self._width:
                    d = obj.x - (self._width + self._buffer*2*GRID_SIZE)
                    obj.x = -self._buffer*GRID_SIZE + d
                elif self._speed < 0 and obj.x < -self._buffer*GRID_SIZE:
                    d = obj.x - (-self._buffer*GRID_SIZE)
                    obj.x = self._width + self._buffer*GRID_SIZE + d
                obj.update(dt)
            else:
                obj.pos = (obj.pos[0]+dt*self._speed, obj.pos[1])
                if self._speed > 0 and obj.pos[0] > self._width:
                    d = obj.pos[0] - (self._width+(self._buffer*2)*GRID_SIZE)
                    obj.pos = (-self._buffer*GRID_SIZE + d, obj.pos[1])
                elif self._speed < 0 and obj.pos[0] < -self._buffer*GRID_SIZE:
                    d = obj.pos[0] - (-self._buffer*GRID_SIZE)
                    obj.pos = (self._width+self._buffer*GRID_SIZE + d, obj.pos[1])


    def draw(self,canvas):
        """
        Draws the game objects to the canvas.

        Parameter canvas: The root object used for drawing by a Widget
        Precondition: canvas is a root object used for drawing by a Widget
        """
        for tile in self._tiles:
            canvas.add(tile)
        for obj in self._objs:
            if isinstance(obj,Turtle):
                obj.draw(canvas)
            else:
                canvas.add(obj)

    def collides(self,obj1,obj2):
        """
        Returns True if obj1 and obj2 collide and False otherwise

        Parameter obj1: The first object
        Precondition: obj1 is a kivy graphics rectangle

        Parameter obj2: The second object
        Precondition: obj2 is a tuple in the form of ((x,y),(width,height),(hitbox))
        """
        obj1x = obj1.pos[0]
        obj1y = obj1.pos[1]
        obj1w = obj1.size[0]
        obj1h = obj1.size[1]

        obj2x = obj2[0][0]
        obj2y = obj2[0][1]
        obj2w = obj2[1][0]
        obj2h = obj2[1][1]
        left =  obj2[2][0]
        top =  obj2[2][1]
        right =  obj2[2][2]
        bottom =  obj2[2][3]

        return (obj1x < obj2x+obj2w-right) and (obj1x+obj1w > obj2x+left) and \
            (obj1y < obj2y+obj2h-top) and (obj1y+obj1h > obj2y+bottom)

    def contains(self,obj1,obj2):
        """
        Returns True if obj1 contains the center of obj2 and False otherwise

        Parameter obj1: The first object
        Precondition: obj1 is a kivy graphics rectangle or Turtle

        Parameter obj2: The second object
        Precondition: obj2 is a tuple in the form of ((x,y),(width,height),(hitbox))
        """
        if isinstance(obj1,Turtle):
            obj1x = obj1.x
            obj1y = obj1.y
            obj1w = obj1.w
            obj1h = obj1.h
        else:
            obj1x = obj1.pos[0]
            obj1y = obj1.pos[1]
            obj1w = obj1.size[0]
            obj1h = obj1.size[1]

        obj2x = obj2[0][0] + GRID_SIZE/2
        obj2y = obj2[0][1] + GRID_SIZE/2
        return (obj2x < obj1x+obj1w) and (obj2x > obj1x) and \
            (obj2y < obj1y+obj1h) and (obj2y > obj1y)


class Grass(Lane):
    """
    A class representing a 'safe' grass area.
    """
    pass


class Road(Lane):
    """
    A class representing a roadway with cars.
    """
    def roadCollision(self,frog):
        """
        Returns True if the frog collides with a hedge.

        Parameter frog: the frog
        Precondition: frog is a Frog object
        """
        tuple = ((frog.x,frog.y),(frog.w,frog.h),(frog.hitbox))
        for obj in self._objs:
            if self.collides(obj,tuple):
                return True


class Water(Lane):
    """
    A class representing a waterway with logs.
    """
    def logContains(self,frog,dt):
        """
        Returns True if the log contains the frog.

        Parameter frog: the frog
        Precondition: frog is a Frog object

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        tuple = ((frog.x,frog.y),(frog.w,frog.h),(frog.hitbox))
        for obj in self._objs:
            if isinstance(obj,Turtle):
                if self.contains(obj,tuple) and obj.frame < 8:
                    frog.x += dt*self._speed
                    return True
            elif self.contains(obj,tuple):
                frog.x += dt*self._speed
                return True

    def waterCollision(self,frog):
        """
        Returns True if the frog collides with water.

        Parameter frog: the frog
        Precondition: frog is a Frog object
        """
        tuple = ((frog.x,frog.y),(frog.w,frog.h),(frog.hitbox))
        for tile in self._tiles:
            if self.collides(tile,tuple):
                return True

    def flyCollision(self,frog):
        """
        Returns True if the frog collides with a fly.

        Parameter frog: the frog
        Precondition: frog is a Frog object
        """
        tuple = ((frog.x,frog.y),(frog.w,frog.h),(frog.hitbox))
        for obj in self._objs:
            if not isinstance(obj,Turtle):
                pos = obj.source.find('Images')
                source = obj.source[pos+7:]
                if source == 'fly.png' and self.collides(obj,tuple):
                    self._objs.remove(obj)
                    return True


class Hedge(Lane):
    """
    A class representing the exit hedge.
    """
    def getNumExits(self):
        """
        Returns the number of exits in the lane.
        """
        numExits = 0
        for obj in self._objs:
            pos = obj.source.find('Images')
            source = obj.source[pos+7:]
            if source == 'exit.png':
                numExits += 1
        return numExits

    def hedgeCollision(self,frog,safeFrogs):
        """
        Returns True if the frog collides with a hedge or safe frog and False
        otherwise.

        Parameter frog: the frog
        Precondition: frog is a Frog object

        Parameter safeFrogs: the safe frogs
        Precondition: safeFrogs is a list of of kivy.graphics Rectangles
        """
        tuple = tuple = ((frog.x,frog.y+GRID_SIZE),(frog.w,frog.h),(frog.hitbox))
        for safeFrog in safeFrogs:
            if self.collides(safeFrog,tuple):
                return True
        for obj in self._objs:
            pos = obj.source.find('Images')
            source = obj.source[pos+7:]
            if source == 'exit.png' or source == 'open.png':
                if self.contains(obj,tuple):
                    return False
        for tile in self._tiles:
            if self.collides(tile,tuple):
                return True

    def frogSafe(self,frog):
        """
        Returns True if the frog is safe.

        Parameter frog: the frog
        Precondition: frog is a Frog object
        """
        tuple = ((frog.x,frog.y),(frog.w,frog.h),(frog.hitbox))
        for obj in self._objs:
            pos = obj.source.find('Images')
            source = obj.source[pos+7:]
            if source == 'exit.png' and self.contains(obj,tuple):
                frog.x = obj.pos[0]
                frog.y = obj.pos[1]
                return True

    def enterFromNorth(self,frog):
        """
        Returns True if the frog enters hedge from North.

        Parameter frog: the frog
        Precondition: frog is a Frog object
        """
        tuple = ((frog.x,frog.y-GRID_SIZE),(frog.w,frog.h),(frog.hitbox))
        for tile in self._tiles:
            if self.collides(tile,tuple):
                return True

    def enterFromSide(self,frog):
        """
        Returns True if the frog enters hedge from the East or West.

        Parameter frog: the frog
        Precondition: frog is a Frog object
        """
        tuple = ((frog.x,frog.y),(frog.w,frog.h),(frog.hitbox))
        for obj in self._objs:
            pos = obj.source.find('Images')
            source = obj.source[pos+7:]
            if source == 'open.png' and self.contains(obj,tuple):
                return True
