import board
import pwmio
import time

from kb import KMKKeyboard
# import logos

from kmk.consts import UnicodeMode
from kmk.handlers.sequences import compile_unicode_string_sequences as cuss
from kmk.handlers.sequences import send_string
from kmk.keys import KC

from kmk.extensions.lock_status import LockStatus
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.oled_1306 import DisplayOLED, LogoScene, StatusScene  # , KeypressesScene
# from kmk.extensions.RGB import RGB
# from kmk.extensions.wpm import WPM
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers
from kmk.modules.modtap import ModTap
from kmk.modules.mouse_keys import MouseKeys
from kmk.modules.oneshot import OneShot
from kmk.modules.pimoroni_trackball import Trackball, TrackballMode, PointingHandler, KeyHandler, ScrollHandler, ScrollDirection
from kmk.modules.tapdance import TapDance
from micropython import const

import busio as io
i2c = io.I2C(scl=board.GP1, sda=board.GP0)

keyboard = KMKKeyboard()

# Extensions
locks = LockStatus()
mediakeys = MediaKeys()
# rgb = RGB(pixel_pin=14, num_pixels=1)
# wpm = WPM(debug=False)
keyboard.extensions = [locks, mediakeys]  # , wpm]  # , rgb]

# Modules
layers = Layers()
modtap = ModTap()
modtap.tap_time = 250
mousekeys = MouseKeys()
oneshot = OneShot()
oneshot.tap_time = 1000
tapdance = TapDance()
tapdance.tap_time = 750

# Rotary encoders
encoders = EncoderHandler()
encoders.pins = (
    (board.GP14, board.GP15, None, False, 4),  # encoder L
    (board.GP17, board.GP16, None, False, 4),  # encoder R
    (board.GP12, board.GP13, None, False, 2),  # roller
)

# Trackball
trackball = Trackball(i2c, mode=TrackballMode.MOUSE_MODE, handlers=[
    PointingHandler(),
    # on layer 1 and above use the default pointing behavior
    ScrollHandler(scroll_direction=ScrollDirection.REVERSE),
    # act like an encoder, input arrow keys
    KeyHandler(KC.UP, KC.RIGHT, KC.DOWN, KC.LEFT, KC.ENTER),
])

# OLED
layers_names = ['0. Qwerty (test)', '1. Fun | Num', '2. Sym | Nav',
                '3. Emoji', '4. Tarmak3', '5. Tarmak4', '6. Colemak']
slblabs_logo = const(
    0x00000000000000000000000000000000000000000000000000000000000000000000c0e0f0f87c3c0c0602000000000000008080808080c0404020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c0e0f0f038180c0c040404000000000000f8ffff0f010000000000000004020303030303010101000000000000000000000080c0e0f0f0f0f0f0f0f0f0f0f0f0e0e0c080000000f0f0f0f0e00000000000000000000000000000f0f0f0f0f0707070707070f0f0f0f0e0c08000000000000000000000000000000000000000000f1f3f3c38706060404000000000000000ffff1f00000000020286cefefcfc78300000000000000000000000000000000000070f1f1f3f3c3c78787878f8f0f1f3e3e3c3000000ffffffffff0000000000000000000000000000ffffffffff38383838383838387fffffffe780000000000000000000000000000000000000000000000000000000808080c040406060b0fff718180c0c0e06078383818180000020206060e0c0c0c0c08080000000000000070f1f3f3e3c3c3c3c3c3c3c3c3f3f1f1f0f0100003f3f3f3f3f3c3c3c3c3c3c3c3c3c3c3c3800003f3f3f3f3f383838383838383c3c3f1f1f0f030000000000000000000000000000000000040404020202030101010100000000000000ffff01000000000000000000818183c79ffefefcf8f09f3f3f1f1f0f0700000000000080c0c0c08000000000000000000000000000000000000000000000000000c0c0c0c000000000000000000000000000000000000000000000000000000000000000000000000000008000004040404040202020202030301010181898fb0f0c0c0c04060606070303038381c1f1fc7f7f3f1f0f01000000000000000000000000ffffffffff000000000000000000000080dcdedeceeeeeeefefcfcf80000ffffffff0e0e0e0e1efefcf8f000003c7cfefeeecececede9c9c00000000000000000000000040602030301818181c1c1c1c06060200000000000080f80f0100000000000000000000000101010100000000000000000000000000000000000000000f1f1f1f1f1c1c1c1c1c1c1c1c1c1c000f0f1f1f1818181c0f1f1f1f00000f0f1f1f1c1c1c1c1e1f0f070300000e0e1e1c1c1c1d1d1f0f0f0200000000000000000000000000000000000000000000000000000000000000080300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000)
