"""
The primary application script for Froggo

This module must be in a folder with the following files and subfolders:

    app.py      (the primary controller)
    level.py    (the subcontroller for each level)
    lanes.py    (the mini-controllers for each lane)
    models.py   (the model classes)
    consts.py   (the application constants)

    Fonts         (fonts for the game)
    Sounds        (sound effects for the game)
    Images        (image files for the the game)
    JSON          (json files for the game)

Author: Lucy Beck
Date: January 2, 2021
"""
from app import *
from constants import *


class FroggoApp(App):
    """
    The controller class for the game application.
    """
    def build(self):
        """
        Initializes the graphics window.
        """
        Window.size = (GAME_WIDTH,GAME_HEIGHT)
        game = Froggo()
        Clock.schedule_interval(game._refresh, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    FroggoApp().run()
