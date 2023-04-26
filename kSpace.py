import pygame
import os
import random

WIDTH = 700
HEIGHT = 800
FPS = 60

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("kSpace")
clock = pygame.time.Clock()

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,"imgs")
sound_folder = os.path.join(game_folder,"sounds")
background = pygame.image.load(os.path.join(img_folder,"bg5.jpg")).convert()
background_rect = background.get_rect()
main_theme = pygame.mixer.Sound(os.path.join(sound_folder,"space await.mp3"))
second_theme = pygame.mixer.Sound(os.path.join(sound_folder,"Blue Space v0_8.mp3"))
laser2 = pygame.mixer.Sound(os.path.join(sound_folder,"lasers", "laser2.mp3"))
laser4 = pygame.mixer.Sound(os.path.join(sound_folder,"lasers", "laser4.mp3"))
laser6 = pygame.mixer.Sound(os.path.join(sound_folder,"lasers", "laser6.mp3"))
pUp_sound = pygame.mixer.Sound(os.path.join(sound_folder,"powup","powerUp7.mp3"))
pUp_end_sound = pygame.mixer.Sound(os.path.join(sound_folder,"powup","lowDown.mp3"))
game_over_sound = pygame.mixer.Sound(os.path.join(sound_folder, "GameOver.wav"))
player_img = pygame.image.load(os.path.join(img_folder, "player.png")).convert_alpha()
ammo_img = pygame.image.load(os.path.join(img_folder, "ammo.png")).convert_alpha()
shield_img = pygame.image.load (os.path.join(img_folder,"shield.png")).convert_alpha()
double_shot_img = pygame.image.load(os.path.join(img_folder,"doubleshot_img.png")).convert_alpha()
split_shot_img = pygame.image.load(os.path.join(img_folder,"split_shot_img.png")).convert_alpha()
shield_effect_img = pygame.image.load(os.path.join(img_folder,"shield_effect.png")).convert_alpha()
bullet_img = pygame.image.load(os.path.join(img_folder, "bullet.png")).convert_alpha()
blue_bullet = pygame.image.load(os.path.join(img_folder, "blue_bullet.png")).convert_alpha()
red_bullet = pygame.image.load(os.path.join(img_folder, "red_bullet.png")).convert_alpha()
green_bullet = pygame.image.load(os.path.join(img_folder, "green_bullet.png")).convert_alpha()
blue_bullet_right = pygame.image.load(os.path.join(img_folder, "blue_bullet_right.png")).convert_alpha()
red_bullet_right = pygame.image.load(os.path.join(img_folder, "red_bullet_right.png")).convert_alpha()
green_bullet_right = pygame.image.load(os.path.join(img_folder, "green_bullet_right.png")).convert_alpha()
blue_bullet_left = pygame.image.load(os.path.join(img_folder, "blue_bullet_left.png")).convert_alpha()
red_bullet_left = pygame.image.load(os.path.join(img_folder, "red_bullet_left.png")).convert_alpha()
green_bullet_left = pygame.image.load(os.path.join(img_folder, "green_bullet_left.png")).convert_alpha()
enemy_img = pygame.image.load(os.path.join(img_folder, "enemy.png")).convert_alpha()
endless_ammo_img = pygame.image.load(os.path.join(img_folder, "endless_ammo_img.png")).convert_alpha()
hard_enemy_img = pygame.image.load(os.path.join(img_folder, "hard_enemy_img.png")).convert_alpha()

BLACK = (0, 0, 0) 
WHITE = (255, 255, 255)  
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
 
laser_sound = [laser2,laser4,laser6]
bullets_imgs = [blue_bullet, red_bullet,green_bullet]
bullets_imgs_left = [blue_bullet_left, red_bullet_left, green_bullet_left]
bullets_imgs_right = [blue_bullet_right, red_bullet_right, green_bullet_right]
music = [main_theme,second_theme]

scr_data = open("score.txt", "r")
data = scr_data.read()
# best_scr = split_line[0]
rewrite_scr = open("score.txt", "w")
score = 0
font_name = pygame.font.match_font("arial")

def restart():
    global pos, enemy_lowest_speed, enemy_hyghest_speed, enemy_speed_timer, hard_enemt_t,shield_condition, double_shot_condition, split_shot_condition, endless_ammo_condition,t_begin, t, ammo, ammo_t, running, pUp_t
    all_sprites.kill()
    pos = HEIGHT-25
    enemy_lowest_speed = 3
    enemy_hyghest_speed = 5
    enemy_speed_timer = 4500
    hard_enemt_t = 6000
    shield_condition = False
    double_shot_condition = False
    split_shot_condition = False
    endless_ammo_condition =False
    t_begin = 2000
    t = t_begin
    ammo = 0
    ammo_t = 2000
    running = True
    pUp_t = 10000
    player = Player()
    music[random.randrange(len(music))].play(10)
