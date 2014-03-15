# This file is part of Foobar.
#
# Foobar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar. If not, see <http://www.gnu.org/licenses/>.
from struct import *
from random import randrange
from itertools import chain
CELL_SIZE = 4
HEADER_SIZE = 16


def read_header(tts_file):
    """
        Read Prefab Header
        @author Nicolas Fortin github@nettrader.fr https://github.com/nicolas-f
    """
    header = {}
    with open(tts_file, "rb") as curs:
        if curs.read(3) != "tts":
            raise IOError("Not a valid tts file")
        #unknown
        curs.read(5)
        header["x"] = unpack("H", curs.read(2))[0]
        header["y"] = unpack("H", curs.read(2))[0]
        header["z"] = unpack("H", curs.read(2))[0]
    return header

def read_x_layer(header, tts_file, x):
    """
        Read YZ Prefab Layer
        @author Nicolas Fortin github@nettrader.fr https://github.com/nicolas-f
    """
    with open(tts_file, "rb") as curs:
        curs.seek(HEADER_SIZE + 1 + x * header["y"] * header["z"] * CELL_SIZE)
        layer = [[unpack("i", curs.read(4))[0] for z in range(header["z"])] for y in range(header["y"])]
        return layer


def render_2d(header, blocks):
    from Tkinter import Tk, Label, mainloop, PhotoImage
    # Create a random color map from the set of blocks values
    colors = {}
    for unique_item in set(chain.from_iterable(blocks)):
        if unique_item == 0:
            colors[0] = (0, 0, 0)
        else:
            colors[unique_item] = (randrange(128), randrange(128), randrange(128))
    master = Tk()
    # Build image
    photo = PhotoImage(width=header["z"], height=header["y"])
    #{#ff0000 #ff0000 #ff0000} {#ff0000 #ff0000 #ff0000} {#ff0000 #ff0000 #ff0000} {#ff0000 #ff0000 #ff0000}
    horizontal_line = " ".join(["{" + " ".join(["#%02x%02x%02x" % tuple(colors[blockId]) for blockId in row]) + "}" for row in blocks])
    photo.put(horizontal_line)
    photo = photo.zoom(4, 4)
    label = Label(master, image=photo)
    label.pack()
    mainloop()

if __name__ == '__main__':
    tts_file = "G:\\SteamLibrary\\steamapps\\common\\7 Days To Die\\Data\\Prefabs\\factory_lg_01.tts"
    header = read_header(tts_file)
    layer = read_x_layer(header, tts_file, 35)
    render_2d(header, layer)
