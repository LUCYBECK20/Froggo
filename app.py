"""
Primary controller module for Froggo

Author: Lucy Beck
Date: January 2, 2021
"""
from kivy.app import App
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import *
import kivy.resources
import json
import os
import inspect

from level  import *
from lanes  import *
from constants import *


class Froggo(FloatLayout):
    """
    The primary controller class for the Froggo application.

    Attribute canvas: The root object used for drawing by a Widget
    Invariant: canvas is a root object used for drawing by a Widget

    Attribute json: The path to the JSON folder
    Invariant: json is a valid path

    Attribute fonts: The path to the Fonts folder
    Invariant: fonts is a valid path

    Attribute images: The path to the Images folder
    Invariant: images is a valid path

    Attribute sounds: The path to the Sounds folder
    Invariant: sounds is a valid path
    """
    # HIDDEN ATTRIBUTES
    # Attribute _keydict: A dictionary containing keyboard keys
    # Invariant: _keydict is a dictionary
    #
    # Attribute _keyboard: A reference to the keyboard
    # Invariant: _keyboard is a kivy.core.window.Keyboard
    #
    # Attribute _leveldict: A dictionary containing level information
    # Invariant: _leveldict is a dictionary
    #
    # Attribute _sounddict: A dictionary of sounds to play
    # Invariant: _sounddict is a dictionary
    #
    # Attribute _state: The current state of the game
    # Invariant: _state is one of STATE_INACTIVE, STATE_LOADING, STATE_PAUSED,
    #            STATE_ACTIVE, STATE_CONTINUE, or STATE_COMPLETE
    #
    # Attribute _level: The subcontroller for a level
    # Invariant: _level is a Level object or None
    #
    # Attribute _levelNum: The number of the current level
    # Invariant: _levelNum is an int
    #
    # Attribute _title: The title of the game
    # Invariant: _title is a Label or None
    #
    # Attribute _text: A message to display to the player
    # Invariant: _text is a Label or None
    #
    # Attribute _livesLabel: The label indicating the number of lives
    # Invariant: _livesLabel is a Label or None
    #

    def __init__(self,**kwargs):
        """
        Initializes the application.

        Parameter **kwargs: allows us to pass any number of keyword arguments
        """
        super(Froggo, self).__init__(**kwargs)
        self._keydict = {}
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._key_down)
        self._keyboard.bind(on_key_up=self._key_up)
        self._setpaths()
        self._leveldict = self._loadjson(LEVEL_1)
        self._sounddict = {}
        self._state = STATE_INACTIVE
        self._level = None
        self._levelNum = 1
        self._title = Label(text="Froggo", color=(0,120/255,0,1), pos=(0,50),\
            halign='center', strip=True, font_size=LARGE_FONT, font_name=OFFICIAL_FONT)
        self.add_widget(self._title)
        self._text = Label(text="Press 's' to start", color=(0,0,0,1), pos=(0,-50),\
            halign='center', strip=True, font_size=MEDIUM_FONT, font_name=OFFICIAL_FONT)
        self.add_widget(self._text)
        self._livesLabel = None

    def update(self,dt):
        """
        Updates the game objects each frame.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._state != STATE_INACTIVE:
            self._title = None
        if self._state == STATE_ACTIVE:
            self._text = None

        if self._state == STATE_INACTIVE and 's' in self._keydict and self._keydict['s']:
            self._state = STATE_LOADING

        if self._state == STATE_LOADING:
            self._level = Level(self.width,self.height,self._leveldict,self.images)
            self._livesLabel = Label(text="Lives:", color=(0,120/255,0,1), pos=(64,290),\
                halign='center', font_size=SMALL_FONT, font_name=OFFICIAL_FONT)
            self.add_widget(self._livesLabel)
            self._sounddict['ribbit'] =  SoundLoader.load(RIBBIT_SOUND)
            self._sounddict['squish'] =  SoundLoader.load(SQUISH_SOUND)
            self._sounddict['activation'] =  SoundLoader.load(ACTIVATION_SOUND)
            self._state = STATE_ACTIVE

        if self._state == STATE_ACTIVE:
            self._level.update(dt,self._keydict,self._leveldict,self._sounddict)
            if len(self._level.getLives()) == 0 or self._level.getWon():
                self._state = STATE_COMPLETE
            elif self._level.getFrog() is None:
                self._state = STATE_PAUSED

        if self._state == STATE_PAUSED:
            self._text = Label(text="Press 'c' to continue", color=(0,120/255,0,1),\
                halign='center', strip=True, font_size=SMALL_FONT, font_name=OFFICIAL_FONT,\
                pos_hint={'top': .95})
            if 'c' in self._keydict and self._keydict['c']:
                self._state = STATE_CONTINUE

        if self._state == STATE_CONTINUE:
            self._level.update(dt,self._keydict,self._leveldict,self._sounddict,True)
            self._state = STATE_ACTIVE

        if self._state == STATE_COMPLETE:
            if self._level.getWon() and self._levelNum == 7:
                text = "Congrats!\nYou have passed all levels\npress 'q' to quit"
            elif self._level.getWon():
                text = "Level Passed\nPress 'n' to play next level\nor press 'q' to quit"
                if 'n' in self._keydict and self._keydict['n']:
                    self._nextLevel()
                    self._state = STATE_LOADING
            else:
                text = "Level Failed\nPress 'p' to play again\nor press 'q' to quit"
                if 'p' in self._keydict and self._keydict['p']:
                    self._state = STATE_LOADING
            self._text = Label(text=text, color=(0,120/255,0,1),\
                halign='center', strip=True, font_size=SMALL_FONT, font_name=OFFICIAL_FONT,\
                pos_hint={'top': .95})
            if 'q' in self._keydict and self._keydict['q']:
                FroggoApp.get_running_app().stop()

    def _nextLevel(self):
        """
        Changes the level to the next level.
        """
        self._levelNum += 1
        if self._levelNum == 2:
            self._leveldict = self._loadjson(LEVEL_2)
        elif self._levelNum == 3:
            self._leveldict = self._loadjson(LEVEL_3)
        elif self._levelNum == 4:
            self._leveldict = self._loadjson(LEVEL_4)
        elif self._levelNum == 5:
            self._leveldict = self._loadjson(LEVEL_5)
        elif self._levelNum == 6:
            self._leveldict = self._loadjson(LEVEL_6)
        elif self._levelNum == 7:
            self._leveldict = self._loadjson(LEVEL_7)

    def draw(self):
        """
        Draws the game objects to the canvas.
        """
        if self._state != STATE_INACTIVE:
            self._level.draw(self.canvas)
            self.remove_widget(self._livesLabel)
            self.add_widget(self._livesLabel)
        if not self._text is None:
            if self._state == STATE_INACTIVE:
                self.canvas.before.add(Rectangle(size=(self.width, self.height)))
            elif self._state == STATE_PAUSED:
                y=len(self._leveldict['lanes'])/2*GRID_SIZE - 1/2*GRID_SIZE
                self.canvas.add(Rectangle(size=(self.width, GRID_SIZE),pos=(0,y)))
                #add text last so that it is on top
                self.remove_widget(self._text)
                self.add_widget(self._text)
            elif self._state == STATE_COMPLETE:
                y=len(self._leveldict['lanes'])/2*GRID_SIZE - 1/2*GRID_SIZE
                self.canvas.add(Rectangle(size=(self.width, 3*GRID_SIZE),pos=(0,y-GRID_SIZE)))
                #add text last so that it is on top
                self.remove_widget(self._text)
                self.add_widget(self._text)

    def _refresh(self,dt):
        """
        Processes a single animation frame.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._text is None:
            self.canvas.clear()
        self.update(dt)
        self.draw()

    def _keyboard_closed(self):
        """
        Enables keyboard events if the keyboard is closed.
        """
        self._keyboard.unbind(on_key_down=self._key_down)
        self._keyboard.unbind(on_key_up=self._key_up)
        self._keyboard = None

    def _key_down(self, keyboard, keycode, text, modifiers):
        """
        Detects when a key is down and adds it to the key dictionary.

        Parameter keyboard: reference to the keyboard
        Precondition: keyboard is a kivy.core.window.Keyboard

        Parameter keycode: the key pressed
        Precondition: keycode is a tuple with first element int and second element string

        Parameter text: the text associated with the key
        Precondition: text is a string

        Parameter modifiers: the modifiers associated with the press
        Precondition: modifiers is list of key codes
        """
        self._keydict[keycode[1]] = True
        return True

    def _key_up(self, keyboard, keycode):
        """
        Detects when a key is released and adds it to the key dictionary.

        Parameter keyboard: reference to the keyboard
        Precondition: keyboard is a kivy.core.window.Keyboard

        Parameter keycode: the key pressed
        Precondition: keycode is a tuple with first element int and second element string
        """
        self._keydict[keycode[1]] = False
        return True

    def _setpaths(self):
        """
        Sets the resource paths to the application directory.
        """
        # inspect.getfile() returns the name of the file in which an object was defined
        # os.path.abspath() returns a normalized absolutized version of the pathname path
        path = os.path.abspath(inspect.getfile(self.__class__))
        # os.path.dirname() returns the directory name from the path given
        path = os.path.dirname(path)

        # os.path.join() combines one or more path names into a single path
        self.json   = str(os.path.join(path, 'JSON'))
        self.fonts  = str(os.path.join(path, 'Fonts'))
        self.images = str(os.path.join(path, 'Images'))
        self.sounds = str(os.path.join(path, 'Sounds'))

        # kivy.resources.resource_add_path() adds a custom path to search in
        kivy.resources.resource_add_path(self.fonts)
        kivy.resources.resource_add_path(self.images)
        kivy.resources.resource_add_path(self.sounds)

    def _loadjson(self,name):
        """
        Returns the JSON for the given file name.

        Parameter name: The file name
        Precondition: name is a valid file name
        """
        # open() returns a file object
        file = open(os.path.join(self.json,name))
        # file.read() returns the whole text of the file
        data = file.read()
        # json.loads() parses the text
        data = json.loads(data)
        return data
