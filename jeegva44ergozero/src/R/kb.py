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
    )

    row_pins = (board.GP29, board.GP28, board.GP27, board.GP26)

    diode_orientation = DiodeOrientation.COL2ROW

    # flake8: noqa
    # coord_mapping = [
    #     0,  1,  2,  3,  4,  5,
    #     6,  7,  8,  9, 10, 11,
    #     12, 13, 14, 15, 16, 17,
    #     18, 19, 20, 21
    # ]
    # coord_mapping = [
    #     24, 25, 26, 27, 28, 29,
    #     30, 31, 32, 33, 34, 35,
    #     36, 37, 38, 39, 40, 41,
    #     42, 43, 44, 45
    # ]
    coord_mapping = [
        0,   1,  2,  3,  4,  5, 24, 25, 26, 27, 28, 29,
        6,   7,  8,  9, 10, 11, 30, 31, 32, 33, 34, 35,
        12, 13, 14, 15, 16, 17, 36, 37, 38, 39, 40, 41,
        20, 21, 22, 23, 42, 43, 44, 45
    ]
