from pico2d import *


# direction : 1 == up, 2 = right, 3 = down, 4 = left
character = {'x' : 400, 'y': 300, 'index': 0, 'direction' : 0}

open_canvas()

character_I = load_image('Ana Spelunky.png')


while(1):
    clear_canvas()
    character_I.clip_draw(character['index'] % 9 * 128, 1918 - 130 * (character['index'] // 9), 128, 130, character['x'], character['y'])
    update_canvas()
    delay(0.075)
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_UP:
                character['direction'] = 1
            elif event.key == SDLK_RIGHT:
                character['direction'] = 2
            elif event.key == SDLK_DOWN:
                character['direction'] = 3
            elif event.key == SDLK_LEFT:
                character['direction'] = 4
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_UP:
                character['direction'] = 0
            elif event.key == SDLK_RIGHT:
                character['direction'] = 0
            elif event.key == SDLK_DOWN:
                character['direction'] = 0
            elif event.key == SDLK_LEFT:
                character['direction'] = 0

    if character['direction'] == 0:
        character['index'] = 0
    elif character['direction'] == 1:
        character['index'] = 0
    elif character['direction'] == 2:
        character['index'] = (character['index'] + 1) % 9
    elif character['direction'] == 3:
        character['index'] = (character['index'] + 1) % 3 + 9
    elif character['direction'] == 4:
        character['index'] = (character['index'] + 1) % 9
    
    
        
                


    
close_canvas()
