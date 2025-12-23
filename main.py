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
PURPLE = (180, 0, 255)     #エリートカラー

# トラップの色定義
trap_color = (255, 165, 0)  # トラップの色
# ORANGE = (255, 165, 0)
# PURPLE = ...

# マップチップ
TILE_PATH = 0
TILE_GRASS = 1
TILE_BASE = 2
TILE_SPAWN = 3

# ゲーム状態
STATE_PLAY = 1


# ====================================================
#  2. クラス定義エリア
# ====================================================

class GameManager:
    """
    ゲーム全体の状態を管理するクラス
    """
    def __init__(self):
        self.chicken = 100  # 通貨
        self.life = 20      # 拠点ライフ
        self.state = STATE_PLAY
        
        # 【担当E】ここにフィーバー用の変数を追加してください (timer, is_feverなど)
        self.fever_gauge = 30 # フィーバーゲージ (最大30)
        self.is_fever = False # フィーバー中かどうかのフラグ
        self.fever_timer = 0 # フィーバーの残り時間 (フレーム数)
        self.FEVER_DURATION = FPS * 20 # 20秒間

    def activate_fever(self):
        """フィーバー状態を開始する"""
        if not self.is_fever:
            self.fever_timer = self.FEVER_DURATION
            self.is_fever = True
            self.fever_gauge = 0 # ゲージをリセット
            print("--- FEVER TIME START! ---")

    def update(self):
        # 【担当E】ここでフィーバータイマーの減算処理などを書いてください
        if self.is_fever:
            self.fever_timer -= 1
            if self.fever_timer <= 0:
                self.is_fever = False
                self.fever_timer = 0
                print("--- FEVER TIME END! ---")

    def check_gameover(self):
        if self.life <= 0:
            print("Game Over! (Logic not implemented yet)")
        
    def check_gameover(self):
        if self.life <= 0:
            print("Game Over! (Logic not implemented yet)")


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
        # 【担当E】is_feverフラグを受け取り、フィーバー中は背景色を変えてください
        if is_fever:
            grass_color = (255, 215, 0)  # フィーバー中の背景色（金色）
        else:
            grass_color = (0, 100, 0)
        screen.fill(BLACK) 
    
        for r, row in enumerate(self.map_data):
            for c, tile in enumerate(row):
                rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile == TILE_PATH: color = (240, 230, 140)
                elif tile == TILE_GRASS: color = grass_color
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
    

    # トラップ設置判定
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
    def __init__(self, waypoints, is_elite = False):
        
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(PURPLE if is_elite else RED) # エリートなら色を変える
        self.rect = self.image.get_rect()
        
        self.waypoints = waypoints
        self.wp_index = 0
        self.speed = 3 if is_elite else 2   # エリートなら速くする
        self.hp = 60 if is_elite else 30     # エリートなら体力を増やす
        self.value = 30 if is_elite else 10  # エリートなら撃破報酬を増やす

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



