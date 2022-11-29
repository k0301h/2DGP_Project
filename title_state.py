from pico2d import *
import play_state

import game_framework
from map_floor import WIDTH, HEIGHT, mode

main_image0 = None
main_image1 = None
main_image2 = None

sub_back_image0 = None

sub_image0 = None
sub_image1 = None
sub_image2 = None
sub_image3 = None
sub_image4 = None

select_image = None

main_body_image = None
main_head_image = None
main_door_image = None

music = None

select_menu_x = WIDTH / 2
select_menu_y = HEIGHT / 2

running = False
game_start = False

radian = 0
move = 2
end_move = 0
end_move_y = 0
rotation_finish = False
select_move = HEIGHT / 10
font = None
character = 'spelunky'

PIXEL_PER_METER = (10 / 0.5)

ROTATION_SPEED_KMPH = 0.5
ROTATION_SPEED_MPM = (ROTATION_SPEED_KMPH * 1000.0 / 60.0)
ROTATION_SPEED_MPS = (ROTATION_SPEED_MPM / 60.0)
ROTATION_SPEED_PPS = (ROTATION_SPEED_MPS * PIXEL_PER_METER)

def enter():
    print('enter title_state')
    global main_image0, main_image1, main_image2, sub_back_image0, sub_image0, sub_image1, sub_image2, sub_image3, \
        sub_image4, select_image, main_body_image, main_head_image, main_door_image, font, music
    main_image0 = load_image('./Textures/hud_controller_buttons.png')
    main_image1 = load_image('./Textures/menu_title.png')
    main_image2 = load_image('./Textures/menu_titlegal.png')

    main_body_image = load_image('./Textures/main_body.png')
    main_head_image = load_image('./Textures/main_head.png')
    main_door_image = load_image('./Textures/main_door.png')

    sub_back_image0 = load_image('./Textures/base_skynight.png')

    sub_image0 = load_image('./Textures/main_dirt.png')
    sub_image1 = load_image('./Textures/main_doorback.png')
    sub_image2 = load_image('./Textures/main_doorframe.png')
    sub_image3 = load_image('./Textures/main_fore2.png')
    sub_image4 = load_image('./Textures/main_fore1.png')

    select_image = load_image('./Textures/menu_basic.png')

    font = load_font('./Textures/ENCR10B.TTF', 50)

    music = load_wav('./sound/title.mp3')

    music.play()

def exit():
    print('exit title_state')
    global main_image0, main_image1, main_image2, sub_back_image0, sub_image0, sub_image1, sub_image2, sub_image3, \
        sub_image4, select_image, main_body_image, main_head_image, main_door_image, font
    del main_image0
    del main_image1
    del main_image2

    del main_head_image
    del main_body_image
    del main_door_image

    del sub_back_image0

    del sub_image0
    del sub_image1
    del sub_image2
    del sub_image3
    del sub_image4

    del select_image
    del font

def update():
    # print('update title_state')
    global running, radian, move, end_move, rotation_finish, end_move_y, select_move

    if radian <= 6.28 and game_start:
        radian += ROTATION_SPEED_PPS * game_framework.frame_time
        delay(0.02)
        move = -move
        if radian >= 6.28:
            rotation_finish = True
    elif rotation_finish:
        delay(0.5)
        rotation_finish = False
    elif end_move <= HEIGHT * 3 / 5 and game_start:
        end_move += HEIGHT / 100
        delay(0.03)
        move = -move
        if end_move >= HEIGHT * 3 / 5:
            rotation_finish = True
    elif end_move_y <= HEIGHT * 3 / 5 and game_start:
        end_move_y += HEIGHT / 80
        delay(0.03)
        move = -move
        if end_move_y >= HEIGHT * 3 / 5:
            running = True
    elif running:
        if mode == 1:
            select_move -= 5
        else:
            select_move -= 10
        select_move = clamp(0, select_move, 100)

