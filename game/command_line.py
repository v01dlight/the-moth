import pprint
import sys
from information import GameInformation
from catalog import Catalog

game_info = GameInformation.parse(sys.argv[1])
if len(sys.argv) > 3:
    if sys.argv[3] == "*":
        items = game_info[sys.argv[2]]
        for key in items:
            print(key)
            print(items[key].description, "\n")
    else:
        pprint.pp(game_info[sys.argv[2]][sys.argv[3]])
elif len(sys.argv) > 2:
    element = game_info[sys.argv[2]]
    if isinstance(element, Catalog):
        print(element.description)
    else:
        print(element)
else:
    pprint.pp(game_info)
