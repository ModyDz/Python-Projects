import pygame as pg
import random
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    RLEACCEL,
    QUIT,
)
class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pg.image.load("Player.png").convert()
        self.surf = pg.transform.smoothscale(self.surf, (75, 75))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
    def move(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -10)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 10)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-10, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(10, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pg.image.load("Enemy.png").convert()
        self.surf = pg.transform.smoothscale(self.surf, (75, 75))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 15)
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
class Cloud(pg.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pg.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
class Missile(pg.sprite.Sprite):
    def __init__(self, pos):
        super(Missile, self).__init__()
        self.surf = pg.image.load("Missile.png").convert()
        self.surf = pg.transform.smoothscale(self.surf, (60, 30))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=pos)
    def update(self):
        self.rect.move_ip(10, 0)
        if self.rect.right < 0:
            self.kill()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
pg.init()
pg.display.set_caption('Space Invaders')
window = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
ADDENEMY = pg.USEREVENT
pg.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pg.USEREVENT + 2
pg.time.set_timer(ADDCLOUD, 1000)
clouds = pg.sprite.Group()
player = Player()
enemies = pg.sprite.Group()
missiles = pg.sprite.Group()
all_sprites = pg.sprite.Group()
all_sprites.add(player)
running = True
while running:
    clock = pg.time.Clock()
    clock.tick(60)
    for xd in pg.event.get():
        if xd.type == pg.QUIT:
            running = False
        elif xd.type == KEYDOWN:
            if xd.key == K_ESCAPE:
                running = False
        elif xd.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif xd.type == pg.MOUSEBUTTONUP:
                missile = Missile(player.rect.midright)
                missiles.add(missile)
                all_sprites.add(missile)
        elif xd.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
    pressed_keys = pg.key.get_pressed()
    player.move(pressed_keys)
    missiles.update()
    enemies.update()
    clouds.update()
    window.fill((135, 206, 250))
    pg.sprite.groupcollide(enemies, missiles, True, True)
    for entity in all_sprites:
        window.blit(entity.surf, entity.rect)
    pg.display.flip()
    if pg.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False