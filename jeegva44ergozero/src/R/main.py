import board
import time

from kb import KMKKeyboard
# from kb import data_pin

from kmk.consts import UnicodeMode
from kmk.handlers.sequences import compile_unicode_string_sequences as cuss
from kmk.handlers.sequences import send_string
from kmk.keys import KC

from kmk.extensions.lock_status import LockStatus
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.RGB import RGB
# from kmk.extensions.wpm import WPM
from kmk.modules.layers import Layers
from kmk.modules.modtap import ModTap
from kmk.modules.mouse_keys import MouseKeys
from kmk.modules.oneshot import OneShot
from kmk.modules.split import Split, SplitType, SplitSide
from kmk.modules.tapdance import TapDance
from micropython import const


keyboard = KMKKeyboard()
keyboard.debug_enabled = True

# Extensions
locks = LockStatus()
mediakeys = MediaKeys()
rgb = RGB(pixel_pin=board.GP16, num_pixels=1)
# wpm = WPM(debug=False)
keyboard.extensions = [locks, mediakeys]  # , wpm]  # , rgb]

# Modules
layers = Layers()
modtap = ModTap()
modtap.tap_time = 250
mousekeys = MouseKeys()
oneshot = OneShot()
oneshot.tap_time = 1000
split = Split(
    split_type=SplitType.UART,
    split_side=SplitSide.RIGHT,
    # split_target_left=False,
    data_pin=board.GP0,
    data_pin2=board.GP1,
    use_pio=True,
    uart_flip=True,
)
tapdance = TapDance()
tapdance.tap_time = 750

keyboard.modules = [layers, modtap, mousekeys, oneshot, split, tapdance]

keyboard.debug_enabled = False
keyboard.tap_time = 100
keyboard.unicode_mode = UnicodeMode.LINUX

# Filler keys
_______ = KC.TRNS
XXXXXXX = KC.NO

# Custom keys
LSFTALT = KC.MT(KC.LSFT, KC.LALT, prefer_hold=False,
                tap_interrupted=False, tap_time=200)
LSFTCTL = KC.MT(KC.LSFT, KC.LCTRL, prefer_hold=False,
                tap_interrupted=False, tap_time=200)
APPRGUI = KC.MT(KC.APP, KC.RGUI, prefer_hold=False,
                tap_interrupted=False, tap_time=200)
OSLSFT = KC.OS(KC.LSFT)
LALTAGR = KC.TD(KC.LALT, KC.RALT)
RALTAGR = KC.TD(KC.RALT, KC.RGUI)
RALTGRA = KC.TD(KC.RGUI, KC.RALT)

LOWER = KC.MO(1)
RAISE = KC.MO(2)
ADJUST = KC.LT(3, KC.LGUI)

BASE = KC.DF(0)

UNDO = KC.LCTRL(KC.Z)
REDO = KC.LCTRL(KC.Y)
ZOOM_IN = KC.LCTRL(KC.EQUAL)
ZOOM_OUT = KC.LCTRL(KC.MINUS)
ZOOM_RST = KC.LCTRL(KC.N0)

emoji = cuss({
    # Emoji
    'BEER': r'🍺',
    'BEER_TOAST': r'🍻',
    'FACE_CUTE_SMILE': r'😊',
    'FACE_HEART_EYES': r'😍',
    'FACE_JOY': r'😂',
    'FACE_SWEAT_SMILE': r'😅',
    'FACE_THINKING': r'🤔',
    'FIRE': r'🔥',
    'FLAG_CA': r'🇨🇦',
    'FLAG_US': r'🇺🇸',
    'HAND_CLAP': r'👏',
    'HAND_HORNS': r'🤘',
    'HAND_OK': r'👌',
    'HAND_THUMB_DOWN': r'👎',
    'HAND_THUMB_UP': r'👍',
    'HAND_WAVE': r'👋',
    'HEART': r'❤️',
    'MAPLE_LEAF': r'🍁',
    'PIEN': r'🥺',
    'POOP': r'💩',
    'TADA': r'🎉',

    # Kaomoji
    'ANGRY_TABLE_FLIP': r'(ノಠ痊ಠ)ノ彡┻━┻',
    'CELEBRATORY_GLITTER': r'+｡:.ﾟヽ(´∀｡)ﾉﾟ.:｡+ﾟﾟ+｡:.ﾟヽ(*´∀)ﾉﾟ.:｡+ﾟ',
    'SHRUGGIE': r'¯\_(ツ)_/¯',
    'TABLE_FLIP': r'(╯°□°）╯︵ ┻━┻',
})

