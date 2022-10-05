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
Gravity = 2.0
JumpSpeed = 20

shift_on = True
Jump_Key_State = False
Down_Jump_state = False

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
            FLOOR_stage_I.clip_draw(0, 1410, 130, 130, index % 25 * 60, 600 - index // 25 * 60, 60, 60)
        elif map_floor_array[index] == 2:
            FLOOR_stage_I.clip_draw(45, 386, 300, 240, index % 25 * 60, 600 - index // 25 * 60, 225, 180)
    

def draw_character():
    # global Jump_Key_State
    # global Can_Jump
    global shift_on
    global JumpSpeed
    global Jump_Key_State
    global Down_Jump_state

    clear_canvas()
    BG_stage_I.draw(200, 200)
    BG_stage_I.draw(600, 200)
    BG_stage_I.draw(200, 600)
    BG_stage_I.draw(600, 600)

    draw_map_floor()
    if character.DIRECTION == 0:
      character_I.clip_draw(character.MotionIndex % 16 * 128, 1918 - 128 * (character.MotionIndex // 16), 128, 128, character.X, character.Y)
    elif character.DIRECTION == 1:
      character_reverse_I.clip_draw(1918 - character.MotionIndex % 16 * 128, 1918 - 128 * (character.MotionIndex // 16), 128, 128, character.X, character.Y)
    # character_I.clip_draw(character.MotionIndex % 16 * 128, 1918 - 128 * (character.MotionIndex // 16), 128, 128, character.X, character.Y)
    update_canvas()
    delay(0.05)
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            close_canvas()
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_UP:
                pass
            elif event.key == SDLK_RIGHT:
                if character.Action != 2:
                    character.Action = 1
                    character.DIRECTION = 0
            elif event.key == SDLK_DOWN:
                character.Action = 2
            elif event.key == SDLK_LEFT:
                if character.Action != 2:
                    character.DIRECTION = 1
                    character.Action = 3
            elif event.key == SDLK_LALT:
                if character.Action == 2 and not Jump_Key_State:
                    Down_Jump_state = True
                else:
                    Jump_Key_State = True
            elif event.key == SDLK_LSHIFT:
                shift_on = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT and character.Action == 1:
                character.Action = 0
            elif event.key == SDLK_DOWN and character.Action == 2:
                character.Action = 0
            elif event.key == SDLK_LEFT and character.Action == 3:
                character.Action = 0
            elif event.key == SDLK_LALT and (Jump_Key_State or Down_Jump_state):
                Jump_Key_State = False
                Down_Jump_state = False
                JumpSpeed = 20
            elif event.key == SDLK_LSHIFT:
                shift_on = False

    Motion()



def Motion():
    global character
    if Jump_Key_State:
        Jump()
    elif Down_Jump_state:
        Down_Jump()


    if character.Action == 0:
        if not Jump_Key_State:
            character.MotionIndex = 0
    elif character.Action == 1:
        if not Jump_Key_State:
            character.MotionIndex = (character.MotionIndex + 1) % 8
        if shift_on == 0:
            character.X += 5
        else:
            character.X += 15
    elif character.Action == 2:
        if character.MotionIndex < 18 and not Jump_Key_State:
            character.MotionIndex = (character.MotionIndex + 1) % 16 % 3 + 16
    elif character.Action == 3:
        if not Jump_Key_State:
            character.MotionIndex = (character.MotionIndex + 1) % 8
        if shift_on == 0:
            character.X -= 5
        else:
            character.X -= 15

def Jump():
    global character
    global JumpSpeed
    character.MotionIndex = (character.MotionIndex + 1) % 16 % 8 + 16 * 9
    JumpSpeed -= Gravity
    if JumpSpeed > 0:
        character.Y += JumpSpeed

def Down_Jump():
    global character
    global JumpSpeed
    character.MotionIndex = (character.MotionIndex + 1) % 16 % 8 + 16 * 9
    JumpSpeed -= Gravity
    if JumpSpeed > 0:
        character.Y -= JumpSpeed

while (1):
    draw_character()


close_canvas()
