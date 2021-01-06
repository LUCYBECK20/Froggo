"""
Models module for Froggo

Author: Lucy Beck
Date: January 2, 2021
"""
from kivy.graphics import *
from constants import *


class Frog(object):
    """
    A class representing the frog
    """
    # Attribute _dead: True if the frog is dead and False otherwise
    # Invariant: _dead is a bool
    #
    # Attribute _x: The x-coordinate of the frog
    # Invariant: _x is a number (int or float)
    #
    # Attribute _y: The y-coordinate of the frog
    # Invariant: _y is a number (int or float)
    #
    # Attribute _w: The width of the frog
    # Invariant: _w is a number (int or float) > 0
    #
    # Attribute _h: The height of the frog
    # Invariant: _h is a number (int or float) > 0
    #
    # Attribute _frame: The current animation frame of the filmstrip
    # Invariant: _frame is a number > 0 and < number of animation frames or None
    #
    # Attribute _direction: The direction of the frog
    # Invariant: _direction is a string of either 'north', 'south', 'east', or 'west' or None
    #
    # Attribute _hitbox: The hitbox for the frog
    # Invariant: _hitbox is a 4-element list of numbers or None
    #
    @property
    def x(self):
        """
        The x-coordinate of the frog

        Invariant: value is a number (int or float)
        """
        return self._x

    @x.setter
    def x(self,value):
        assert type(value) == int or type(value) == float
        self._x = value

    @property
    def y(self):
        """
        The y-coordinate of the frog

        Invariant: value is a number (int or float)
        """
        return self._y

    @y.setter
    def y(self,value):
        assert type(value) == int or type(value) == float
        self._y = value

    @property
    def w(self):
        """
        The width of the frog

        Invariant: value is a number (int or float) > 0
        """
        return self._w

    @property
    def h(self):
        """
        The height of the frog

        Invariant: value is a number (int or float) > 0
        """
        return self._h

    @property
    def direction(self):
        """
        The direction of the frog

        Invariant: value is a string of either 'north', 'south', 'east', or 'west' or None
        """
        return self._direction

    @direction.setter
    def direction(self,value):
        assert type(value) == str and value in ['north', 'south', 'east', 'west'] or value is None
        self._direction = value

    @property
    def dead(self):
        """
        True if the frog is dead, False otherwise

        Invariant: value is a bool
        """
        return self._dead

    @property
    def hitbox(self):
        """
        The hitbox for the frog

        Invariant: value is a 4-element list of numbers or None
        """
        return self._hitbox

    def __init__(self,leveldict,dead=False,lastx=None,lasty=None):
        """
        Initializes the frog

        Parameter leveldict: a dictionary containing level information
        Precondition: leveldict is a dictionary

        Parameter dead: True if the frog is dead and False otherwise
        Precondition: dead is a bool

        Parameter deadx: The x-coordinate of where the frog died
        Precondition: deadx is a number (int or float) or None

        Parameter deady: The y-coordinate of where the frog died
        Precondition: deady is a number (int or float) or None
        """
        self._dead = dead
        if dead:
            self._x = lastx
            self._y = lasty
            self._w = GRID_SIZE
            self._h = GRID_SIZE
            self._direction = None
            self._frame = 1
            self._hitbox = None
        else:
            self._x = leveldict['start'][0]*GRID_SIZE
            self._y = leveldict['start'][1]*GRID_SIZE
            self._w = GRID_SIZE
            self._h = GRID_SIZE
            self._direction = 'north'
            self._frame = None
            self._hitbox = [2,14,2,14]

    def draw(self,canvas):
        if self._dead:
            source = "atlas://skulls/frame" + str(self._frame)
            skulls = Rectangle(source=source, pos=(self._x,self._y), size=(self._w, self._h))
            canvas.add(skulls)
        else:
            if self._direction == 'north':
                source = FROG_NORTH
                self._hitbox = [2,14,2,14]
            elif self._direction == 'south':
                source = FROG_SOUTH
                self._hitbox = [2,14,2,14]
            elif self._direction == 'east':
                source = FROG_EAST
                self._hitbox = [14,2,14,2]
            elif self._direction == 'west':
                source = FROG_WEST
                self._hitbox = [14,2,14,2]
            frog = Rectangle(source=source, pos=(self._x,self._y), size=(self._w, self._h))
            canvas.add(frog)

    def animateDeath(self):
        """
        Animates a frog death over DEATH_SPEED seconds.

        This method is a coroutine that takes a break (so that the game
        can redraw the image) every time it moves it. The coroutine takes
        the dt as periodic input so it knows how many (parts of) seconds
        to animate.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.
        """
        time = 0
        animating = True
        while animating:
            if time >= DEATH_SPEED:
                animating = False
            dt = (yield)
            time += dt
            frame = round(time/DEATH_SPEED*7)
            if frame == 0:
                frame = 1
            self._frame = frame

