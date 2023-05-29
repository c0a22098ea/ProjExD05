import random
import sys
import time

import pygame as pg

WIDTH = 1600  # ゲームウィンドウの幅
HEIGHT = 800  # ゲームウィンドウの高さ

def check_left(obj: pg.Rect) -> tuple[bool]:
    """
    オブジェクトが画面内か画面外かを判定し、真理値タプルを返す
    引数　obj：オブジェクト(こうかとん)SurfaceのRect
    戻り値：縦方向のはみ出し判定（画面内：True／画面外：False）
    """
    tate = True

    if obj.top < 0 or HEIGHT < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return tate


class Difficulty_level:
    """
    ゲームの難易度に関するクラス
    """
    def __init__(self, level: str):
        """
        ゲームの難易度を設定・難易度を表示する
        引数：難易度の名前
        """
        self.level = level
        self.color = (0, 0, 0)
        self.font = pg.font.Font(None, 50)
        self.image = self.font.render(f"level: {self.level}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH-150, HEIGHT-50
        self.flag = 0
        self.str_flag = 0
        self.count = 200

    def change_level(self, change_level: str, count: int):
        """
        ゲームの難易度を変更する
        引数１：変更する難易度の名前
        引数２：敵機の出現する間隔
        """
        self.level = change_level
        self.str_flag = 1 #  難易度を一度変更すると再び変更できなくする
        self.count = count

    def update(self, screen: pg.Surface):
        """
        ゲーム難易度を表示する
        引数：画面Surfase
        """
        self.image = self.font.render(f"level: {self.level}", 0, self.color)
        screen.blit(self.image, self.rect)


class Bird(pg.sprite.Sprite):
    """
    ゲームキャラクター(こうかとん)に関するクラス
    """

    delta = {  # 押下キーと移動量の辞書
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, +1),
    }

    def __init__(self, xy: tuple[int, int]):
        """
        こうかとん画像Surfaceを生成する
        引数1:こうかとん画像の位置座標タプル
        """

        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load("ex01/fig/3.png"), 0 , 2.0)
        self.image = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.speed = 6

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてこうかとんを上下に移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                self.rect.move_ip(0, +self.speed*mv[1])
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        if check_left(self.rect) != (True):
            for k, mv in __class__.delta.items():
                if key_lst[k]:
                    self.rect.move_ip(0, -self.speed*mv[1])

        screen.blit(self.image, self.rect)


class Enemy(pg.sprite.Sprite):
    """
    障害物に関するクラス
    """
    imgs = [pg.image.load(f"ex04/fig/alien{i}.png") for i in range(1, 4)]

    def __init__(self):
        """
        障害物の画像Surfaceを生成する
        """

        super().__init__()
        self.image = random.choice(__class__.imgs)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH + 50, random.randint(50, (HEIGHT - 50))
        self.vx = -6
         

    def update(self, diff_level: Difficulty_level):
        """
        敵機を速度ベクトルself.vyに基づき移動（左向きに向かって移動）させる
        難易度によって敵機の速さを変える
        引数 screen：画面Surface
        """
        if diff_level.flag == 2:
            self.vx = -8
        if diff_level.flag == 2:
            self.speed  = -12
        self.rect.move_ip(self.vx, 0)
        if self.rect.right < 0:
            self.kill()


class Coin(pg.sprite.Sprite):
    """
    コインに関するクラス
    """
    colors = [(237, 204, 45), (233, 233, 233), (233, 233, 233), (233, 233, 233)]

    def __init__(self):
        """
        コイン円Surfaceを生成する
        """

        super().__init__()
        rad = 30  # 爆弾円の半径：10以上50以下の乱数
        color = random.choice(__class__.colors)  # 爆弾円の色：クラス変数からランダム選択
        self.image = pg.Surface((2*rad, 2*rad))
        pg.draw.circle(self.image, color, (rad, rad), rad)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.vx, self.vy = -6, 0
        self.rect.center = WIDTH + 50, random.randint(rad, (HEIGHT-rad))

    def update(self):
        """
        コインをを速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        self.rect.move_ip(self.vx, self.vy)
        if self.rect.right < 0:
            self.kill()


def main():
    pg.display.set_caption("避けろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("ex01/fig/pg_bg.jpg")
    re_bg_img = pg.transform.flip(bg_img, True, False)

    diff_level = Difficulty_level("normal")
    bird = Bird([100,200])
    emys = pg.sprite.Group()
    coins = pg.sprite.Group()
    tmr = 0
    
    while True:
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_2 and diff_level.str_flag == 0:
                diff_level.change_level("Hard", 150)
                diff_level.flag = 1 #  難易度に対応したフラグを立てる
            if event.type == pg.KEYDOWN and event.key == pg.K_3 and diff_level.str_flag == 0:
                diff_level.change_level("Lunatic", 100)
                diff_level.flag = 2
        tmr += 1
        x = tmr%3200

        
        if tmr%diff_level.count == 0:  # 難易度によって敵機の出現フレームを変化させている。
            emys.add(Enemy())
        if tmr%200 == 0: #  200フレームごとにコインを出現させる
            coins.add(Coin())

        for up in pg.sprite.spritecollide(bird, coins, True):
            diff_level.count -= 2 #  コインを獲得した時、敵機の出現間隔を２づつ短くする
        if len(pg.sprite.spritecollide(bird, emys, True)) != 0:
                pg.display.update()
                time.sleep(2)
                return


        screen.blit(bg_img ,[-x, 0] )
        screen.blit(re_bg_img, [1600-x, 0])
        screen.blit(bg_img ,[3200-x, 0] )

        coins.update()
        coins.draw(screen)
        emys.update(diff_level)
        emys.draw(screen)
        bird.update(key_lst, screen)
        diff_level.update(screen)
        pg.display.update()
        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()