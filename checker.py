from typing import List, Tuple
from pygame.color import THECOLORS

from settings import checker_field


class Checker:

    def __init__(self, x: int, y: int, color: int, is_queen: bool = False):
        """
        Init
        :param x: x position on coordinates
        :param y: y position on coordinates
        :param color: color of checker (1 - white, 2 - black)
        """
        self.x = x
        self.y = y
        self.color = color
        self.is_queen = is_queen

    def move(self, x: int, y: int):
        """
        Checker's move
        :param x: new x position
        :param y: new y position
        """
        self.x = x
        self.y = y
        if not self.is_queen:
            # queen check after every move
            self.check_is_queen()

    def check_is_queen(self):
        """
        Queen check
        """
        if self.color == 1 and self.y == 0:
            self.is_queen = True
        if self.color == 2 and self.y == 7:
            self.is_queen = True

    def get_params(self) -> tuple:
        """
        Return params of checker: (x_position, y_position, side_of_move)
        """
        return self.x, self.y, -1 if self.color == 1 else 1

    def __str__(self):
        """
        Return checker's color (1 or 2)
        """
        return str(self.color)


class Checkers:

    def __init__(self):
        self.checkers: List[Checker] = []
        self.init()
        self.all_field = []

    def init(self):
        """
        Placement of checkers
        """
        self.checkers = self.generate_checkers(checker_field)

    @staticmethod
    def generate_checkers(field) -> list:
        checkers = []
        for row in range(8):
            for column in range(8):
                if field[row][column] in (1, 2):
                    checkers.append(Checker(column, row, field[row][column], True))
        # for y in [0, 1, 2, 5, 6, 7]:
        #     for x in range(8):
        #         if (x + y) % 2:
        #             checkers.append(Checker(x, y, 2 if y < 3 else 1))
        return checkers[:]

    def get_field(self) -> tuple:
        """
        Return arrangement of checker's
        """
        field = [[0 for _ in range(8)] for _ in range(8)]
        for checker in self:
            field[checker.y][checker.x] = checker.color
        return tuple(field)

    def get_whites(self) -> tuple:
        """
        Return white checkers
        """
        return tuple(filter(lambda x: x.color == 1, self))

    def get_blacks(self) -> tuple:
        """
        Return black checkers
        """
        return tuple(filter(lambda x: x.color == 2, self))

    def get_checker(self, x: int, y: int) -> Checker:
        """
        Return checker by x and y positions
        """
        for checker in self:
            if checker.x == x and checker.y == y:
                return checker

    @staticmethod
    def __check_range(x, y) -> bool:
        """
        Check for the presence of coordinates on the field
        """
        return all([x in range(8), y in range(8)])

    def eat_checker(self, checker: Checker):
        """
        Eat checker
        """
        # self.all_field.append(self.checkers)
        self.checkers.remove(checker)

    def eat(self, field: tuple, x: int, y: int, color: int) -> tuple:
        eat_color = 2 if color == 1 else 1
        eat_moves = []
        for i in [-1, 1]:
            for j in [-1, 1]:
                cur_x, cur_y = x + i, y + j
                if self.__check_range(cur_x, cur_y) and field[cur_y][cur_x] == eat_color:
                    if self.__check_range(cur_x + i, cur_y + j) and field[cur_y + j][cur_x + i] == 0:
                        eat_checker = self.get_checker(cur_x, cur_y)
                        eat_moves.append((cur_x + i, cur_y + j, THECOLORS["green"], True, eat_checker))
        return tuple(eat_moves)

    def eat_queen(self, field: tuple, x: int, y: int, color: int, again: bool = False, i_prev: int = 0,
                  j_prev: int = 0) -> tuple:
        eat_color = 2 if color == 1 else 1
        eat_moves = []
        for i in [-1, 1]:
            for j in [-1, 1]:
                flag_can_eat = False
                eat_checker = None
                temp_moves = []
                temp_moves_with_eats = []
                if i == i_prev and j == j_prev:
                    continue
                for dlt in range(1, 8):
                    cur_x, cur_y = x + i * dlt, y + j * dlt
                    if self.__check_range(cur_x, cur_y) and field[cur_y][cur_x] == color:
                        break
                    if self.__check_range(cur_x, cur_y) and field[cur_y][cur_x] == eat_color and not flag_can_eat:
                        flag_can_eat = True
                        eat_checker = self.get_checker(cur_x, cur_y)
                        continue
                    if not flag_can_eat:
                        continue
                    if self.__check_range(cur_x, cur_y) and field[cur_y][cur_x] == 0:
                        if not again and len(self.eat_queen(field, cur_x, cur_y, color, True, 0 - i, 0 - j)):
                            temp_moves_with_eats.append((cur_x, cur_y, THECOLORS["green"], True, eat_checker))
                        else:
                            temp_moves.append((cur_x, cur_y, THECOLORS["green"], True, eat_checker))
                    else:
                        break
                if len(temp_moves_with_eats):
                    eat_moves.extend(temp_moves_with_eats)
                else:
                    eat_moves.extend(temp_moves)
        return tuple(eat_moves)

    def move(self, field: tuple, x: int, y: int, move: int) -> tuple:
        moves = []
        for i in [-1, 1]:
            cur_x, cur_y = x + i, y + move
            if self.__check_range(cur_x, cur_y) and field[cur_y][cur_x] == 0:
                moves.append((cur_x, cur_y, THECOLORS["blue"], False, None))
        return tuple(moves)

    def move_queen(self, field: tuple, x: int, y: int) -> tuple:
        moves = []
        for i in [-1, 1]:
            for j in [-1, 1]:
                for dlt in range(1, 8):
                    cur_x, cur_y = x + i * dlt, y + j * dlt
                    if self.__check_range(cur_x, cur_y) and field[cur_y][cur_x] == 0:
                        moves.append((cur_x, cur_y, THECOLORS["blue"], False, None))
                    else:
                        break
        return tuple(moves)

    def get_moves(self, checker: Checker) -> tuple:
        x, y, move = checker.get_params()
        field = self.get_field()
        if checker.is_queen:
            eat_moves = self.eat_queen(field, x, y, checker.color)
            moves = self.move_queen(field, x, y)
        else:
            eat_moves = self.eat(field, x, y, checker.color)
            moves = self.move(field, x, y, move)
        if len(eat_moves):
            return eat_moves[:]
        return tuple(moves)

    def must_move(self, color: int) -> tuple:
        checkers = self.get_whites() if color == 1 else self.get_blacks()
        checker_with_move = []
        for checker in checkers:
            x, y, _ = checker.get_params()
            field = self.get_field()
            moves = self.eat_queen(field, x, y, checker.color) if checker.is_queen else self.eat(field, x, y,
                                                                                                 checker.color)
            if len(moves):
                checker_with_move.append(checker)
        return tuple(checker_with_move)

    def all_turns(self, color: int) -> tuple:
        checkers = self.get_whites() if color == 1 else self.get_blacks()
        checker_with_move = []
        for checker in checkers:
            x, y, move = checker.get_params()
            field = self.get_field()
            moves = self.move_queen(field, x, y) if checker.is_queen else self.move(field, x, y, move)
            eat_moves = self.eat_queen(field, x, y, checker.color) if checker.is_queen else self.eat(field, x, y,
                                                                                                     checker.color)

            if len(moves):
                checker_with_move.append(checker)
            if len(eat_moves):
                checker_with_move.append(eat_moves)
        return tuple(checker_with_move)

    def __str__(self):
        return '\n'.join(' '.join(str(cell) for cell in row) for row in self.get_field())

    def __iter__(self):
        return iter(self.checkers)
