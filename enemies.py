# pygameを読み込む
import pygame
# ランダムに関する計算を簡単にするライブラリを読み込む
import random

# 画面のサイズ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

# 色をRGBで定義。RGB: Red, Green, Blueの値を0~255の256段階で表す
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)

class Block(pygame.sprite.Sprite):
    # ブロックの関数
    def __init__(self,x,y,color,width,height):
        pygame.sprite.Sprite.__init__(self)
        
        # 画像の大きさを設定
        self.image = pygame.Surface([width,height])
        # 指定した色で描画
        self.image.fill(color)
        # 画像を囲む四角形
        self.rect = self.image.get_rect()
        # 四角形の左上すみの座標を設定
        self.rect.topleft = (x,y)


class Ellipse(pygame.sprite.Sprite):
    # 楕円のクラス。ドットを楕円で描画する
    def __init__(self,x,y,color,width,height):
        pygame.sprite.Sprite.__init__(self)
        # 画像の大きさを設定
        self.image = pygame.Surface([width,height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        
        pygame.draw.ellipse(self.image,color,[0,0,width,height])
        # 画像を囲む四角形
        self.rect = self.image.get_rect()
        # 四角形の左上すみの座標を設定
        self.rect.topleft = (x,y)

        
class Slime(pygame.sprite.Sprite):
    # スライムのクラス
    def __init__(self,x,y,change_x,change_y):
        """
        初期化関数
        """
        pygame.sprite.Sprite.__init__(self)
        
        self.change_x = change_x
        self.change_y = change_y
        
        # 画像を読み込む
        self.image = pygame.image.load("slime.png").convert_alpha()
        # 画像を囲む四角形
        self.rect = self.image.get_rect()
        # 四角形の左上すみの座標を設定
        self.rect.topleft = (x,y)
 

    def update(self,horizontal_blocks,vertical_blocks):
        """
        スライムの移動
        """
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        # 画面左端に出た（画像右端の座標が画面左端を飛び出る）
        if self.rect.right < 0:
            # 画面右端に移動（画像左端の座標が、画面右端の座標となる）
            self.rect.left = SCREEN_WIDTH
        # 画面右端に出た（画像左端の座標が画面右端を飛び出る）
        elif self.rect.left > SCREEN_WIDTH:
            # 画像右端の座標が0になる
            self.rect.right = 0
         # 画像の下端が画面の下端を出る
        if self.rect.bottom < 0:
            # 画像の上端が画面の上端になる
            self.rect.top = SCREEN_HEIGHT
        # 画像の上端が画面の上端を飛び出る
        elif self.rect.top > SCREEN_HEIGHT:
            # 画像の下端が0になる
            self.rect.bottom = 0

        # 敵がステージのグリッド状のポイントにいたときに以下が実行
        if self.rect.topleft in self.get_intersection_position():
            # 上下左右の移動をランダムで選択
            direction = random.choice(("left","right","up","down"))
            # 左に移動
            if direction == "left" and self.change_x == 0:
                self.change_x = -2
                self.change_y = 0
            # 右に移動
            elif direction == "right" and self.change_x == 0:
                self.change_x = 2
                self.change_y = 0
            # 上に移動
            elif direction == "up" and self.change_y == 0:
                self.change_x = 0
                self.change_y = -2
            # 下に移動
            elif direction == "down" and self.change_y == 0:
                self.change_x = 0
                self.change_y = 2
                

    def get_intersection_position(self):
        items = []
        # ステージ上の物体を一つずつ確かめていく
        # 行をみていく
        for i,row in enumerate(enviroment()):
            # 列を見ていく
            for j,item in enumerate(row):
                # ステージで「3」と定義されている場所に敵を配置
                if item == 3:
                    items.append((j*32,i*32))

        return items
    
        
def enviroment():
    """
    ステージを定義
    """
    grid = ((0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,3,1),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,3,1),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,3,1),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,3,1),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0))

    return grid

def draw_enviroment(screen):
    for i,row in enumerate(enviroment()):
        for j,item in enumerate(row):
            # ステージで「1」「2」と定義されている場所に線を描画
            if item == 1:
                pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32+32,i*32], 3)
                pygame.draw.line(screen, BLUE , [j*32, i*32+32], [j*32+32,i*32+32], 3)
            elif item == 2:
                pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32,i*32+32], 3)
                pygame.draw.line(screen, BLUE , [j*32+32, i*32], [j*32+32,i*32+32], 3)
