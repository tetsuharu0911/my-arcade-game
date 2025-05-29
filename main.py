import pygame
import sys # sysモジュールをインポートして、プログラムを安全に終了できるようにします

# 1. Pygameの初期化
pygame.init()

# 2. 画面（ウィンドウ）の設定
screen_width = 800  # ウィンドウの幅
screen_height = 600 # ウィンドウの高さ
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("初めてのPyGameウィンドウ") # ウィンドウのタイトル

# 3. ゲームループ
running = True
while running:
    # 4. イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # ウィンドウの閉じるボタンがクリックされたら
            running = False

    # 5. 画面の描画 (今はまだ何もないので、背景色だけ設定してみましょう)
    screen.fill((0, 0, 255))  # RGBで色を指定 (0, 0, 255) は青色

    # 6. 画面の更新
    pygame.display.flip() # 画面全体を更新

# 7. Pygameの終了処理
pygame.quit()
sys.exit()