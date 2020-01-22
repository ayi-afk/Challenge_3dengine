# This is not real project just a challange

Me and my friends had a challange, we need to write simple 3d graphics in language of choice.

Assumptions:
 - we cannot use internet at all (need kinda reinvent things)
 - before task we can just check how to open window, draw a dot and line
 - we cannot use any 3d liblaried


Tested with python 3.7 on Windows10

to run simple create virtualenv/conda env
run 

` pip install -r requirements.txt` - to install dependencies
` python engine3d.py`

What I managed to do:
 - camera
 - multiple objects
 - tranformations (slow ones i know i'd need to use matrixes with numpy but didn't want to waste time as we were looking more on visual part)
 - 1 simple object cube, with edges
 - FOV (even through it was by accident atleast i know 100% what is this FOV from games :)

What i really wanted to do but time ended:
 - faces
 - another object like circle, or some more advanced ones
 - software vertex shader

 all done in less than 4 hours with lunch break


 ![](preview3d.gif)