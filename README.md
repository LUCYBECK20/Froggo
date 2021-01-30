# Froggo
Froggo is a clone of the 1981 arcade game Frogger. 

If you are not familiar with Frogger, you may be familiar with its modern equivalent: Crossy Road.

I designed seven levels that support JSON files, audio, 2D graphics with hitboxes, and scheduled events. I also utilized property decorators, generators, and coroutines to create model classes that support 2D animation. All code is written in Python and follows the model-view-controller design pattern. 
# Prerequisites
Follow these instructions to download Kivy: https://kivy.org/doc/stable/gettingstarted/installation.html

IMPORTANT: Make sure to follow the instructions for "Installing Kivy’s dependencies" to support video and audio.

For Windows users, open up a command shell and run the following commands in order one at a time:
```
python -m pip install kivy[base] kivy_examples

python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew; 

python -m pip install kivy.deps.gstreamer
```
# Launching Froggo
Download the code as a ZIP file and extract the file. 
Change the directory in your command shell to just outside of the extracted Froggo folder.
Type ```python froggo-main``` on your command line and press enter. 
# How to Play
Use the up, down, left, and right arrow keys to move the frog.
The frog is safe in the grass.
The frog will die and lose a life if it is hit by a car, drowns in the water, is carried offscreen by a moving turtle or log, or is still on the turtle when the turtle dunks underwater.
If there are less than 3 lives and the frog lands on a fly, one life will be added.
The frog must jump on top of an unoccupied lily pad in a hedge to be safe. 
All lily pads must be occupied by a safe frog to move on to the next level.
There are 7 levels in total.
# Videos
Click here to view a playlist on youtube with previews of all 7 levels: [Froggo Game by Lucy Beck](https://youtube.com/playlist?list=PL4oFuWmD_bSWF9CO4Yglt4EQ9ZP_mkdIL)
# Acknowledgements
[Images](https://www.clipartkey.com/view/xxboTb_frogger-sprite-sheet/)
[Fonts](https://www.1001freefonts.com/keep-on-truckin.font)
[Sounds](http://www.orangefreesounds.com/)






