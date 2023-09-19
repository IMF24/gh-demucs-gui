import os as OS

OWD = OS.getcwd()
""" Original working directory. """

VERSION = "1.0"
""" Version of the program. """

BG_COLOR = '#090C10'
""" Background color of the program. """

FG_COLOR = '#FFFFFF'
""" Text color for the program. """

FONT = "Segoe UI"
""" The main text font everything uses. """

FONT_SIZE = 9
""" The main font size. """

FONT_INFO = (FONT, FONT_SIZE)
""" Tuple containing the various font information for the program. """

FONT_INFO_BOLD = (FONT, FONT_SIZE, 'bold')
""" Same info tuple as `FONT_INFO`, but for bold text. """

FONT_INFO_CODE = ("Consolas", 11)
""" Tuple contining font information for the INI Editor or any other code editor. """

FONT_INFO_HEADER = (FONT, 10)
""" Font information for headers (meant for more important/pronounced text). """

FONT_INFO_FOOTER = (FONT, 11)
""" Font information for the footer (text along the bottom of the program). """

HOVER_DELAY = 0.35
""" Time delay before tooltips appear, in seconds. """

TOOLTIP_WIDTH = 500
""" In pixels, the width of tooltips when hovering over the various options. """