# pygameを読み込む
import pygame

# 自作クラスGameを読み込む
from game import Game

# 画面のサイズ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

def main():
    """
    main関数
    """

    # pygameを初期化。最初に必ず必要な処理。
    pygame.init()

    # 画面のサイズを設定
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    # 画面のタイトルを設定
    pygame.display.set_caption("PACMAN")

    # ゲーム実行フラグ
    done = False
    # 時計を設定
    clock = pygame.time.Clock()
    # Gameクラスからインスタンスを生成
    game = Game()

    # 実行フラグがTrueである限り、以下を実行する
    while not done:
        # Gameクラスのprocess_events関数を実行。戻り値はゲーム実行フラグ
        done = game.process_events()
        # Gameクラスのrun_logic関数を実行
        game.run_logic()
        # Gameクラスのdisplay_frame関数を実行
        game.display_frame(screen)
        # 時計のtick?を実行
        clock.tick(30)
    # 実行フラグがFalseになったらpygameのquit関数を実行。ゲームが終了する。
    pygame.quit()

if __name__ == '__main__':
    main()
