import pico2d
import game_framework

pico2d.open_canvas(1920, 1080)
import logo_state
import title_state
game_framework.run(title_state)
pico2d.close_canvas()