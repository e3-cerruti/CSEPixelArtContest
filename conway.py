# Python code to implement Conway's Game Of Life
import argparse

import numpy as np

# setting up the values for the grid
from CSEPixelArt import create_img, load_img, save_anim
from rle2img import RLE

LARGE = '_large'

GIF = '.gif'

NUMBER_OF_FRAMES = 48

BACKGROUND_SCROLL_RATE = 2

ON = 255
OFF = 0
vals = [ON, OFF]


def random_grid(grid_size):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, grid_size * grid_size, p=[0.2, 0.8]).reshape(grid_size, grid_size)


def add_glider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0, 0, 255],
                       [255, 0, 255],
                       [0, 255, 255]])
    grid[i:i + 3, j:j + 3] = glider


def add_gosper_glider_gun(i, j, grid):
    """adds a Gosper Glider Gun with top left
    cell at (i, j)"""
    gun = np.zeros(11 * 38).reshape(11, 38)

    gun[5][1] = gun[5][2] = 255
    gun[6][1] = gun[6][2] = 255

    gun[3][13] = gun[3][14] = 255
    gun[4][12] = gun[4][16] = 255
    gun[5][11] = gun[5][17] = 255
    gun[6][11] = gun[6][15] = gun[6][17] = gun[6][18] = 255
    gun[7][11] = gun[7][17] = 255
    gun[8][12] = gun[8][16] = 255
    gun[9][13] = gun[9][14] = 255

    gun[1][25] = 255
    gun[2][23] = gun[2][25] = 255
    gun[3][21] = gun[3][22] = 255
    gun[4][21] = gun[4][22] = 255
    gun[5][21] = gun[5][22] = 255
    gun[6][23] = gun[6][25] = 255
    gun[7][25] = 255

    gun[3][35] = gun[3][36] = 255
    gun[4][35] = gun[4][36] = 255

    grid[i:i + 11, j:j + 38] = gun


def add_rle(source, grid):
    rle = RLE(source)
    (x, y) = rle.dimensions

    if len(grid) < max(x, y):
        raise IndexError

    offset_x = (len(grid) - x) // 2
    offset_y = (len(grid) - y) // 2

    xp = 0
    yp = 0
    (symbol, length) = rle.next_sequence()
    while symbol != '!':
        if symbol == '$':
            xp = 0
            yp += 1
        elif symbol == 'b':
            xp += length
        else:
            for i in range(length):
                grid[offset_y + yp, offset_x + xp + i] = 255
            xp += length
        (symbol, length) = rle.next_sequence()


def update(frame_number, grid, grid_size, rate):
    # def update(frame_number, img, grid, grid_size, rate):

    # copy grid since we require 8 neighbors
    # for calculation and we go line by line

    # scroll window
    if rate > 0 and frame_number % rate == 0:
        x_offset = -1
    elif rate < 0:
        x_offset = -rate
    else:
        x_offset = 0

    new_grid = np.zeros((grid_size, grid_size))
    for i in range(grid_size):
        for j in range(grid_size):

            # compute 8-neghbor sum
            # using toroidal boundary conditions - x and y wrap around
            # so that the simulaton takes place on a toroidal surface.
            total = int((grid[i, (j - 1) % grid_size] +
                         grid[i, (j + 1) % grid_size] +
                         grid[(i - 1) % grid_size, j] +
                         grid[(i + 1) % grid_size, j] +
                         grid[(i - 1) % grid_size, (j - 1) % grid_size] +
                         grid[(i - 1) % grid_size, (j + 1) % grid_size] +
                         grid[(i + 1) % grid_size, (j - 1) % grid_size] +
                         grid[(i + 1) % grid_size, (j + 1) % grid_size]) / 255)

            # apply Conway's rules
            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    new_grid[i, j + x_offset] = OFF
                else:
                    new_grid[i, j + x_offset] = ON
            else:
                if total == 3:
                    new_grid[i, j + x_offset] = ON
                else:
                    new_grid[i, j + x_offset] = OFF

    # update data
    grid[:] = new_grid[:]

    for i in range(grid_size):
        for j in range(grid_size):
            if new_grid[j, i] == OFF:
                new_grid[j, i] = (i * 32 + j) % 255
    # img.set_data(new_grid)
    # return img,


# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")

    # add arguments
    parser.add_argument('--grid-size', dest='grid_size', required=False)
    parser.add_argument('--pixelart', dest='pixelart', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)
    parser.add_argument('--rle', dest='rle', required=False)
    parser.add_argument('--rate', dest='rate', required=False)
    args = parser.parse_args()

    # set grid size
    grid_size = 32
    if args.grid_size and int(args.grid_size) > 8:
        grid_size = int(args.grid_size)

    # check if "glider" demo flag is specified
    if args.glider:
        grid = np.zeros(grid_size * grid_size).reshape(grid_size, grid_size)
        add_glider(1, 1, grid)
    elif args.gosper:
        grid = np.zeros(grid_size * grid_size).reshape(grid_size, grid_size)
        add_gosper_glider_gun(10, 10, grid)
    elif args.rle:
        grid = np.zeros(grid_size * grid_size).reshape(grid_size, grid_size)
        add_rle(args.rle, grid)

    else:  # populate grid with random on/off -
        # more off than on
        grid = random_grid(grid_size)

    # set image scrolling
    rate = 0
    if args.rate:
        rate = float(args.rate)

    background = load_img("background.gif")
    frames, rows, cols = (NUMBER_OF_FRAMES, grid_size, grid_size)
    imgs = []

    for frame in range(frames):
        # Create the image with the scrolling background
        img = [[background[row][(col + BACKGROUND_SCROLL_RATE * frame) % len(background[0])]
               for col in range(grid_size)] for row in range(grid_size)]

        # Add spaceship
        # TODO Choose spaceship color (constant)
        for row in range(grid_size):
            for col in range(grid_size):
                if grid[row][col] == ON:
                    img[row][col] = (160, 160, 160)

        # Add the frame to our list of images
        imgs.append(img)

        # Update Conway's Game of Life
        update(frame, grid, grid_size, rate)

    save_anim(imgs, args.pixelart + GIF, scale=1)
    save_anim(imgs, args.pixelart + LARGE + GIF, scale=10)


# call main
if __name__ == '__main__':
    main()