# slblabs_logo_inv = const(
#    0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff3f1f0f0783c3f3f9fdffffffffffffff7f7f7f7f7f3fbfbfdfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff3f1f0f0fc7e7f3f3fbfbfbffffffffffff070000f0fefffffffffffffffbfdfcfcfcfcfcfefefeffffffffffffffffffffff7f3f1f0f0f0f0f0f0f0f0f0f0f0f1f1f3f7fffffff0f0f0f0f1fffffffffffffffffffffffffffff0f0f0f0f0f8f8f8f8f8f8f0f0f0f0f1f3f7ffffffffffffffffffffffffffffffffffffffffff0e0c0c3c78f9f9fbfbfffffffffffffff0000e0fffffffffdfd793101030387cffffffffffffffffffffffffffffffffffff8f0e0e0c0c3c387878787070f0e0c1c1c3cffffff0000000000ffffffffffffffffffffffffffff0000000000c7c7c7c7c7c7c7c780000000187fffffffffffffffffffffffffffffffffffffffffffffffffffffff7f7f7f3fbfbf9f9f4f0008e7e7f3f3f1f9f87c7c7e7e7fffffdfdf9f9f1f3f3f3f3f7f7ffffffffffffff8f0e0c0c1c3c3c3c3c3c3c3c3c0c0e0e0f0feffffc0c0c0c0c0c3c3c3c3c3c3c3c3c3c3c3c7ffffc0c0c0c0c0c7c7c7c7c7c7c7c3c3c0e0e0f0fcfffffffffffffffffffffffffffffffffffbfbfbfdfdfdfcfefefefeffffffffffffff0000feffffffffffffffffff7e7e7c3860010103070f60c0c0e0e0f0f8ffffffffffff7f3f3f3f7fffffffffffffffffffffffffffffffffffffffffffffffffff3f3f3f3fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7fffffbfbfbfbfbfdfdfdfdfdfcfcfefefe7e76704f0f3f3f3fbf9f9f9f8fcfcfc7c7e3e0e038080c0e0f0feffffffffffffffffffffffff0000000000ffffffffffffffffffffff7f2321213111111101030307ffff00000000f1f1f1f1e10103070fffffc383010111313131216363ffffffffffffffffffffffffbf9fdfcfcfe7e7e7e3e3e3e3f9f9fdffffffffffff7f07f0fefffffffffffffffffffffffefefefefffffffffffffffffffffffffffffffffffffffff0e0e0e0e0e3e3e3e3e3e3e3e3e3e3fff0f0e0e0e7e7e7e3f0e0e0e0fffff0f0e0e0e3e3e3e3e1e0f0f8fcfffff1f1e1e3e3e3e2e2e0f0f0fdfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7fcffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)
# slblabs_logo_v2 = const(
#    0x000000000000000000000000000080c0c0e0e0f0f0f0f83808000000f8fcfcfc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000fcfcfcf80000000838f8f0f0f0e0e0c0c080000000000000000000000000000000000000000080c0e0f0fcfcfeffffffff7f3f1f0703000000000000ffffffff000000e0f8fcfcfefe9e1e1e1e1e3e3e7e7cfcf870000000fefefefefc00000000000000000000000000fcfefefefe1e1e1e1e1e1e1ebefefcfcf8e000000000ffffffff00000000000003071f3f7ffffffffffefcfcf0e0c080000000000000000000c0f8feffffffffffff9f0f0701000000000000000000000000ffffffff000000c0e3e7e7c78f8f8f8f9f9f9ebefefefcfcf8e00000ffffffffff80808080808080808080000000ffffffffff8f0f0f0f0f0f0f8ffffffffff860000000ffffffff00000000000000000000000001070f7ffffffffffffffef8c000000000007e7fffffffffffffffffffffffffffffffffffffffff0f070000ffffffff00000000030307070707070707070707070707030300000007070707070707070707070707070707020007070707070707070707070707070707030100000000ffffffff0000070ffffffffffffffffffffffefefcf9f9f3e3e7c7c38380000000000080000000000000000000000000000000000000000000000000ffffffff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ffffffff000000000001030307070f1f1f3f3f7f7fffffffffffffffff7f0000000000031f7ffefefcfcf8f0f0e0c080000000000000000000000000ffffffff000000000000fefffffffe0000000000000000000060707078383838f8f0f0e00000ffffffff70383878f0f0e0c000e0f0f0f8b8383870707060000000000000ffffffff00000000000000000000000080e0f0f8feffffffffff7f1f030000000000000000000103070f3f3f7ffffffffffefefcf8f0f0e0e0e00000ffffffff0000000000003f7f7f7f7f787878787878787870083e7f7f777777773f7f7f7f00003f7f7f7f707070787f3f3f0f00393b7b737777777f7f3e1c000000000000ffffffff0000e0e0e0f0f0f8fcfefeffffffff7f3f3f0f070301000000000000000000000000000000000000000001030307070f0f0f1f1f1f3f00003f3f3f3f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003f3f3f3f00003f1f1f1f0f0f0f07070303010000000000000000000000000000)
# slblabs_logo_v2_inv = const(
#    0xffffffffffffffffffffffffffff7f3f3f1f1f0f0f0f07c7f7ffffff07030303ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff03030307fffffff7c7070f0f0f1f1f3f3f7fffffffffffffffffffffffffffffffffffffffff7f3f1f0f0303010000000080c0e0f8fcffffffffffff00000000ffffff1f070303010161e1e1e1e1c1c1818303078fffffff0101010103ffffffffffffffffffffffffff0301010101e1e1e1e1e1e1e141010303071fffffffff00000000fffffffffffffcf8e0c080000000000103030f1f3f7fffffffffffffffffff3f070100000000000060f0f8feffffffffffffffffffffffff00000000ffffff3f1c181838707070706060614101010303071fffff00000000007f7f7f7f7f7f7f7f7f7fffffff000000000070f0f0f0f0f0f07000000000079fffffff00000000fffffffffffffffffffffffffef8f08000000000000001073fffffffffff81800000000000000000000000000000000000000000f0f8ffff00000000fffffffffcfcf8f8f8f8f8f8f8f8f8f8f8f8f8fcfcfffffff8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8fdfff8f8f8f8f8f8f8f8f8f8f8f8f8f8f8f8fcfeffffffff00000000fffff8f00000000000000000000001010306060c1c18383c7c7fffffffffff7fffffffffffffffffffffffffffffffffffffffffffffffff00000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff00000000fffffffffffefcfcf8f8f0e0e0c0c08080000000000000000080fffffffffffce08001010303070f0f1f3f7fffffffffffffffffffffffff00000000ffffffffffff0100000001ffffffffffffffffffff9f8f8f87c7c7c7070f0f1fffff000000008fc7c7870f0f1f3fff1f0f0f0747c7c78f8f8f9fffffffffffff00000000ffffffffffffffffffffffff7f1f0f0701000000000080e0fcfffffffffffffffffffefcf8f0c0c08000000000010103070f0f1f1f1fffff00000000ffffffffffffc08080808087878787878787878ff7c1808088888888c0808080ffffc08080808f8f8f8780c0c0f0ffc6c4848c8888888080c1e3ffffffffffff00000000ffff1f1f1f0f0f070301010000000080c0c0f0f8fcfefffffffffffffffffffffffffffffffffffffffffefcfcf8f8f0f0f0e0e0e0c0ffffc0c0c0c0ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc0c0c0c0ffffc0e0e0e0f0f0f0f8f8fcfcfeffffffffffffffffffffffffffff)

