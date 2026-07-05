#initialization
import pygame
import random 
import math
pygame.init()
pygame.font.init()
win_score = 5 
# set up screen
SPAWN_BALL = pygame.USEREVENT + 1
should_spawn = True
should_move = False
screen = pygame.display.set_mode((600,600))
button = pygame.Rect(190,400,200,100)
paddle1 = pygame.image.load("player1.png")
paddle2 = pygame.image.load("player2.png")
clock = pygame.time.Clock()
start_screen = True
running = False
pygame.display.set_caption("pong")
pygame.display.set_icon(pygame.image.load("soccer-ball-variant.png"))
ball_image = pygame.image.load("soccer-ball-variant.png")
menue_ball_image = pygame.transform.smoothscale(ball_image, (180,180))
font_surface = pygame.font.SysFont("Arial", 32) # FIX TEXT
font_countdown = pygame.font.SysFont("Arial", 200)
font_title=pygame.font.SysFont("Arial", 65)
text_surface = font_surface.render("  Click 2 Start", True, (9, 9, 9))
text_surface2 = font_surface.render("  Click 2 Quit!", True, (9, 9, 9))

text_title = font_title.render("Pong Game by Chaniel", False, (0,0,0),None,700)
maximum_score = font_surface.render("First to 5!", True,(0,0,0))
# game variables
player1_score  = 0
player2_score = 0
player_that_won = 0
ballX = 300
ballY = 300
in_bounds = True
in_bounds_paddle1 = True
in_bounds_paddle2 = True
reduce=1.414
paddleX1 = 10
paddleY1=250
paddleX2 = 570
paddleY2 = 250
paddle_speed = 0.4
ball_speedX= random.choice([-1.00001, 1.00001])
ball_speedY = 1.000001
ball_angle = 0
speed_modifier = 0.3
speed_modifier_max = 1
end_screen = False
def spawning_ball():
    global ballX
    global ballY
    global should_spawn
    global ball_image
    global should_move
    global ball_speedX
    global ball_speedY
    global speed_modifier
    global  ball_angle
    screen.blit(ball_image,(ballX,ballY))
    if should_spawn == True:
        should_move = False
        should_spawn = False
        ball_angle = 0 
        speed_modifier = 0.2
        ball_speedX = random.choice([-1.00001, 1.00001])
        ball_speedY = 1.00001
        ballX =300
        ballY =300
        pygame.time.set_timer(SPAWN_BALL, 500, loops=0)
def ball(x,y):
    global ballX
    global ballY
    global ball_image
    global should_move
    global ball_angle
    
    if should_move == True:
        screen.blit(ball_image,(ballX,ballY))
        ballX += (speed_modifier)*(ball_speedX * (math.cos(ball_angle)))
        ballY += (speed_modifier)*(ball_speedY * (math.sin(ball_angle))) 
def paddle_movment1(x,y):

    global paddleX1
    global paddleY1
    global paddle1
    global screen
    global paddle_speed
    global should_spawn
    global ball_image
    global  ball_speed

    screen.blit(paddle1,(paddleX1,paddleY1))
    if x <570 and x> 0 and y>0 and y<510:
        in_bounds_paddle1 = True
    else:
        in_bounds_paddle1 = False
    keys = pygame.key.get_pressed()
    if in_bounds_paddle1 == True:
        if keys[pygame.K_s]: paddleY1+=paddle_speed
        if keys[pygame.K_w]: paddleY1-=paddle_speed
           
    if in_bounds_paddle1 == False:
         if paddleY1<0:
             paddleY1+=0.2
         if paddleY1>510:
             paddleY1-=0.2
