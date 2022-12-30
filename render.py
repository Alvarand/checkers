import pygame
import sys
from pygame.color import THECOLORS
from settings import (
    white_queen_checker,
    white_checker,
    white_checker_small,
    black_queen_checker,
    black_checker,
    black_checker_small
)
from render_variable import (
    menu_rects, field_rects
)
from checker import Checker, Checkers


class Game:

    def __init__(self, width: int, height: int):
        self.checkers = Checkers()
        self.WIDTH = width
        self.HEIGHT = height
        self.running = True
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clicked = [False, Checker(-1, -1, -1)]
        self.turn = 1  # starting white
        self.turns = {
            1: white_checker_small,
            2: black_checker_small
        }
        self.clock = pygame.time.Clock()
        self.can_eat_again = False
        self.wins = {
            1: 0,
            2: 0
        }
        self.is_menu = True
        self.mouse_x = self.mouse_y = 0
        self.font = None
        self.button = 0
        self.is_start = False

    def restart(self):
        self.checkers = Checkers()
        self.clicked = [False, Checker(-1, -1, -1)]
        self.turn = 1  # starting white
        self.can_eat_again = False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.is_start:
                        self.change_menu_status()
                    # self.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.button = event.button
                if not self.is_menu:
                    self.event_click()
            else:
                self.button = 0
            if event.type == pygame.MOUSEMOTION:
                self.mouse_x, self.mouse_y = event.pos

    def event_click(self):
        mouse_x, mouse_y = self.mouse_x // 64, self.mouse_y // 64
        if self.button == 1:
            if not self.clicked[0]:
                checker = self.checkers.get_checker(mouse_x, mouse_y)
                checker_with_move = self.checkers.must_move(self.turn)
                if len(checker_with_move):
                    if checker in checker_with_move:
                        self.clicked[0] = True
                        self.clicked[1] = checker
                elif isinstance(checker, Checker) and checker.color == self.turn:
                    self.clicked[0] = True
                    self.clicked[1] = checker
            else:
                self.move(mouse_x, mouse_y)
        elif self.button == 3 and not self.can_eat_again:
            self.clicked[0] = False

    def change_menu_status(self):
        self.is_menu = not self.is_menu
        self.is_start = True

    def change_turn(self):
        self.turn = 2 if self.turn == 1 else 1

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

    def render_all(self):
        self.screen.fill(THECOLORS.get("white"))
        if self.is_menu:
            self.render_menu()
        else:
            self.render_field()
            self.render_checker()
            self.render_move()
            self.render_details()

    def render_field(self):
        for cell in field_rects:
            pygame.draw.rect(self.screen, THECOLORS["black"], cell, 0)

    @staticmethod
    def get_checker_type(checker: Checker):
        if checker.color == 1:
            checker_type = white_queen_checker if checker.is_queen else white_checker
        else:
            checker_type = black_queen_checker if checker.is_queen else black_checker
        return checker_type

    def render_checker(self):
        for checker in self.checkers:
            checker_type = self.get_checker_type(checker)
            self.screen.blit(checker_type, (checker.x * 64, checker.y * 64))

    def render_move(self):
        if self.clicked[0]:
            all_moves = self.checkers.get_moves(self.clicked[1])
            for x, y, color, *_ in all_moves:
                cell = pygame.Rect(64 * x, 64 * y, 64, 64)
                pygame.draw.rect(self.screen, color, cell, 4)
            cell = pygame.Rect(64 * self.clicked[1].x, 64 * self.clicked[1].y, 64, 64)
            pygame.draw.rect(self.screen, THECOLORS["pink"], cell, 4)
        else:
            checker_with_move = self.checkers.must_move(self.turn)
            for checker in checker_with_move:
                cell = pygame.Rect(64 * checker.x, 64 * checker.y, 64, 64)
                pygame.draw.rect(self.screen, THECOLORS["green"], cell, 4)

    def render_details(self):
        pygame.draw.rect(self.screen, THECOLORS["grey"], pygame.Rect(0, 512, 512, 128), 0)
        self.screen.blit(self.turns[self.turn], (220, 560))

        texts = [
            (self.font.render("Eaten", True, THECOLORS["black"]), (10, 520)),
            (self.font.render("White: ", True, THECOLORS["black"]), (10, 560)),
            (self.font.render("Black: ", True, THECOLORS["black"]), (10, 600)),
            (self.font.render("Current turn", True, THECOLORS["black"]), (180, 520)),
            (self.font.render("Winners", True, THECOLORS["black"]), (400, 520)),
            (self.font.render(f"White: {self.wins[1]}", True, THECOLORS["black"]), (400, 560)),
            (self.font.render(f"Black: {self.wins[2]}", True, THECOLORS["black"]), (400, 600))
        ]

        for text, pos in texts:
            self.screen.blit(text, pos)

        for i in range(12 - len(self.checkers.get_blacks())):
            self.screen.blit(self.turns[2], (80 + i * 10, 560))

        for i in range(12 - len(self.checkers.get_whites())):
            self.screen.blit(self.turns[1], (80 + i * 10, 600))

    def render_menu(self):

        for cell, method, text, pos in (menu_rects if self.is_start else menu_rects[1:]):
            if self.button == 1 and cell.collidepoint(self.mouse_x, self.mouse_y) and method:

                self.__getattribute__(method)()

            pygame.draw.rect(
                self.screen, THECOLORS["grey"], cell, 0 if cell.collidepoint(self.mouse_x, self.mouse_y) else 1
            )

            self.screen.blit(self.font.render(text, True, THECOLORS["black"]), pos)

    def check_win(self):
        whites = self.checkers.get_whites()
        blacks = self.checkers.get_blacks()
        if not len(whites) or not len(self.checkers.all_turns(1)):
            self.wins[2] += 1
            self.restart()
        if not len(blacks) or not len(self.checkers.all_turns(2)):
            self.wins[1] += 1
            self.restart()

    def run(self):
        pygame.init()
        self.font = pygame.font.SysFont("verdana", 20)
        pygame.display.set_caption("Checkers")
        while self.running:
            self.events()
            self.render_all()
            self.check_win()
            pygame.display.flip()
            self.clock.tick(60)
        self.exit()

    @staticmethod
    def exit():
        pygame.quit()
        sys.exit()