scenes = [
    # LogoScene(logos.slblabs_logo_16),
    LogoScene(slblabs_logo),
    StatusScene(layers_names=layers_names, separate_default_layer=True, rgb_ext=None),
    # LogoScene(slblabs_logo_v2),
    # LogoScene(slblabs_logo_v2_inv),
    # LogoScene(slblabs_logo_inv),
    # KeypressesScene(matrix_width=12, matrix_height=5, split=False,),
]
oled = DisplayOLED(i2c, scenes, flip=False)

keyboard.modules = [layers, modtap, mousekeys,
                    oneshot, encoders, tapdance, trackball, oled]

keyboard.debug_enabled = False
keyboard.tap_time = 100
keyboard.unicode_mode = UnicodeMode.LINUX

# Filler keys
_______ = KC.TRNS
XXXXXXX = KC.NO

# Custom keys
LSFTCFL = KC.MT(KC.LSFT, KC.LCTRL, prefer_hold=False,
                tap_interrupted=False, tap_time=200)
APPRGUI = KC.MT(KC.APP, KC.RGUI, prefer_hold=False,
                tap_interrupted=False, tap_time=200)
OSLSFT = KC.OS(KC.LSFT)
ALTAGR = KC.TD(KC.LALT, KC.RALT)

LOWER = KC.MO(1)
RAISE = KC.MO(2)
ADJUST = KC.LT(3, KC.LGUI)

