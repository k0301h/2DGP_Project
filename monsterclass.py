from characterclass import *
import random
import math

class Snake(UNIT):
    # UNIT.HP = 2
    # UNIT.ATK = 1
    # UNIT.Action = 0
    # UNIT.MotionIndex = 0
    # UNIT.X = 400
    # UNIT.Y = 400
    # UNIT.DIRECTION = 0

    Gravity = 0.5
    JumpSpeed = 10
    DownSpeed = 0
    Image = None
    rImage = None
    grid_image = None

    Gravity_state = False
    Attack_state = False

    # def __init__(self):
        # if Snake.Image == None:
        #     Snake.Image = load_image('./Textures/Entities/Monsters/snake.png')
        # if Snake.rImage == None:
        #     Snake.rImage = load_image('./Textures/Entities/Monsters/snake_reverse.png')

    def Place(self):
        self.X, self.Y = random.randint(200, 700), 100
        self.DIRECTION = random.randint(0, 1)

    def Conflict_checking(self, mode, move):  # mode : x,y충돌 검사 , move : 다음에 움직일 크기
        if mode == 1:  # Y충돌 체크
            character_index_x = int(self.X // 60)
            character_index_y = int((HEIGHT - (self.Y + move)) // 60)
            for index_x in range(character_index_x - 1, character_index_x + 2):
                for index_y in range(character_index_y - 2, character_index_y + 3):
                    if 0 <= index_x < map_size and 0 <= index_y < map_size and \
                            2 <= map_floor_array[index_y][index_x] <= 29 and \
                            abs(self.X - index_x * 60) <= 55 and abs(self.Y + move - (HEIGHT - index_y * 60)) <= 60:
                        return False

        elif mode == 2:  # X충돌 체크
            character_index_x = int((self.X + move) // 60)
            character_index_y = int((HEIGHT - self.Y) // 60)
            for index_y in range(character_index_y - 1, character_index_y + 2):
                for index_x in range(character_index_x - 2, character_index_x + 3):
                    if 0 <= index_x < map_size and 0 <= index_y < map_size and \
                            2 <= map_floor_array[index_y][index_x] <= 29 and \
                            (abs(self.Y - (HEIGHT - index_y * 60)) < 60 and abs(self.X + move - index_x * 60) <= 55)\
                            or map_floor_array[character_index_y + 1][character_index_x + 1] == 0:
                        if self.DIRECTION:
                            self.DIRECTION = 0
                        else:
                            self.DIRECTION = 1
        elif mode == 3:  # 캐릭터 여기서 move는 캐릭터의 위치
            if math.sqrt((self.X - move.X) ** 2 + (self.Y - move.Y) ** 2) <= 120:
                self.Action = 1
        return True

    def attack(self, character):
        if self.MotionIndex < 11.9:
            self.MotionIndex = (self.MotionIndex + 0.1) % 8 + 4
            print(self.MotionIndex)
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
        if self.Action == 0:
            self.MotionIndex = (self.MotionIndex + 0.1) % 4
            if self.Conflict_checking(2, 3) and self.DIRECTION == 0:
                self.X += 3
            elif self.Conflict_checking(2, -3) and self.DIRECTION == 1:
                self.X -= 3
            self.Conflict_checking(3, character)
        elif self.Action == 1:
            self.attack(character)

        self.gravity()

    def draw_monster(self, main_character, monster_grid):
        monster_grid.clip_draw(int(self.MotionIndex) % 4 * 128,
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