def check_paddle_colision():
    global paddle1
    global paddle2
    global ball_image
    global ball_image_hitbox
    global paddle1_hitbox
    global paddle2_hitbox
    global ball_speedX
    global ball_speedY
    global ball_angle
    global speed_modifier
    global ballX
    global speed_modifier_max
    ball_image_hitbox = pygame.mask.from_surface(ball_image)
    paddle1_hitbox = pygame.mask.from_surface(paddle1)
    paddle2_hitbox = pygame.mask.from_surface(paddle2)
    ball_rect = ball_image.get_rect()
    ball_rect.x = ballX
    ball_rect.y = ballY
    paddle2_rect = paddle2.get_rect()
    paddle2_rect.x = paddleX2
    paddle2_rect.y = paddleY2
    paddle1_rect = paddle1.get_rect()
    paddle1_rect.x = paddleX1
    paddle1_rect.y = paddleY1
    offset2 = (
    paddle2_rect.x - ball_rect.x,
    paddle2_rect.y - ball_rect.y
    )

    offset1 = (
    paddle1_rect.x - ball_rect.x,
    paddle1_rect.y - ball_rect.y
    )
    
    if ballY <0 or ballY>580:
        ball_speedY *=-1

    if ball_image_hitbox.overlap(paddle1_hitbox, offset1):
        ballX+=0.3
        ball_speedX = ball_speedX*-1
        ball_angle = ((ballY - (paddleY1 + 100)) / 100)*0.7854
        if speed_modifier<=speed_modifier_max: 
            speed_modifier+=0.05     
    
    if ball_image_hitbox.overlap(paddle2_hitbox, offset2):
        ballX-=0.3
        ball_angle = -((ballY - (paddleY2 + 100)) / 100)*0.7854
        ball_speedX = ball_speedX*-1
        if speed_modifier<=speed_modifier_max: 
            speed_modifier+=0.05    
def paddle_movment2(x,y):
    global paddle1
    global paddleX2
    global paddleY2
    global paddle2
    global paddle1
    global screen
    global paddle_speed
    screen.blit(paddle2,(paddleX2,paddleY2))
    if y>0 and y<510:
        in_bounds_paddle2 = True
    else:
        in_bounds_paddle2 = False
    keys = pygame.key.get_pressed()
    if in_bounds_paddle2 == True:
        if keys[pygame.K_DOWN]: paddleY2+=paddle_speed
        if keys[pygame.K_UP]: paddleY2-=paddle_speed
           
    if in_bounds_paddle2 == False:
         if paddleY2<0:
             paddleY2+=0.2
         if paddleY2>510:
             paddleY2-=0.2
def score_manager():
    global win_score
    global player1_score; global player2_score; global ballX;global should_spawn; global player1_win; global player1_win
    global end_screen; global running
    if ballX<0:
        print("player 2 scores")
        player2_score+=1
        should_spawn = True
    if ballX>575:
        print("player 1 scores")
        player1_score+=1
        should_spawn = True
    if player1_score==win_score or player2_score==win_score:
        running = False
        end_screen = True
   
while start_screen:
    
    screen.fill((137,207,240))
    mouse_position = pygame.mouse.get_pos()
    pygame.draw.rect(screen, (200, 100, 100), button)
    screen.blit(text_surface, (200, 425))
    screen.blit((text_title),(20,100))
    screen.blit(menue_ball_image,(370,200))
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start_screen = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if button.collidepoint(mouse_position):
                    screen.fill((137,207,240))
                    pygame.display.flip() 
                    for i in range(3):
                        text_countdown = font_countdown.render(str(3-i), True, (0, 0, 0))
                        screen.blit(text_countdown,(250,200))
                        pygame.display.flip() 
                        pygame.time.delay(600)
                        screen.fill((137,207,240))
                        pygame.display.flip()
                    running = True
                    start_screen = False
        
            
    
    pygame.display.flip() 
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if  event.type == SPAWN_BALL:
            should_move = True
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]: should_spawn = True
    screen.fill((137,207,240))
    paddle_movment1(paddleX1,paddleY1)
    paddle_movment2(paddleX2,paddleY2)
    score_manager()    
    spawning_ball()
    ball(ballX,ballY)  
    check_paddle_colision()
    screen.blit(maximum_score,(245,20))
    screen.blit(font_countdown.render(str(player1_score),True,(0,0,0)),(30,10))
    screen.blit(font_countdown.render(str(player2_score),True,(0,0,0)),(480,10))
#if should_spawn is set equal to true outside of the game loop then ball movment works
    should_spawn = False
    pygame.display.flip() 
pygame.display.flip() 

while end_screen:
    screen.fill((137,207,240)) 
    pygame.draw.rect(screen, (200, 100, 100), button)
    screen.blit(text_surface2, (200, 425))
    if player1_score==win_score:
        screen.blit(font_title.render("Player 1 Wins!!!",True,(0,0,0)),(134,195))
        screen.blit(font_title.render("Thank you for playing!!!",True,(0,0,0)),(24,285))
    if player2_score==win_score:
        screen.blit(font_title.render("Player 2 Wins!!!",True,(0,0,0)),(134,195))
        screen.blit(font_title.render("Thank you for playing!!!",True,(0,0,0)),(24,285))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_screen = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if button.collidepoint(mouse_position):
                    screen.fill((137,207,240))
                    end_screen = False
                    pygame.display.flip() 
                    
                    
    pygame.display.flip() 

pygame.quit