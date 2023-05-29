import math
import random
import sys
import time
from typing import Any

import pygame as pg

WIDTH = 1600  # ゲームウィンドウの幅
HEIGHT = 900  # ゲームウィンドウの高さ

class Player(pg.sprite.Sprite):
    
    delta = {  # 押下キーと移動量の辞書
        pg.K_LEFT: (+1, 0),
        pg.K_RIGHT: (-1, 0),
    }

    def __init__(self):
        
        super().__init__()
        self.image = pg.Surface((120, 120))
        pg.draw.circle(self.image, [255, 0, 0], (60, 60), 30)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (800,700)
        self.speed = 1
        self.mx = 0
        
    def update(self, key_lst: list, screen: pg.Surface):
        for k, mv in __class__.delta.items():
                if key_lst[k]:
                    self.rect.move_ip(-self.speed*mv[0], -self.speed*mv[1])
        screen.blit(self.image, self.rect)

def main():
    pg.display.set_caption("アイスホッケーこうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    lock = pg.time.Clock()
    bg_image = pg.Surface((WIDTH, HEIGHT)) 
    pg.draw.rect(bg_image, (255, 230, 255), pg.Rect(0, 0, WIDTH, HEIGHT)) #黒い四角を描く 
    bd_image = pg.Surface((WIDTH, HEIGHT)) 
    pg.draw.rect(bd_image, (255, 255, 255), pg.Rect(400, 0, 800, HEIGHT))
    bd_image.set_colorkey((0,0,0))
    player = Player()
    while True:
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0         
        screen.blit(bg_image, [0, 0])
        screen.blit(bd_image, [0, 0])
        player.update(key_lst, screen)
        pg.display.update()
        

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
