import pygame
import sys
import os
import math
import random

# ====================================================
#  1. 初期設定・定数 (SETTINGS)
# ====================================================

# 実行環境のディレクトリに移動 (資料の条件)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 画面設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TILE_SIZE = 40

# 色定義
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (255, 50, 50)     # 通常こうかとん
BLUE   = (50, 50, 255)     # タワー
YELLOW = (255, 255, 0)     # 弾


# マップチップ
TILE_PATH = 0
TILE_GRASS = 1
TILE_BASE = 2
TILE_SPAWN = 3

# ゲーム状態
STATE_PLAY = 1

STATE_GAMEOVER = 2

# ====================================================
#  2. クラス定義エリア
# ====================================================

class GameManager:
    """
    ゲーム全体の状態を管理するクラス
    """
    def __init__(self):
        self.chicken = 100  # 通貨
        self.life = 10     # 拠点ライフ
        self.state = STATE_PLAY
        
        

    def update(self):
        pass
        
    def check_gameover(self):
        if self.life <= 0:
            print("Game Over! (Logic not implemented yet)")
            
            self.state = STATE_GAMEOVER
            

    
    
    def reset_game(self):
        self.chicken = 100
        self.life = 10
        self.state = STATE_PLAY

    


class MapManager:
    def __init__(self):
        # 0:道, 1:草, 2:拠点, 3:出現
        # 縦15行 x 横20列 (600px x 800px)
        self.map_data = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        
        # 敵が通るルートの座標 (マスの中心座標: index * 40 + 20)
        # 上記のmap_dataの「曲がり角」に合わせて正確に設定
        self.waypoints = [
            (60, 100),    # [1][2] スタート
            (500, 100),   # [12][2] 右へ（最初の角）
            (500, 260),  # [12][6] 下へ（次の角）
            (220, 260),  # [5][6] 左へ
            (220, 500),  # [5][12] 下へ
            (660, 500),  # [16][12] 右へ
            (660, 380)   # [16][9] 右へ（ゴール）
        ]

    def draw(self, screen, is_fever=False):
       
        screen.fill(BLACK) 

        for r, row in enumerate(self.map_data):
            for c, tile in enumerate(row):
                rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile == TILE_PATH: color = (240, 230, 140)
                elif tile == TILE_GRASS: color = (0, 100, 0)
                elif tile == TILE_BASE: color = BLUE
                elif tile == TILE_SPAWN: color = RED
                else: color = BLACK
                
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (0, 50, 0), rect, 1)
    
    def is_placeable(self, x, y):
        c = x // TILE_SIZE
        r = y // TILE_SIZE
        if 0 <= r < len(self.map_data) and 0 <= c < len(self.map_data[0]):
            return self.map_data[r][c] == TILE_GRASS
        return False
    
    
    def is_path(self, x, y):
        c = x // TILE_SIZE
        r = y // TILE_SIZE
        if 0 <= r < len(self.map_data) and 0 <= c < len(self.map_data[0]):
            return self.map_data[r][c] == TILE_PATH
        return False


class Koukaton(pygame.sprite.Sprite):
    """
    敵キャラクタークラス
    """
    def __init__(self, waypoints):
        
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED) 
        self.rect = self.image.get_rect()
        
        self.waypoints = waypoints
        self.wp_index = 0
        self.speed = 2   
        self.hp = 30     
        self.value = 10  

        if waypoints:
            self.rect.center = waypoints[0]

    def update(self, gm):
        if self.wp_index < len(self.waypoints) - 1:
            target = self.waypoints[self.wp_index + 1]
            dx = target[0] - self.rect.centerx
            dy = target[1] - self.rect.centery
            
            if dx > 0: self.rect.centerx += min(self.speed, dx)
            elif dx < 0: self.rect.centerx -= min(self.speed, -dx)
            if dy > 0: self.rect.centery += min(self.speed, dy)
            elif dy < 0: self.rect.centery -= min(self.speed, -dy)
            
            if abs(dx) < 5 and abs(dy) < 5:
                self.wp_index += 1
        else:
            gm.life -= 1
            self.kill()