def draw_text (surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render (text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop =(x,y)
    surf.blit(text_surface, text_rect)

class Bullet (pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        if direction == "right":
            self.image = bullets_imgs_right[random.randrange(len(bullets_imgs_right))]
        elif direction =="left":
            self.image = bullets_imgs_left[random.randrange(len(bullets_imgs_left))]
        else :
            self.image = bullets_imgs[random.randrange(len(bullets_imgs))]
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.direction = direction

    def collision (self):
        self.kill()

    def update(self):
        if self.direction == "right":
            self.rect.y -= 8
            self.rect.x += 3
        elif self.direction =="left":
            self.rect.y -= 8
            self.rect.x -= 3
        else :
            self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()
pos = HEIGHT-25 


class Ammo_image(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ammo_img
        self.rect = self.image.get_rect()
        self.rect.center = (20,pos)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,HEIGHT-80)
        self.radius = 27
    
    def move(self):
        self.x_speed = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.x_speed = -8
        if keystate [pygame.K_d]:
            self.x_speed = 8
        if self.rect.x <= 50:
            self.rect.left = 50
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        self.rect.x += self.x_speed

    def update(self):
        self.move()

enemy_lowest_speed = 3
enemy_hyghest_speed = 5
enemy_speed_timer = 4500
hard_enemt_t = 6000

class Enemy (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH)
        self.rect.y = -70
        self.x_speed = random.randrange(-2,2)
        self.y_speed = random.randrange(enemy_lowest_speed,enemy_hyghest_speed)

    def update (self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        if self.rect.right <= 0 or self.rect.left >= WIDTH or self.rect.top >= HEIGHT:
            self.kill()

#class Hard_Enemy (pygame.sprite.Sprite):
    #def __init__(self):
        #self.image = hard_enemy_img
        #self.rect = self.image.get_rect()
        #self.rect.center = (random.randrange(0,WIDTH), -50)
        #if self.rect.x <= WIDTH/2:
            #self.x_speed = random.randrange(1,3)
        #else:
            #self.x_speed = random.randrange(-3,-1)
        #self.y_speed = random.randrange (4,7)

    #def update(self):
        #self.rect.x += self.x_speed
        #self.rect.y += self.y_speed
        #if self.rect.right <= 0 or self.rect.left >= WIDTH or self.rect.top >= HEIGHT:
            #self.kill()

PowerUp_types = ["double_shot","split_shot","endless_ammo","shield"]
shield_condition = False
double_shot_condition = False
split_shot_condition = False
endless_ammo_condition =False

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.type = PowerUp_types[random.randrange(len(PowerUp_types))]
        if self.type == "shield":
            self.image = shield_img
        if self.type == "double_shot":
            self.image = double_shot_img
        if self.type == "split_shot":
            self.image = split_shot_img
        if self.type == "endless_ammo":
            self.image = endless_ammo_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - 55)
        self.rect.y = 0
        
    def update (self):
        global pUp_collision, shield_condition, double_shot_condition, split_shot_condition
        global endless_ammo_condition, double_shot_t, split_shot_t, endless_ammo_t
        self.rect.y += 6
        if self.rect.top > HEIGHT:
            self.kill()
        pUp_collision = pygame.sprite.spritecollide(player, pUp_group,False)
        if pUp_collision:
            pUp_sound.play()
            if self.type == "shield":
                shield_condition = True
            if self.type == "double_shot":
                double_shot_condition = True
                double_shot_t = 20000
            if self.type == "split_shot":
                split_shot_condition = True
                split_shot_t = 20000
            if self.type == "endless_ammo":
                endless_ammo_condition = True
                endless_ammo_t = 10000
            if double_shot_condition and self.type == "split_shot" and double_shot_t <= 3000:
                double_shot_t += 2000
            if split_shot_condition and self.type == "double_shot" and split_shot_t <= 3000:
                split_shot_t += 2000
            self.kill()
            if shield_condition:
                last_player_x = player.rect.centerx
                last_player_y = player.rect.centery
                player.image = shield_effect_img
                player.rect = player.image.get_rect()
                player.rect.centerx = last_player_x
                player.rect.centery = last_player_y
                player.radius = 57

def shoot (x,y,direct,ammo_usage):
    if endless_ammo_condition == False:
        bullet = Bullet(x,y,direct)
        all_sprites.add(bullet)
        bullets.add(bullet)
        if ammo_usage:
            ammo_minus()
    else:
        bullet = Bullet(x,y,direct)
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser_sound[random.randrange(len(laser_sound))].play()

def ammo_minus():
    global pos
    global ammo
    laser_sound[random.randrange(len(laser_sound))].play()
    ammo_images_objects.pop().kill()
    ammo -= 1
    pos +=25


def shield_fall():
    global shield_condition
    pUp_end_sound.play()
    shield_condition = False
    last_player_x = player.rect.x
    last_player_y = player.rect.y
    player.image = player_img
    player.rect = player.image.get_rect()
    player.rect.x = last_player_x
    player.rect.y = last_player_y
    player.radius = 29

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
bullets = pygame.sprite.Group()
pUp_group = pygame.sprite.Group()

ammo_images_objects = []
def en():
        e = Enemy()
        all_sprites.add(e)
        mobs.add(e)
t_begin = 2000
t = t_begin
ammo = 0
ammo_t = 2000

#Цикл гри
running = True
pUp_t = 10000

music[random.randrange(len(music))].play(10)
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and ammo > 0:
                if double_shot_condition and split_shot_condition:
                    shoot(player.rect.x - 3, player.rect.y + 27, "left", True)
                    shoot(player.rect.centerx - 18, player.rect.y + 17, "left", False)
                    shoot(player.rect.centerx - 18, player.rect.y + 17, "normal", False)
                    shoot(player.rect.right - 3, player.rect.y + 27, "right", False)
                    shoot(player.rect.centerx + 18, player.rect.y + 17, "right", False)
                    shoot(player.rect.centerx + 18, player.rect.y + 17, "normal", False)

                elif double_shot_condition and shield_condition:
                    shoot(player.rect.x + 18, player.rect.y + 17, "normal", True)
                    shoot(player.rect.right - 18, player.rect.y + 17, "normal", False)

                elif double_shot_condition :
                    shoot(player.rect.x + 4, player.rect.y + 17, "normal", True)
                    shoot(player.rect.right - 4, player.rect.y + 17, "normal", False)
                elif split_shot_condition:
                    shoot(player.rect.centerx, player.rect.y+5, "left", True)
                    shoot(player.rect.centerx, player.rect.y+5, "right", False)
                    shoot(player.rect.centerx, player.rect.y+5, "mormal", False)
                else:
                    shoot(player.rect.centerx, player.rect.y+5, "mormal", True)
    ammo_t -= 16.666
    if ammo_t <= 0 and ammo < 10:
        ammo += 1
        ammo_t = 2000
        ammo_image = Ammo_image()
        ammo_images_objects.append(ammo_image)
        all_sprites.add(ammo_image)
        pos -= 25

    t -=16.666
    if t <= 0 :
        en()
        if t_begin > 250:
            t_begin -= t_begin / 30
        t = t_begin
    enemy_speed_timer -= 16.666
    if enemy_speed_timer <= 0 and enemy_hyghest_speed <= 12:
        enemy_hyghest_speed += 1
        enemy_speed_timer = 5000
    pUp_t -= 16.666
    if pUp_t <=0:
        powerUp = PowerUp()
        all_sprites.add(powerUp)
        pUp_group.add(powerUp)
        pUp_t = random.randrange(8000,12000)

    if double_shot_condition :        
        double_shot_t -= 16.666
        if double_shot_t <= 0:
            double_shot_condition = False
            pUp_end_sound.play()

    if split_shot_condition:
        split_shot_t -=16.666
        if split_shot_t <= 0:
            split_shot_condition = False
            pUp_end_sound.play()
 
    
    if endless_ammo_condition:
        endless_ammo_t -=16.666
        if endless_ammo_t <=0:
            endless_ammo_condition = False
            pUp_end_sound.play()

    #hard_enemt_t -=16.666
    #if hard_enemt_t <= 0:
        #hard_enemy = Hard_Enemy()
        #all_sprites.add(hard_enemy)
        #mobs.add(hard_enemy)
        #hard_enemt_t = random.randrange (3000, 5000)

    all_sprites.update()

    hits = pygame.sprite.groupcollide(mobs,bullets,True,True)

    if hits:
        score += 10
    
    selfCollision = pygame.sprite.spritecollide(player, mobs, shield_condition, pygame.sprite.collide_circle)
    if selfCollision and shield_condition:
        shield_fall()
    elif selfCollision:
        main_theme.stop()
        second_theme.stop()
        game_over_sound.play()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # if score > int(best_scr):
                #     best_scr = score
                #     rewrite_scr.write(str(best_scr))
                draw_text (screen, "GAME OVER\n" + str(score) + "\n" + "best: " + str(best_scr), 40, WIDTH/2, HEIGHT/2 - 40)
                pygame.display.flip()

    #Рендерінгінг012356789+-*/
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 19, WIDTH - 30, 10)
    pygame.display.flip()

pygame.quit()
