from drawscreen import *

from pico2d import *

open_canvas(WIDTH, HEIGHT)

import play_state

now_state = play_state
now_state.enter()
while 1:
    now_state.draw()
    now_state.update()
    now_state.handle_events()
    delay(0.01)

close_canvas()