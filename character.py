import pygame

class Character():
    def __init__(self, speed, hitbox, playerMovement):
        self.playerMovement = playerMovement
        self.hitbox = hitbox
        self.speed = speed
        self.action = 'idle'
        self.frame = 0

    def ChangeAction(self, newAction):
        if self.action != newAction:
            self.action = newAction
            self.frame = 0

    def Move(self, up, down, left, right, collidables, rect):
        import main
        self.playerMovement = [0, 0]

        #Movement
        if up: self.playerMovement[1] -= self.speed
        if down: self.playerMovement[1] += self.speed
        if right: self.playerMovement[0] += self.speed
        if left: self.playerMovement[0] -= self.speed

        #Collisions
        rect.x += self.playerMovement[0]
        collided = main.CollisionTest(self.hitbox, collidables)
        for tile in collided:
            if self.playerMovement[0] > 0: rect.right = tile.left
            elif self.playerMovement[0] < 0: rect.left = tile.right

        rect.y += self.playerMovement[1]
        collided = main.CollisionTest(self.hitbox, collidables)
        for tile in collided:
            if self.playerMovement[1] > 0: rect.bottom = tile.top
            elif self.playerMovement[1] < 0: rect.top = tile.bottom

        if self.playerMovement[0] == 0 and self.playerMovement[1] == 0: self.ChangeAction('idle')
        else: self.ChangeAction('walk')