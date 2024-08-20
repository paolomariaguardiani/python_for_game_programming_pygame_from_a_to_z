import pygame
pygame.init()

w_width = 500
w_height = 500

screen = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Adding Jump Logic")

# Creating object
x = 0
y = 0
width = 50
height = 50
vel = 5

clock = pygame.time.Clock()

# Jump variables
is_jump = False
jump_count = 10

done = True # better is gameloop = True
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and y > 0:
        y -= vel
    elif keys[pygame.K_DOWN] and y < w_height - height: # also: and (y + height) < w_height:
        y += vel
    if keys[pygame.K_LEFT] and x > 0:
        x -= vel
    if keys[pygame.K_RIGHT] and x < w_width - width:
        x += vel
    if keys[pygame.K_SPACE]:
        is_jump = True
    
    if is_jump:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            y -= (jump_count ** 2) * neg * 0.5 # we divide the hight by 2 (* 0.5)
            # y -= jump_count
            jump_count -= 1
        else:
            jump_count = 10
            is_jump = False


    screen.fill("white")
    pygame.draw.rect(screen, "purple", (x, y, width, height))
    clock.tick(5)
    pygame.display.flip()