class Tower(pygame.sprite.Sprite):
    """
    タワークラス
    """
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.range = 150
        self.cooldown = 30
        self.timer = 0
        
     

    def update(self, enemy_group, bullet_group, is_fever=False):
        
        
        self.timer += 1
        if self.timer >= self.cooldown:
            nearest_enemy = None
            min_dist = self.range
            for enemy in enemy_group:
                dist = math.hypot(self.rect.centerx - enemy.rect.centerx,
                                  self.rect.centery - enemy.rect.centery)
                if dist <= min_dist:
                    min_dist = dist
                    nearest_enemy = enemy
            
            if nearest_enemy:
                new_bullet = Bullet(self.rect.center, nearest_enemy.rect.center)
                bullet_group.add(new_bullet)
                self.timer = 0
    
   


class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=start_pos)
        self.speed = 10
        
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        distance = math.hypot(dx, dy)
        if distance == 0: distance = 1
        
        self.vx = (dx / distance) * self.speed
        self.vy = (dy / distance) * self.speed
        self.life_timer = 60

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.life_timer -= 1
        if self.life_timer <= 0:
            self.kill()


# ====================================================
#  3. メインループ
# ====================================================

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Koukaton Defense Base")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)
    large_font = pygame.font.SysFont(None,40)

    gm = GameManager()
    map_manager = MapManager()
    
    enemy_group = pygame.sprite.Group()
    tower_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    
    
    

    # 初期配置（テスト用）
    tower_group.add(Tower(14 * TILE_SIZE, 4 * TILE_SIZE))
    
    spawn_timer = 0
    
    start_ticks = pygame.time.get_ticks()
    
    running = True
    while running:
        # --- 1. イベント処理 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
       
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        gm.reset_game()
                        enemy_group.empty()
                        bullet_group.empty()
                        tower_group.empty()
                        tower_group.add(Tower(14 * TILE_SIZE, 4 * TILE_SIZE))
                        spawn_timer = 0
                    elif event.key == pygame.K_q:
                            running = False


        # --- 2. 更新処理 ---
        if gm.state == STATE_PLAY:
            gm.update()
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
            difficulty_scale = elapsed_time / 30
            spawn_timer += 1
            # 敵出現ロジック
            spawn_timer += 1
            if spawn_timer >= 120: 
                spawn_timer = 0
                new_enemy = Koukaton(map_manager.waypoints)
                
                new_enemy.hp += int(1.2 * difficulty_scale)    # HP増加
                new_enemy.speed += (1.05 * difficulty_scale) # 速度増加
                
          
                new_enemy = Koukaton(map_manager.waypoints)
                enemy_group.add(new_enemy)

            enemy_group.update(gm)
            tower_group.update(enemy_group, bullet_group) # 【担当E】is_feverを渡す
            bullet_group.update()
           

            # 衝突判定：弾 vs こうかとん
            hits = pygame.sprite.groupcollide(bullet_group, enemy_group, True, False)
            for bullet, hit_enemies in hits.items():
                for enemy in hit_enemies:
                    enemy.hp -= 10
                    if enemy.hp <= 0:
                        enemy.kill()
                        gm.chicken += enemy.value
                       

            gm.check_gameover()

        # --- 3. 描画処理 ---
        screen.fill(BLACK)
        
        if gm.state == STATE_PLAY:
            map_manager.draw(screen) #
           
            tower_group.draw(screen)
            enemy_group.draw(screen)
            bullet_group.draw(screen)
            
            # UI表示
            txt_chicken = font.render(f"Chicken: {gm.chicken}", True, WHITE)
            txt_life = font.render(f"Life: {gm.life}", True, WHITE)
            screen.blit(txt_chicken, (10, 10))
            screen.blit(txt_life, (10, 50))
            
  
        elif gm.state == STATE_GAMEOVER:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            screen.blit(overlay, (0,0))
            
            txt_over = large_font.render("GAME OVER", True, RED)
            txt_retry = font.render("Press R to Restart / Q to Quit", True, WHITE)
            
            # 中央に配置
            screen.blit(txt_over, (SCREEN_WIDTH//2 - 160, SCREEN_HEIGHT//2 - 50))
            screen.blit(txt_retry, (SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT//2 + 50))
            
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()