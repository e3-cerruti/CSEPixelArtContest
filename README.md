# CSEPixelArtContest

UCSD CSE is hosting a [Pixel Art Competition](https://pixel-art.goto.ucsd.edu/).

# 32x32 Entry
The Python script ```conway``` uses the CSE Pixel Art library to generate my contest entry.

My entry has two parts.

The first element is a scrolling background drawn by hand in [PixilArt](https://pixilart.com). You can find the background in the file ```background.gif```. 
You will understand why either it was a good thing I didn't go to art school or maybe I should have gone to at least some art school.

The second part is a Coe Spaceship from Conway's Game of Life. I chose the Coe Spaceship simply because it would fit inside the required space. In choosing a
spaceship I was forced to move the grid to remain in view, this drove my idea for a defender like display. The code includes the elements to read an RLE file,
so you can try other Conway structures.

The command line to generate my contest entry:
```
python conway.py --grid-size 32 --rle coeship.rle --rate 2 --pixel-art coeship --ship-color 255 192 203
```

| ![Coe Spaceship over Planet X](coeship_large.gif?raw=true) | ![Small Coe Spaceship over Planet X](coeship.gif?raw=true) |
| :-------------------------: | :-------------------------: |
| Large: scale 10 (320x320) | Small: scale 1 (32x32)    |

Credits:
  * CSEPixelArt is from UCSD CSE and is provided with examples in the contest description.
  * The code for Conway's Game of Life was shamelessly lifted from [Geeks for Geeks](https://www.geeksforgeeks.org/conways-game-life-python-implementation/) and in turn that code came from [Mahesh Venkitachalam](https://github.com/electronut/pp/tree/master/conway) supporting his book __Python Playground__. The code is provided under the MIT License.
  * [RLE2Image](https://github.com/rtvu/rle2img) is provided by Ryan Vu also under MIT license, I did make a change to the file parsing that may relate to Python 3.

The UCSD Pixel Art library is distributed without a license therefore I don't know what license to add here. Obviously the vast majority of this code is not mine and is licensed under an MIT license. Please feel free to use my changes in any way you like (CC-0).

# 16x16 Entry

How this entry works can be reversed engineered from the code, but the secrets are supplied via command line. I suspect that the code could be modified to suss out the secrets.

| ![Large pixel art](puzzle_encoded_large.gif?raw=true) | ![Small pixel art](puzzle_encoded.gif?raw=true) |
| :-------------------------: | :-------------------------: |
| Large: scale 10 (320x320) | Small: scale 1 (32x32)    |

Credits:
 * The Morse Code translation script is from [Geeks for Geeks](https://www.geeksforgeeks.org/morse-code-translator-python/) as provided by [Palash Nigam](https://www.linkedin.com/in/palash25).
 * QR Code generation is from the [Segno](https://github.com/heuer/segno) written by Lars Heuer