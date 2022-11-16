from characterclass import *
import random
import math

PIXEL_PER_METER = (10 / 0.5)

WALK_SPEED_KMPH = 20.0
WALK_SPEED_MPM = (WALK_SPEED_KMPH * 1000.0 / 60.0)
WALK_SPEED_MPS = (WALK_SPEED_MPM / 60.0)
WALK_SPEED_PPS = (WALK_SPEED_MPS * PIXEL_PER_METER)

GRAVITY_ASPEED_KMPH = 2.5
GRAVITY_ASPEED_MPM = (GRAVITY_ASPEED_KMPH * 1000.0 / 60.0)
GRAVITY_ASPEED_MPS = (GRAVITY_ASPEED_MPM / 60.0)
GRAVITY_ASPEED_PPS = (GRAVITY_ASPEED_MPS * PIXEL_PER_METER)

JUMP_SPEED_KMPH = 90.0
JUMP_SPEED_MPM = (JUMP_SPEED_KMPH * 1000.0 / 60.0)
JUMP_SPEED_MPS = (JUMP_SPEED_MPM / 60.0)
JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

# monster gravity 시간 적용 필요

class Snake():
    HP = 2
    ATK = 1
    Action = 0
    MotionIndex = 0
    X = 400
    Y = 400
    DIRECTION = 0

    Gravity = 0.5
    DownSpeed = 0
    Image = None
    rImage = None
    grid_image = None

    Gravity_state = False
    Attack_state = False

    def __init__(self):
        if Snake.Image == None:
            Snake.Image = load_image('./Textures/Entities/Monsters/snake.png')
        if Snake.rImage == None:
            Snake.rImage = load_image('./Textures/Entities/Monsters/snake_reverse.png')
        if Snake.grid_image == None:
           Snake.grid_image = load_image('./Textures/Entities/Monsters/snake_grid.png')

    def Place(self, index_x, index_y):
        self.X, self.Y = index_x * 60, HEIGHT - index_y * 60
        self.DIRECTION = random.randint(0, 1)
        self.HP = 2
        self.ATK = 1
        self.Action = 0
        self.MotionIndex = 0

    def Conflict_checking(self, mode, move):  # mode : x,y충돌 검사 , move : 다음에 움직일 크기
        if mode == 1:  # Y충돌 체크
            character_index_x = int(self.X // 60)
            character_index_y = int((HEIGHT - (self.Y + move)) // 60)
            for index_x in range(character_index_x - 1, character_index_x + 2):
                for index_y in range(character_index_y - 2, character_index_y + 3):
                    if 0 <= index_x < map_size and 0 <= index_y < map_size and \
                            2 <= map_floor_array[index_y][index_x] <= 29 and \
                            abs(self.X - index_x * 60) <= 55 and abs(self.Y + move - (HEIGHT - index_y * 60)) <= 58:
                        return False

        elif mode == 2:  # X충돌 체크
            character_index_x = int((self.X + move) // 60)
            character_index_y = int((HEIGHT - self.Y) // 60)
            for index_y in range(character_index_y - 1, character_index_y + 2):
                for index_x in range(character_index_x - 2, character_index_x + 3):
                    if 0 <= index_x < map_size and 0 <= index_y < map_size\
                        and character_index_y + 1 < map_size and character_index_x + 1 < map_size and\
                            2 <= map_floor_array[index_y][index_x] <= 29 and \
                            (abs(self.Y - (HEIGHT - index_y * 60)) < 58 and abs(self.X + move - index_x * 60) <= 55)\
                            or not 2 <= map_floor_array[character_index_y + 1][character_index_x + 1] <= 29\
                            or not 2 <= map_floor_array[character_index_y + 1][character_index_x] <= 29:
                        if self.DIRECTION:
                            self.DIRECTION = 0
                        else:
                            self.DIRECTION = 1
        elif mode == 3:  # 캐릭터 여기서 move는 캐릭터의 위치
            if math.sqrt((self.X - move.X) ** 2 + (self.Y - move.Y) ** 2) <= 80:
                self.Action = 1
                self.MotionIndex = 4
                if self.X > move.X:
                    self.DIRECTION = 1
                elif self.X < move.X:
                    self.DIRECTION = 0
        return True

    def attack(self, character):
        if self.MotionIndex < 11.9:
            if  math.sqrt((self.X - character.X) ** 2 + (self.Y - character.Y) ** 2) < 60:
                # character.Stun_state = True
                if character.mode:
                    character.HP -= self.ATK
        else:
            self.Action = 0

    def gravity(self):
        if self.Conflict_checking(1, -self.DownSpeed):
            if self.DownSpeed <= 10:
                self.DownSpeed += self.Gravity
            self.Y = self.Y - self.DownSpeed
            self.Gravity_state = True
        else:
            self.DownSpeed = 0
            self.Gravity_state = False

    def Motion(self, character):
        self.run_move_speed = RUN_SPEED_PPS * game_framework.frame_time
        if self.Action == 0:
            self.MotionIndex = (self.MotionIndex + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) / 2) % 4
            self.Conflict_checking(3, character)
            if self.Conflict_checking(2, self.run_move_speed / 2) and self.DIRECTION == 0:
                self.X += self.run_move_speed / 2
            elif self.Conflict_checking(2, -self.run_move_speed / 2) and self.DIRECTION == 1:
                self.X -= self.run_move_speed / 2
        elif self.Action == 1:
            self.attack(character)
            self.MotionIndex = (self.MotionIndex + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)) % 12
            if not (self.X - 10 <= character.X <= self.X + 10):
                if self.Conflict_checking(2, self.run_move_speed / 2) and self.DIRECTION == 0:
                    self.X += self.run_move_speed / 2
                elif self.Conflict_checking(2, -self.run_move_speed / 2) and self.DIRECTION == 1:
                    self.X -= self.run_move_speed / 2
        if self.HP <= 0:
            del self
        self.gravity()

    def draw_monster(self, main_character):
        self.grid_image.clip_draw(int(self.MotionIndex) % 4 * 128,
                               544 - 128 * (int(self.MotionIndex) // 4 + 1),
                               128, 128, self.X - main_character.camera_move_x,
                               self.Y - main_character.camera_move_y,
                               60, 60)
        if self.DIRECTION == 0 and self.HP > 0:
            self.Image.clip_draw(int(self.MotionIndex) % 4 * 128,
                                    544 - 128 * (int(self.MotionIndex) // 4 + 1),
                                    128, 128, self.X - main_character.camera_move_x,
                                    self.Y - main_character.camera_move_y,
                                    60, 60)
        elif self.DIRECTION == 1 and self.HP > 0:
            self.rImage.clip_draw(512 - (int(self.MotionIndex) % 4 + 1) * 128,
                                            544 - 128 * (int(self.MotionIndex) // 4 + 1),
                                            128, 128, self.X - main_character.camera_move_x,
                                            self.Y - main_character.camera_move_y,
                                            60, 60)


class Bat():
    HP = 1
    ATK = 1
    Action = 0
    MotionIndex = 0
    Motion_dir = 0
    X = 400
    Y = 400
    DIRECTION = 0

    Image = None
    rImage = None
    grid_image = None

    Attack_state = False

    def __init__(self):
        if Bat.Image == None:
            Bat.Image = load_image('./Textures/Entities/Monsters/bat.png')
        if Bat.rImage == None:
            Bat.rImage = load_image('./Textures/Entities/Monsters/bat_reverse.png')
        if Bat.grid_image == None:
            Bat.grid_image = load_image('./Textures/Entities/Monsters/bat_grid.png')

    def Place(self, index_x, index_y):
        self.X, self.Y = index_x * 60, HEIGHT - index_y * 60
        self.Action = 0
        self.DIRECTION = random.randint(0, 1)
        self.HP = 1
        self.ATK = 1
        self.MotionIndex = 0
        self.Motion_dir = 0

    def Conflict_checking(self, mode, move):  # mode : x,y충돌 검사 , move : 다음에 움직일 크기
        if mode == 1:  # Y충돌 체크
            character_index_x = int(self.X // 60)
            character_index_y = int((HEIGHT - (self.Y + move)) // 60)
            for index_x in range(character_index_x - 1, character_index_x + 2):
                for index_y in range(character_index_y - 2, character_index_y + 3):
                    if 0 <= index_x < map_size and 0 <= index_y < map_size and \
                            2 <= map_floor_array[index_y][index_x] <= 29 and \
                            abs(self.X - index_x * 60) <= 55 and abs(self.Y + move - (HEIGHT - index_y * 60)) <= 58:
                        return False

        elif mode == 2:  # X충돌 체크
            character_index_x = int((self.X + move) // 60)
            character_index_y = int((HEIGHT - self.Y) // 60)
            for index_y in range(character_index_y - 1, character_index_y + 2):
                for index_x in range(character_index_x - 2, character_index_x + 3):
                    if 0 <= index_x < map_size and 0 <= index_y < map_size and \
                            2 <= map_floor_array[index_y][index_x] <= 29 and \
                            (abs(self.Y - (HEIGHT - index_y * 60)) < 58 and abs(self.X + move - index_x * 60) <= 55):
                        return False
        elif mode == 3:  # 캐릭터 여기서 move는 캐릭터의 위치
            if math.sqrt((self.X - move.X) ** 2 + (self.Y - move.Y) ** 2) <= 90:
                self.Action = 1
                self.MotionIndex = 6
        return True

    def attack(self, character):
        if  math.sqrt((self.X - character.X) ** 2 + (self.Y - character.Y) ** 2) < 60:
            # character.Stun_state = True
            if character.mode:
                character.HP -= self.ATK

    def Motion(self, character):
        if self.Action == 0:
            self.MotionIndex = (self.MotionIndex + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) / 2) % 4
            self.Conflict_checking(3, character)
        elif self.Action == 1:
            self.run_move_speed = RUN_SPEED_PPS * game_framework.frame_time
            if self.Y >= character.Y:
                self.DIRECTION = 1
            elif self.Y < character.Y:
                self.DIRECTION = 0
            if self.Conflict_checking(1, self.run_move_speed / 2) and self.DIRECTION == 0:
                self.Y += self.run_move_speed / 2
            elif self.Conflict_checking(1, -self.run_move_speed / 2) and self.DIRECTION == 1:
                self.Y -= self.run_move_speed / 2
            if self.X >= character.X:
                self.DIRECTION = 1
            elif self.X < character.X:
                self.DIRECTION = 0
            if not (self.X - 10 <= character.X <= self.X + 10):
                if self.Conflict_checking(2, self.run_move_speed / 2) and self.DIRECTION == 0:
                    self.X += self.run_move_speed / 2
                elif self.Conflict_checking(2, -self.run_move_speed / 2) and self.DIRECTION == 1:
                    self.X -= self.run_move_speed / 2
            self.attack(character)
            if self.Motion_dir == 0:
                self.MotionIndex = self.MotionIndex + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) * 3 / 2
                if self.MotionIndex >= 11.6:
                    self.Motion_dir = 1
            elif self.Motion_dir == 1:
                self.MotionIndex = self.MotionIndex - (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) * 3 / 2
                if self.MotionIndex <= 6.4:
                    self.Motion_dir = 0

    def draw_monster(self, main_character):
        self.grid_image.clip_draw(int(self.MotionIndex) % 4 * 128,
                               544 - 128 * (int(self.MotionIndex) // 4 + 1),
                               128, 128, self.X - main_character.camera_move_x,
                               self.Y - main_character.camera_move_y,
                               60, 60)
        if self.DIRECTION == 0 and self.HP > 0:
            self.Image.clip_draw(int(self.MotionIndex) % 4 * 128,
                                    544 - 128 * (int(self.MotionIndex) // 4 + 1),
                                    128, 128, self.X - main_character.camera_move_x,
                                    self.Y - main_character.camera_move_y,
                                    60, 60)
        elif self.DIRECTION == 1 and self.HP > 0:
            self.rImage.clip_draw(512 - (int(self.MotionIndex) % 4 + 1) * 128,
                                            544 - 128 * (int(self.MotionIndex) // 4 + 1),
                                            128, 128, self.X - main_character.camera_move_x,
                                            self.Y - main_character.camera_move_y,
                                            60, 60)

class Horned_Lizard():
    HP = 3
    ATK = 1
    Action = 0
    MotionIndex = 0
    X = 400
    Y = 400
    DIRECTION = 0

    Gravity = 0.3
    JumpSpeed = 15
    DownSpeed = 0
    Image = None
    rImage = None
    grid_image = None

    timer = 0

    Jump_state = False
    Gravity_state = False
    Attack_state = False

    def __init__(self):
        if Horned_Lizard.Image == None:
            Horned_Lizard.Image = load_image('./Textures/Entities/Monsters/horned_lizard.png')
        if Horned_Lizard.rImage == None:
            Horned_Lizard.rImage = load_image('./Textures/Entities/Monsters/horned_lizard_reverse.png')
        if Horned_Lizard.grid_image == None:
            Horned_Lizard.grid_image = load_image('./Textures/Entities/Monsters/horned_lizard_grid.png')

    def Place(self, index_x, index_y):
        self.X, self.Y = index_x * 60, HEIGHT - index_y * 60
        self.DIRECTION = random.randint(0,1)
        self.HP = 3
        self.ATK = 1
        self.Action = 0
        self.MotionIndex = 0

    def Conflict_checking(self, mode, move):  # mode : x,y충돌 검사 , move : 다음에 움직일 크기
        if mode == 1:  # Y충돌 체크
            character_index_x = int(self.X // 60)
            character_index_y = int((HEIGHT - (self.Y + move)) // 60)
            for index_x in range(character_index_x - 1, character_index_x + 2):
                for index_y in range(character_index_y - 2, character_index_y + 3):
                    if 0 <= index_x < map_size and 0 <= index_y < map_size and \
                            2 <= map_floor_array[index_y][index_x] <= 29 and \
                            abs(self.X - index_x * 60) <= 55 and abs(self.Y + move - (HEIGHT - index_y * 60)) <= 58:
                        return False

        elif mode == 2:  # X충돌 체크
            character_index_x = int((self.X + move) // 60)
            character_index_y = int((HEIGHT - self.Y) // 60)
            for index_y in range(character_index_y - 1, character_index_y + 2):
                for index_x in range(character_index_x - 2, character_index_x + 3):
                    if 0 <= index_x < map_size and 0 <= index_y < map_size \
                            and character_index_y + 1 < map_size and character_index_x + 1 < map_size and \
                            2 <= map_floor_array[index_y][index_x] <= 29 and \
                            (abs(self.Y - (HEIGHT - index_y * 60)) < 58 and abs(self.X + move - index_x * 60) <= 55) \
                            or (map_floor_array[character_index_y + 1][character_index_x + 1] == 0 and 2 <= map_floor_array[character_index_y + 1][character_index_x] <= 29  \
                            or map_floor_array[character_index_y + 1][character_index_x] == 0 and 2 <= map_floor_array[character_index_y + 1][character_index_x + 1] <= 29):
                        if self.DIRECTION:
                            self.DIRECTION = 0
                        else:
                            self.DIRECTION = 1
        elif mode == 3:  # 캐릭터 여기서 move는 캐릭터의 위치
            if math.sqrt((self.X - move.X) ** 2 + (self.Y - move.Y) ** 2) <= 240:
                return False
        return True

    def attack(self, character):
        if math.sqrt((self.X - character.X) ** 2 + (self.Y - character.Y) ** 2) < 60:
            # character.Stun_state = True
            if character.mode:
                character.HP -= self.ATK
        # if self.Conflict_checking(3, character):
        #     self.Action = 0

    def Jump(self):
        if self.Conflict_checking(1, self.JumpSpeed) and not self.Jump_state:
            self.JumpSpeed -= self.Gravity
            if self.JumpSpeed > 0:
                self.Y += self.JumpSpeed
        else:
            self.Jump_state = True

    def gravity(self):
        if self.Conflict_checking(1, -self.DownSpeed):
            if self.DownSpeed <= 10:
                self.DownSpeed += self.Gravity
            self.Y = self.Y - self.DownSpeed
            self.Gravity_state = True
        else:
            self.timer += 1
            self.DownSpeed = 0
            self.JumpSpeed = 15
            self.Gravity_state = False
            self.Jump_state = False

    def Motion(self, character):
        self.run_move_speed = RUN_SPEED_PPS * game_framework.frame_time
        if self.Action == 0:
            self.MotionIndex = (self.MotionIndex + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) / 2) % 7
            if self.Conflict_checking(2, self.run_move_speed / 2) and self.DIRECTION == 0:
                self.X += self.run_move_speed / 2
            elif self.Conflict_checking(2, -self.run_move_speed / 2) and self.DIRECTION == 1:
                self.X -= self.run_move_speed / 2
            if not self.Conflict_checking(3, character):
                self.Action = 1
                self.MotionIndex = 8
                self.Jump_state = False
                if self.X > character.X:
                    self.DIRECTION = 1
                elif self.X < character.X:
                    self.DIRECTION = 0
        elif self.Action == 1:
            if self.timer >= 3:
                self.Action = 0
                self.timer = 0
            self.attack(character)
            self.Jump()
            self.MotionIndex = (self.MotionIndex + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time))
            if self.MotionIndex >= 13:
                self.MotionIndex = 10
            if not (self.X - 10 <= character.X <= self.X + 10):
                if self.Conflict_checking(2, self.run_move_speed * 2 / 3) and self.DIRECTION == 0:
                    self.X += self.run_move_speed * 2 / 3
                elif self.Conflict_checking(2, -self.run_move_speed * 2 / 3) and self.DIRECTION == 1:
                    self.X -= self.run_move_speed * 2 / 3

        self.gravity()

    def draw_monster(self, main_character):
        self.grid_image.clip_draw(int(self.MotionIndex) % 5 * 128,
                               800 - 128 * (int(self.MotionIndex) // 5 + 1),
                               128, 128, self.X - main_character.camera_move_x,
                               self.Y - main_character.camera_move_y,
                               60, 60)
        if self.DIRECTION == 0 and self.HP > 0:
            self.Image.clip_draw(int(self.MotionIndex) % 5 * 128,
                                    800 - 128 * (int(self.MotionIndex) // 5 + 1),
                                    128, 128, self.X - main_character.camera_move_x,
                                    self.Y - main_character.camera_move_y,
                                    60, 60)
        elif self.DIRECTION == 1 and self.HP > 0:
            self.rImage.clip_draw(640 - (int(self.MotionIndex) % 5 + 1) * 128,
                                            800 - 128 * (int(self.MotionIndex) // 5 + 1),
                                            128, 128, self.X - main_character.camera_move_x,
                                            self.Y - main_character.camera_move_y,
                                            60, 60)

monster_place = [[33, 18], [22, 23], [4, 41], [31, 45], # lizard
                 [17, 2], [40, 1], [40, 15], [18, 16], [29, 21], [29, 25], [17, 28], [43, 32], [5, 44], [26, 44], [12, 47], [32, 47],   # bat
                 [38, 7], [10, 17], [38, 12], [8, 22], [39, 26], [11, 30], [16, 39], [17, 46], [43, 48]]                                # snake

monster_list = []
monster_list_3 = [Snake() for i in range(9)]
monster_list_2 = [Bat() for i in range(12)]
monster_list_1 = [Horned_Lizard() for i in range(4)]

monster_list += monster_list_1 + monster_list_2 + monster_list_3