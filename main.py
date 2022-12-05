import pico2d
import game_framework

pico2d.open_canvas(1280, 720)
import logo_state
game_framework.run(logo_state)
pico2d.close_canvas()