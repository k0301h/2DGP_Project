from pico2d import *
from characterclass import *
from map_floor import *
import time
import threading

character = CHARACTER()

WIDTH = 1280
HEIGHT = 800

for index in range(0, 25 * 25):
    if map_floor_array[index] == 1:
        character.X = index % 25 * 60
        character.Y = HEIGHT - index // 25 * 60 - 30

open_canvas(WIDTH, HEIGHT)

character_I = load_image('char_yellow.png')
character_reverse_I = load_image('r_char_yellow.png')
BG_stage_I = load_image('bg_cave.png')
FLOOR_stage_I = load_image('floor_cave.png')

Gravity = 0.3
JumpSpeed = 10
DownSpeed = 0

camera_move_x = 0
camera_move_y = 0

shift_on = False
Can_Jump = True
Jump_Key_State = False
Down_Jump_state = False
Gravity_state = False

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
        if map_floor_array[index] == 0:
            pass
        elif map_floor_array[index] == 1:
            FLOOR_stage_I.clip_draw(45, 386, 300, 240, index % 25 * 60 + camera_move_x,
                                    HEIGHT - index // 25 * 60 + camera_move_y, 225, 180)
        # elif map_floor_array[index] == 2:
        #     FLOOR_stage_I.clip_draw(0, 1410, 128, 128, index % 25 * 60 + camera_move_x,
        #                             WIDTH - index // 25 * 60 + camera_move_y, 60, 60)
        else:
            FLOOR_stage_I.clip_draw(128 * ((map_floor_array[index] - 2) % 4), 1410 - 128 * ((map_floor_array[index] - 2) // 4), 128, 128, index % 25 * 60 + camera_move_x,
                                    HEIGHT - index // 25 * 60 + camera_move_y, 60, 60)
            if not index % 25 == 24 and map_floor_array[index + 1] == 0:
                FLOOR_stage_I.clip_draw(687, 765, 30, 130, index % 25 * 60 + camera_move_x + 30,
                                        HEIGHT - index // 25 * 60 + camera_move_y, 15, 60)
            if not index % 25 == 0 and map_floor_array[index - 1] == 0:
                FLOOR_stage_I.clip_draw(687, 765, 30, 130, index % 25 * 60 + camera_move_x - 30,
                                        HEIGHT - index // 25 * 60 + camera_move_y, 15, 60)
#               좌우반전 필요
            if index + 25 < 25 * 25 and map_floor_array[index + 25] == 0:
                FLOOR_stage_I.clip_draw(640, 560, 130, 40, index % 25 * 60 + camera_move_x,
                                        HEIGHT - index // 25 * 60 + camera_move_y - 30, 60, 20)
            if index - 25 >= 0 and map_floor_array[index - 25] == 0:
                FLOOR_stage_I.clip_draw(640, 680, 130, 40, index % 25 * 60 + camera_move_x,
                                        HEIGHT - index // 25 * 60 + camera_move_y + 30, 60, 20)


def draw_character():
    # global Jump_Key_State
    # global Can_Jump
    global shift_on
    global JumpSpeed
    global Jump_Key_State
    global Down_Jump_state

    clear_canvas()
    BG_stage_I.draw(320, 320)
    BG_stage_I.draw(960, 320)
    BG_stage_I.draw(320, 960)
    BG_stage_I.draw(960, 960)

    draw_map_floor()
    if character.DIRECTION == 0:
      character_I.clip_draw(int(character.MotionIndex) % 16 * 128, 1918 - 128 * (int(character.MotionIndex) // 16), 128, 128, character.X, character.Y, 120, 120)
    elif character.DIRECTION == 1:
      character_reverse_I.clip_draw(1918 - int(character.MotionIndex) % 16 * 128, 1918 - 128 * (int(character.MotionIndex) // 16), 128, 128, character.X, character.Y, 120, 120)

    update_canvas()
    delay(0.01)
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
                if character.Action == 2 and not Jump_Key_State and Can_Jump:
                    Down_Jump_state = True
                elif not Jump_Key_State and Can_Jump:
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
                JumpSpeed = 10
            elif event.key == SDLK_LSHIFT:
                shift_on = False

    Motion()

def Conflict_checking(Action):
    # index = int((HEIGHT - character.Y + 60) // 60 + 2 + camera_move_y // 60) * 25 + int(
    #     character.X // 60 - camera_move_x // 60) - 25
    index = character.X // 60
    print(index)
    if Action == 1:
        for i in range(0,25):
            if map_floor_array[i * 25 + index] == 0 or map_floor_array[i * 25 + index] == 1:
                return True


def gravity():
    global character
    global Gravity_state
    global Can_Jump
    global DownSpeed
    global camera_move_y
    index = int((HEIGHT - character.Y + 32) // 60 + 2 + camera_move_y // 60) * 25 + int(character.X // 60 - camera_move_x // 60) - 25

    if map_floor_array[index] == 0 or map_floor_array[index] == 1:
        DownSpeed += Gravity
        character.Y = character.Y - DownSpeed
        camera_move_y += DownSpeed
        character.MotionIndex = (character.MotionIndex + 0.1) % 16 % 8 + 16 * 9
        Can_Jump = False
    else:
        Can_Jump = True
        DownSpeed = 0

def Motion():
    global character
    global camera_move_x
    global camera_move_y
    if Jump_Key_State:
        Jump()
    elif Down_Jump_state:
        Down_Jump()

    if character.Action == 0:
        if not Jump_Key_State and not Gravity_state:
            character.MotionIndex = 0
    elif character.Action == 1:
        if Conflict_checking(character.Action):
            if shift_on == 0:
                character.X += 1
                camera_move_x -= 1
                if not Jump_Key_State:
                    character.MotionIndex = (character.MotionIndex + 0.1) % 8
            else:
                character.X += 3
                camera_move_x -= 3
                if not Jump_Key_State:
                    character.MotionIndex = (character.MotionIndex + 0.3) % 8
    elif character.Action == 2:
        if character.MotionIndex < 18 and not Jump_Key_State:
            character.MotionIndex = (character.MotionIndex + 0.1) % 16 % 3 + 16
    elif character.Action == 3:
        if shift_on == 0:
            character.X -= 1
            camera_move_x += 1
            if not Jump_Key_State:
                character.MotionIndex = (character.MotionIndex + 0.1) % 8
        else:
            character.X -= 3
            camera_move_x += 3
            if not Jump_Key_State:
                character.MotionIndex = (character.MotionIndex + 0.3) % 8

    gravity()


def Jump(): # 점프키 입력시간에 비례하여 점프 높이 조절
    global character
    global JumpSpeed
    global camera_move_y
    character.MotionIndex = (character.MotionIndex + 0.1) % 16 % 8 + 16 * 9
    JumpSpeed -= Gravity
    if JumpSpeed > 0:
        character.Y += JumpSpeed
        camera_move_y -= JumpSpeed

def Down_Jump():
    global character
    global JumpSpeed
    global camera_move_y
    character.MotionIndex = (character.MotionIndex + 0.1) % 16 % 8 + 16 * 9
    JumpSpeed -= Gravity
    if JumpSpeed > 0:
        character.Y -= JumpSpeed
        camera_move_y += JumpSpeed




while (1):
    draw_character()

close_canvas()