# flake8: noqa
# Keyboard mapping
keyboard.keymap = [

    [  # base: qwerty
        KC.GESC,   KC.Q,      KC.W,      KC.E,      KC.R,      KC.T,                            KC.Y,      KC.U,      KC.I,     KC.O,      KC.P,      KC.MINUS,
        KC.TAB,    KC.A,      KC.S,      KC.D,      KC.F,      KC.G,                            KC.H,      KC.J,      KC.K,     KC.L,      KC.SCLN,   KC.QUOT,
        KC.LSFT,   KC.Z,      KC.X,      KC.C,      KC.V,      KC.B,                            KC.N,      KC.M,      KC.COMM,  KC.DOT,    KC.SLSH,   KC.RSFT,
        KC.LALT,   LOWER,     KC.LCTRL,  KC.SPC,                                                KC.ENT,    KC.BSPC,   RAISE,    RALTGRA,
    ],

    # [  # lower: sym/num
    #     _______,   KC.N1,     KC.N2,     KC.N3,     KC.N4,     KC.N5,                           KC.N6,     KC.N7,     KC.N8,    KC.N9,     KC.N0,     KC.PPLS,
    #     KC.PIPE,   KC.EXLM,   KC.AT,     KC.HASH,   KC.DLR,    KC.PERC,                         KC.CIRC,   KC.AMPR,   KC.PAST,  XXXXXXX,   XXXXXXX,   KC.EQL,
    #     XXXXXXX,   XXXXXXX,   XXXXXXX,   KC.LCBR,   KC.LBRC,   KC.LPRN,                         KC.RPRN,   KC.RBRC,   KC.RCBR,  XXXXXXX,   KC.BSLS,   KC.ENT,
    #     _______,   XXXXXXX,   _______,   _______,                                               _______,   KC.DEL,    XXXXXXX,  _______,
    # ],

    [  # lower: sym/num
        _______,   KC.EXLM,   KC.AT,     KC.HASH,   KC.DLR,    KC.LPRN,                         KC.RPRN,   KC.N7,     KC.N8,    KC.N9,     KC.PAST,   KC.PPLS,
        KC.PIPE,   KC.CIRC,   KC.AMPR,   KC.PAST,   KC.PERC,   KC.LBRC,                         KC.RBRC,   KC.N4,     KC.N5,    KC.N6,     XXXXXXX,   KC.EQL,
        XXXXXXX,   XXXXXXX,   XXXXXXX,   XXXXXXX,   XXXXXXX,   XXXXXXX,                         KC.N0,     KC.N1,     KC.N2,    KC.N3,     KC.BSLS,   KC.ENT,
        _______,   XXXXXXX,   _______,   _______,                                               _______,   KC.DEL,    XXXXXXX,  _______,
    ],

    [  # raise: fn/nav
        KC.F1,     KC.F2,     KC.F3,     KC.F4,     KC.F5,     KC.F6,                           KC.F7,     KC.F8,     KC.F9,    KC.F10,    KC.F11,    KC.F12,
        XXXXXXX,   XXXXXXX,   XXXXXXX,   XXXXXXX,   XXXXXXX,   XXXXXXX,                         KC.VOLU,   KC.HOME,   KC.UP,    KC.END,    KC.GRV,    KC.PGUP,
        XXXXXXX,   XXXXXXX,   XXXXXXX,   XXXXXXX,   XXXXXXX,   XXXXXXX,                         KC.VOLD,   KC.LEFT,   KC.DOWN,  KC.RIGHT,  KC.PSCR,   KC.PGDOWN,
        ADJUST,    XXXXXXX,   _______,   _______,                                               _______,   _______,   XXXXXXX,  _______,
    ],

]

# Main
if __name__ == '__main__':
    print(keyboard.extensions)
    print(keyboard.modules)
    keyboard.go()
