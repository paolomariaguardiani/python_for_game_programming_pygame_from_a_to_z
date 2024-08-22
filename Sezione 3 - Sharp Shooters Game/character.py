import pygame
pygame.init()

w_width = 500
w_height = 500

screen = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Moving and animating sprites")

# Creating object
x = 50
y = 435
width = 64
height = 64
vel = 5

clock = pygame.time.Clock()

# Jump variables
is_jump = False
jump_count = 10

# Loading the image
bg_img = pygame.image.load("images/bg_img.jpeg")
bg_img = pygame.transform.scale(bg_img, (w_width, w_height))

# Character
left = False
right = False
walkCount = 0 # This variable is used to tracks the image to display


# Carico in una lista le immagini del soldato che si muove verso destra
walkRight = [pygame.image.load(f'soldier/{i}.png') for i in range(1, 10)]
# carico le immagini del soldato che si muove a sinistra
walkLeft = [pygame.image.load(f'soldier/L{i}.png') for i in range(1, 10)]
char = pygame.image.load('soldier/standing.png')


def DrawInGameloop():
    screen.blit(bg_img, (0,0))
    clock.tick(25)

    global walkCount

    # if walkCount +1 >= 9:
    # We are going to make sure that every image is
    # displayed for three frames before the image is shown
    if walkCount +1 >= 28:
        walkCount = 0

    if left:
        # screen.blit(walkLeft[walkCount], (x, y)) # moving fast
        screen.blit(walkLeft[walkCount // 3], (x, y)) # moving slower
        walkCount += 1
    elif right: 
        # screen.blit(walkRight[walkCount], (x, y)) # moving fast
        screen.blit(walkRight[walkCount // 3], (x, y)) # moving slower
        walkCount += 1
    else:
        screen.blit(char, (x, y))


    pygame.display.flip()


done = True # better is gameloop = True
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > 0:
        x -= vel
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and x < w_width - width:
        x += vel
        right = True
        left = False
    else:
        left = False
        right = False
        walkCount = 0


    if not(is_jump):
        if keys[pygame.K_SPACE]:
            is_jump = True
            right = False
            left = False
    else:
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


    DrawInGameloop()