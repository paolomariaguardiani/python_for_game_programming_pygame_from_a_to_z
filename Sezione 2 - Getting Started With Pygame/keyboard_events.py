import pygame
pygame.init()

w_width = 500
w_height = 500

screen = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Handling Keyboard Events")

# Creating object
x = 0
y = 0
width = 50
height = 50
vel = 1

clock = pygame.time.Clock()
done = True # better is gameloop = True
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        y -= vel
    elif keys[pygame.K_DOWN]:
        y += vel
    if keys[pygame.K_LEFT]:
        x -= vel
    if keys[pygame.K_RIGHT]:
        x += vel

    screen.fill("white")
    pygame.draw.rect(screen, "purple", (x, y, width, height))
    clock.tick(60)
    pygame.display.flip()