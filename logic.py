from checker import Checker, Checkers
from random import choice


class CheckersLogic:

    def __init__(self):
        self.checkers = Checkers()
        self.clicked = [False, Checker(-1, -1, -1)]
        self.turn = 1  # starting white
        self.turn_number = [0, 24]  # [turn_number, total_amount_of_checkers]
        self.can_eat_again = False

    def change_turn(self):
        self.turn = 2 if self.turn == 1 else 1
        if self.turn_number[1] > len(self.checkers):
            self.turn_number[0] = 0
            self.turn_number[1] = len(self.checkers)
        else:
            self.turn_number[0] += 0.5

    def move(self, mouse_x: int, mouse_y: int):
        all_moves = self.checkers.get_moves(self.clicked[1])
        for x, y, color, is_eat, eat_checker in all_moves:
            if x != mouse_x or y != mouse_y:
                continue
            self.clicked[1].move(x, y)
            if is_eat:
                self.checkers.eat_checker(eat_checker)
                all_moves = self.checkers.get_moves(self.clicked[1])
                if len(all_moves):
                    self.can_eat_again = all_moves[0][3]
                else:
                    self.can_eat_again = False
            if not self.can_eat_again:
                self.clicked[0] = False
                self.change_turn()
            break

    def bot_move(self):
        checkers_with_move = self.checkers.must_move(self.turn)
        if not len(checkers_with_move):
            checkers = self.checkers.get_whites() if self.turn == 1 else self.checkers.get_blacks()
            checkers_with_move = tuple(
                checker for checker in checkers if len(self.checkers.get_moves(checker))
            )
        if len(checkers_with_move):
            checker = choice(checkers_with_move)
            self.clicked[1] = checker
            x, y, *_ = choice(self.checkers.get_moves(checker))
            self.move(x, y)
        self.clicked = [False, Checker(-1, -1, -1)]
