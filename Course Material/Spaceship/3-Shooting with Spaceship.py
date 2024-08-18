import pygame
pygame.init()

w_width = 650 
w_height = 600
window = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Spaceship")

#loading images
bg = pygame.image.load("media/bg.png")
bg = pygame.transform.scale(bg, (w_width, w_height))
spaceship_img = pygame.image.load("media/spaceship.png")
bullet = pygame.image.load("media/bullet.png")

# game varibles
clock = pygame.time.Clock()
bullets = []
shoot_counter = 0

#spaceship class
class Spaceship():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 75
        self.height = 75
        self.vel = 8
        self.rect = (self.x, self.y, self.width, self.height)
        self.health = 5
        self.alive = True 

    def draw(self, window):
        window.blit(spaceship_img, (self.x, self.y))
        pygame.draw.rect(window, "red", (self.x, self.y+self.height, self.width, 10))
        pygame.draw.rect(window, "green", (self.x, self.y+self.height, round(self.width * (self.health/5)), 10))
        self.rect = (self.x, self.y, self.width, self.height)

class Projectile():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 3

    def draw(self, window):
        self.y -= self.vel
        window.blit(bullet, (self.x, self.y))

#game objects
spaceship = Spaceship(round(w_width/2)- 34, w_height- 100)

#drawing on the window surface
def DrawInGameLoop():
    clock.tick(60)
    window.blit(bg, (0,0))
    spaceship.draw(window)
    for projectile in bullets:
        projectile.draw(window)
    pygame.display.flip()


#game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if shoot_counter > 0:
        shoot_counter += 1
    if shoot_counter > 10:
        shoot_counter = 0
    for projectile in bullets:
        if projectile.y > 0:
            projectile.y -= projectile.vel
        else:
            bullets.pop(bullets.index(projectile))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and spaceship.x>0:
        spaceship.x -= spaceship.vel

    elif keys[pygame.K_RIGHT] and spaceship.x<w_width - spaceship.width:
        spaceship.x += spaceship.vel

    if keys[pygame.K_SPACE] and shoot_counter == 0:
        if len(bullets) < 5:
            bullets.append(Projectile(spaceship.x + round(spaceship.width/2), spaceship.y))

        shoot_counter = 1
    DrawInGameLoop()

pygame.quit()