# 敵と衝突したらダメージを与える処理
class Trap(pygame.sprite.Sprite):
    """
    トラップクラス（道に設置し、敵にダメージを与える）
    """
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        # トラップを分かりやすくするため、半透明のTRAP_COLORにする
        self.image.fill(trap_color) # 変数をTRAP_COLORに修正
        self.image.set_alpha(150) # 半透明化
        self.rect = self.image.get_rect(topleft=(x, y))

        self.damage = 20 # 衝突時のダメージ量
        self.life = 1   # トラップの耐久回数（1回衝突したら消える）

    def update(self, enemy_group, gm):
         # 敵との衝突判定をメインループではなく、トラップのupdate内で行う
        hits = pygame.sprite.spritecollide(self, enemy_group, False)

        if hits:
            for enemy in hits:
                enemy.hp -= self.damage
                self.life -= 1
                print(f"Trap hit! Enemy HP: {enemy.hp}, Trap Life: {self.life}")
                    
                # --- 追加：敵の死亡判定 ---
                if enemy.hp <= 0:
                    gm.chicken += enemy.value  # 報酬を加算
                    enemy.kill()               # 敵を消滅させる

        # トラップの耐久が0になったら削除
        if self.life <= 0:
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
        # 【担当E】is_feverフラグを受け取り、フィーバー中はクールダウンを短くしてください
        # 通常のクールダウン時間
        current_cooldown = self.cooldown
        # フィーバー中はクールダウンを短縮 (例: 半分にする)
        if is_fever:
            current_cooldown = self.cooldown // 2          
        self.timer += 1
        if self.timer >= current_cooldown:
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

    gm = GameManager()
    map_manager = MapManager()
    
    enemy_group = pygame.sprite.Group()
    tower_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()


    
    trap_group = pygame.sprite.Group()
    # 初期配置（テスト用）
    tower_group.add(Tower(14 * TILE_SIZE, 4 * TILE_SIZE))
    
    spawn_timer = 0
    TRAP_COST = 50  # トラップの設置コスト
    running = True
    while running:
        # --- 1. イベント処理 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        #             # 新規配置
        #             # if map_manager.is_placeable(mx, my):
        #             #      cost = 100
        #             #      if gm.chicken >= cost:
        #             #          gm.chicken -= cost
        #             #          tower_group.add(Tower((mx//TILE_SIZE)*TILE_SIZE, (my//TILE_SIZE)*TILE_SIZE))

                # 「右クリックでトラップ配置」処理
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                
                #             # 新規配置
                #             # if map_manager.is_placeable(mx, my):
                #             #      cost = 100
                #             #      if gm.chicken >= cost:
                #             #          gm.chicken -= cost
                #             #          tower_group.add(Tower((mx//TILE_SIZE)*TILE_SIZE, (my//TILE_SIZE)*TILE_SIZE))
                
                
                if event.button == 3: # 右クリック 
                    # タイル座標に変換
                    tx = (mx // TILE_SIZE) * TILE_SIZE
                    ty = (my // TILE_SIZE) * TILE_SIZE
        
                        # 道の上であり、コストがあり、そのマスにトラップがまだない場合
                    if map_manager.is_path(mx, my) and gm.chicken >= TRAP_COST:
                        # 既に同じマスにトラップがあるかチェック
                        existing_trap = None
                        for trap in trap_group:
                            if trap.rect.topleft == (tx, ty):
                                existing_trap = trap
                                break
        
                        if not existing_trap:
                            gm.chicken -= TRAP_COST
                            trap_group.add(Trap(tx, ty))
                            print(f"Trap placed at ({tx}, {ty}). Cost: {TRAP_COST}")
                
            # 【担当E】ここに「フィーバー発動キー（例: Fキー）」の処理を追加してください
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    # ゲージが満タンならフィーバー発動
                    if gm.fever_gauge >= 30:
                        gm.activate_fever()

        # --- 2. 更新処理 ---
        if gm.state == STATE_PLAY:
            gm.update()

            # 敵出現ロジック
            spawn_interval = 120
            if gm.is_fever:
                spawn_interval = 50  # 【担当E】フィーバー中は出現間隔を短くする
            spawn_timer += 1
            if spawn_timer >= spawn_interval: 
                spawn_timer = 0
                is_elite = random.random() < 0.2 # 20%でエリート
                new_enemy = Koukaton(map_manager.waypoints, is_elite)
                enemy_group.add(new_enemy)
                
            if spawn_timer >= 120: 
                
                new_enemy = Koukaton(map_manager.waypoints)
                enemy_group.add(new_enemy)
                spawn_timer = 0
            enemy_group.update(gm)
            tower_group.update(enemy_group, bullet_group, gm.is_fever) # 【担当E】is_feverを渡す
            tower_group.update(enemy_group, bullet_group)
            bullet_group.update()
            trap_group.update(enemy_group, gm)
            # 衝突判定：弾 vs こうかとん
            hits = pygame.sprite.groupcollide(bullet_group, enemy_group, True, False)
            for bullet, hit_enemies in hits.items():
                for enemy in hit_enemies:
                    enemy.hp -= 10
                    if enemy.hp <= 0:
                        enemy.kill()
                        gm.chicken += enemy.value
                        # 【担当E】ここにフィーバーゲージ増加処理を追加
                        if not gm.is_fever:
                             gm.fever_gauge = min(30, gm.fever_gauge + 1)

            gm.check_gameover()

        # --- 3. 描画処理 ---
        screen.fill(BLACK)
        
        if gm.state == STATE_PLAY:
            map_manager.draw(screen, gm.is_fever) # 【担当E】is_feverを渡す
            # 【担当C】trap_group.draw(screen) を追加
            tower_group.draw(screen)
            enemy_group.draw(screen)
            bullet_group.draw(screen)
            trap_group.draw(screen)  # トラップ描画
            
            # UI表示
            txt_chicken = font.render(f"Chicken: {gm.chicken}", True, WHITE)
            txt_life = font.render(f"Life: {gm.life}", True, WHITE)
            screen.blit(txt_chicken, (10, 10))
            screen.blit(txt_life, (10, 50))
            
            # 【担当E】フィーバーゲージのUI表示
            FEVER_MAX = 30
            gauge_ratio = gm.fever_gauge / FEVER_MAX
            pygame.draw.rect(screen, (50, 50, 50), (10, 550, 150, 20), 0) # ゲージ背景
            pygame.draw.rect(screen, (255, 0, 255), (10, 550, 150 * gauge_ratio, 20), 0) # ゲージ本体
            txt_fever = font.render(f"Fever: {gm.fever_gauge}/{FEVER_MAX}", True, WHITE)
            screen.blit(txt_fever, (170, 550))

            # 【担当E】フィーバー中のテキスト表示
            if gm.is_fever:
                sec = gm.fever_timer // FPS + 1
                txt_fever_time = font.render(f"FEVER TIME! ({sec}s)", True, (255, 0, 255))
                screen.blit(txt_fever_time, (SCREEN_WIDTH // 2 - txt_fever_time.get_width() // 2, 10))

        # 【担当A】ここに「elif gm.state == STATE_GAMEOVER:」の描画処理を追加してください

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()