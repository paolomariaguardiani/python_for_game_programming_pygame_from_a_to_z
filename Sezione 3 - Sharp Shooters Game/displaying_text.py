import pygame
pygame.init()

w_width = 500
w_height = 500

screen = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Displaying Text")

clock = pygame.time.Clock()
bg_img = pygame.image.load("images/bg_img.jpeg")
bg_img = pygame.transform.scale(bg_img, (w_width, w_height))
walkRight = [pygame.image.load(f'soldier/{i}.png') for i in range(1, 10)]
walkLeft = [pygame.image.load(f'soldier/L{i}.png') for i in range(1, 10)]
char = pygame.image.load('soldier/standing.png')
moveLeft = [pygame.image.load(f'enemy/L{i}.png') for i in range(1, 10)]
moveRight = [pygame.image.load(f'enemy/R{i}.png') for i in range(1, 10)]
font = pygame.font.SysFont("helvetica", 30, 1, 1) # 1, 1 = bold(true) and italic(true)
score = 0

class player():
    # Self refers to the instance of the class that's being created.
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.is_jump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.walkCount = 0 # This variable is used to tracks the image to display
        self.standing = True
        # We create a hit box, a rectangle around the character
        self.hitbox = (self.x, self.y, self.width, self.height) 
        self.hit = pygame.Rect(self.hitbox)


    def draw(self, screen):
        if self.walkCount +1 >= 27:
            self.walkCount = 0

        if not(self.standing): # if the player is moving
            if self.left:
                # screen.blit(walkLeft[walkCount], (x, y)) # moving fast
                screen.blit(walkLeft[self.walkCount // 3], (self.x, self.y)) # moving slower
                self.walkCount += 1
            elif self.right: 
                # screen.blit(walkRight[walkCount], (x, y)) # moving fast
                screen.blit(walkRight[self.walkCount // 3], (self.x, self.y)) # moving slower
                self.walkCount += 1
        else:
            if self.right: # se è fermo o guarda a destra o guarda a sinistra
                screen.blit(walkRight[0], (self.x, self.y))
            else:
                screen.blit(walkLeft[0], (self.x, self.y))
        
        # We create a hit box, a rectangle around the character
        self.hitbox = (self.x, self.y, self.width, self.height)
        # We draw the rectangle around the character for the collision detection
        # pygame.draw.rect(screen, "black", self.hitbox, 2)
        self.hit = pygame.Rect(self.hitbox)

class projectile():
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.vel = 8 * direction

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class enemy():
    def __init__(self, x, y, width, height, end):
         self.x = x
         self.y = y
         self.width = width
         self.height = height
         self.walkCount = 0
         self.vel = 3
         self.path = [x, end]
         # We create a hit box, a rectangle around the character
         self.hitbox = (self.x + 20, self.y, self.width - 40, self.height - 4) 
         self.hit = pygame.Rect(self.hitbox)
    
    def draw(self, screen):
        self.move()
        if self.walkCount +1 >= 27:
            self.walkCount = 0

        if self.vel > 0:
            # screen.blit(walkLeft[walkCount], (x, y)) # moving fast
            screen.blit(moveRight[self.walkCount // 3], (self.x, self.y)) # moving slower
            self.walkCount += 1
        else: 
            # screen.blit(walkRight[walkCount], (x, y)) # moving fast
            screen.blit(moveLeft[self.walkCount // 3], (self.x, self.y)) # moving slower
            self.walkCount += 1
        
        # We create a hit box, a rectangle around the character
        self.hitbox = (self.x + 20, self.y, self.width - 40, self.height - 4)
        # We draw the rectangle around the character for the collision detection
        # pygame.draw.rect(screen, "black", self.hitbox, 2)
        self.hit = pygame.Rect(self.hitbox)
        
    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] - self.width + 20: 
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - 20:
                self.x += self.vel
            else: 
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
      

def DrawInGameloop():
    screen.blit(bg_img, (0,0))
    clock.tick(25)
    soldier.draw(screen)
    text = font.render("Score : " + str(score), 1, "red") # 1 = antialyasing
    # text = font.render(f"Score : {score}", 1, "red") # 1 = antialyasing
    screen.blit(text, (0, 10))
    enemy.draw(screen)
    # We crate the bullets
    for bullet in bullets:
        bullet.draw(screen)
    pygame.display.flip()


soldier = player(210,435, 64, 64)
enemy = enemy(0, w_height - 64, 64, 64, w_width) # w_width è quando cambia la direzione
bullets = []
shoot = 0
done = True # better is gameloop = True
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = False

    if soldier.hit.colliderect(enemy.hit):
        enemy.vel = enemy.vel * -1


    if shoot > 0:
        shoot += 1
    if shoot > 3:
        shoot = 0

    for bullet in bullets: 
        # We search if the bullet y position is within the vertical range of the enemy hitbox
        if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > enemy.hitbox[1]:
            if bullet.x + bullet.radius > enemy.hitbox[0] and bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]:
                 bullets.pop(bullets.index(bullet))
                 score += 1

        if bullet.x < 500 and bullet.x > 0: # bullet.x is the center of the circle
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shoot == 0: # shoot == 0 is a sort of delay
        if soldier.right:
            direction = 1
        else:
            direction = -1
        
        if len(bullets) < 5:
            bullets.append(projectile((soldier.x + soldier.width // 2), 
                                      (soldier.y + soldier.height // 2),
                                      6, "black", direction ))
        shoot = 1

    if keys[pygame.K_LEFT] and soldier.x > 0:
        soldier.x -= soldier.vel
        soldier.left = True
        soldier.right = False
        soldier.standing = False
    elif keys[pygame.K_RIGHT] and soldier.x < w_width - soldier.width:
        soldier.x += soldier.vel
        soldier.right = True
        soldier.left = False
        soldier.standing = False
    else:
        soldier.standing = True
        soldier.walkCount = 0


    if not(soldier.is_jump):
        if keys[pygame.K_UP]:
            soldier.is_jump = True
            soldier.right = False
            soldier.left = False
    else:
        if soldier.is_jump:
            if soldier.jump_count >= -10:
                neg = 1
                if soldier.jump_count < 0:
                    neg = -1
                soldier.y -= (soldier.jump_count ** 2) * neg * 0.5 # we divide the hight by 2 (* 0.5)
                # y -= jump_count
                soldier.jump_count -= 1
            else:
                soldier.jump_count = 10
                soldier.is_jump = False


    DrawInGameloop()