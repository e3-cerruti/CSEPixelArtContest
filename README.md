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