BASE = KC.DF(0)
TARMAK3 = KC.DF(4)
TARMAK4 = KC.DF(5)
COLEMAK = KC.DF(6)

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

    [  # base: qwerty (test)
        KC.Q,      KC.W,      KC.E,      KC.R,      KC.T,      KC.OLED_TOG,           KC.MUTE,   KC.Y,      KC.U,      KC.I,     KC.O,      KC.P,
        KC.A,      KC.S,      KC.D,      KC.F,      KC.G,      KC.TB_NEXT_HANDLER,               KC.H,      KC.J,      KC.K,     KC.L,      KC.SCLN,
        KC.Z,      KC.X,      KC.C,      KC.V,      KC.B,      KC.LBRC,               KC.RBRC,   KC.N,      KC.M,      KC.COMM,  KC.DOT,    KC.SLSH,
        LSFTCFL,   KC.TAB,    OSLSFT,    ALTAGR,    KC.LCTRL,  KC.SPC,                KC.RSFT,   KC.BSPC,   KC.RALT,   KC.MINUS, KC.RSFT,   KC.ENT,
        KC.GESC,   ADJUST,    LOWER,                                                                        RAISE,     APPRGUI,  KC.QUOT,
    ],


    [  # lower: fn/num
        KC.F9,     KC.F10,    KC.F11,    KC.F12,    XXXXXXX,   _______,               ZOOM_RST,  KC.PAST,   KC.N7,     KC.N8,    KC.N9,     KC.BKDL,
        KC.F5,     KC.F6,     KC.F7,     KC.F8,     XXXXXXX,   _______,                          KC.PSLS,   KC.N4,     KC.N5,    KC.N6,     KC.PMNS,
        KC.F1,     KC.F2,     KC.F3,     KC.F4,     XXXXXXX,   KC.GRV,                KC.BSLS,   KC.INS,    KC.N1,     KC.N2,    KC.N3,     KC.PPLS,
        _______,   _______,   _______,   _______,   _______,   KC.MB_LMB,             KC.MB_RMB, KC.PSCR,   KC.LPRN,   KC.N0,    KC.RPRN,   _______,
        _______,   _______,   XXXXXXX,                                                                      KC.NLCK,   KC.EQL,   KC.PDOT,
    ],

    [  # raise: sym/nav
        KC.EXLM,   KC.AT,     KC.HASH,   KC.DLR,    KC.PERC,   _______,               ZOOM_RST,   KC.VOLU,   UNDO,      REDO,     KC.HOME,   KC.END,
        XXXXXXX,   XXXXXXX,   XXXXXXX,   XXXXXXX,   XXXXXXX,   _______,                           KC.VOLD,   XXXXXXX,   XXXXXXX,  XXXXXXX,   KC.PGUP,
        XXXXXXX,   XXXXXXX,   XXXXXXX,   XXXXXXX,   XXXXXXX,   KC.CIRC,               KC.AMPR,    KC.MUTE,   XXXXXXX,   KC.UP,    XXXXXXX,   KC.PGDOWN,
        TARMAK3,   _______,   _______,   _______,   _______,   _______,               _______,    _______,   KC.LEFT,   KC.DOWN,  KC.RIGHT,  _______,
        _______,   BASE,      KC.CAPS,                                                                       XXXXXXX,   XXXXXXX,  XXXXXXX,
    ],

    [  # adjust: emoji
        KC.Q,      KC.W,      KC.E,      KC.R,      KC.T,      KC.TB_NEXT_HANDLER,    KC.MUTE,   KC.Y,      KC.U,      KC.I,     KC.O,      KC.P,
        KC.A,      KC.S,      KC.D,      KC.F,      KC.G,      KC.OLED_TOG,                      KC.H,      KC.J,      KC.K,     KC.L,      KC.SCLN,
        KC.Z,      KC.X,      KC.C,      KC.V,      KC.B,      KC.LBRC,               KC.RBRC,   KC.N,      KC.M,      KC.COMM,  KC.DOT,    KC.SLSH,
        LSFTCFL,   KC.TAB,    OSLSFT,    KC.CAPS,   ALTAGR,    KC.SPC,                KC.SPC,    KC.RALT,   KC.BSPC,   KC.RSFT,  KC.MINUS,  emoji.PIEN,
        KC.GESC,   XXXXXXX,   LOWER,                                                                        TARMAK4,   COLEMAK,  BASE,
    ],

    [  # tarmak 3
        KC.Q,      KC.W,      KC.F,      KC.J,      KC.G,      KC.TB_NEXT_HANDLER,    KC.MUTE,   KC.Y,      KC.U,      KC.I,     KC.O,      KC.P,
        KC.A,      KC.R,      KC.S,      KC.T,      KC.D,      KC.OLED_TOG,                      KC.H,      KC.N,      KC.E,     KC.L,      KC.SCLN,
        KC.Z,      KC.X,      KC.C,      KC.V,      KC.B,      KC.LBRC,               KC.RBRC,   KC.K,      KC.M,      KC.COMM,  KC.DOT,    KC.SLSH,
        LSFTCFL,   KC.TAB,    OSLSFT,    KC.CAPS,   ALTAGR,    KC.SPC,                KC.SPC,    KC.RALT,   KC.BSPC,   KC.RSFT,  KC.MINUS,  KC.ENT,
        KC.GESC,   ADJUST,    LOWER,                                                                        RAISE,     APPRGUI,  KC.QUOT,
    ],

    [  # tarmak 4
        KC.Q,      KC.W,      KC.F,      KC.P,      KC.G,      KC.TB_NEXT_HANDLER,    KC.MUTE,   KC.J,      KC.U,      KC.I,     KC.Y,      KC.SCLN,
        KC.A,      KC.R,      KC.S,      KC.T,      KC.D,      KC.OLED_TOG,                      KC.H,      KC.N,      KC.E,     KC.L,      KC.O,
        KC.Z,      KC.X,      KC.C,      KC.V,      KC.B,      KC.LBRC,               KC.RBRC,   KC.K,      KC.M,      KC.COMM,  KC.DOT,    KC.SLSH,
        LSFTCFL,   KC.TAB,    OSLSFT,    KC.CAPS,   ALTAGR,    KC.SPC,                KC.SPC,    KC.RALT,   KC.BSPC,   KC.RSFT,  KC.MINUS,  KC.ENT,
        KC.GESC,   ADJUST,    LOWER,                                                                        RAISE,     APPRGUI,  KC.QUOT,
    ],

    [  # colemak
        KC.Q,      KC.W,      KC.F,      KC.P,      KC.G,      KC.TB_NEXT_HANDLER,    KC.MUTE,   KC.J,      KC.L,      KC.U,     KC.Y,      KC.SCLN,
        KC.A,      KC.R,      KC.S,      KC.T,      KC.D,      KC.OLED_TOG,                      KC.H,      KC.N,      KC.E,     KC.I,      KC.O,
        KC.Z,      KC.X,      KC.C,      KC.V,      KC.B,      KC.LBRC,               KC.RBRC,   KC.K,      KC.M,      KC.COMM,  KC.DOT,    KC.SLSH,
        LSFTCFL,   KC.TAB,    OSLSFT,    KC.CAPS,   ALTAGR,    KC.SPC,                KC.SPC,    KC.RALT,   KC.BSPC,   KC.RSFT,  KC.MINUS,  KC.ENT,
        KC.GESC,   ADJUST,    LOWER,                                                                        RAISE,     APPRGUI,  KC.QUOT,
    ],

]

