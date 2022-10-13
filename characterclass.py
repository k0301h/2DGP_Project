from Unitclass import *
import map_floor
from pico2d import *



class CHARACTER(UNIT):
    UNIT.HP = 5
    UNIT.ATK = 1
    UNIT.Action = 0
    UNIT.MotionIndex = 0
    UNIT.X = 400
    UNIT.Y = 400
    UNIT.DIRECTION = 0
    BombCount = 4
    RopeCount = 4
    Money = 0

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

    def Place(self):
        for index_x in range(0, 25):
            for index_y in range(0, 25):
                if map_floor.map_floor_array[index_y][index_x] == 1:
                    self.X = index_x * 60
                    self.Y = map_floor.HEIGHT - index_y * 60 - 30

    def Conflict_checking(self):
        # index = int((HEIGHT - character.Y + 60) // 60 + 2 + camera_move_y // 60) * 25 + int(
        #     character.X // 60 - camera_move_x // 60) - 25
        # index_X = character.X // 60
        # index_Y = (HEIGHT - character.Y) // 60
        #
        # if map_floor_array[int((index_Y + 2) * 25 + index_X)] == 0 or map_floor_array[int((index_Y + 2) * 25 + index_X)] == 1:
        #     return True
        # tmpx_index = int(self.X // 60)
        # tmpy_index = int((map_floor.HEIGHT - self.Y) // 60)
        # distance = 0
        #
        # for index_Y in range(tmpy_index - 5, tmpy_index + 5):
        #     for index_X in range(tmpx_index - 5, tmpx_index + 5):
        #         if not map_floor.map_floor_array[index_Y * 25 + index_X] == 0 and not map_floor.map_floor_array[index_Y * 25 + index_X] == 1:
        #             distance = ((index_X * 60 - self.X) ** 2 + (index_Y * 60 - self.Y) ** 2) ** (1 / 2)
        #
        #             if distance <= 100:
        #                 print(distance)
        #                 return False
        character_index_x = int(self.X // 60 - self.camera_move_x // 60)
        character_index_y = int((map_floor.HEIGHT - self.Y) // 60 + self.camera_move_y // 60)

        for index_y in range(character_index_y - 2, character_index_y + 3):
            for index_x in range(character_index_x - 2, character_index_x + 3):
                #index % 25 * 60 + self.camera_move_x, map_floor.HEIGHT - index // 25 * 60 + self.camera_move_y
                if (not map_floor.map_floor_array[index_y][index_x] == 0 and not map_floor.map_floor_array[index_y][index_x] == 1) and \
                        index_x * 60 + self.camera_move_x - 40 <= self.X <= index_x * 60 + self.camera_move_x + 40:
                    return False

                if index_x == 3:
                    print(self.Y)
                    print(index_x, index_y)
                    print(map_floor.HEIGHT - index_y * 60 + self.camera_move_y - 40 <= self.Y)
        return True
    def Jump(self):  # 점프키 입력시간에 비례하여 점프 높이 조절
        self.MotionIndex = (self.MotionIndex + 0.1) % 16 % 8 + 16 * 9
        self.JumpSpeed -= self.Gravity
        if self.JumpSpeed > 0:
            self.Y += self.JumpSpeed
            self.camera_move_y -= self.JumpSpeed

    def Down_Jump(self):
        self.MotionIndex = (self.MotionIndex + 0.1) % 16 % 8 + 16 * 9
        self.JumpSpeed -= self.Gravity
        if self.JumpSpeed > 0:
            self.Y -= self.JumpSpeed
            self.camera_move_y += self.JumpSpeed
    def gravity(self):
        # index = int((map_floor.HEIGHT - self.Y + 60) // 60 + self.camera_move_y // 60) * 25 + int(
        #     self.X // 60 - self.camera_move_x // 60)
        # index_X = character.X // 60
        # index_Y = (HEIGHT - character.Y) // 60
        # print(index)

        character_index_x = int(self.X // 60 - self.camera_move_x // 60)
        character_index_y = int((map_floor.HEIGHT - self.Y) // 60 + self.camera_move_y // 60)

        for index_y in range(character_index_y - 2, character_index_y + 3):
            for index_x in range(character_index_x - 2, character_index_x + 3):
                if map_floor.HEIGHT - index_y * 60 + self.camera_move_y - 40 <= self.Y <= map_floor.HEIGHT - index_y * 60 + self.camera_move_y + 40:
                    if self.DownSpeed <= 5:
                        self.DownSpeed += self.Gravity
                    self.Y = self.Y - self.DownSpeed
                    self.camera_move_y += self.DownSpeed
                    self.MotionIndex = (self.MotionIndex + 0.1) % 16 % 8 + 16 * 9
                    self.Can_Jump = False
                else:
                    self.Can_Jump = True
                    self.DownSpeed = 0


    def Motion(self):
        if self.Conflict_checking():
            self.gravity()

            if self.Jump_Key_State:
                self.Jump()
            elif self.Down_Jump_state:
                self.Down_Jump()

            if self.Action == 0:
                if not self.Jump_Key_State and not self.Gravity_state:
                    self.MotionIndex = 0
            elif self.Action == 1:
                if self.shift_on == 0:
                    self.X += 2
                    self.camera_move_x -= 2
                    if not self.Jump_Key_State:
                        self.MotionIndex = (self.MotionIndex + 0.1) % 8
                else:
                    self.X += 5
                    self.camera_move_x -= 5
                    if not self.Jump_Key_State:
                        self.MotionIndex = (self.MotionIndex + 0.3) % 8
            elif self.Action == 2:
                if self.MotionIndex < 18 and not self.Jump_Key_State:
                    self.MotionIndex = (self.MotionIndex + 0.1) % 16 % 3 + 16
            elif self.Action == 3:
                if self.shift_on == 0:
                    self.X -= 2
                    self.camera_move_x += 2
                    if not self.Jump_Key_State:
                        self.MotionIndex = (self.MotionIndex + 0.1) % 8
                else:
                    self.X -= 5
                    self.camera_move_x += 5
                    if not self.Jump_Key_State:
                        self.MotionIndex = (self.MotionIndex + 0.3) % 8


    def key_down(self):
        events = get_events()

        for event in events:
            if event.type == SDL_QUIT:
                close_canvas()
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_UP:
                    pass
                elif event.key == SDLK_RIGHT:
                    if self.Action != 2:
                        self.Action = 1
                        self.DIRECTION = 0
                elif event.key == SDLK_DOWN:
                    self.Action = 2
                elif event.key == SDLK_LEFT:
                    if self.Action != 2:
                        self.DIRECTION = 1
                        self.Action = 3
                elif event.key == SDLK_LALT:
                    if self.Action == 2 and not self.Jump_Key_State and self.Can_Jump:
                        self. Down_Jump_state = True
                    elif not self.Jump_Key_State and self.Can_Jump:
                        self.Jump_Key_State = True
                elif event.key == SDLK_LSHIFT:
                    self.shift_on = True
                elif event.key == SDLK_ESCAPE:
                    pass
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_RIGHT and self.Action == 1:
                    self.Action = 0
                elif event.key == SDLK_DOWN and self.Action == 2:
                    self.Action = 0
                elif event.key == SDLK_LEFT and self.Action == 3:
                    self.Action = 0
                elif event.key == SDLK_LALT and (self.Jump_Key_State or self.Down_Jump_state):
                    self.Jump_Key_State = False
                    self.Down_Jump_state = False
                    self.JumpSpeed = 10
                elif event.key == SDLK_LSHIFT:
                    self.shift_on = False