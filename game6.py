#08/07/2025



import pygame
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH ,SCREEN_HEIGHT))
pygame.display.set_caption("Clues in the Dark")

#set a framerate
clock = pygame.time.Clock()
FPS = 60

#define game variables
GRAVITY = 0.75
TILE_SIZE = 40

#define palyer action variables
moving_left = False
moving_right = False
shoot = False

#load images
#bullet
bullet_img = pygame.image.load().convert_alpha()
# put the image path()


#define Colours
BG = (144,201,120)
BLACK = (0, 0, 0)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, (0, 0, 0), (0, 300), (SCREEN_WIDTH, 300))



class Soldier(pygame.sprite.Sprite):
    def __init__(self,char_type,x,y,scale,speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        #we are not using granadees
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        #load all image for the palyers
        animation_types = ['IDle','Run','jump', 'Death']

        for animation in animation_types:
            #reset temporary list of the images
            temp_list = []
            #count number of files in the folder
            num_of_frames = len(os.listdir())#input the animation part
            for i in range(num_of_frames):
                img = pygame.image.load() #image and animation
                img = pygame.transform.scale(img,(int(img.get_width()*scale),int(img.get_height()*scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list) 


       
        self.image = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height() * scale)))
        #self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x , y)


    def update(self):
        self.update_animation()
        self.char_alive()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1


    def move(self, moving_left, moving_right):
        #rest movement variable
        dx = 0
        dy = 0

        #assign movement variable if moving left or right
        if moving_left:
            dx =- self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        #jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

		#apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

		#check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False


        ##update rectangle psotion
        self.rect.x += dx
        self.rect.y += dy


    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
			#reduce ammo
            self.ammo -= 1

    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN =100
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        
        if pygame.time.get_ticks() - self.update_time>ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        
        #if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:    
                self.frame_index = 0


    def update_action(self, new_action):
		#check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
			#update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    #Dead
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)


    def draw(self):
        screen.blit(pygame.transform.flip(self.image,self.flip,False), self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,directon):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = directon
    
    def update(self):
        #move bullet
        self.rect.x += (self.direction * self.speed)
        #check if the bullect has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        # check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        if pygame.sprite.spritecollide(enemy, bullet_group, False):
            if enemy.alive:
                enemy.health -= 25
                self.kill()

#create sprite groups
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()



player = Soldier('player',200,200,3,5)
enemy = Soldier('enemy',400,200,3,5)
enemy2 = Soldier('enemy',300,300,3,5,20,0)


run = True
while run:

    clock.tick(FPS)

    draw_bg()

    
    player.update()
    player.draw()
    
    for enemy in enemy_group:
        enemy.update()
        enemy.draw()
    # do i nedd to add the update ocde ?
    bullet_group.update()
    bullet_group.draw(screen)

    #update player actions
    if player.alive:
        #shoot bullets
         if shoot:
            player.shoot()
        #we dont have the grenades


    # update player actions
    if player.alive:
        #shoot bullets
            if shoot:
                player.shoot()
            if player.in_air:
                player.update_action(2) #2 : jump
    elif moving_left or moving_right:
            player.update_action(1) #1 : run
    else:
            player.update_action(0) #0: idle
    player.move(moving_left, moving_right)


    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
            run = False

        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE:
                shoot = True
                #if event.key == pygame.K_w and player.alive:
				#player.jump = True
			    ##run = False


        #keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            
                
    pygame.display.update()

pygame.quit()