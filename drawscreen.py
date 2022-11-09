from map_floor import *
import time
import threading

start = 0
end = 0

if ROUND == 0:
    map_floor_array += map_tutorial
elif ROUND == 1:
    map_floor_array += map_floor_array_1

def start_time():
    global start
    start = time.time()

def end_timer():
    global end
    end = time.time()

def draw_background(BG_stage_I):
    BG_stage_I.draw(320, 320)
    BG_stage_I.draw(320, 960)
    BG_stage_I.draw(960, 320)
    BG_stage_I.draw(960, 960)
    BG_stage_I.draw(1600, 320)
    BG_stage_I.draw(1600, 960)

# 느낌만 구현 나중에 맵 구체적으로 계획후 배열 제작
def draw_map_floor(FLOOR_stage_I, Deco_tutorial_I, trap, character, range_l = 0, range_r = WIDTH, range_b = 0, range_t = HEIGHT):
    if ROUND == 0:
        Deco_tutorial_I.clip_draw(0, 1024 - 255, 510, 255, 13 * 60 - character.camera_move_x,
                                  HEIGHT - 3 * 60 - character.camera_move_y, 300, 150)
        Deco_tutorial_I.clip_draw(510, 1024 - 255, 510, 255, 22 * 60 - character.camera_move_x,
                                  HEIGHT - 5 * 60 - character.camera_move_y, 300, 150)

    for index_x in range(0, map_size):
        for index_y in range(0, map_size):
            if range_b - 30 <= HEIGHT - index_y * 60 <= range_t + 30 and\
                    range_l - 30 <= index_x * 60  - character.camera_move_x <= range_r + 30:
                if map_floor_array[index_y][index_x] == 0:
                    pass
                elif map_floor_array[index_y][index_x] == 1:
                    FLOOR_stage_I.clip_draw(45, 386, 300, 240, index_x * 60 - character.camera_move_x,
                                            HEIGHT - index_y * 60 - character.camera_move_y, 200, 160)
                elif map_floor_array[index_y][index_x] == -1:
                    FLOOR_stage_I.clip_draw(45, 386, 300, 240, index_x * 60 - character.camera_move_x,
                                            HEIGHT - index_y * 60 - character.camera_move_y, 200, 160)
                elif 30 <= map_floor_array[index_y][index_x] <= 35:
                    FLOOR_stage_I.clip_draw(128 * 4, 1410 - 128 * (map_floor_array[index_y][index_x] - 30)
                                            , 128, 128, index_x * 60 - character.camera_move_x,
                                            HEIGHT - index_y * 60 - character.camera_move_y, 60, 60)
                elif 36 <= map_floor_array[index_y][index_x] <= 39:
                    FLOOR_stage_I.clip_draw(128 * (map_floor_array[index_y][index_x] - 31), 1410 - 1155
                                            , 128, 128, index_x * 60 - character.camera_move_x,
                                            HEIGHT - index_y * 60 - character.camera_move_y, 60, 60)
                    if index_x * 60 - 30 <= character.X <= index_x * 60 + 30 and\
                        index_y * 60 + 120 <= character.Y <= index_y * 60 + 175:
                        FLOOR_stage_I.clip_draw(128 * (map_floor_array[index_y][index_x] - 31), 1410 - 1282
                                                , 128, 128, index_x * 60 - character.camera_move_x,
                                                HEIGHT - index_y * 60 - character.camera_move_y, 60, 60)
                elif 40 == map_floor_array[index_y][index_x]:
                    trap.image.clip_composite_draw(0, 1600 - 160, 160, 160, 0, '', index_x * 60 - character.camera_move_x,
                                                HEIGHT - index_y * 60 - character.camera_move_y, 60, 60)
                elif 41 == map_floor_array[index_y][index_x]:
                    trap.image.clip_composite_draw(0, 1600 - 160, 160, 160, 0, 'h', index_x * 60 - character.camera_move_x,
                                                HEIGHT - index_y * 60 - character.camera_move_y, 60, 60)
                else:
                    FLOOR_stage_I.clip_draw(128 * ((map_floor_array[index_y][index_x] - 2) % 4),
                                            1410 - 128 * ((map_floor_array[index_y][index_x] - 2) // 4), 128, 128,
                                            index_x * 60 - character.camera_move_x,
                                            HEIGHT - index_y * 60 - character.camera_move_y, 60, 60)
                    if not index_x == map_size - 1 and not 2 <= map_floor_array[index_y][index_x + 1] <= 29:
                        FLOOR_stage_I.clip_draw(687, 765, 30, 130, index_x * 60 - character.camera_move_x + 27,
                                                HEIGHT - index_y * 60 - character.camera_move_y, 15, 60)
                    if not index_x == 0 and not 2 <= map_floor_array[index_y][index_x - 1] <= 29:
                        FLOOR_stage_I.clip_composite_draw(687, 765, 30, 130, 0, 'h',index_x * 60 - character.camera_move_x - 30,
                                                HEIGHT - index_y * 60 - character.camera_move_y, 15, 60)
                    #               좌우반전 필요
                    if index_y * map_size + index_x < map_size * map_size and index_y + 1 < map_size and not 2 <= map_floor_array[index_y + 1][index_x] <= 29:
                        FLOOR_stage_I.clip_draw(640, 560, 130, 40, index_x * 60 - character.camera_move_x,
                                                HEIGHT - index_y * 60 - character.camera_move_y - 27, 60, 20)
                    if index_x + index_y * map_size >= 0 and not 2 <= map_floor_array[index_y - 1][index_x] <= 29:
                        FLOOR_stage_I.clip_draw(640, 680, 130, 40,index_x * 60 - character.camera_move_x,
                                                HEIGHT - index_y * 60 - character.camera_move_y + 27, 60, 20)
