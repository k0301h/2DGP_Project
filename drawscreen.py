from pico2d import *
from characterclass import *
from map_floor import *
import time
import threading

character = CHARACTER()
open_canvas()

character_I = load_image('char_yellow.png')
character_reverse_I = load_image('r_char_yellow.png')
BG_stage_I = load_image('bg_cave.png')
FLOOR_stage_I = load_image('floor_cave.png')

# Jump_Key_State = False
# Can_Jump = True
Gravity = 3.0
JumpSpeed = 20

shift_on = 0

start = 0
end = 0

def start_time():
    global start
    start = time.time()

def end_timer():
    global end
    end = time.time()

# 느낌만 구현 나중에 맵 구체적으로 계획후 배열 제작
def draw_map_floor():
    for index in range(0, 25 * 25):
        if map_floor_array[index] == 1:
            FLOOR_stage_I.clip_draw(0, 448, 64, 64, index % 25 * 64, 600 - index // 25 * 64)
    

def draw_character():
    # global Jump_Key_State
    # global Can_Jump
    global shift_on
    global JumpSpeed

    clear_canvas()
    BG_stage_I.draw(400, 300)
    draw_map_floor()
    if character.DIRECTION == 0:
      character_I.clip_draw(character.MotionIndex % 16 * 128, 1918 - 128 * (character.MotionIndex // 16), 128, 128, character.X, character.Y)
    elif character.DIRECTION == 1:
      character_reverse_I.clip_draw(1918 - character.MotionIndex % 16 * 128, 1918 - 128 * (character.MotionIndex // 16), 128, 128, character.X, character.Y)
    # character_I.clip_draw(character.MotionIndex % 16 * 128, 1918 - 128 * (character.MotionIndex // 16), 128, 128, character.X, character.Y)
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
                character.DIRECTION = 0
            elif event.key == SDLK_DOWN:
                character.Action = 2
            elif event.key == SDLK_LEFT:
                character.DIRECTION = 1
                character.Action = 3
            elif event.key == SDLK_LALT:
                # Jump_Key_State = True
                character.Action = 4
            elif event.key == SDLK_LSHIFT:
                shift_on = 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_UP:
                character.Action = 0
            elif event.key == SDLK_RIGHT:
                character.Action = 0
            elif event.key == SDLK_DOWN:
                character.Action = 0
            elif event.key == SDLK_LEFT:
                character.Action = 0
            elif event.key == SDLK_LALT:
                # Jump_Key_State = False
                character.Action = 0
                JumpSpeed = 20
            elif event.key == SDLK_LSHIFT:
                shift_on = 0

    if character.Action == 0:
        character.MotionIndex = 0
    elif character.Action == 1:
        character.MotionIndex = (character.MotionIndex + 1) % 8
        if shift_on == 0:
            character.X += 5
        else:
            character.X += 15
    elif character.Action == 2:
        if character.MotionIndex < 18:
            character.MotionIndex = (character.MotionIndex + 1) % 16 % 3 + 16
    elif character.Action == 3:
        character.MotionIndex = (character.MotionIndex + 1) % 8
        if shift_on == 0:
            character.X -= 5
        else:
            character.X -= 15
    elif character.Action == 4:
        character.MotionIndex = (character.MotionIndex + 1) % 16 % 8 + 16 * 9
        Jump()



def Jump():
    global JumpSpeed
    global character
    JumpSpeed -= Gravity
    if JumpSpeed > 0:
        character.Y += JumpSpeed

while (1):
    draw_character()


close_canvas()
