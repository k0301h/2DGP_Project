from map_floor import *
from pico2d import *

class SUB():
    MotionIndex = 0
    X = 400
    Y = 400

class CHARACTER():
    HP = 5
    ATK = 1
    Action = 0
    MotionIndex = 0
    X = 400
    Y = 400
    DIRECTION = 0
    BombCount = 4
    RopeCount = 4
    Money = 0

    # hnadle = None

    Gravity = 0.5
    JumpSpeed = 15
    DownSpeed = 0
    Down_Distance = 0

    camera_move_x = 0
    camera_move_y = 0

    shift_on = False
    Can_Jump = True
    Jump_Key_State = False
    Down_Jump_state = False
    Gravity_state = False
    Attack_state = False
    Climb_state = False
    Climb_up_key_state = False
    Climb_down_key_state = False
    Attack_key_state = False
    Stun_state = False
    Hanging_state = False

    image = None
    grid_image = None

    whip = SUB()
    stun = SUB()

    def __init__(self):
        if CHARACTER.image == None:
            CHARACTER.image = load_image('./Textures/char_yellow.png')
        if CHARACTER.grid_image == None:
            CHARACTER.grid_image = load_image('./Textures/Entities/char_yellow_full_grid.png')

    def Place(self):
        for index_x in range(0, map_size):
            for index_y in range(0, map_size):
                if map_floor_array[index_y][index_x] == 1:
                    self.X = index_x * 60
                    self.Y = HEIGHT - index_y * 60 - 30

    def Conflict_checking(self, mode, move): # mode : 충돌체크 유형 , move : 다음에 움직일 크기
        if mode == 1:       # Y충돌 체크
            character_index_x = int(self.X // 60)
            character_index_y = int((HEIGHT - (self.Y + move)) // 60)
            for index_x in range(character_index_x - 1, character_index_x + 2):
                for index_y in range(character_index_y - 2, character_index_y + 3):
                    if 0 <= index_x < map_size and 0 <= index_y < map_size and\
                            2 <= map_floor_array[index_y][index_x] <= 29 and\
                            abs(self.X - index_x * 60) <= 55 and abs(self.Y + move - (HEIGHT - index_y * 60)) <= 58:
                        return False
        elif mode == 2:     # X충돌 체크
            character_index_x = int((self.X + move) // 60)
            character_index_y = int((HEIGHT - self.Y) // 60)
            for index_y in range(character_index_y - 1, character_index_y + 2):
                for index_x in range(character_index_x - 2, character_index_x + 3):
                    if 0 <= index_x < map_size and 0 <= index_y < map_size and\
                            2 <= map_floor_array[index_y][index_x] <= 29 and \
                            abs(self.Y - (HEIGHT - index_y * 60)) < 58 and abs(self.X + move - index_x * 60) <= 55:
                        return False
        elif mode == 3:     # 사다리 체크
            character_index_x = int(self.X // 60)
            character_index_y = int((HEIGHT - (self.Y + move)) // 60)
            if not 30 <= map_floor_array[character_index_y][character_index_x] <= 35 or (30 <= map_floor_array[character_index_y][character_index_x] <= 35 and\
                    abs(self.X - character_index_x * 60) > 20):
                return False
            elif 30 <= map_floor_array[character_index_y][character_index_x] <= 35 and not self.Climb_state:
                self.X = character_index_x * 60
        elif mode == 4:     # 출구 체크
            character_index_x = int(self.X // 60)
            character_index_y = int((HEIGHT - self.Y) // 60)
            if not map_floor_array[character_index_y][character_index_x] == -1:
                return False
        elif mode == 5:     # 블럭에 매달리기
            character_index_x = int(self.X // 60)
            character_index_y = int((HEIGHT - (self.Y + move)) // 60)
            for index_x in range(character_index_x - 1, character_index_x + 2):
                for index_y in range(character_index_y - 2, character_index_y + 3):
                    if 0 <= index_x < map_size - 1 and 0 <= index_y < map_size - 1 and\
                            2 <= map_floor_array[index_y][index_x] <= 29 and\
                            not 2 <= map_floor_array[index_y - 1][index_x] <= 29 and\
                            not 2 <= map_floor_array[index_y + 1][character_index_x] <= 29 and\
                            abs(self.X - index_x * 60) <= 60 and HEIGHT - index_y * 60 + 15 <= self.Y + move <= HEIGHT - index_y * 60 + 25:
                        return False
        return True

    def attack_conflict_checking(self, monster):
        if abs(self.Y - monster.Y) < 40 and abs(self.X - monster.X) <= 90:
            return True
        return False

    def Jump(self):  # 점프키 입력시간에 비례하여 점프 높이 조절
        if self.Conflict_checking(1, self.JumpSpeed) and not self.Climb_state and not self.Hanging_state:
            if not self.Attack_state:
                self.MotionIndex = (self.MotionIndex + 0.1) % 16 % 8 + 16 * 9
            self.JumpSpeed -= self.Gravity
            if self.JumpSpeed > 0:
                self.Y += self.JumpSpeed
                if self.Y - self.camera_move_y >= HEIGHT - 200:
                    self.camera_move_y += self.JumpSpeed
        else:
            self.Jump_Key_State = False
            self.JumpSpeed = 15

    def Attack(self, monster):
        if self.MotionIndex % 16 < 5:
            self.Attack_state = True
            if self.whip.MotionIndex % 16 - 10 < 3:
                if self.DIRECTION == 0:
                    self.whip.X = self.X - 45
                    self.whip.Y = self.Y - 10
                elif self.DIRECTION == 1:
                    self.whip.X = self.X + 45
                    self.whip.Y = self.Y - 10
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
                    self.whip.Y = self.Y - 10
                elif self.DIRECTION == 1:
                    self.whip.X = self.X - 45
                    self.whip.Y = self.Y - 10
        else:
            if self.attack_conflict_checking(monster):
                monster.HP -= 1
            self.Attack_state = False
            self.Attack_key_state = False
            self.whip.MotionIndex = 16 * 12 + 10

    def Down_Jump(self):
        # self.MotionIndex = (self.MotionIndex + 0.1) % 16 % 8 + 16 * 9
        # self.JumpSpeed -= self.Gravity
        # if self.JumpSpeed > 0:
        #     self.Y -= self.JumpSpeed
        #     if self.Y <= 100:
        #         self.camera_move_y == self.JumpSpeed
        pass

    def gravity(self):
        if self.Conflict_checking(1, -self.DownSpeed) and not self.Climb_state:
            if self.Gravity_state and not self.Conflict_checking(5, -self.DownSpeed):
                # if self.MotionIndex <= 58:
                #     self.MotionIndex = (self.MotionIndex + 0.1) % 3 % 16 + 16 * 3 + 8
                # elif self.MotionIndex > 58:
                self.Hanging_state = True
                self.Can_Jump = True
                self.MotionIndex = 59
                self.JumpSpeed = 10
                self.DownSpeed = 0
                self.Down_Distance = 0
            else:
                if self.DownSpeed <= 20:
                    self.DownSpeed += self.Gravity
                self.Y = self.Y - self.DownSpeed
                self.Down_Distance += self.DownSpeed
                if self.Y - self.camera_move_y <= 200:
                    self.camera_move_y -= self.DownSpeed
                if not self.Attack_state and not self.Stun_state:
                    self.MotionIndex = (self.MotionIndex + 0.3) % 16 % 8 + 16 * 9
                self.Gravity_state = True
        else:
            if self.Down_Distance >= 600:
                self.HP -= 1
                self.MotionIndex = 9
                self.stun.MotionIndex = 16 * 13
                self.Stun_state = True
            self.Can_Jump = True
            self.JumpSpeed = 15
            self.DownSpeed = 0
            self.Down_Distance = 0
            self.Gravity_state = False
            self.Hanging_state = False

    def Stun(self):
        if self.stun.MotionIndex <= 16 * 13 + 10.9:
            self.stun.MotionIndex = (self.stun.MotionIndex + 0.2) % 11 + 16 * 13
        else:
            self.Stun_state = False

    def Motion(self, monster):
        if self.Stun_state:
            self.Stun()
        else:
            if self.Jump_Key_State:
                self.Jump()
            elif self.Down_Jump_state:
                self.Down_Jump()

            if self.Climb_state:
                if self.Climb_up_key_state and self.Conflict_checking(3, 2):
                    self.Y += 2
                    self.MotionIndex = (self.MotionIndex + 0.1) % 6 + 16 * 6
                elif self.Climb_down_key_state and self.Conflict_checking(3, -2):
                    self.Y -= 2
                    self.MotionIndex = (self.MotionIndex + 0.1) % 6 + 16 * 6
            else:
                if self.Action == 0:
                    if not self.Jump_Key_State and not self.Gravity_state and not self.Attack_state:
                        self.MotionIndex = 0
                elif self.Action == 1:
                    if self.shift_on == 0:
                        if self.X - self.camera_move_x <= WIDTH - 200:
                            if self.Conflict_checking(2, 3):
                                self.X += 3
                        elif self.X - self.camera_move_x > WIDTH - 200:
                            if self.Conflict_checking(2, 0):
                                self.X += 3
                                self.camera_move_x += 3

                        if not self.Jump_Key_State and not self.Attack_state:
                            self.MotionIndex = (self.MotionIndex + 0.1) % 8
                    else:
                        if self.Conflict_checking(2, 6):
                            if self.X - self.camera_move_x <= WIDTH - 200:
                                self.X += 6
                            elif self.X - self.camera_move_x > WIDTH - 200:
                                self.X += 6
                                self.camera_move_x += 6

                        if not self.Jump_Key_State and not self.Attack_state:
                            self.MotionIndex = (self.MotionIndex + 0.3) % 8

                elif self.Action == 2:
                    if self.MotionIndex < 18 and not self.Jump_Key_State and not self.Attack_state:
                        self.MotionIndex = (self.MotionIndex + 0.25) % 16 % 3 + 16

                elif self.Action == 3:
                    if self.shift_on == 0:
                        if self.Conflict_checking(2, -3):
                            if self.X - self.camera_move_x >= 200:
                                self.X -= 3
                            elif self.X - self.camera_move_x < 200:
                                self.X -= 3
                                self.camera_move_x -= 3

                        if not self.Jump_Key_State and not self.Attack_state:
                            self.MotionIndex = (self.MotionIndex + 0.1) % 8
                    else:
                        if self.Conflict_checking(2, -6):
                            if self.X - self.camera_move_x >= 200:
                                self.X -= 6
                            elif self.X - self.camera_move_x < 200:
                                self.X -= 6
                                self.camera_move_x -= 6
                        if not self.Jump_Key_State and not self.Attack_state:
                            self.MotionIndex = (self.MotionIndex + 0.3) % 8
                elif self.Action == 5:
                    self.MotionIndex = (self.MotionIndex + 0.3) % 16 % 6 + 16 * 5
                    if self.MotionIndex % 16 == 5:
                        pass

                if self.Attack_key_state:
                    for i in range(0, len(monster)):
                        self.Attack(monster[i])
                    self.whip.MotionIndex = (self.MotionIndex + 0.3) % 16 % 6 + 16 * 12 + 10
                    self.MotionIndex = (self.MotionIndex + 0.3) % 16 % 6 + 16 * 4

        self.gravity()

    def key_down(self):
        for event in self.handle:
            if event.type == SDL_QUIT:
                close_canvas()
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_UP:
                    if self.Conflict_checking(3, 0):
                        self.Climb_up_key_state = True
                        self.Climb_state = True
                        self.Can_Jump = True
                        self.JumpSpeed = 3
                        self.Jump_Key_State = False
                elif event.key == SDLK_RIGHT:
                    if self.Action != 2 and (not self.Climb_state or self.Jump_Key_State) and not self.Stun_state:
                        self.Action = 1
                        self.DIRECTION = 0
                elif event.key == SDLK_DOWN:
                    if self.Conflict_checking(3, 0) and self.Climb_state:
                        self.Climb_down_key_state = True
                        self.Can_Jump = True
                        self.JumpSpeed = 3
                        self.Jump_Key_State = False
                    else:
                        self.Action = 2
                elif event.key == SDLK_LEFT:
                    if self.Action != 2 and (not self.Climb_state or self.Jump_Key_State) and not self.Stun_state:
                        self.DIRECTION = 1
                        self.Action = 3
                elif event.key == SDLK_LALT:
                    if self.Action == 2 and not self.Jump_Key_State and self.Can_Jump:
                        self. Down_Jump_state = True
                    elif not self.Jump_Key_State and self.Can_Jump:
                        self.Jump_Key_State = True
                        self.Can_Jump = False
                        self.Hanging_state = False
                        if not self.Climb_down_key_state and not self.Climb_up_key_state:
                            self.Climb_state = False
                elif event.key == SDLK_LSHIFT:
                    self.shift_on = True
                elif event.key == SDLK_ESCAPE:
                    pass
                elif event.key == SDLK_LCTRL and not self.Attack_state and (not self.Climb_state or self.Jump_Key_State):
                    self.MotionIndex = 0
                    self.Attack_key_state = True
                    # 공격시 채찍 위치 오류 완화
                    if self.DIRECTION == 0:
                        self.whip.X = self.X - 45
                        self.whip.Y = self.Y - 10
                    elif self.DIRECTION == 1:
                        self.whip.X = self.X + 45
                        self.whip.Y = self.Y - 10
                elif event.key == SDLK_x:
                    if self.Conflict_checking(4, 0):
                        self.Action = 5
                        self.MotionIndex = 0
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_RIGHT and self.Action == 1 and (not self.Climb_state or self.Jump_Key_State):
                    self.Action = 0
                elif event.key == SDLK_DOWN and self.Action == 2 and (not self.Climb_state or self.Jump_Key_State):
                    self.Action = 0
                elif event.key == SDLK_DOWN:
                    self.Climb_down_key_state = False
                elif event.key == SDLK_LEFT and self.Action == 3 and (not self.Climb_state or self.Jump_Key_State):
                    self.Action = 0
                elif event.key == SDLK_LALT and (self.Jump_Key_State or self.Down_Jump_state):
                    self.Jump_Key_State = False
                    self.Down_Jump_state = False
                    self.JumpSpeed = 15
                    self.Climb_up_key_state = False
                    self.Climb_down_key_state = False
                elif event.key == SDLK_LSHIFT:
                    self.shift_on = False
                elif event.key == SDLK_UP:
                    self.Climb_up_key_state = False

    def draw(self):
        self.grid_image.clip_draw(int(self.MotionIndex) % 16 * 128,
                                  1918 - 128 * (int(self.MotionIndex) // 16) + 50,
                                  128, 128, self.X - self.camera_move_x,
                                  self.Y - self.camera_move_y,
                                  50, 60)
        if self.Stun_state and self.MotionIndex == 9:
            self.image.clip_draw(int(self.stun.MotionIndex) % 16 * 128,
                              1918 - 128 * (int(self.stun.MotionIndex) // 16),
                              128, 128, self.X - self.camera_move_x,
                              self.Y - self.camera_move_y + 10, 60, 60)
        if self.DIRECTION == 0:
            if self.Attack_state:
                self.image.clip_draw(int(self.whip.MotionIndex) % 16 * 128,
                                      1918 - 128 * (int(self.whip.MotionIndex) // 16),
                                      128, 128, self.whip.X - self.camera_move_x,
                                      self.whip.Y - self.camera_move_y, 60, 60)
            self.image.clip_draw(int(self.MotionIndex) % 16 * 128,
                                  1918 - 128 * (int(self.MotionIndex) // 16),
                                  128, 128, self.X - self.camera_move_x,
                                  self.Y - self.camera_move_y,
                                  60, 60)
        elif self.DIRECTION == 1:
            if self.Attack_state:
                self.image.clip_composite_draw(int(self.whip.MotionIndex) % 16 * 128,
                                      1918 - 128 * (int(self.whip.MotionIndex) // 16),
                                      128, 128, 0, 'h', self.whip.X - self.camera_move_x,
                                      self.whip.Y - self.camera_move_y, 60, 60)
            self.image.clip_composite_draw(int(self.MotionIndex) % 16 * 128,
                                  1918 - 128 * (int(self.MotionIndex) // 16),
                                  128, 128, 0, 'h', self.X - self.camera_move_x,
                                  self.Y - self.camera_move_y,
                                  60, 60)

    def draw_UI(self, UI, UI_count):
        UI.clip_draw(0, 512 - 250, 60, 59, 30, HEIGHT - 30, 40, 40)                 # 생명
        UI_count.clip_draw(64 * (self.HP % 4), 320 - 64 * (self.HP // 4 + 1), 64, 64, 35, HEIGHT - 35, 30, 30)
        UI.clip_draw(140, 512 - 125, 40, 40, 90, HEIGHT - 35, 30, 30)               # 폭탄
        UI.clip_draw(200, 512 - 125, 40, 40, 140, HEIGHT - 35, 30, 30)              # 로프
        UI.clip_draw(270, 512 - 115, 30, 40, WIDTH - 300, HEIGHT - 30, 30, 40)      # 돈
