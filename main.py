import pygame, sys, os

from pygame.constants import *
import character, gun

pygame.init()

winSize = [1920, 1080]
displaySize = [480, 270]
win = pygame.display.set_caption("Donut Survive")
win = pygame.display.set_mode(winSize, 0, 32)
cursorDisplay = pygame.Surface((winSize), pygame.SRCALPHA)
display = pygame.Surface((displaySize))

clock = pygame.time.Clock()

#Sprites
backgroundSprite = pygame.image.load('Assets/background.png')
gunSprite = pygame.image.load('Assets/pistol.png')
cursor = pygame.image.load('Assets/Crosshair.png')

up, down, left, right = False, False, False, False
playerPos = [0, 0]

#Objects
char = character.Character(5, pygame.Rect(playerPos[0], playerPos[1], 21, 21), playerPos)
pistol = gun.Gun(4, gunSprite, display, 0, 0)
bullets = None
gunAngle = None

cameraOffset = [0, 0]

def CameraMovement():
    global cameraOffset

    mousePos = [pygame.mouse.get_pos()[0] + 480, pygame.mouse.get_pos()[1] + 270]

    mouseDist = [240, 135]
    mouseDist[0] -= mousePos[0]/6
    mouseDist[1] -= mousePos[1]/6

    camOffset = cameraOffset
    camOffset[0] += (char.hitbox.x - camOffset[0] - 230 - mouseDist[0])/15
    camOffset[1] += (char.hitbox.y - camOffset[1] - 125 - mouseDist[1])/15

    intCamOffset = camOffset.copy()
    intCamOffset[0] = int(camOffset[0])
    intCamOffset[1] = int(camOffset[1])
    return intCamOffset, camOffset

animationFrames = {}
def LoadAnimations(path, timeBetweenFrames):
    global animationFrames
    name = path.split('/')[-1]
    animFrameData = []
    idIndex = 0
    
    for frame in timeBetweenFrames:
        #Finding Sprite
        animFrameId = f"{name}_{idIndex}"
        location = f"{path}/{animFrameId}.png"
        sprite = pygame.image.load(location)
        animationFrames[animFrameId] = sprite.copy()

        for i in range(frame): animFrameData.append(animFrameId)
        idIndex += 1
    return animFrameData

characterAnims = {}
#Creating Frames Id Names
characterAnims['walk'] = LoadAnimations('Assets/Animations/Character/Walk', [4, 4, 4, 4])
characterAnims['idle'] = LoadAnimations('Assets/Animations/Character/Idle', [45, 45])

def LoadTiles():
    tiles = []
    for filename in os.listdir('Assets/Tiles/'):
        if filename.endswith('.png'):
            path = os.path.join('Assets/Tiles/', filename)
            tiles.append(pygame.image.load(path))
    return tiles   

def CollisionTest(charRect, tiles):
    collidedList = []
    for tile in tiles:
        if charRect.colliderect(tile): 
            collidedList.append(tile)
    return collidedList

def LoadMap(path, intCamOffset):
    tileSprites = LoadTiles()
    file = open(f'Maps/map{path}.txt', 'r')
    mapData = file.read()
    mapData = mapData.split('\n')
    map = []

    for row in mapData: map.append(list(row))
    collidables = []

    y = 0
    for row in map:
        x = 0
        for tile in row:
            #Wall, Top, Bottom, Right, Left, TopRight, TopLeft, BottomRight, BottomRight
            if tile == '1': display.blit(tileSprites[8], (x * 20 - intCamOffset[0], y * 20 - intCamOffset[1]))
            if tile == '2': display.blit(tileSprites[5], (x * 20 - intCamOffset[0], y * 20 - intCamOffset[1]))
            if tile == '3': display.blit(tileSprites[0], (x * 20 - intCamOffset[0], y * 20 - intCamOffset[1]))
            if tile == '4': display.blit(tileSprites[4], (x * 20 - intCamOffset[0], y * 20 - intCamOffset[1]))
            if tile == '5': display.blit(tileSprites[3], (x * 20 - intCamOffset[0], y * 20 - intCamOffset[1]))
            if tile == '6': display.blit(tileSprites[7], (x * 20 - intCamOffset[0], y * 20 - intCamOffset[1]))
            if tile == '7': display.blit(tileSprites[6], (x * 20 - intCamOffset[0], y * 20 - intCamOffset[1]))
            if tile == '8': display.blit(tileSprites[2], (x * 20 - intCamOffset[0], y * 20 - intCamOffset[1]))
            if tile == '9': display.blit(tileSprites[1], (x * 20 - intCamOffset[0], y * 20 - intCamOffset[1]))
            if tile != '0': collidables.append(pygame.Rect(x * 20, y * 20, 20, 20))
            x += 1
        y += 1
    return collidables

while True:
    display.fill((255, 255, 255))

    intCamOffset, camOffset = CameraMovement()
    collidables = LoadMap(1, intCamOffset)

    #Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == K_w: up = True
            if event.key == K_s: down = True
            if event.key == K_d: right = True
            if event.key == K_a: left = True

        if event.type == pygame.KEYUP:
            if event.key == K_w: up = False
            if event.key == K_s: down = False
            if event.key == K_d: right = False
            if event.key == K_a: left = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            bullets = pistol.Shoot(cameraOffset)

    gunTargetPos = [char.hitbox.x, char.hitbox.y]
    char.Move(up, down, left, right, collidables, char.hitbox)

    char.frame += 1
    if char.frame >= len(characterAnims[char.action]): char.frame = 0
    charSprite = animationFrames[characterAnims[char.action][char.frame]]
    display.blit(charSprite, (char.hitbox.x - camOffset[0], char.hitbox.y - camOffset[1]))
    gunAngle = pistol.Rotation(camOffset, gunTargetPos)
    
    if bullets != None: 
        bullets.update(1.5, cameraOffset, collidables)
        bullets.draw(display)

    #Cursor
    cursorDisplay.fill(pygame.SRCALPHA)
    #pygame.mouse.set_visible(False)
    sizedCursor = pygame.transform.scale(cursor, (50, 50))
    cursorDisplay.blit(sizedCursor, (pygame.mouse.get_pos()[0] - sizedCursor.get_width()/2, pygame.mouse.get_pos()[1] - sizedCursor.get_height()/2))

    win.blit(pygame.transform.scale(display, winSize), (0, 0))
    win.blit(cursorDisplay, (0, 0))
    pygame.display.update()
    clock.tick(75)