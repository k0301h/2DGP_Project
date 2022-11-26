from pico2d import *
from map_floor import WIDTH, HEIGHT
import game_framework

pico2d.open_canvas(WIDTH, HEIGHT)

from drawscreen import *

import logo_state
import title_state
import play_state

game_framework.run(play_state)
pico2d.close_canvas()


# from drawscreen import *
#
# from pico2d import *
#
# open_canvas(WIDTH, HEIGHT)
#
# import play_state
# import logo_state
# import title_state
#
# now_state = title_state
# now_state.enter()
# while 1:
#     now_state.draw()
#     now_state.update()
#     now_state.handle_events()
#     delay(0.015)
#
# now_state.exit()
#
# close_canvas()