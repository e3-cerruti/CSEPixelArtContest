# Python code to implement Conway's Game Of Life
import argparse

import numpy as np

# setting up the values for the grid
from CSEPixelArt import load_img, save_anim
from rle2img import RLE

LARGE = '_large'

GIF = '.gif'

NUMBER_OF_FRAMES = 48

BACKGROUND_SCROLL_RATE = 2

ON = True
OFF = False
values = [ON, OFF]


def random_grid(grid_size):
    """returns a grid of NxN random values"""
    return np.random.choice(values, grid_size * grid_size, p=[0.2, 0.8]).reshape(grid_size, grid_size)


def add_glider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[OFF, OFF, ON],
                       [ON, OFF, ON],
                       [OFF, ON, ON]])
    grid[i:i + 3, j:j + 3] = glider


def add_gosper_glider_gun(i, j, grid):
    """adds a Gosper Glider Gun with top left
    cell at (i, j)"""
    gun = np.zeros(11 * 38).reshape(11, 38)

    gun[5][1] = gun[5][2] = ON
    gun[6][1] = gun[6][2] = ON

    gun[3][13] = gun[3][14] = ON
    gun[4][12] = gun[4][16] = ON
    gun[5][11] = gun[5][17] = ON
    gun[6][11] = gun[6][15] = gun[6][17] = gun[6][18] = ON
    gun[7][11] = gun[7][17] = ON
    gun[8][12] = gun[8][16] = ON
    gun[9][13] = gun[9][14] = ON

    gun[1][25] = ON
    gun[2][23] = gun[2][25] = ON
    gun[3][21] = gun[3][22] = ON
    gun[4][21] = gun[4][22] = ON
    gun[5][21] = gun[5][22] = ON
    gun[6][23] = gun[6][25] = ON
    gun[7][25] = ON

    gun[3][35] = gun[3][36] = ON
    gun[4][35] = gun[4][36] = ON

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
                grid[offset_y + yp, offset_x + xp + i] = ON
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

    new_grid = np.zeros((grid_size, grid_size), dtype=bool)
    for i in range(grid_size):
        for j in range(grid_size):

            # compute 8-neighbor sum
            # using toroidal boundary conditions - x and y wrap around
            # so that the simulation takes place on a toroidal surface.
            neighbors = [
                grid[i, (j - 1) % grid_size],
                grid[i, (j + 1) % grid_size],
                grid[(i - 1) % grid_size, j],
                grid[(i + 1) % grid_size, j],
                grid[(i - 1) % grid_size, (j - 1) % grid_size],
                grid[(i - 1) % grid_size, (j + 1) % grid_size],
                grid[(i + 1) % grid_size, (j - 1) % grid_size],
                grid[(i + 1) % grid_size, (j + 1) % grid_size]
            ]
            total = len([cell for cell in neighbors if cell])

            # apply Conway's rules
            if grid[i, j] and 2 <= total <= 3:
                new_grid[i, j + x_offset] = True
            elif total == 3:
                new_grid[i, j + x_offset] = True

    # update data
    grid[:] = new_grid[:]


# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")

    # add arguments
    parser.add_argument('--grid-size', dest='grid_size', required=False)
    parser.add_argument('--pixel-art', dest='pixel_art', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)
    parser.add_argument('--rle', dest='rle', required=False)
    parser.add_argument('--rate', dest='rate', required=False)
    parser.add_argument('--ship-color', nargs='+', type=int)

    args = parser.parse_args()

    # set grid size
    grid_size = 32
    if args.grid_size and int(args.grid_size) > 8:
        grid_size = int(args.grid_size)

    ship_color = (202, 44, 146)
    if args.ship_color:
        ship_color = tuple(args.ship_color)

    # check if "glider" demo flag is specified
    grid = np.zeros((grid_size, grid_size), dtype=bool)
    if args.glider:
        add_glider(1, 1, grid)
    elif args.gosper:
        add_gosper_glider_gun(10, 10, grid)
    elif args.rle:
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
    images = []

    for frame in range(frames):
        # Create the image with the scrolling background
        img = [[background[row][(col + BACKGROUND_SCROLL_RATE * frame) % len(background[0])]
                for col in range(grid_size)] for row in range(grid_size)]

        # Add spaceship
        for row in range(grid_size):
            for col in range(grid_size):
                if grid[row][col] == ON:
                    img[row][col] = ship_color

        # Add the frame to our list of images
        images.append(img)

        # Update Conway's Game of Life
        update(frame, grid, grid_size, rate)

    save_anim(images, args.pixel_art + GIF, scale=1)
    save_anim(images, args.pixel_art + LARGE + GIF, scale=10)


# call main
if __name__ == '__main__':
    main()
