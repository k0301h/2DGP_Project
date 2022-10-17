from map_floor import *
import time
import threading

start = 0
end = 0

def start_time():
    global start
    start = time.time()

def end_timer():
    global end
    end = time.time()

# 느낌만 구현 나중에 맵 구체적으로 계획후 배열 제작
def draw_map_floor(FLOOR_stage_I, character):
    for index_x in range(0, map_size):
        for index_y in range(0, map_size):
            if map_floor_array[index_y][index_x] == 0:
                pass
            elif map_floor_array[index_y][index_x] == 1:
                FLOOR_stage_I.clip_draw(45, 386, 300, 240, index_x * 60 - character.camera_move_x + 30,
                                        HEIGHT - index_y * 60 - character.camera_move_y - 30, 200, 160)
            elif 30 <= map_floor_array[index_y][index_x] <= 35:
                FLOOR_stage_I.clip_draw(128 * 4, 1410 - 128 * (map_floor_array[index_y][index_x] - 30)
                                        , 128, 128, index_x * 60 - character.camera_move_x + 30,
                                        HEIGHT - index_y * 60 - character.camera_move_y - 30, 60, 60)
            else:
                FLOOR_stage_I.clip_draw(128 * ((map_floor_array[index_y][index_x] - 2) % 4),
                                        1410 - 128 * ((map_floor_array[index_y][index_x] - 2) // 4), 128, 128,
                                        index_x * 60 - character.camera_move_x + 30,
                                        HEIGHT - index_y * 60 - character.camera_move_y - 30, 60, 60)
                if not index_x == map_size - 1 and map_floor_array[index_y][index_x + 1] == 0:
                    FLOOR_stage_I.clip_draw(687, 765, 30, 130, index_x * 60 - character.camera_move_x + 27 + 30,
                                            HEIGHT - index_y * 60 - character.camera_move_y - 30, 15, 60)
                if not index_x == 0 and map_floor_array[index_y][index_x - 1] == 0:
                    FLOOR_stage_I.clip_draw(687, 765, 30, 130, index_x * 60 - character.camera_move_x - 27 + 30,
                                            HEIGHT - index_y * 60 - character.camera_move_y - 30, 15, 60)
                #               좌우반전 필요
                if index_y * map_size + index_x < map_size * map_size and map_floor_array[index_y + 1][index_x] == 0:
                    FLOOR_stage_I.clip_draw(640, 560, 130, 40, index_x * 60 - character.camera_move_x + 30,
                                            HEIGHT - index_y * 60 - character.camera_move_y - 27 - 30, 60, 20)
                if index_x + index_y * map_size >= 0 and map_floor_array[index_y - 1][index_x] == 0:
                    FLOOR_stage_I.clip_draw(640, 680, 130, 40, index_x * 60 - character.camera_move_x + 30,
                                            HEIGHT - index_y * 60 - character.camera_move_y + 27 - 30, 60, 20)


def draw_character(character, BG_stage_I, FLOOR_stage_I, character_I, character_reverse_I):
    BG_stage_I.draw(320, 320)
    BG_stage_I.draw(960, 320)
    BG_stage_I.draw(320, 960)
    BG_stage_I.draw(960, 960)

    draw_map_floor(FLOOR_stage_I, character)
    if character.DIRECTION == 0:
        if character.Attack_state:
            character_I.clip_draw(int(character.whip.MotionIndex) % 16 * 128,
                                  1918 - 128 * (int(character.whip.MotionIndex) // 16),
                                  128, 128, character.whip.X - character.camera_move_x + 30,
                                  character.whip.Y - character.camera_move_y - 30, 60, 60)
        character_I.clip_draw(int(character.MotionIndex) % 16 * 128, 1918 - 128 * (int(character.MotionIndex) // 16),
                              128, 128, character.X - character.camera_move_x + 30, character.Y - character.camera_move_y - 30,
                              70, 70)
    elif character.DIRECTION == 1:
        if character.Attack_state:
            character_I.clip_draw(int(character.whip.MotionIndex) % 16 * 128,
                                  1918 - 128 * (int(character.whip.MotionIndex) // 16),
                                  128, 128, character.whip.X - character.camera_move_x + 30,
                                  character.whip.Y - character.camera_move_y - 30, 60, 60)
        character_reverse_I.clip_draw(1918 - int(character.MotionIndex) % 16 * 128,
                                      1918 - 128 * (int(character.MotionIndex) // 16), 128, 128,
                                      character.X - character.camera_move_x + 30,
                                      character.Y - character.camera_move_y - 30, 70, 70)