from pygame.image import load

WIDTH, HEIGHT = 512, 640
black_checker = load("png/black.png")
black_queen_checker = load("png/black_queen.png")
black_checker_small = load("png/black_small.png")
white_checker = load("png/white.png")
white_queen_checker = load("png/white_queen.png")
white_checker_small = load("png/white_small.png")

# field = [
#     [0, 2, 0, 2, 0, 2, 0, 2],
#     [2, 0, 2, 0, 2, 0, 2, 0],
#     [0, 2, 0, 2, 0, 2, 0, 2],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 0, 1, 0, 1, 0, 1, 0],
#     [0, 1, 0, 1, 0, 1, 0, 1],
#     [1, 0, 1, 0, 1, 0, 1, 0],
# ]

field = [
    # 0  1  2  3  4  5  6  7
    [0, 0, 0, 0, 0, 0, 0, 0],  # 0
    [0, 0, 0, 0, 0, 0, 2, 0],  # 1
    [0, 0, 0, 0, 0, 0, 0, 0],  # 2
    [0, 0, 0, 0, 0, 0, 0, 0],  # 3
    [0, 0, 0, 0, 0, 0, 0, 0],  # 4
    [0, 0, 0, 0, 0, 0, 0, 0],  # 5
    [0, 0, 0, 0, 0, 0, 0, 0],  # 6
    [0, 0, 1, 0, 0, 0, 0, 0],  # 7
]
