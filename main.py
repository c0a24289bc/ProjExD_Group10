import pygame
import sys
import os
from settings import *

# 各担当のモジュールをインポート (ファイルを作成してから有効化する)
# from map_data import MapData
# from enemy import Enemy
# from tower import Tower
# from ui import UIManager

# --- 資料8ページ：実行環境のパス設定 ---
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ProjExD Tower Defense")
    clock = pygame.time.Clock()

    # --- インスタンス生成 (後で各担当が実装) ---
    # map_data = MapData()
    # enemy_group = pygame.sprite.Group()
    # tower_group = pygame.sprite.Group()
    # ui_manager = UIManager()

    running = True
    while running:
        # --- イベント処理 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # マウスクリック等の処理 (担当Dが記述)
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     pass

        # --- 更新処理 ---
        # enemy_group.update()
        # tower_group.update()

        # --- 描画処理 ---
        screen.fill(BLACK)
        
        # map_data.draw(screen) (担当C)
        # tower_group.draw(screen) (担当A)
        # enemy_group.draw(screen) (担当B)
        # ui_manager.draw(screen) (担当D)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()