from PIL import Image, ImageDraw
from itertools import cycle

# Funkcja wykorzystywan do utworzenia planszy gry

def draw_checkers_board(n=8, pixel_width=75 * 8):

    def sq_start(i):
        return i * pixel_width / n

    def square(i, j):
        return list(map(sq_start, [i, j, i + 1, j + 1]))

    image = Image.new("RGB", (pixel_width, pixel_width), (0, 0, 0))
    draw_square = ImageDraw.Draw(image).rectangle
    squares = (square(i, j)
               for i_start, j in zip(cycle((0, 1)), list(range(n)))
               for i in range(i_start, n, 2))
    for sq in squares:
        draw_square(sq, fill='#ffffff')
    squares = (square(i, j)
               for i_start, j in zip(cycle((0, 1)), list(range(n)))
               for i in range(i_start, n, 2))
    image.save("board.png")

draw_checkers_board(8)
