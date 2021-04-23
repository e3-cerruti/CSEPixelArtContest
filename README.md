# CSEPixelArtContest

UCSD CSE is hosting a [Pixel Art Competition](https://pixel-art.goto.ucsd.edu/).

The Python script ```conway``` uses the CSE Pixel Art library to generate my contest entry.

My entry has two parts.

The first element is a scrolling background drawn by hand in [PixilArt](https://pixilart.com). You can find the background in the file ```background.gif``. 
You will understand why either it was a good thing I didn't go to art school or maybe I should have gone to at least some art school.

The second part is a Coe Spaceship from Conway's Game of Life. I chose the Coe Spaceship simply because it would fit inside the required space. In choosing a
spaceship I was forced to move the grid to remain in view, this drove my idea for a defender like display. The code includes the elements to read an RLE file
so you can try other Conway structures.

The command line to generate my contest entry:
```
python conway.py --grid-size 32 --rle coeship.rle --rate 2 --pixelart coeship
```

![Coe Spaceship over Planet X](https://github.com/e3-cerruti/CSEPixelArtContest/blob/master/coeship_large.gif?raw=true)

Credits:
  * CSEPixelArt is from UCSD CSE and is provided with examples in the contest description.
  * The code for Conway's Game of Life was shamelessly lifted from [Geeks for Geeks](https://www.geeksforgeeks.org/conways-game-life-python-implementation/) and in turn that code came from [Mahesh Venkitachalam](https://github.com/electronut/pp/tree/master/conway) supporting his book __Python Playground__. The code is provided under the MIT License.
  * [RLE2Image](https://github.com/rtvu/rle2img) is provided by Ryan Vu also under MIT license, I did make a change to the file parsing that may relate to Python 3.

Because the UCSD Pixel Art library is distributed without a license I don't know what license to add here. Obviously the vast majority of this code is not mine and is licensed under an MIT license. Please feel free to use my changes in any way you like (CC-0).
