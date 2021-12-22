import pygame, math, bullet

bullets = pygame.sprite.Group()

class Gun():
    def __init__(self, fireRate, gunSprite, display, gunX, gunY):
        self.lastShot = pygame.time.get_ticks() - fireRate * 100
        self.gunSprite = gunSprite
        self.fireRate = fireRate
        self.display = display
        self.gunX = gunX
        self.gunY = gunY

    def Rotation(self, camOffset, playerPos):
        #Rotating Gun
        targetedPos = [pygame.mouse.get_pos()[0]/4 - 240 + 12.5/4, pygame.mouse.get_pos()[1]/4 - 135 + 12.5/4]
        gunAngle = math.degrees(math.atan2(targetedPos[0], targetedPos[1])) - 90

        #Moving Gun
        gunDirAngle = math.atan2(targetedPos[0], targetedPos[1])
        gunDir = [math.sin(gunDirAngle), math.cos(gunDirAngle)]

        global gunCopy
        gunCopy = self.gunSprite.copy()
        if targetedPos[0] + 240 < 240: gunCopy = pygame.transform.flip(gunCopy, False, True) 
        else: gunCopy = pygame.transform.flip(gunCopy, False, False)
        gunCopy = pygame.transform.rotate(gunCopy, gunAngle)
        
        #Moving Gun
        self.gunX = gunDir[0] * 20 - camOffset[0] + playerPos[0] + 10.5 - gunCopy.get_width()/2
        self.gunY = gunDir[1] * 20 - camOffset[1] + playerPos[1] + 9.5 - (gunCopy.get_height()/2)

        self.display.blit(gunCopy, (self.gunX, self.gunY))
        return gunAngle

    def Shoot(self, cameraOffset):
        global bullets

        #Finding Direction
        targetedPos = [pygame.mouse.get_pos()[0]/4 - 240 + 12.5/4, pygame.mouse.get_pos()[1]/4 - 135 + 12.5/4]
        gunAngle = math.atan2(targetedPos[0], targetedPos[1])
        shootDir = [math.sin(gunAngle), math.cos(gunAngle)]

        startPos = [gunCopy.get_width() * shootDir[0] + self.gunX + cameraOffset[0], gunCopy.get_height() * shootDir[1] + self.gunY + cameraOffset[1]]
        #Spawning Bullet
        if pygame.time.get_ticks() - self.lastShot >= self.fireRate * 100:
            import main
            main.CreateParticles(True, startPos, [6, 8], [2, 4], 10, [[255, 50, 0], [255, 255, 0]])
            bullets.add(bullet.Bullet(startPos, shootDir, 6, False))
            self.lastShot = pygame.time.get_ticks()
        
        return bullets
