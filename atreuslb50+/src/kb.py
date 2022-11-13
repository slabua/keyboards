import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        board.GP2,
        board.GP3,
        board.GP4,
        board.GP5,
        board.GP6,
        board.GP7,
        board.GP8,
    )

    row_pins = (board.GP28, board.GP27, board.GP26, board.GP22,
                board.GP21, board.GP20, board.GP19, board.GP18)

    diode_orientation = DiodeOrientation.COL2ROW

    # flake8: noqa
    coord_mapping = [
        0,   1,  2,  3,  4,  5,      33, 28, 29, 30, 31, 32,
        7,   8,  9, 10, 11,     12,      35, 36, 37, 38, 39,
        14, 15, 16, 17, 18, 19,      47, 42, 43, 44, 45, 46,
        21, 22, 23, 24, 25, 26,      54, 49, 50, 51, 52, 53,
        6,  13, 20,                          48, 41, 34
    ]
