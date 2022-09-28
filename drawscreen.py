from pico2d import *
from characterclass import *

character = CHARACTER()
open_canvas()

character_I = load_image('char_yellow.png')

def draw_character():
    clear_canvas()
    character_I.clip_draw(character.MotionIndex % 16 * 128, 1918 - 128 * (character.MotionIndex // 16), 128, 128,
                          character.X, character.Y)
    update_canvas()
    delay(0.075)
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            close_canvas()
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_UP:
                pass
            elif event.key == SDLK_RIGHT:
                character.Action = 1
                character.X += 5
            elif event.key == SDLK_DOWN:
                character.Action = 2
            elif event.key == SDLK_LEFT:
                character.Action = 3
            elif event.key == SDLK_b:
                character.Action = 4
                character.Y += 10
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_UP:
                character.Action = 0
            elif event.key == SDLK_RIGHT:
                character.Action = 0
            elif event.key == SDLK_DOWN:
                character.Action = 0
            elif event.key == SDLK_LEFT:
                character.Action = 0
            elif event.key == SDLK_b:
                character.Action = 0

    if character.Action == 0:
        character.MotionIndex = 0
    elif character.Action == 1:
        character.MotionIndex = (character.MotionIndex + 1) % 8
        character.X += 5
    elif character.Action == 2:
        if character.MotionIndex < 18:
            character.MotionIndex = (character.MotionIndex + 1) % 16 % 3 + 16
    elif character.Action == 3:
        character.MotionIndex = (character.MotionIndex + 1) % 8
        character.X -= 5
    elif character.Action == 4:
        character.MotionIndex = (character.MotionIndex + 1) % 16 % 8 + 16 * 9

while (1):
    draw_character()

close_canvas()
