import pygame

field_rects = [
    pygame.Rect(64 * x, 64 * y, 64, 64) for x in range(8) for y in range(8) if (x + y) % 2
]
menu_rects = [
    (pygame.Rect(106, 155, 300, 50), "change_menu_status", "Continue", (200, 165)),
    (pygame.Rect(106, 225, 300, 50), "restart", "Restart", (200, 235)),
    (pygame.Rect(106, 295, 300, 50), "play_with_bot", "Play with computer", (160, 305)),
    (pygame.Rect(106, 365, 300, 50), "play_with_friend", "Play with friend", (180, 375)),
    (pygame.Rect(106, 435, 300, 50), "exit", "Exit", (230, 445)),
]
