import argparse
import os

import numpy
from PIL import Image

from CSEPixelArt import load_img, save_anim, save_img, add_gif_comment
from morse import encrypt

COMMENT = 'Created for UCSD CSE Pixel Art Competition 2021\n' +\
          'https://pixel-art.goto.ucsd.edu/\n' + \
          'Copyright Stephen Cerruti 2021 CC BY-SA 4.0'
BLUE = (0, 98, 155)
GOLD = (255, 205, 0)
BLACK = (0, 0, 0)
ENCODED = '_encoded'
LARGE = '_large'
GIF = '.gif'
PNG = '.gif'


def encode_message(input_image, message):
    output_image = input_image.copy()

    row = 0
    column = 0
    for code in map(ord, message.upper()):
        if row >= len(input_image):
            print('Warning: Message too long.')
            return output_image

        while input_image[row][column] != BLACK:
            output_image[row][column] = GOLD
            column = (column + 1) % len(input_image)
            if column == 0:
                row += 1
            if row >= len(input_image):
                print('Warning: Message too long.')
                return output_image

        green_offset = code // 3
        blue_offset = code - green_offset

        output_image[row][column] = tuple(map(lambda i, j: i - j, BLUE, (0, green_offset, blue_offset)))
        column = (column + 1) % len(input_image)
        if column == 0:
            row += 1

    for r in range(row, len(input_image)):
        for c in range(column, len(input_image[row])):
            output_image[r][c] = GOLD
        column = 0

    return output_image


def encode_morse(image, message):
    """
    The length of a dot is 1 time unit.
    A dash is 3 time units.
    The space between symbols (dots and dashes) of the same letter is 1 time unit.
    The space between letters is 3 time units.
    The space between words is 7 time units.
    """
    def morse_timing(char):
        timing = {'.': 1, '-': 3, ' ': 3, '/': 7}
        return timing[char]

    def dim(pixel):
        return max(pixel - 25, 0)

    morse = encrypt(message.upper())
    sequence = list(map(morse_timing, morse))
    if sum(sequence) + len(sequence) + 6 > 60:
        print('Warning: morse message too long, truncated')

    images = []
    image_off = [[list(map(dim, pixel)) for pixel in column] for column in image]
    for period in sequence:
        for n in range(period):
            images.append(image)
        images.append(image_off)

    for i in range(6):
        images.append(image_off)

    return images


def main():
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")

    parser.add_argument('--input', dest='input', required=False)
    parser.add_argument('--count', action='store_true', required=False)
    parser.add_argument('--message', dest='message', required=False)
    parser.add_argument('--morse', dest='morse', required=False)

    args = parser.parse_args()

    input_image = numpy.zeros((16, 16))
    if args.input:
        input_image = load_img(args.input)

    if args.count and input_image:
        pixels = [pixel for column in input_image for pixel in column if pixel == BLACK]
        print(f'There are {len(pixels)} black pixels.')

    output_image = None
    output_images = None

    if args.message:
        output_image = encode_message(input_image, args.message)

    if args.morse and output_image:
        output_images = encode_morse(output_image, args.morse)

    image_name = os.path.splitext(args.input)[0]
    if output_image and not output_images:
        save_img(output_image, image_name + ENCODED + PNG, scale=1)
        save_img(output_image, image_name + ENCODED + LARGE + PNG, scale=10)

    if output_images:
        save_anim(output_images, image_name + ENCODED + GIF, scale=1, comment=COMMENT)
        save_anim(output_images, image_name + ENCODED + LARGE + GIF, scale=10, comment=COMMENT)


# call main
if __name__ == '__main__':
    main()
