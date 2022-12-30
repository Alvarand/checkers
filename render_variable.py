import pygame

field_rects = [
    pygame.Rect(64 * x, 64 * y, 64, 64) for x in range(8) for y in range(8) if (x + y) % 2
]
menu_rects = [
    (pygame.Rect(106, 155, 300, 50), "change_menu_status", "Continue", (200, 165)),
    (pygame.Rect(106, 225, 300, 50), "", "Play with computer", (160, 235)),
    (pygame.Rect(106, 295, 300, 50), "change_menu_status", "Play with friend", (180, 305)),
    (pygame.Rect(106, 365, 300, 50), "exit", "Exit", (230, 375)),
]
