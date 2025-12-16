import pygame

# 画面設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
FPS = 60

# 色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)

# マップチップ定義
TILE_PATH = 0  # 敵が通る道
TILE_GRASS = 1 # タワーが置ける場所
TILE_BASE = 2  # 防衛拠点
TILE_SPAWN = 3 # 敵出現地点