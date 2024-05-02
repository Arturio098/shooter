from pygame import *
from random import randint
from time import time as tm 
#создай окно игры

# number = input('Какая сложность')

window = display.set_mode((800,500))
display.set_caption('Космическое путешествие')
win_picture = transform.scale(image.load('turniket.jpg'), (900, 500))


clock = time.Clock()

mixer.init()
# mixer.music.load('sub.wav')
# mixer.music.play()

# fire = mixer.Sound('fire.ogg')


class Game_Sprite(sprite.Sprite):
    def __init__(self , player_image , player_x , player_y , w , h , player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (w , h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x  
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image , (self.rect.x, self.rect.y))

class Pplayer(Game_Sprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[ K_a ] and self.rect.x > 5:
            self.rect.x  -= self.speed
        if key_pressed[ K_d ] and self.rect.x < 730:
            self.rect.x  += self.speed
    def fiire(self):
        bullet = Bullet('zhurnal.jpg', self.rect.centerx, self.rect.top, 30, 20, -15)
        bullets.add(bullet)

scorp = 0
lost = 0

class Enemy(Game_Sprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80,720)
            self.rect.y = 0
            lost += 1

class Port_Enemy(Game_Sprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80,720)
            self.rect.y = 0

class Bullet(Game_Sprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0 :
            self.kill()

geroy = Pplayer('oh.png', 5, 400, 150, 100, 10)

font.init()
font = font.SysFont('Arial', 50)

win = font.render( ' YOU SAVE THE PEINCESS ' , True , (255,0,0))
not_win = font.render( ' YOU DIE ' , True , (255,0,0))

aliens = sprite.Group()
for i in range(5):
    alien = Enemy('aaaa.png', randint(80,720), -40, 80, 50, randint(1,3))
    aliens.add(alien)

bossess = sprite.Group()
for i in range(3):
    boss = Port_Enemy('port.png', randint(80,720), -40, 80, 50, randint(1,3))
    bossess.add(boss)

bullets = sprite.Group()

num_fire = 0
rel_num = 0
life = 5

game = True
finish = False
while game:
    
    
    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                if num_fire < 5 and rel_num == False:
                    num_fire += 1
                    geroy.fiire()
                    # fire.play()
                if num_fire >= 5 and rel_num == False:
                    rel_num = True
                    timer_old = tm() 



    if finish != True:

        window.blit(win_picture,(0,0))

        text_lose = font.render("Пропущено:" + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10, 20))
        aliens.update()
        bossess.update()
        geroy.update()
        bullets.update()

        bullets.draw(window)
        geroy.reset()
        aliens.draw(window)
        bossess.draw(window)
        
        if rel_num == True:
            timer_new = tm()
            if timer_new - timer_old < 3:
                real_number = font.render("Поздравляю, у вас перезарядка", 1, (255,0,0))
                window.blit(real_number, (10, 200))
            else:
                rel_num = False
                num_fire = 0    
        spisok = sprite.groupcollide(aliens, bullets, True, True)
        text_win = font.render("Счёт:" + str(scorp), 1, (255,255,255))
        window.blit(text_win, (10, 60))
        for h in spisok:
            scorp += 1
            alien = Enemy('aaaa.png', randint(80,720), -40, 80, 50, randint(1,3))
            aliens.add(alien)

        if sprite.spritecollide(geroy, aliens, False) or sprite.spritecollide(geroy, bossess, False):
            sprite.spritecollide(geroy, bossess, True)
            sprite.spritecollide(geroy, aliens, True)
            alien = Enemy('aaaa.png', randint(80,720), -40, 80, 50, randint(1,3))
            aliens.add(alien)
            life -= 1
            
            


        if scorp >= 30:
            finish = True 
            win_win = font.render("Поздравляю вас повысили", 1, (255,255,255))
            window.blit(win_win, (50, 200))
            win_win2 = font.render("до охранника чипсов", 1, (255,255,255))
            window.blit(win_win2, (100, 250))
        if lost >= 3 or life <= 0:
            finish = True 
            looooose = font.render( "Поздравляю вас повысили", 1, (255,255,255))
            window.blit(looooose, (50, 200))
            loooooooooose = font.render("до охранника пустоты", 1, (255,255,255))
            window.blit(loooooooooose, (100, 250))

        
        life_win = font.render('жизней осталось:' + str(life), 1, (255,255,255))
        window.blit(life_win, (250, 50))

    display.update()
    clock.tick(60)