class Turtle(object):
    """
    A class representing the turtle
    """
    # Attribute _x: The x-coordinate of the turtle
    # Invariant: _x is a number (int or float)
    #
    # Attribute _y: The y-coordinate of the turtle
    # Invariant: _y is a number (int or float)
    #
    # Attribute _w: The width of the turtle
    # Invariant: _w is a number (int or float) > 0
    #
    # Attribute _h: The height of the turtle
    # Invariant: _h is a number (int or float) > 0
    #
    # Attribute _frame: The current animation frame of the filmstrip
    # Invariant: _frame is a number > 0 and < number of animation frames
    #
    # Attribute _direction: The direction of the turtle
    # Invariant: _direction is a string of either 'east' or 'west'
    #
    # Attribute _animator: A coroutine for performing an animation
    # Invariant: _animator is a generator-based coroutine or None
    #

    @property
    def x(self):
        """
        The x-coordinate of the turtle

        Invariant: value is a number (int or float)
        """
        return self._x

    @x.setter
    def x(self,value):
        assert type(value) == int or type(value) == float
        self._x = value

    @property
    def y(self):
        """
        The y-coordinate of the turtle

        Invariant: value is a number (int or float)
        """
        return self._y

    @property
    def w(self):
        """
        The width of the turtle

        Invariant: value is a number (int or float) > 0
        """
        return self._w

    @property
    def h(self):
        """
        The height of the turtle

        Invariant: value is a number (int or float) > 0
        """
        return self._h

    @property
    def frame(self):
        """
        The frame of the turtle

        Invariant: value is a number > 0 and < number of animation frames
        """
        return self._frame

    def __init__(self,direction,x,y):
        """
        Initializes the turtle

        Parameter direction: The direction of the turtle
        Precondition: direction is a string of either 'east' or 'west'

        Parameter x: The x-coordinate of the turtle
        Precondition: x is a number (int or float)

        Parameter y: The y-coordinate of the turtle
        Precondition: y is a number (int or float)
        """
        self._x = x
        self._y = y
        self._w = GRID_SIZE
        self._h = GRID_SIZE
        self._frame = 1
        self._direction = direction
        self._animator = None

    def update(self,dt):
        """
        Updates the game objects each frame.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if not self._animator is None:
            try:
                self._animator.send(dt)
            except:
                self._animator = None
        else:
            self._animator = self._animateTurtle()
            next(self._animator)

    def draw(self,canvas):
        """
        Draws the game objects to the canvas.

        Parameter canvas: The root object used for drawing by a Widget
        Precondition: canvas is a root object used for drawing by a Widget
        """
        if self._direction == 'east':
            source = "atlas://turtle_east/frame" + str(self._frame)
        elif self._direction == 'west':
            source = "atlas://turtle_west/frame" + str(self._frame)
        turtle = Rectangle(source=source, pos=(self._x,self._y), size=(self._w, self._h))
        canvas.add(turtle)

    def _animateTurtle(self):
        """
        Animates a sprite move over TURTLE_SPEED seconds.

        This method is a coroutine that takes a break (so that the game
        can redraw the image) every time it moves it. The coroutine takes
        the dt as periodic input so it knows how many (parts of) seconds
        to animate.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.
        """
        time = 0
        animating = True
        while animating:
            if time >= TURTLE_SPEED:
                animating = False
            dt = (yield)
            time += dt
            frame = round(time/TURTLE_SPEED*8)
            if frame == 0:
                frame = 1
            self._frame = frame
