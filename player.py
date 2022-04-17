# pygameを読み込む
import pygame


# 画面のサイズ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576


# 色をRGBで定義。RGB: Red, Green, Blueの値を0~255の256段階で表す
BLACK = (0,0,0)
WHITE = (255,255,255)

class Player(pygame.sprite.Sprite):
    """
    プレイヤーを定義するクラス
    """
    change_x = 0
    change_y = 0
    explosion = False
    game_over = False
    def __init__(self,x,y,filename):
        """
        初期化関数
        """
        pygame.sprite.Sprite.__init__(self)
        # 画像ファイルを読み込み
        self.image = pygame.image.load(filename).convert()
        # colorkeyに黒を設定
        self.image.set_colorkey(BLACK)
        # 画像を囲む四角形を取得
        self.rect = self.image.get_rect()
        # 画像の左上すみの座標を設定
        self.rect.topleft = (x,y)

        img = pygame.image.load("player.png").convert() 

        # 右移動のアニメーション
        self.move_right_animation = Animation(img,32,32)
        # 左移動のアニメーション。画像が水平反転する
        self.move_left_animation = Animation(pygame.transform.flip(img,True,False),32,32)
        # 上移動のアニメーション。90度回転
        self.move_up_animation = Animation(pygame.transform.rotate(img,90),32,32)
        # 下移動のアニメーション。270度回転
        self.move_down_animation = Animation(pygame.transform.rotate(img,270),32,32)
        
        # 敵と衝突したときの爆発アニメーション
        self.explosion_animation = Animation(img,30,30)

        # プレイヤーの画像を読み込む
        self.player_image = pygame.image.load(filename).convert()
        self.player_image.set_colorkey(BLACK)

    def update(self,horizontal_blocks,vertical_blocks):
        """
        update関数
        """

        # 爆発状態ではない
        if not self.explosion:
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
            # プレイヤーの水平方向の移動
            self.rect.x += self.change_x
            self.rect.y += self.change_y

            # プレイヤーと水平方向のブロックとの衝突
            for block in pygame.sprite.spritecollide(self,horizontal_blocks,False):
                self.rect.centery = block.rect.centery
                # ブロックがあるので移動できない
                self.change_y = 0
            # プレイヤーと垂直方向のブロックとの衝突
            for block in pygame.sprite.spritecollide(self,vertical_blocks,False):
                self.rect.centerx = block.rect.centerx
                # ブロックがあるので移動できない
                self.change_x = 0

            # x方向の移動が正
            if self.change_x > 0:
                # 右移動のアニメーション
                self.move_right_animation.update(10)
                # 右移動時の画像を設定
                self.image = self.move_right_animation.get_current_image()
            # x方向の移動が負
            elif self.change_x < 0:
                # 左移動のアニメーション
                self.move_left_animation.update(10)
                # 左移動時の画像を設定
                self.image = self.move_left_animation.get_current_image()

            # y方向の移動が正
            if self.change_y > 0:
                # 下移動のアニメーション
                self.move_down_animation.update(10)
                # 下移動時の画像を設定
                self.image = self.move_down_animation.get_current_image()
            # y方向の移動が負
            elif self.change_y < 0:
                # 上移動のアニメーション
                self.move_up_animation.update(10)
                # 上移動時の画像を設定
                self.image = self.move_up_animation.get_current_image()
        else:
            # プレイヤーが爆発した
            if self.explosion_animation.index == self.explosion_animation.get_length() -1:
                # 少し時間を置いてゲームオーバー
                pygame.time.wait(500)
                self.game_over = True
            self.explosion_animation.update(12)
            # 爆発時の画像を設定
            self.image = self.explosion_animation.get_current_image()
            

    def move_right(self):
        # 右移動の量
        self.change_x = 3

    def move_left(self):
        # 左移動の量
        self.change_x = -3

    def move_up(self):
        # 上移動の量
        self.change_y = -3

    def move_down(self):
        # 下移動の量
        self.change_y = 3

    def stop_move_right(self):
        # 移動が停止したら、デフォルトのプレイヤーの画像を設定
        if self.change_x != 0:
            self.image = self.player_image
        self.change_x = 0

    def stop_move_left(self):
        # 移動が停止したら、水平反転したプレイヤーの画像を設定
        if self.change_x != 0:
            self.image = pygame.transform.flip(self.player_image,True,False)
        self.change_x = 0

    def stop_move_up(self):
        # 移動が停止したら、90度回転したプレイヤーの画像を設定
        if self.change_y != 0:
            self.image = pygame.transform.rotate(self.player_image,90)
        self.change_y = 0

    def stop_move_down(self):
        # 移動が停止したら、270度回転したプレイヤーの画像を設定
        if self.change_y != 0:
            self.image = pygame.transform.rotate(self.player_image,270)
        self.change_y = 0



class Animation(object):
    """
    アニメーションのクラス
    """
    def __init__(self,img,width,height):
        """
        初期化関数
        """
        self.sprite_sheet = img
        self.image_list = []
        self.load_images(width,height)
        self.index = 0
        self.clock = 1
        
    def load_images(self,width,height):
        # スプライトシートに並んだ画像をそれぞれリストに入れる
        for y in range(0,self.sprite_sheet.get_height(),height):
            for x in range(0,self.sprite_sheet.get_width(),width): 
                img = self.get_image(x,y,width,height)
                self.image_list.append(img)

    def get_image(self,x,y,width,height):
        image = pygame.Surface([width,height]).convert()
        image.blit(self.sprite_sheet,(0,0),(x,y,width,height))
        image.set_colorkey((0,0,0))
        return image

    def get_current_image(self):
        # 現在の状態の画像を取得
        return self.image_list[self.index]

    def get_length(self):
        return len(self.image_list)

    def update(self,fps=30):
        # 画像をupdateする
        # frame per secondが30のときはstep数は1
        step = 30 // fps
        if self.clock == 30:
            self.clock = 1
        else:
            self.clock += 1

        if self.clock in range(1,30,step):
            self.index += 1
            if self.index == len(self.image_list):
                self.index = 0
