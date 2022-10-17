from drawscreen import *
import play_state
from pico2d import *

open_canvas(WIDTH, HEIGHT)

now_state = play_state
now_state.enter()
while 1:
    now_state.draw()
    now_state.update()
    delay(0.005)

close_canvas()