# Encoders mapping
encoders.map = [
    (  # base: qwerty
        (KC.OLED_PRV, KC.OLED_NXT, None,),
        (KC.VOLD, KC.VOLU, None,),
        (KC.PGDOWN, KC.PGUP, None,),
    ),
    (  # lower: sym/nav
        (_______, _______, None,),
        (_______, _______, None,),
        (ZOOM_OUT, ZOOM_IN, None,),
    ),
    (  # raise: fn/num
        (_______, _______, None,),
        (_______, _______, None,),
        (ZOOM_OUT, ZOOM_IN, None,),
    ),
    (  # adjust: emoji
        (_______, _______, None,),
        (_______, _______, None,),
        (ZOOM_OUT, ZOOM_IN, None,),
    ),
    (  # tarmak 3
        (KC.OLED_PRV, KC.OLED_NXT, None,),
        (KC.VOLD, KC.VOLU, None,),
        (KC.PGDOWN, KC.PGUP, None,),
    ),
    (  # tarmak 4
        (KC.OLED_PRV, KC.OLED_NXT, None,),
        (KC.VOLD, KC.VOLU, None,),
        (KC.PGDOWN, KC.PGUP, None,),
    ),
    (  # colemak
        (KC.OLED_PRV, KC.OLED_NXT, None,),
        (KC.VOLD, KC.VOLU, None,),
        (KC.PGDOWN, KC.PGUP, None,),
    ),
]

# Trackball setup
trackball.set_rgbw(255, 128, 0, 0)
time.sleep(0.25)
trackball.set_rgbw(4, 8, 32, 0)

# Buzzer
buzzer = pwmio.PWMOut(board.GP9, variable_frequency=True)
OFF = 0
ON = 2**15
buzzer.duty_cycle = ON
buzzer.frequency = 2000
time.sleep(0.1)
buzzer.frequency = 1000
time.sleep(0.1)
buzzer.duty_cycle = OFF

# Main
if __name__ == '__main__':
    print(keyboard.extensions)
    print(keyboard.modules)
    keyboard.go()