def draw():
    # print('draw title_state')
    pico2d.clear_canvas()
    if not game_start:
        main_image1.clip_draw(0, 0, 1920, 1080, WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT)
        main_image2.clip_draw(0, 0, 1024, 1024, WIDTH / 3, HEIGHT / 3, HEIGHT, HEIGHT)
        main_image0.clip_draw(126, 0, 130, 130, (7 * WIDTH) / 11, HEIGHT / 5, HEIGHT / 20, HEIGHT / 20)
    elif game_start:
        sub_back_image0.clip_draw(0, 0, 512, 512, WIDTH / 2 + move, HEIGHT / 2, WIDTH, HEIGHT)
        sub_image0.clip_draw(0, 0, 1024, 256, WIDTH / 2 + move, HEIGHT / 5, (2 * WIDTH) / 3, HEIGHT / 4)

        font.draw(WIDTH * 3 / 7, HEIGHT * 3 / 5, 'Game Start', (255, 255, 255))
        if character == 'Anna':
            font.draw(WIDTH * 7 / 15, HEIGHT / 2, 'Anna', (255, 255, 255))
        elif character == 'spelunky':
            font.draw(WIDTH * 4 / 9, HEIGHT / 2, 'spelunky', (255, 255, 255))
        font.draw(WIDTH * 7 / 15, HEIGHT * 2 / 5, 'Exit', (255, 255, 255))

        if running:
            select_image.clip_draw(895, 1280 - 730, 360, 55, select_menu_x - WIDTH / 6 - select_move, select_menu_y, 210, 30)
            select_image.clip_composite_draw(895, 1280 - 730, 360, 55, 0, 'h', select_menu_x + WIDTH / 6 + select_move, select_menu_y,
                                         210, 30)
        sub_image1.clip_draw(0, 0, 1024, 1024, WIDTH / 2 + move, HEIGHT / 2, HEIGHT, HEIGHT)

        if end_move < HEIGHT:
            main_body_image.clip_composite_draw(0, 0, 512, 512, 0, '', WIDTH / 2 + move, HEIGHT / 2 - HEIGHT / 5 - end_move_y,
                                                HEIGHT / 2, HEIGHT / 2)
            if radian <= 6.28:
                main_door_image.clip_composite_draw(0, 0, 1024, 1024, radian / 2, 'h', WIDTH / 2 + move, HEIGHT / 2 - end_move, HEIGHT * 6 / 7,
                                                    HEIGHT * 6 / 7)
            else:
                main_door_image.clip_composite_draw(0, 0, 512, 1024, radian / 2, 'h', WIDTH / 2 + move - end_move - HEIGHT * 3 / 14,
                                                    HEIGHT / 2, HEIGHT * 3 / 7,
                                                    HEIGHT * 6 / 7)
                main_door_image.clip_composite_draw(512, 0, 512, 1024, radian / 2, 'h', WIDTH / 2 + move + end_move + HEIGHT * 3 / 14,
                                                    HEIGHT / 2, HEIGHT * 3 / 7,
                                                    HEIGHT * 6 / 7)
            main_head_image.clip_composite_draw(0, 0, 512, 512, -radian, '', WIDTH / 2 + move, HEIGHT / 2 - end_move_y, HEIGHT / 2 - move,
                                                HEIGHT / 2)

        sub_image2.clip_draw(0, 0, 1280, 1080, WIDTH / 2 + move, HEIGHT / 2, (4 * HEIGHT) / 3 , HEIGHT)
        sub_image3.clip_draw(0, 0, 768, 1080, WIDTH / 5 + move, HEIGHT / 2, HEIGHT, HEIGHT)
        sub_image3.clip_draw(768, 0, 768, 1080, (4 * WIDTH) / 5 + move, HEIGHT / 2, HEIGHT, HEIGHT)
        sub_image4.clip_draw(0, 0, 512, 1080, HEIGHT / 4 + move, HEIGHT / 2, HEIGHT / 2, HEIGHT)
        sub_image4.clip_draw(512, 0, 512, 1080, WIDTH - HEIGHT / 4 + move, HEIGHT / 2, HEIGHT / 2, HEIGHT)

    pico2d.update_canvas()

def handle_events():
    handle = get_events()
    global game_start, select_menu_y, select_move, radian, end_move, end_move_y, running, character
    for event in handle:
        if event.type == SDL_QUIT:
            game_framework.quit()
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_RETURN:
                if game_start:
                    radian = 7
                    end_move = HEIGHT
                    end_move_y = HEIGHT
                    running = True
                if running and select_menu_y == HEIGHT / 2 + HEIGHT / 10:
                    play_state.character = character
                    game_framework.change_state(play_state)
                elif running and select_menu_y == HEIGHT / 2:
                    if play_state.character == None:
                        if character == 'Anna':
                            character = 'spelunky'
                        elif character == 'spelunky':
                            character = 'Anna'
                elif running and select_menu_y == HEIGHT / 2 - HEIGHT / 10:
                    game_framework.quit()
                game_start = True
            elif event.key == SDLK_UP:
                select_menu_y += HEIGHT // 10
                select_move = 100
                select_menu_y = clamp(HEIGHT / 2 - HEIGHT / 10, select_menu_y, HEIGHT / 2 + HEIGHT / 10)
            elif event.key == SDLK_DOWN:
                select_menu_y -= HEIGHT // 10
                select_move = 100
                select_menu_y = clamp(HEIGHT / 2 - HEIGHT / 10, select_menu_y, HEIGHT / 2 + HEIGHT / 10)
            elif event.key == SDLK_SPACE:
                pass

def pause(): pass

def resume(): pass