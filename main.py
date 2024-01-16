import random
import pygame
import math
pygame.font.init()
pygame.mixer.init()

cheat_mode = False
WIDTH,HEIGHT = 900,500
BORDER = pygame.Rect(WIDTH//2-5,0,10,HEIGHT)
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("First Game!")
FPS = 60
SPACESHIP_WIDTH,SPACESHIP_HEIGHT = 55,40
VELOCITY = 5
BULLET_VELCOITY = 7
MAX_BULLETS = 3
YELLOW_HIT= pygame.USEREVENT +1
RED_HIT = pygame.USEREVENT +2
HEALTH_FONT = pygame.font.SysFont('comicscans',40)
WINNER_FONT = pygame.font.SysFont('cosmicans',100)
BULLET_HIT_SOUND = pygame.mixer.Sound("Assets/Grenade+1.mp3")
BULLET_FIRE_SOUND = pygame.mixer.Sound("Assets/Gun+Silencer.mp3")



YELLOW_SPACESHIP_IMAGE = pygame.image.load("Assets/spaceship_yellow.png")
YELLOW_SPACESHIP = pygame.transform.scale(pygame.transform.rotate(YELLOW_SPACESHIP_IMAGE,90),(SPACESHIP_WIDTH,SPACESHIP_HEIGHT))
RED_SPACESHIP_IMAGE = pygame.image.load("Assets/spaceship_red.png")
RED_SPACESHIP = pygame.transform.scale(pygame.transform.rotate(RED_SPACESHIP_IMAGE,270),(SPACESHIP_WIDTH,SPACESHIP_HEIGHT))
SPACE = pygame.transform.scale(pygame.image.load("Assets/space.png"),(WIDTH,HEIGHT))



def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
    WINDOW.blit(SPACE,(0,0))
    pygame.draw.rect(WINDOW,"black",BORDER)
    red_health_text = HEALTH_FONT.render("Health: "+str(red_health),1,"white")
    yellow_health_text = HEALTH_FONT.render("Health: "+str(yellow_health),1,"white")
    WINDOW.blit(red_health_text,(WIDTH-red_health_text.get_width()-10,10))
    WINDOW.blit(yellow_health_text,(10,10))
    WINDOW.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WINDOW.blit(RED_SPACESHIP,(red.x,red.y))
    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW,"yellow",bullet)
    for bullet in red_bullets:
         pygame.draw.rect(WINDOW,"red",bullet)
    pygame.display.update()

def yellow_handle_movements(keys_pressed,yellow):
    if keys_pressed[pygame.K_w] and yellow.y-VELOCITY >0: #up
            yellow.y -= VELOCITY
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY >0: #left
            yellow.x -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y+VELOCITY + yellow.height<HEIGHT: #down
            yellow.y += VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width< BORDER.x: #right
            yellow.x += VELOCITY

def red_handle_movements(keys_pressed,red):
    if keys_pressed[pygame.K_UP] and red.y-VELOCITY>0: #up
            red.y -= VELOCITY
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x+BORDER.width: #left
            red.x -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height<HEIGHT: #down
            red.y += VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY+red.width < WIDTH: #right
            red.x += VELOCITY

def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELCOITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
            BULLET_HIT_SOUND.play()
        if bullet.x > WIDTH:
             yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        if cheat_mode:
            angle = cheat(bullet,yellow)
            move_bullet(bullet,angle,BULLET_VELCOITY)
        else:
            bullet.x -= BULLET_VELCOITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
            BULLET_HIT_SOUND.play()
        if bullet.x < 0:
             red_bullets.remove(bullet)
        
    for red_bullet in red_bullets:
         for yellow_bullet in yellow_bullets:
              if(red_bullet.colliderect(yellow_bullet)):
                    red_bullets.remove(red_bullet)
                    yellow_bullets.remove(yellow_bullet)
                    BULLET_HIT_SOUND.play()

            
def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,"white")
    WINDOW.blit(draw_text,(WIDTH//2 - draw_text.get_width()//2,HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)  

def cheat(bullet,yellow):
     dx = yellow.x - bullet.x
     dy = yellow.y - bullet.y
     angle = math.atan2(dy,dx)
     return angle

def move_bullet(bullet,angle,speed):
     bullet.x += speed*math.cos(angle)
     bullet.y += speed*math.sin(angle)

              
           

def main():
    red = pygame.Rect(700,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    clock = pygame.time.Clock()
    yellow_bullets = []
    red_bullets = []
    red_health = 5
    yellow_health = 5
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LMETA and len(yellow_bullets) < MAX_BULLETS: #left command
                    bullet = pygame.Rect(yellow.x+yellow.width,yellow.y+yellow.height//2,10,5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RMETA and len(red_bullets) < MAX_BULLETS: #right command 
                      bullet = pygame.Rect(red.x,red.y+red.height//2,10,5)
                      red_bullets.append(bullet)
                      BULLET_FIRE_SOUND.play()
                    

            if event.type == RED_HIT:
                 red_health -= 1
            if event.type == YELLOW_HIT:
                 yellow_health -=1

        draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health)
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movements(keys_pressed,yellow)
        red_handle_movements(keys_pressed,red)
        handle_bullets(yellow_bullets,red_bullets,yellow,red)

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow wins"
        if yellow_health <= 0:
             winner_text = "Red wins"
        if winner_text != "":
            draw_winner(winner_text)
            break

        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()

