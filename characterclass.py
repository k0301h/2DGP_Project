from Unitclass import *
from map_floor import *
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
    JumpSpeed = 11
    DownSpeed = 0

    camera_move_x = 0
    camera_move_y = 0

    shift_on = False
    Can_Jump = True
    Jump_Key_State = False
    Down_Jump_state = False
    Gravity_state = False
    Attack_state = False

    whip = UNIT()

    def Place(self):
        for index_x in range(0, map_size):
            for index_y in range(0, map_size):
                if map_floor_array[index_y][index_x] == 1:
                    self.X = index_x * 60
                    self.Y = HEIGHT - index_y * 60 - 30

    def Conflict_checking(self, mode, move): # mode : x,y충돌 검사 , move : 다음에 움직일 크기
        character_index_x = int((self.X + move) // 60)
        character_index_y = int((HEIGHT - (self.Y + move)) // 60)

        if mode == 1:       # Y충돌 체크
            for index_x in range(character_index_x - 1, character_index_x + 2):
                for index_y in range(character_index_y - 2, character_index_y + 3):
                    if 0 <= index_x < map_size and  0 <= index_y < map_size and\
                            (not map_floor_array[index_y][index_x] == 0 and not map_floor_array[index_y][index_x] == 1) and \
                            abs(self.X - index_x * 60) <= 60 and abs(self.Y + move - (HEIGHT - index_y * 60)) <= 65:
                        return False

        elif mode == 2:     # X충돌 체크
            for index_y in range(character_index_y - 1, character_index_y + 2):
                for index_x in range(character_index_x - 2, character_index_x + 3):
                    if 0 <= index_x < map_size and 0 <= index_y < map_size and\
                            (not map_floor_array[index_y][index_x] == 0 and not map_floor_array[index_y][index_x] == 1) and \
                            abs(self.Y - (HEIGHT - index_y * 60)) <= 65 and abs(self.X + move - index_x * 60) <= 60:
                        print(abs(self.X + move - index_x * 60), index_x)
                        return False
        return True

    def Jump(self):  # 점프키 입력시간에 비례하여 점프 높이 조절
        if self.Conflict_checking(1, self.JumpSpeed):
            if not self.Attack_state:
                self.MotionIndex = (self.MotionIndex + 0.1) % 16 % 8 + 16 * 9
            self.JumpSpeed -= self.Gravity
            if self.JumpSpeed > 0:
                self.Y += self.JumpSpeed
                if self.Y <= 100:
                    self.camera_move_y += self.JumpSpeed
        else:
            self.Jump_Key_State = False
            self.JumpSpeed = 11

    def Down_Jump(self):
        # self.MotionIndex = (self.MotionIndex + 0.1) % 16 % 8 + 16 * 9
        # self.JumpSpeed -= self.Gravity
        # if self.JumpSpeed > 0:
        #     self.Y -= self.JumpSpeed
        #     if self.Y <= 100:
        #         self.camera_move_y == self.JumpSpeed

        pass
    def gravity(self):
        if self.Conflict_checking(1, -self.DownSpeed):
            if self.DownSpeed <= 5:
                self.DownSpeed += self.Gravity
            self.Y = self.Y - self.DownSpeed
            if self.Y <= 200:
                self.camera_move_y -= self.DownSpeed
            if not self.Attack_state:
                self.MotionIndex = (self.MotionIndex + 0.3) % 16 % 8 + 16 * 9
            self.Can_Jump = False
            self.Gravity_state = True
        else:
            self.Can_Jump = True
            self.DownSpeed = 0
            self.Gravity_state = False

    def Motion(self):
        if self.Jump_Key_State:
            self.Jump()
        elif self.Down_Jump_state:
            self.Down_Jump()

        if self.Action == 0:
            if not self.Jump_Key_State and not self.Gravity_state and not self.Attack_state:
                self.MotionIndex = 0
        elif self.Action == 1:
            if self.shift_on == 0:
                if self.X - self.camera_move_x <= 1000:
                    if self.Conflict_checking(2, 2):
                        self.X += 2
                elif self.X - self.camera_move_x > 1000:
                    if self.Conflict_checking(2, 0):
                        self.X += 2
                        self.camera_move_x += 2

                if not self.Jump_Key_State and not self.Attack_state:
                    self.MotionIndex = (self.MotionIndex + 0.1) % 8
            else:
                if self.Conflict_checking(2, 4):
                    if self.X - self.camera_move_x <= 1000:
                        self.X += 4
                    elif self.X - self.camera_move_x > 1000:
                        self.X += 4
                        self.camera_move_x += 4

                if not self.Jump_Key_State and not self.Attack_state:
                    self.MotionIndex = (self.MotionIndex + 0.3) % 8

        elif self.Action == 2:
            if self.MotionIndex < 18 and not self.Jump_Key_State and not self.Attack_state:
                self.MotionIndex = (self.MotionIndex + 0.1) % 16 % 3 + 16

        elif self.Action == 3:
            if self.shift_on == 0:
                if self.Conflict_checking(2, -2):
                    if self.X - self.camera_move_x >= 200:
                        self.X -= 2
                    elif self.X - self.camera_move_x < 200:
                        self.X -= 2
                        self.camera_move_x -= 2

                if not self.Jump_Key_State and not self.Attack_state:
                    self.MotionIndex = (self.MotionIndex + 0.1) % 8

            else:
                if self.Conflict_checking(2, -4):
                    if self.X - self.camera_move_x >= 200:
                        self.X -= 4
                    elif self.X - self.camera_move_x < 200:
                        self.X -= 4
                        self.camera_move_x -= 4

                if not self.Jump_Key_State and not self.Attack_state:
                    self.MotionIndex = (self.MotionIndex + 0.3) % 8
        if self.Attack_state:
            print(self.MotionIndex % 16)
            if self.MotionIndex % 16 < 5:
                if self.whip.MotionIndex % 16 - 10 < 3:
                    if self.DIRECTION == 0:
                        self.whip.X = self.X - 45
                        self.whip.Y = self.Y - 10
                    elif self.DIRECTION == 1:
                        self.whip.X = self.X + 45
                        self.whip.Y = self.Y- 10
                elif 3 <= self.whip.MotionIndex % 16 - 10 < 4:
                    if self.DIRECTION == 0:
                        self.whip.X = self.X + 20
                        self.whip.Y = self.Y - 10
                    elif self.DIRECTION == 1:
                        self.whip.X = self.X - 20
                        self.whip.Y = self.Y - 10
                elif 4 <= self.whip.MotionIndex % 16 - 10:
                    if self.DIRECTION == 0:
                        self.whip.X = self.X + 45
                        self.whip.Y = self.Y- 10
                    elif self.DIRECTION == 1:
                        self.whip.X = self.X - 45
                        self.whip.Y = self.Y- 10

                self.whip.MotionIndex = (self.MotionIndex + 0.1) % 16 % 6 + 16 * 12 + 10
                self.MotionIndex = (self.MotionIndex + 0.1) % 16 % 6 + 16 * 4
            else:
                self.Action = 0
                self.Attack_state = False
                self.whip.MotionIndex = 0
        self.gravity()

    def key_down(self):
        for event in get_events():
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
                elif event.key == SDLK_LCTRL and self.Attack_state == False:
                    self.Attack_state = True
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
                    self.JumpSpeed = 11
                elif event.key == SDLK_LSHIFT:
                    self.shift_on = False