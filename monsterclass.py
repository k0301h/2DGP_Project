from Unitclass import *
from map_floor import *
from pico2d import *
import characterclass

class MONSTER(UNIT):
    monster_type = 1 # 1 == 뱀(1round)
    UNIT.HP = 2
    UNIT.ATK = 1
    UNIT.Action = 0
    UNIT.MotionIndex = 0
    UNIT.X = 400
    UNIT.Y = 400
    UNIT.DIRECTION = 0
    BombCount = 4
    RopeCount = 4
    Money = 0

    Gravity = 0.5
    JumpSpeed = 10
    DownSpeed = 0

    Gravity_state = False
    Attack_state = False

    def Place(self):
        self.X = 200
        self.Y = 200

    def Conflict_checking(self, mode, move): # mode : x,y충돌 검사 , move : 다음에 움직일 크기
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
                            abs(self.Y - (HEIGHT - index_y * 60)) < 60 and abs(self.X + move - index_x * 60) <= 55:
                        return False
        return True

    def gravity(self):
        if self.Conflict_checking(1, -self.DownSpeed):
            if self.DownSpeed <= 10:
                self.DownSpeed += self.Gravity
            self.Y = self.Y - self.DownSpeed
            self.Gravity_state = True
        else:
            self.DownSpeed = 0
            self.Gravity_state = False

    def Motion(self):
        if self.Action == 0:
            self.MotionIndex = (self.MotionIndex + 1) % 4
            if self.Conflict_checking(2, 3):
                self.X += 3

        self.gravity()

    def draw_monster(self, monster_image, monster_grid):
        monster_grid.clip_draw(int(self.MotionIndex) % 4 * 128,
                                  544 - 128 * (int(self.MotionIndex) // 4 + 1),
                                  128, 128, self.X - characterclass.CHARACTER.camera_move_x + 30,
                                  self.Y - characterclass.CHARACTER.camera_move_y - 30,
                                  60, 60)
        if self.DIRECTION == 0:
            monster_image.clip_draw(int(self.MotionIndex) % 4 * 128,
                                  544 - 128 * (int(self.MotionIndex) // 4 + 1),
                                  128, 128, self.X - characterclass.CHARACTER.camera_move_x + 30,
                                  self.Y - characterclass.CHARACTER.camera_move_y - 30,
                                  60, 60)
        # elif self.DIRECTION == 1:
        #     if self.Attack_state:
        #     character_reverse_I.clip_draw(1918 - int(self.MotionIndex) % 16 * 128,
        #                                   1918 - 128 * (int(self.MotionIndex) // 16), 128, 128,
        #                                   self.X - self.camera_move_x + 30,
        #                                   self.Y - self.camera_move_y - 30, 70, 70)

