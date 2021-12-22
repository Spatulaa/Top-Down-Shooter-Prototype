import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, startPos, shootDir, speed, died):
        super().__init__()

        self.image = pygame.Surface((2.5, 2.5))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(center = (startPos[0], startPos[1]))
        self.startPos = startPos
        self.shootDir = shootDir
        self.spawnStart = pygame.time.get_ticks()
        self.speed = speed
        self.died = died

    def update(self, lifeSpan, cameraOffset, tiles):
        global spawnStart

        #Destroying Object
        if (pygame.time.get_ticks() - self.spawnStart >= lifeSpan * 1000): 
            self.kill()

        #Moving Object
        self.startPos[0] += self.shootDir[0] * self.speed
        self.startPos[1] += self.shootDir[1] * self.speed

        #Collision Detection
        import main
        collidedList = main.CollisionTest(pygame.Rect(self.startPos[0], self.startPos[1], 2.5, 2.5), tiles)
        if collidedList != []: 
            main.CreateParticles(True, self.startPos, [4, 4], [1, 3], 3, [[0, 0, 255], [0, 0, 255]])
            self.kill()

        self.rect = self.image.get_rect(center = (self.startPos[0] - cameraOffset[0], self.startPos[1] - cameraOffset[1]))