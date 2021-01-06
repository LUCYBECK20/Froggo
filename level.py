"""
Subcontroller module for Froggo

Author: Lucy Beck
Date: January 2, 2021
"""
from kivy.graphics import *
from lanes import *
from models import *
from constants import *


class Level(object):
    """
    This class controls a single level of Froggo.
    """
    # Attribute _width: The width of the window to animate in
    # Invariant: _width is a number (int or float) > 0
    #
    # Attribute _height: The height of the window to animate in
    # Invariant: _height is a number (int or float) > 0
    #
    # Attribute _lanes: The list of horizontal lanes that the frog has to cross
    # Invariant: _lanes is a list of Lane objects
    #
    # Attribute _frog: The frog
    # Invariant: _frog is a Frog object or None or string
    #
    # Attribute _lives: The list of frog heads that represent the number of lives
    # Invariant: _lives is a list of kivy.graphics Rectangles
    #
    # Attribute _coolDown: the amount of time before the player can move again
    # Invariant: _coolDown is a number (int or float)
    #
    # Attribute _safeFrogs: The list of safe frogs
    # Invariant: _safeFrogs is a list of kivy.graphics Rectangles
    #
    # Attribute _numExits: The number of exits in a level
    # Invariant: _numExits is an int
    #
    # Attribute _animator: A coroutine for performing an animation
    # Invariant: _animator is a generator-based coroutine or None
    #

    def getFrog(self):
        """
        Returns the frog or None
        """
        return self._frog

    def getLives(self):
        """
        Returns the list of lives
        """
        return self._lives

    def getWon(self):
        """
        Returns True if the player won the game and False otherwise
        """
        return self._numExits == len(self._safeFrogs)

    def __init__(self,width,height,leveldict,imagespath):
        """
        Initializes the level.

        Parameter width: The width of the window to animate in
        Precondition : width is a number (int or float) > 0

        Parameter height: The height of the window to animate in
        Precondition: height is a number (int or float) > 0

        Parameter leveldict: A dictionary containing level information
        Precondition: leveldict is a dictionary

        Parameter imagespath: The path to the Images folder
        Precondition: imagespath is a valid path
        """
        self._width = width
        self._height = height
        self._lanes = []
        self._laneHelper(leveldict,imagespath)

        self._frog = Frog(leveldict)
        self._lives = []
        for x in range(1,4):
            image = Rectangle(source=FROG_HEAD, size=(GRID_SIZE, GRID_SIZE), \
            pos=(width-GRID_SIZE*x, height-GRID_SIZE))
            self._lives.append(image)
        self._coolDown = 0
        self._safeFrogs = []
        self._numExits = 0
        for lane in self._lanes:
            if isinstance(lane,Hedge):
                self._numExits += lane.getNumExits()
        self._animator = None

    def update(self,dt,keydict,leveldict,sounddict,reset=False):
        """
        Updates the game objects each frame.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter keydict: A dictionary containing keyboard keys
        Precondition: leveldict is a dictionary

        Parameter leveldict: A dictionary containing level information
        Precondition: leveldict is a dictionary

        Parameter sounddict: a dictionary containing sounds to play
        Precondition: sounddict is a dictionary of Sound objects

        Parameter reset: True if the level needs to be reset and False otherwise
        Precondition: reset is a bool
        """
        if reset == True:
            self._frog = Frog(leveldict)
        if not self._frog.dead:
            if self._coolDown > 0:
                self._coolDown -= dt
            else:
                self._keysDown(keydict,sounddict)
            lastx = self._frog.x
            lasty = self._frog.y
            self._updateLanes(dt,sounddict)
            if self._frog == 'dead':
                sounddict['squish'].play()
                self._frog = Frog(leveldict,True,lastx,lasty)
        else:
            if not self._animator is None:
                try:
                    self._animator.send(dt)
                except:
                    self._animator = None
                    self._frog = None
                    self._lives.pop()
            else:
                self._animator = self._frog.animateDeath()
                next(self._animator)

    def draw(self,canvas):
        """
        Draws the game objects to the view.

        Parameter canvas: The root object used for drawing by a Widget
        Precondition: canvas is a root object used for drawing by a Widget
        """
        for lane in self._lanes:
            lane.draw(canvas)
        for safeFrog in self._safeFrogs:
            canvas.add(safeFrog)
        for life in self._lives:
            canvas.add(life)
        if not self._frog is None:
            self._frog.draw(canvas)

    def _laneHelper(self,leveldict,imagespath):
        """
        Creates and appends each lane to a list.

        Parameter leveldict: A dictionary containing level information
        Precondition: leveldict is a dictionary

        Parameter imagespath: The path to the Images folder
        Precondition: imagespath is a valid path
        """
        for pos in range(len(leveldict['lanes'])):
            if leveldict['lanes'][pos]['type'] == 'grass':
                self._lanes.append(Grass(self._width,leveldict,imagespath,pos))
            elif leveldict['lanes'][pos]['type'] == 'road':
                self._lanes.append(Road(self._width,leveldict,imagespath,pos))
            elif leveldict['lanes'][pos]['type'] == 'water':
                self._lanes.append(Water(self._width,leveldict,imagespath,pos))
            elif leveldict['lanes'][pos]['type'] == 'hedge':
                self._lanes.append(Hedge(self._width,leveldict,imagespath,pos))

    def _keysDown(self,keydict,sounddict):
        """
        Determines if up, down, left, or right keys were pressed and changes
        the frog's direction and position accordingly

        Parameter keydict: A dictionary containing keyboard keys
        Precondition: leveldict is a dictionary

        Parameter sounddict: a dictionary containing sounds to play
        Precondition: sounddict is a dictionary of Sound objects
        """
        if 'up' in keydict and keydict['up']:
            self._frog.direction = 'north'
            if self._frog.y + 3*GRID_SIZE <= self._height and not self._hedgePresent('up'):
                self._frog.y += GRID_SIZE
                sounddict['ribbit'].play()
            self._coolDown = FROG_SPEED
        elif 'down' in keydict and keydict['down']:
            self._frog.direction = 'south'
            if self._frog.y - GRID_SIZE >= 0 and not self._hedgePresent('down'):
                self._frog.y -= GRID_SIZE
                sounddict['ribbit'].play()
            self._coolDown = FROG_SPEED
        elif 'right' in keydict and keydict['right']:
            self._frog.direction = 'east'
            if self._frog.x + 2*GRID_SIZE <= self._width and not self._hedgePresent('east'):
                self._frog.x += GRID_SIZE
                sounddict['ribbit'].play()
            self._coolDown = FROG_SPEED
        elif 'left' in keydict and keydict['left']:
            self._frog.direction = 'west'
            if self._frog.x - GRID_SIZE >= 0 and not self._hedgePresent('west'):
                self._frog.x -= GRID_SIZE
                sounddict['ribbit'].play()
            self._coolDown = FROG_SPEED

    def _updateLanes(self,dt,sounddict):
        """
        Updates the lanes each frame.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter sounddict: a dictionary containing sounds to play
        Precondition: sounddict is a dictionary of Sound objects
        """
        for lane in self._lanes:
            if not self._frog is None and self._frog != 'dead':
                if isinstance(lane,Road) or isinstance(lane,Water):
                    lane.update(dt)
                if isinstance(lane,Road) and lane.roadCollision(self._frog):
                    self._frog = 'dead'
                if isinstance(lane,Water):
                    if lane.flyCollision(self._frog):
                        if len(self._lives) == 1:
                            image = Rectangle(source=FROG_HEAD, size=(GRID_SIZE, GRID_SIZE), \
                            pos=(self._width-GRID_SIZE*2, self._height-GRID_SIZE))
                            self._lives.append(image)
                            sounddict['activation'].play()
                        elif len(self._lives) == 2:
                            image = Rectangle(source=FROG_HEAD, size=(GRID_SIZE, GRID_SIZE), \
                            pos=(self._width-GRID_SIZE*3, self._height-GRID_SIZE))
                            self._lives.append(image)
                            sounddict['activation'].play()
                    if lane.logContains(self._frog,dt):
                        if self._frog.x+GRID_SIZE/2 < 0 or self._frog.x+GRID_SIZE/2 > self._width:
                            self._frog = 'dead'
                    elif lane.waterCollision(self._frog):
                        self._frog = 'dead'
                if isinstance(lane,Hedge) and lane.frogSafe(self._frog):
                    image = Rectangle(source=FROG_SAFE, pos=(self._frog.x,self._frog.y),\
                        size=(GRID_SIZE,GRID_SIZE))
                    self._safeFrogs.append(image)
                    self._frog = None
                    sounddict['activation'].play()

    def _hedgePresent(self,direction):
        """
        Returns True if the next move is a hedge, False otherwise

        Parameter direction: The direction to move.
        Precondition: direction is a string and one of 'up' or 'down'.
        """
        lst = []
        if direction == 'up':
            for lane in self._lanes:
                if not self._frog is None and isinstance(lane,Hedge):
                    lst.append(lane.hedgeCollision(self._frog,self._safeFrogs))
        elif direction == 'down':
            for lane in self._lanes:
                if not self._frog is None and isinstance(lane,Hedge):
                    lst.append(lane.enterFromNorth(self._frog))
        elif direction == 'east' or direction == 'west':
            for lane in self._lanes:
                if not self._frog is None and isinstance(lane,Hedge):
                    lst.append(lane.enterFromSide(self._frog))
        return True in lst
