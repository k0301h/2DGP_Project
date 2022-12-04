from map_floor import *
from pico2d import *
import game_framework
import time
from itemclass import *

class SUB():
    MotionIndex = 0
    X = 400
    Y = 400

PIXEL_PER_METER = (10 / 0.5)

RUN_SPEED_KMPH = 45.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

WALK_SPEED_KMPH = 25.0
WALK_SPEED_MPM = (WALK_SPEED_KMPH * 1000.0 / 60.0)
WALK_SPEED_MPS = (WALK_SPEED_MPM / 60.0)
WALK_SPEED_PPS = (WALK_SPEED_MPS * PIXEL_PER_METER)

# if mode == 1:
#     GRAVITY_ASPEED_KMPH = 1.2  # 1.2
# elif mode == 2:
#     GRAVITY_ASPEED_KMPH = 2.3      # 2.3
GRAVITY_ASPEED_KMPH = 2.0
GRAVITY_ASPEED_MPM = (GRAVITY_ASPEED_KMPH * 1000.0 / 60.0)
GRAVITY_ASPEED_MPS = (GRAVITY_ASPEED_MPM / 60.0)
GRAVITY_ASPEED_PPS = (GRAVITY_ASPEED_MPS * PIXEL_PER_METER)

# if mode == 1:
#     JUMP_SPEED_KMPH = 120.0  # 120
# elif mode == 2:
#     JUMP_SPEED_KMPH = 100.0     # 100
JUMP_SPEED_KMPH = 70.0
JUMP_SPEED_MPM = (JUMP_SPEED_KMPH * 1000.0 / 60.0)
JUMP_SPEED_MPS = (JUMP_SPEED_MPM / 60.0)
JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class CHARACTER():
    HP = 1
    ATK = 1
    Action = 0
    MotionIndex = 0
    X = 400
    Y = 400
    DIRECTION = 0
    # BombCount = 4
    # RopeCount = 4
    # Money = 0

    type = 'Anna'

    mode = 0
    itemmode = 0 # 0 : 맨손 1 : 샷건
    handle_item = shotgun()
    reload = True

    Gravity = None
    JumpSpeed = None
    JUMP_Distance = 0
    DownSpeed = 0
    Down_Distance = 0

    run_move_speed = None
    walk_move_speed = None

    timer = 0
    effect = False
    scale = 40 # 40

    camera_move_x = 0
    camera_move_y = 0

    hit_state = False
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
    Hanging_jump = False
    enter_walking = True
    jump_landing = True
    image = None
    grid_image = None

    jump_sound = None
    landing_sound = None
    whip_sound = None
    hit_sound = None
    stun_sound = None

    whip = SUB()
    stun = SUB()

    def __init__(self):
        if CHARACTER.grid_image == None:
            CHARACTER.grid_image = load_image('./Textures/Entities/char_yellow_full_grid.png')
        self.jump_sound = load_wav('./sound/player_jump.wav')
        self.landing_sound = load_wav('./sound/Landing.wav')
        self.whip_sound = load_wav('./sound/whip.wav')
        self.hit_sound = load_wav('./sound/damage.wav')
        self.stun_sound = load_wav('./sound/stun.wav')
        self.landing_sound.set_volume(30)
        self.stun_sound.set_volume(30)

    def Place(self):
        if CHARACTER.image == None:
            if self.type == 'Anna':
                CHARACTER.image = load_image('./Textures/char_yellow.png')
            elif self.type == 'spelunky':
                CHARACTER.image = load_image('./Textures/guy_spelunky.png')
        for index_x in range(0, map_size):
            for index_y in range(0, map_size):
                if map_floor_array[index_y][index_x] == 1:
                    self.X = index_x * 60
                    self.Y = HEIGHT - index_y * 60 - 59
                    self.enter_walking = True
                    self.camera_move_x = 0
                    self.camera_move_y = 0
                    if self.X > WIDTH - 200:
                        self.camera_move_x = self.X - WIDTH / 2
                    if self.Y < 200:
                        self.camera_move_y = self.Y - HEIGHT / 2
                    self.scale =40
                    self.JUMP_Distance = 0

    def Conflict_checking(self, mode, move): # mode : 충돌체크 유형 , move : 다음에 움직일 크기
        if mode == 1:       # Y충돌 체크
            character_index_x = int(self.X // 60)
            character_index_y = int((HEIGHT - (self.Y + move)) // 60)
            for index_x in range(character_index_x - 1, character_index_x + 2):
                for index_y in range(character_index_y - 2, character_index_y + 3):
                    if 0 <= index_x < map_size and 0 <= index_y < map_size and \
                            (2 <= map_floor_array[index_y][index_x] <= 29 or 40 <= map_floor_array[index_y][index_x] <= 41) and\
                            abs(self.X - index_x * 60) <= 55 and abs(self.Y + move - (HEIGHT - index_y * 60)) <= 58:
                        return False
        elif mode == 2:     # X충돌 체크
            character_index_x = int((self.X + move) // 60)
            character_index_y = int((HEIGHT - self.Y) // 60)
            for index_y in range(character_index_y - 1, character_index_y + 2):
                for index_x in range(character_index_x - 2, character_index_x + 3):
                    if 0 <= index_x < map_size and 0 <= index_y < map_size and\
                            (2 <= map_floor_array[index_y][index_x] <= 29 or 40 <= map_floor_array[index_y][index_x] <= 41) and \
                            abs(self.Y - (HEIGHT - index_y * 60)) < 58 and abs(self.X + move - index_x * 60) <= 55:
                        return False
        elif mode == 3:     # 사다리 체크
            character_index_x = int(self.X // 60)
            character_index_y = int((HEIGHT - (self.Y + move)) // 60)
            if not 30 <= map_floor_array[character_index_y][character_index_x] <= 35 and\
                not 30 <= map_floor_array[character_index_y][character_index_x + 1] <= 35:
                return False
            if 30 <= map_floor_array[character_index_y][character_index_x] <= 35 and\
                self.X - character_index_x * 60 > 20:
                return False
            if 30 <= map_floor_array[character_index_y][character_index_x + 1] <= 35 and\
                (character_index_x + 1) * 60 - self.X > 20:
                return False

            # if not 30 <= map_floor_array[character_index_y][character_index_x] <= 35 and\
            #         self.X - character_index_x * 60 < 20:
            #     return False
            # elif not 30 <= map_floor_array[character_index_y][character_index_x + 1] <= 35 and \
            #         (character_index_x + 1) * 60 - self.X < 20:
            #     return False
            elif 30 <= map_floor_array[character_index_y][character_index_x] <= 35 and not self.Climb_state:
                self.X = character_index_x * 60
            elif 30 <= map_floor_array[character_index_y][character_index_x + 1] <= 35 and not self.Climb_state:
                self.X = (character_index_x + 1) * 60
        elif mode == 4:     # 출구 체크
            character_index_x = int(self.X // 60)
            character_index_y = int((HEIGHT - self.Y) // 60)
            if map_floor_array[character_index_y - 1][character_index_x] == -1:
                return True
            if not map_floor_array[character_index_y][character_index_x] == -1:
                return False
        elif mode == 5:     # 블럭에 매달리기
            character_index_x = int((self.X + 30) // 60)
            character_index_y = int((HEIGHT - (self.Y + move)) // 60)
            for index_x in range(character_index_x - 2, character_index_x + 2):
                for index_y in range(character_index_y - 1, character_index_y + 2):
                    if self.DIRECTION == 0:
                        if 0 <= index_x < map_size - 1 and 0 <= index_y < map_size - 1 and \
                                (2 <= map_floor_array[index_y][index_x] <= 29 or 40 <= map_floor_array[index_y][
                                    index_x] <= 41) and\
                                not (2 <= map_floor_array[index_y - 1][index_x] <= 29 or 40 <= map_floor_array[index_y - 1][index_x] <= 41)  and\
                                not (2 <= map_floor_array[index_y + 1][character_index_x] <= 29 or 40 <= map_floor_array[index_y + 1][character_index_x] <= 41) and\
                                0 < index_x * 60 - self.X <= 60 and HEIGHT - index_y * 60 + 15 <= self.Y + move <= HEIGHT - index_y * 60 + 25:
                            return False
                    elif self.DIRECTION == 1:
                        if 0 <= index_x < map_size - 1 and 0 <= index_y < map_size - 1 and \
                                (2 <= map_floor_array[index_y][index_x] <= 29 or 40 <= map_floor_array[index_y][index_x] <= 41) and \
                                not (2 <= map_floor_array[index_y - 1][index_x] <= 29 or 40 <= map_floor_array[index_y - 1][index_x] <= 41) and \
                                not (2 <= map_floor_array[index_y + 1][character_index_x] <= 29 or 40 <= map_floor_array[index_y + 1][character_index_x] <= 41)and \
                                0 < self.X - index_x * 60 <= 60 and HEIGHT - index_y * 60 + 15 <= self.Y + move <= HEIGHT - index_y * 60 + 25:
                            return False

        elif mode == 6:     # 뼈 장애물(위에서 아래로 적용)
            character_index_x = int((self.X + 30) // 60)
            character_index_y = int((HEIGHT - (self.Y + move)) // 60)
            if 36 <= map_floor_array[character_index_y + 1][character_index_x] <= 38 or \
                36 <= map_floor_array[character_index_y][character_index_x] <= 38:
                return False
        elif mode == 7:
            character_index_x = int(self.X // 60)
            character_index_y = int((HEIGHT - self.Y) // 60)

            for index_x in range(character_index_x - 1, character_index_x + 2):
                for index_y in range(character_index_y - 1, character_index_y + 2):
                    if 2 <= map_floor_array[index_y][index_x] <= 29 and \
                        index_x * 60 - 30 <= self.X <= index_x * 60 + 30 and\
                        HEIGHT - (index_y * 60) + 58 <= self.Y <= HEIGHT - (index_y * 60) + 65:
                        return False
        return True

    def attack_conflict_checking(self, monster):
        if abs(self.Y - monster.Y) < 40 and abs(self.X - monster.X) <= 90:
            return True
        return False

    def Jump(self):  # 점프키 입력시간에 비례하여 점프 높이 조절
        # 원본
        # grav = clamp(0, self.DownSpeed, JUMP_SPEED_PPS * game_framework.frame_time)
        # if self.Hanging_jump:
        #     self.JumpSpeed = (JUMP_SPEED_PPS * game_framework.frame_time - grav) * 2 / 3
        # else:
        #     self.JumpSpeed = JUMP_SPEED_PPS * game_framework.frame_time - grav
        # # print(JUMP_SPEED_PPS, game_framework.frame_time, self.JumpSpeed, self.Hanging_jump)
        # if self.JumpSpeed > 0 and self.Conflict_checking(1, self.JumpSpeed) and not self.Climb_state and not self.Hanging_state:
        #     self.Gravity = GRAVITY_ASPEED_PPS * game_framework.frame_time
        #     if not self.Attack_state:
        #         self.MotionIndex = (self.MotionIndex + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 16 % 8 + 16 * 9
        #     if self.JumpSpeed > 0:
        #         if self.Conflict_checking(1, self.JumpSpeed):
        #             self.Y += self.JumpSpeed
        #         if self.Y - self.camera_move_y >= HEIGHT - 200:
        #             self.camera_move_y += self.JumpSpeed
        # 점프 크기 똑같이 하고 올라가는 높이 측정 ==> 최대 높이로 올라가면 점프키 비활성화
        # print(self.JumpSpeed, self.JUMP_Distance, self.Y)
        if self.Hanging_jump:
            self.JumpSpeed = (JUMP_SPEED_PPS * game_framework.frame_time) * 2 / 3
            self.JUMP_Distance += self.JumpSpeed
        else:
            self.JumpSpeed = JUMP_SPEED_PPS * game_framework.frame_time
        if self.JUMP_Distance < 90 and self.Conflict_checking(1, self.JumpSpeed) and not self.Climb_state and not self.Hanging_state:
            if not self.Attack_state:
                self.MotionIndex = (self.MotionIndex + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 16 % 8 + 16 * 9
            if self.Conflict_checking(1, self.JumpSpeed):
                self.Y += self.JumpSpeed
                self.JUMP_Distance += self.JumpSpeed
                if self.Y - self.camera_move_y >= HEIGHT - 200:
                    self.camera_move_y += self.JumpSpeed
        else:
            self.Jump_Key_State = False
            self.JUMP_Distance = 0
            self.JumpSpeed = JUMP_SPEED_PPS * game_framework.frame_time

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
                monster.hit_sound.play()
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
            self.Gravity = GRAVITY_ASPEED_PPS * game_framework.frame_time
            if self.Gravity_state and not self.Conflict_checking(5, -self.DownSpeed) and not self.Jump_Key_State:
                # if self.MotionIndex <= 58:
                #     self.MotionIndex = (self.MotionIndex + 0.1) % 3 % 16 + 16 * 3 + 8
                # elif self.MotionIndex > 58:
                self.Hanging_state = True
                self.Hanging_jump = True
                self.Can_Jump = True
                self.jump_landing = True
                self.MotionIndex = 59
                self.DownSpeed = 0
                self.Down_Distance = 0
            elif not self.Conflict_checking(6, -self.DownSpeed):
                self.Stun_state = True
                self.HP = 0
                self.MotionIndex = 9
                if self.timer <= 3:
                    self.Y -= self.Gravity * 3
                    self.timer += game_framework.frame_time
            else:
                if self.DownSpeed <= 10:
                    self.DownSpeed += self.Gravity
                if self.Conflict_checking(1, -self.DownSpeed):
                    self.Y -= self.DownSpeed
                    self.Down_Distance += self.DownSpeed
                if self.Y - self.camera_move_y <= 200:
                    self.camera_move_y -= self.DownSpeed
                if not self.Attack_state and not self.Stun_state and self.DownSpeed > 1:
                    self.MotionIndex = (self.MotionIndex + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 16 % 8 + 16 * 9
                self.Gravity_state = True
        else:
            if self.Down_Distance >= 600:
                if self.mode:
                    self.HP -= 1
                self.MotionIndex = 9
                self.stun.MotionIndex = 16 * 13
                self.Stun_state = True
            self.JumpSpeed = JUMP_SPEED_PPS * game_framework.frame_time
            self.JUMP_Distance = 0
            self.DownSpeed = self.Gravity
            self.Down_Distance = 0
            self.Gravity_state = False
            self.Hanging_jump = False
            if not self.Conflict_checking(7,0) and not self.jump_landing:
                self.jump_landing = True
                self.landing_sound.play()
            self.Can_Jump = True

    def Stun(self):
        self.stun_sound.play()
        self.stun.MotionIndex = (self.stun.MotionIndex + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)) % 16 % 11 + 16 * 13
        self.timer += game_framework.frame_time
        if self.timer >= 2:
            self.Stun_state = False
            self.timer = 0

    def Motion(self, monster):
        if self.enter_walking:
            self.timer += game_framework.frame_time
            self.scale -= 0.5
            self.scale = clamp(0, self.scale, 60)
            self.MotionIndex = (self.MotionIndex + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) / 2) % 16 % 6 + 16 * 5 + 6
            if self.timer >= 1:
                self.timer = 0
                self.enter_walking = False
        elif self.Stun_state:
            if self.HP > 0: # 가시 장애물에 안걸렸을 때
                self.Stun()
            else:
                self.MotionIndex = 9
                self.Stun_state = False
        else:
            if self.HP <= 0:
                self.Stun_state = True
            else:
                if self.Jump_Key_State:
                    self.Jump()
                # elif self.Down_Jump_state:
                #     self.Down_Jump()

                if self.Climb_state:
                    self.walk_move_speed = WALK_SPEED_PPS * game_framework.frame_time
                    self.Can_Jump = True
                    self.jump_landing = True
                    self.Jump_Key_State = False
                    self.Action = 0
                    if self.Climb_up_key_state and self.Conflict_checking(3, self.walk_move_speed):
                        self.Y += self.walk_move_speed
                        if self.Y - self.camera_move_y >= HEIGHT - 200:
                            self.camera_move_y += self.walk_move_speed
                        self.MotionIndex = (self.MotionIndex + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) / 2) % 6 + 16 * 6
                    elif self.Climb_down_key_state and self.Conflict_checking(3, -self.walk_move_speed):
                        self.Y -= self.walk_move_speed
                        if self.Y - self.camera_move_y <= 200:
                            self.camera_move_y -= self.walk_move_speed
                        self.MotionIndex = (self.MotionIndex + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) / 2) % 6 + 16 * 6
                else:
                    if self.Action == 0:
                        if not self.Jump_Key_State and not self.Gravity_state and not self.Attack_state:
                            if self.itemmode == 0:
                                self.MotionIndex = 0
                            elif self.itemmode == 1:
                                self.MotionIndex = 11 + 16 * 2
                    elif self.Action == 1:
                        self.run_move_speed = RUN_SPEED_PPS * game_framework.frame_time
                        self.walk_move_speed = WALK_SPEED_PPS * game_framework.frame_time
                        if self.shift_on == 0:
                            if self.X - self.camera_move_x <= WIDTH - 200:
                                if self.Conflict_checking(2, self.walk_move_speed):
                                    self.X += self.walk_move_speed
                            elif self.X - self.camera_move_x > WIDTH - 200:
                                if self.Conflict_checking(2, 0):
                                    self.X += self.walk_move_speed
                                    self.camera_move_x += self.walk_move_speed

                            if not self.Jump_Key_State and not self.Attack_state:
                                self.MotionIndex = (self.MotionIndex + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) / 2) % 8
                        else:
                            if self.Conflict_checking(2, self.run_move_speed):
                                if self.X - self.camera_move_x <= WIDTH - 200:
                                    self.X += self.run_move_speed
                                elif self.X - self.camera_move_x > WIDTH - 200:
                                    self.X += self.run_move_speed
                                    self.camera_move_x += self.run_move_speed

                            if not self.Jump_Key_State and not self.Attack_state:
                                self.MotionIndex = (self.MotionIndex + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)) % 8

                    elif self.Action == 2:
                        if self.MotionIndex < 18 and not self.Jump_Key_State and not self.Attack_state:
                            self.MotionIndex = (self.MotionIndex + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) * 2) % 16 % 3 + 16

                    elif self.Action == 3:
                        self.run_move_speed = RUN_SPEED_PPS * game_framework.frame_time
                        self.walk_move_speed = WALK_SPEED_PPS * game_framework.frame_time
                        if self.shift_on == 0:
                            if self.Conflict_checking(2, -self.walk_move_speed):
                                if self.X - self.camera_move_x >= 200:
                                    self.X -= self.walk_move_speed
                                elif self.X - self.camera_move_x < 200:
                                    self.X -= self.walk_move_speed
                                    self.camera_move_x -= self.walk_move_speed

                            if not self.Jump_Key_State and not self.Attack_state:
                                self.MotionIndex = (self.MotionIndex + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) / 2) % 8
                        else:
                            if self.Conflict_checking(2, -self.run_move_speed):
                                if self.X - self.camera_move_x >= 200:
                                    self.X -= self.run_move_speed
                                elif self.X - self.camera_move_x < 200:
                                    self.X -= self.run_move_speed
                                    self.camera_move_x -= self.run_move_speed
                            if not self.Jump_Key_State and not self.Attack_state:
                                self.MotionIndex = (self.MotionIndex + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)) % 8
                    elif self.Action == 5:
                        self.MotionIndex = (self.MotionIndex + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)) % 16 % 6 + 16 * 5
                        self.scale += 0.5
                        self.scale = clamp(0, self.scale, 60)

                    if self.Attack_key_state:
                        if self.itemmode == 0:      # 맨손 채찍 공격
                            for m in monster:
                                self.Attack(m)
                            self.whip.MotionIndex = (self.MotionIndex + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)) % 16 % 6 + 16 * 12 + 10
                            self.MotionIndex = (self.MotionIndex + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)) % 16 % 6 + 16 * 4
                        elif self.itemmode == 1:    # 샷건 공격
                            for i in range(3):
                                self.handle_item.bullet_object[i].move()
                                self.handle_item.update(self)

                                for m in monster:
                                    for i in range(3):
                                        self.handle_item.bullet_object[i].Conflict_check(2, 0, m)
                if self.hit_state:
                    if self.timer < 4:
                        self.timer += game_framework.frame_time
                        if 0.0 <= self.timer % 0.1 <= 0.01:
                            if self.effect:
                                self.effect = False
                            else:
                                self.effect = True
                    else:
                        self.timer = 0
                        self.hit_state = False
                        self.effect = False
        if not self.Jump_Key_State:
            self.gravity()

    def key_down(self):
        global ROUND
        for event in self.handle:
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_UP:
                    if self.Conflict_checking(3, 0) and not self.Action == 5:
                        self.Climb_up_key_state = True
                        self.Climb_state = True
                        self.Can_Jump = True
                        self.jump_landing = True
                        self.Jump_Key_State = False
                        self.Action = 0
                elif event.key == SDLK_RIGHT:
                    if self.Action != 2 and (not self.Climb_state or self.Jump_Key_State) and not self.Stun_state and not self.Action == 5:
                        self.Action = 1
                        if self.HP > 0:
                            self.DIRECTION = 0
                elif event.key == SDLK_DOWN:
                    if self.Conflict_checking(3, 0) and self.Climb_state and not self.Action == 5:
                        self.Climb_down_key_state = True
                        self.Can_Jump = True
                        self.JumpSpeed = 3
                        self.Jump_Key_State = False
                    elif not self.Action == 5:
                        self.Action = 2
                elif event.key == SDLK_LEFT:
                    if self.Action != 2 and not self.Action == 5 and (not self.Climb_state or self.Jump_Key_State) and not self.Stun_state:
                        if self.HP > 0:
                            self.DIRECTION = 1
                        self.Action = 3
                elif event.key == SDLK_LALT:
                    if self.Action == 2 and not self.Jump_Key_State and self.Can_Jump and not self.Action == 5:
                        self. Down_Jump_state = True
                    elif not self.Jump_Key_State and self.Can_Jump and self.jump_landing and not self.Action == 5:
                        if not self.Jump_Key_State:
                            self.Jump_Key_State = True
                        self.jump_sound.play()
                        self.Can_Jump = False
                        self.jump_landing = False
                        self.Hanging_state = False
                        if not self.Climb_down_key_state and not self.Climb_up_key_state:
                            self.Climb_state = False
                elif event.key == SDLK_LSHIFT:
                    self.shift_on = True
                elif event.key == SDLK_b:
                    if self.itemmode:
                        self.itemmode = 0
                    else:
                        self.itemmode = 1
                elif event.key == SDLK_m:
                    if self.mode:
                        self.mode = 0
                    else: 
                        self.mode= 1
                    pass
                elif event.key == SDLK_LCTRL and not self.Attack_state and (not self.Climb_state or self.Jump_Key_State) and not self.Action == 5 and not self.Hanging_state:
                    self.Attack_key_state = True
                    if not self.itemmode:
                        self.whip_sound.play()
                        self.MotionIndex = 0
                        # 공격시 채찍 위치 오류 완화
                        if self.DIRECTION == 0:
                            self.whip.X = self.X - 45
                            self.whip.Y = self.Y - 10
                        elif self.DIRECTION == 1:
                            self.whip.X = self.X + 45
                            self.whip.Y = self.Y - 10
                    elif self.reload:
                        self.handle_item.sound.play()
                        self.reload = False
                        for i in range(3):
                            self.handle_item.bullet_object[i].Place(self, i)
                elif event.key == SDLK_x:
                    if self.Conflict_checking(4, 0):
                        self.Action = 5
                        self.itemmode = 0
                        self.MotionIndex = 0
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_RIGHT and self.Action == 1 and (not self.Climb_state or self.Jump_Key_State) and not self.Action == 5:
                    self.Action = 0
                elif event.key == SDLK_DOWN and self.Action == 2 and (not self.Climb_state or self.Jump_Key_State) and not self.Action == 5:
                    self.Action = 0
                elif event.key == SDLK_DOWN and not self.Action == 5:
                    self.Climb_down_key_state = False
                elif event.key == SDLK_LEFT and self.Action == 3 and (not self.Climb_state or self.Jump_Key_State) and not self.Action == 5:
                    self.Action = 0
                elif event.key == SDLK_LALT and not self.Action == 5:
                    self.Jump_Key_State = False
                    self.Down_Jump_state = False
                    self.Can_Jump = True
                    # self.Climb_up_key_state = False
                    # self.Climb_down_key_state = False
                elif event.key == SDLK_LSHIFT:
                    self.shift_on = False
                elif event.key == SDLK_UP:
                    self.Climb_up_key_state = False

    def game_clear_motion(self):
        if self.timer < 1.6:
            self.DIRECTION = 0
            self.Action = 1
            self.timer += game_framework.frame_time / 2
        else:
            if self.MotionIndex % 16 < 8:
                self.MotionIndex = 16 * 9 + 8
            self.MotionIndex = (self.MotionIndex + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)) % 16 % 11 + 16 * 9

    def clear_motion(self):
        if self.timer < 1.6:
            self.DIRECTION = 0
            self.Action = 1
            self.timer += game_framework.frame_time / 2
        else:
            self.MotionIndex = (self.MotionIndex + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)) % 16 % 7 + 16 * 3


    def draw(self):
        if self.hit_state and self.effect:
            # self.grid_image.clip_draw(8 * 128,
            #                           1918 - 128 * 14,
            #                           128, 128, self.X - self.camera_move_x,
            #                           self.Y - self.camera_move_y,
            #                           50, 60)
            if self.Stun_state and self.MotionIndex == 9 and self.HP > 0:
                self.image.clip_draw(8 * 128, 1918 - 128 * 14,
                                     128, 128, self.X - self.camera_move_x,
                                     self.Y - self.camera_move_y + 10, 60, 60)
            if self.DIRECTION == 0:
                if self.Attack_state:
                    self.image.clip_draw(8 * 128, 1918 - 128 * 14,
                                         128, 128, self.whip.X - self.camera_move_x,
                                         self.whip.Y - self.camera_move_y, 60, 60)
                self.image.clip_draw(8 * 128, 1918 - 128 * 14,
                                     128, 128, self.X - self.camera_move_x,
                                     self.Y - self.camera_move_y - self.scale / 2,
                                     60 - self.scale, 60 - self.scale)
            elif self.DIRECTION == 1:
                if self.Attack_state:
                    self.image.clip_composite_draw(8 * 128, 1918 - 128 * 14,
                                                   128, 128, 0, 'h', self.whip.X - self.camera_move_x,
                                                   self.whip.Y - self.camera_move_y, 60, 60)
                self.image.clip_composite_draw(8 * 128, 1918 - 128 * 14,
                                               128, 128, 0, 'h', self.X - self.camera_move_x,
                                               self.Y - self.camera_move_y - self.scale / 2,
                                               60 - self.scale, 60 - self.scale)
        else:
            # self.grid_image.clip_draw(int(self.MotionIndex) % 16 * 128,
            #                           1918 - 128 * (int(self.MotionIndex) // 16) + 50,
            #                           128, 128, self.X - self.camera_move_x,
            #                           self.Y - self.camera_move_y,
            #                           50, 60)
            if self.Stun_state and self.MotionIndex == 9 and self.HP > 0:
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
                                      self.Y - self.camera_move_y - self.scale / 2,
                                      60 - self.scale, 60 - self.scale)
            elif self.DIRECTION == 1:
                if self.Attack_state:
                    self.image.clip_composite_draw(int(self.whip.MotionIndex) % 16 * 128,
                                          1918 - 128 * (int(self.whip.MotionIndex) // 16),
                                          128, 128, 0, 'h', self.whip.X - self.camera_move_x,
                                          self.whip.Y - self.camera_move_y, 60, 60)
                self.image.clip_composite_draw(int(self.MotionIndex) % 16 * 128,
                                      1918 - 128 * (int(self.MotionIndex) // 16),
                                      128, 128, 0, 'h', self.X - self.camera_move_x,
                                               self.Y - self.camera_move_y - self.scale / 2,
                                               60 - self.scale, 60 - self.scale)
        if self.itemmode:
            self.handle_item.draw(self)
        if self.Attack_key_state:
            for i in range(3):
                self.handle_item.bullet_object[i].draw(self)

    def draw_UI(self, UI, UI_count):
        UI.clip_draw(0, 512 - 250, 60, 59, 30, HEIGHT - 30, 40, 40)                 # 생명
        UI_count.clip_draw(64 * (self.HP % 4), 320 - 64 * (self.HP // 4 + 1), 64, 64, 35, HEIGHT - 35, 30, 30)
        # UI.clip_draw(140, 512 - 125, 40, 40, 90, HEIGHT - 35, 30, 30)               # 폭탄
        # UI.clip_draw(200, 512 - 125, 40, 40, 140, HEIGHT - 35, 30, 30)              # 로프
        # UI.clip_draw(270, 512 - 115, 30, 40, WIDTH - 300, HEIGHT - 30, 30, 40)      # 돈
