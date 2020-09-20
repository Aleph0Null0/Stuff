#--------------------------------------------------------------------------------
#Program: Space Adventure V1.0
#Author: Arya Hosseini
#Date: June 19, 2018
#Desription: This program is a game set in space where the player controls a
#            spaceship which fires at enemies. If the player gets hit by enemy lasers too
#            many times, they die.
#Input: The user inputs the controls for the spaceship. They can move
#       omnidirectionally, and also fire its laser.
#--------------------------------------------------------------------------------
import pygame
import time
import random
pygame.init()
highscore = open('highscore.txt','r') #Opening the highscore file and storing the current highscore for later
topScore = int(highscore.readline())
highscore.close()
spaceFont = pygame.font.SysFont('bauhaus93',12) #Creates a font for the HUD
spaceFontLarge = pygame.font.SysFont('bauhaus93',50) #Font for the gameover screen
ship = pygame.image.load('mainship.png')
laserBlue = pygame.image.load('BLUELASER.fw.png')
laserRed = pygame.image.load('laserRED.fw.png')
greenEnemy = pygame.image.load('greenship.png')
blueEnemy = pygame.image.load('blueship.png')
orangeEnemy = pygame.image.load('orangeship.png')
explosion = pygame.image.load('explosion.png')
enemies = (greenEnemy,blueEnemy,orangeEnemy)#The list of enemies for the spawnEnemies function to call upon
heartPowerUp = pygame.image.load('heart.png')
energyCorePowerUp = pygame.image.load('powercore.png')
powerUps = (heartPowerUp,energyCorePowerUp)
window = pygame.display.set_mode([640,900])
pygame.display.set_caption('Space Adventure V1.0')
pygame.display.update()
score = 0
global shipCoor
global shipHealth
global shipSpeed
global laserCD
def kaBoom(positionX,positionY):
    explosionsSpawned.append(explosion)
    explosionsData.append([positionX,positionY])
    explosionTimers.append(time.time())
def spawnPowerUp(powerup,position):
    powerUpsSpawned.append(powerup)
    powerUpsData.append(position)
def heartPickup():
    global shipHealth
    if not powerUpsSpawned == [] and powerUpsSpawned[0] == powerUps[0]:
        if isCollision(ship, powerUpsSpawned[0],shipCoor,powerUpsData[0]):
            shipHealth += 1
            del powerUpsSpawned[0]
            del powerUpsData[0]
def energyCorePickup():
    global energyCoreActive
    global shipSpeed
    global laserCD
    global energyCoreTimer
    if not powerUpsSpawned == [] and powerUpsSpawned[0] == powerUps[1]:
        if isCollision(ship,powerUpsSpawned[0],shipCoor,powerUpsData[0]):
            energyCoreTimer = time.time()
            energyCoreActive = True
            del powerUpsSpawned[0]
            del powerUpsData[0]
    if energyCoreActive:
        powerUpTimerEnd = time.time()
        shipSpeed = 6
        laserCD = 0
        if round(powerUpTimerEnd - energyCoreTimer,0) == 2:
            energyCoreActive = False
            shipSpeed = 4
            laserCD = 0.1
def spawnEnemy(enemy,position):
    enemiesSpawned.append(enemy)
    enemiesData.append(position)
def isCollision(objA,objB,coorA,coorB):
    widthA = objA.get_width()
    widthB = objB.get_width()
    heightA = objA.get_height()
    heightB = objB.get_height()
    if coorB[0] <= coorA[0] <= coorB[0]+widthB or coorB[0] <= coorA[0]+widthA <= coorB[0]+widthB:
        if coorB[1] <= coorA[1] <= coorB[1]+heightB or coorB[1] <= coorA[1]+heightA <= coorB[1]+heightB:
            return True
def laserCoolDown(cdTime):
    global begin
    global start
    if begin:
        start = time.time()
        begin = False
    end = time.time()
    if end - start >= cdTime:
        begin = True
        return True
def newWaveSetup():
    global explosionsSpawned,explosionsData,explosionTimers,powerUpsSpawned,powerUpsData
    explosionsSpawned = []
    explosionsData = []
    explosionTimers = []
    powerUpsSpawned = []
    powerUpsData = []
def waveTimer(waveTime):
    global shipHealth
    endTimer = time.time()
    if endTimer - waveTime > 12:
        shipHealth -= 1
    global waveTimerText
    waveTimerText = spaceFont.render('Time: '+str(round(12-(endTimer - waveTime))),True,(255,255,255))
def explosionRemoval():
    endTimer = time.time()
    for explosion in range(len(explosionTimers)):
        if 0.26 >= round(endTimer - explosionTimers[explosion],2) >= 0.24:
            del explosionsSpawned[explosion]
            del explosionsData[explosion]
            del explosionTimers[explosion]
            break
def isBorderCollision(objCoors):
    collision = False
    if objCoors[0] < 0:
        objCoors[0] = 1
        collision = True
    if objCoors[0] > 590:
        objCoors[0] = 589
        collision = True
    if objCoors[1] < 0:
        objCoors[1] = 1
        collision = True
    if objCoors[1] > 830:
        objCoors[1] = 829
        collision = True
    return collision
def checkLaserFire(laserCD):
    global laserOut
    if button[pygame.K_SPACE] and laserCoolDown(laserCD):
        laserCoor = shipCoor[:]
        laserCoor[0] += 19
        laserCoor[1] -= 30
        laserOut = True
        laserCoors.append(laserCoor)
        lasersSpawned.append(laserBlue)
def enemyLaserFire(enemyLaserSpeed,fireFrequency):
    global shipHealth
    for enemyindex,enemy in enumerate(enemiesSpawned):
            randomFire = random.randrange(1,252-fireFrequency)
            if randomFire == 1:
                enemyLaserCoor = enemiesData[enemyindex][:]
                enemyLaserCoor[0] += 8
                enemyLaserCoor[1] += 30
                enemyLasers.append(laserRed)
                enemyLaserCoors.append(enemyLaserCoor)
def enemyMovement(movementType,enemy,direction):
    global enemyMoveSpeed
    global warpTicker
    if movementType == 'jiggle':
        jiggleValue = random.randrange(0,2)
        if 0 < enemiesData[enemy][0] < 590:
            if jiggleValue == 0:
                enemiesData[enemy][0] += enemyMoveSpeed
            elif jiggleValue == 1:
                enemiesData[enemy][0] -= enemyMoveSpeed
        elif 0 > enemiesData[enemy][0]:
                enemiesData[enemy][0] += enemyMoveSpeed
        elif enemiesData[enemy][0] > 590:
                enemiesData[enemy][0] -= enemyMoveSpeed
    elif movementType == 'strafe':
        if direction == 0:
            enemiesData[enemy][0] += enemyMoveSpeed
        elif direction == 1:
            enemiesData[enemy][0] -= enemyMoveSpeed
    elif movementType == 'warp' and warpTicker%19 == 0:
        if direction == 0:
                enemiesData[enemy][0] += enemyMoveSpeed*20
        elif direction == 1:
            enemiesData[enemy][0] -= enemyMoveSpeed*20
def shipStateCheck():
    if movement:
        ship = pygame.image.load('mainship1.png')
    elif laserOut and not movement:
        ship = pygame.image.load('mainship2.png')
    else:
        ship = pygame.image.load('mainship.png')
    return ship
def updateDisplay():
    window.fill([0,0,0])
    window.blit(scoreText,(0,0))
    window.blit(healthText,(0,13))
    window.blit(waveTimerText,(580,0))
    window.blit(ship,shipCoor)
    for laserindex in range(len(lasersSpawned)):
        window.blit(lasersSpawned[laserindex],laserCoors[laserindex])
    for enemy in range(len(enemiesSpawned)):
        window.blit(enemiesSpawned[enemy],enemiesData[enemy])
    for enemylaserindex in range(len(enemyLasers)):
        window.blit(enemyLasers[enemylaserindex],enemyLaserCoors[enemylaserindex])
    for explosion in range(len(explosionsData)):
        window.blit(explosionsSpawned[explosion],explosionsData[explosion])
    for powerupindex in range(len(powerUpsData)):
        window.blit(powerUpsSpawned[powerupindex],powerUpsData[powerupindex])
    pygame.display.update()
def gameOver(score):
    global topScore
    gameovermessage = spaceFontLarge.render('GAME OVER',True,[0,0,0])
    scoredisplay = spaceFontLarge.render('YOU SCORED: '+ str(score),True,[0,0,0])
    playagain = spaceFontLarge.render('Press "r" to Retry',True,[0,0,0])
    newhighscore = spaceFontLarge.render('NEW HIGH SCORE!',True,[0,0,0])
    window.fill([255,255,255])
    if score >= topScore:
        highscore = open('highscore.txt','w')
        highscore.write(str(score))
        window.blit(newhighscore,[10,500])
    window.blit(gameovermessage,[10,200])
    window.blit(scoredisplay,[10,300])
    window.blit(playagain,[10,400])
    pygame.display.update()
#MAINLINE
running = True
while running:
#SETUP
    if score == 0:
        scoreMultiplier = 1
        shipCoor = [305,800]
        enemiesSpawned = []
        enemiesData = []
        enemyLasers = []
        enemyLaserCoors = []
        laserCoors = []
        lasersSpawned = []
        explosionsSpawned = []
        explosionsData = []
        explosionTimers = []
        powerUpsSpawned = []
        powerUpsData = []
        enemiesMoving = False
        warpTicker = 0
        laserOut = False
        laserSpeed = 10
        enemyLaserSpeed = 3
        laserCD = 0.1
        fireFrequency = 1
        enemyMoveSpeed = 3
        shipSpeed = 4
        shipHealth = 3
        resetCount = 0
        phase = 1
        wave = 1
        begin = True
        reset = False
        energyCoreActive = False
#GAME
    while shipHealth > 0:
#EVENTCHECK + MOVEMENT
        button = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()
        movement = True
        if button[pygame.K_a] and button[pygame.K_w]:
            shipCoor[0] -= shipSpeed*0.70710678118
            shipCoor[1] -= shipSpeed*0.70710678118
        elif button[pygame.K_a] and button[pygame.K_s]:
            shipCoor[0] -= shipSpeed*0.70710678118
            shipCoor[1] += shipSpeed*0.70710678118
        elif button[pygame.K_d] and button[pygame.K_w]:
            shipCoor[0] += shipSpeed*0.70710678118
            shipCoor[1] -= shipSpeed*0.70710678118
        elif button[pygame.K_d] and button[pygame.K_s]:
            shipCoor[0] += shipSpeed*0.70710678118
            shipCoor[1] += shipSpeed*0.70710678118
        elif button[pygame.K_a]:
            shipCoor[0] -= shipSpeed
        elif button[pygame.K_d]:
            shipCoor[0] += shipSpeed
        elif button[pygame.K_w]:
            shipCoor[1] -= shipSpeed
        elif button[pygame.K_s]:
            shipCoor[1] += shipSpeed
        else:
            movement = False
        isBorderCollision(shipCoor)
        checkLaserFire(laserCD)
        if laserOut:
            for index,laser in enumerate(lasersSpawned):
                laserCoors[index][1] -= laserSpeed
                if laserCoors[index][1] < 0:
                            del laserCoors[index]
                            del lasersSpawned[index]
            for index,laser in enumerate(lasersSpawned):
                for enemyindex,enemy in enumerate(enemiesSpawned):
                    if isCollision(lasersSpawned[index],enemiesSpawned[enemyindex],laserCoors[index],enemiesData[enemyindex]):
                        kaBoom(laserCoors[index][0]-60,laserCoors[index][1]-100)
                        del laserCoors[index]
                        del lasersSpawned[index]
                        del enemiesSpawned[enemyindex]
                        del enemiesData[enemyindex]
                        score += 100*scoreMultiplier
                        scoreMultiplier += 1
                        break
            if lasersSpawned == []:
                laserOut = False
        for enemylaserindex,enemylaser in enumerate(enemyLaserCoors):
            enemyLaserCoors[enemylaserindex][1] += enemyLaserSpeed
            if enemyLaserCoors[enemylaserindex][1] > 900:
                del enemyLasers[enemylaserindex]
                del enemyLaserCoors[enemylaserindex]
        for enemylaserindex,enemylaser in enumerate(enemyLaserCoors):
            if isCollision(enemyLasers[enemylaserindex],ship,enemyLaserCoors[enemylaserindex],shipCoor):
                shipHealth -= 1
                del enemyLasers[enemylaserindex]
                del enemyLaserCoors[enemylaserindex]
                break
        if phase == 1:
            if wave == 1:
                newWaveSetup()
                waveTime = time.time()
                spawnEnemy(enemies[0],[305, 200])
                wave = 2
            if wave == 2 and enemiesSpawned == []:
                newWaveSetup()
                waveTime = time.time()
                for i in range(3):
                    spawnEnemy(enemies[0],[275+i*30,200])
                spawnPowerUp(powerUps[0],[100,750])
                wave = 3
            if wave == 3 and enemiesSpawned == []:
                newWaveSetup()
                waveTime = time.time()
                spawnEnemy(enemies[0],[305,180])
                for i in range(4):
                    if i < 2:
                        spawnEnemy(enemies[0],[375+i*70,180])
                    else:
                        spawnEnemy(enemies[0],[375-i*70,180])
                for i in range(3):
                    spawnEnemy(enemies[0],[275+i*30,230])
                wave = 1
                phase = 2
        if phase == 2 and enemiesSpawned == []:
            fireFrequency += 10
            if wave == 1:
                newWaveSetup()
                waveTime = time.time()
                for i in range(16):
                    spawnEnemy(enemies[1],[10+i*40,130])
                spawnPowerUp(powerUps[0],[100,800])
                wave = 2
            if wave == 2 and enemiesSpawned == []:
                newWaveSetup()
                waveTime = time.time()
                for i in range(16):
                    if i < 8:
                        spawnEnemy(enemies[1],[10+i*40,100-i*10])
                    else:
                        spawnEnemy(enemies[1],[10+i*40,200+i*10])
                spawnPowerUp(powerUps[1],[400,600])
                wave = 3
            if wave == 3 and enemiesSpawned == []:
                newWaveSetup()
                waveTime = time.time()
                for i in range(3):
                    spawnEnemy(enemies[1],[305,100+i*50])
                enemiesMoving = True
                enemyMoveType = 'strafe'
                wave = 4
            if wave == 4 and enemiesSpawned == []:
                newWaveSetup()
                waveTime = time.time()                
                for i in range(8):
                    spawnEnemy(enemies[1],[10+i*80,100-(i%2*50)])
                for i in range(4):
                    spawnEnemy(enemies[0],[10+i*160,200])
                enemiesMoving = False
                wave = 5
            if wave == 5 and enemiesSpawned == []:
                newWaveSetup()
                waveTime = time.time()
                for x in range(2):
                    for y in range(2):
                        spawnEnemy(enemies[1],[10+x*40,50+y*40])
                for i in range(16):
                    spawnEnemy(enemies[0],[10+i*40,300-i*20])
                wave = 1
                phase = 3
        if phase == 3 and enemiesSpawned == []:
            fireFrequency += 10
            enemyLaserSpeed += 1
            if wave == 1:
                newWaveSetup()
                waveTime = time.time()
                for i in range(5):
                    spawnEnemy(enemies[2],[305,300-i*50])
                enemiesMoving = True
                enemyMoveType = 'jiggle'
                wave = 2
                spawnPowerUp(powerUps[1],[500,850])
            if wave == 2 and enemiesSpawned == []:
                newWaveSetup()
                waveTime = time.time()
                for i in range(7):
                    spawnEnemy(enemies[2],[215+i*30,500-i*50])
                spawnEnemy(enemies[0],[305,550])
                enemyMoveType = 'strafe'
                wave = 3
            if wave == 3 and enemiesSpawned == []:
                newWaveSetup()
                waveTime = time.time()
                for i in range(3):
                    spawnEnemy(enemies[2],[305,20+i*60])
                    spawnEnemy(enemies[1],[305,200+i*40])
                    spawnEnemy(enemies[0],[305,320+i*20])
                enemyMoveType = 'warp'
                spawnPowerUp(powerUps[0],[300,850])
                wave = 4
            if wave == 4 and enemiesSpawned == []:
                reset = True
        if reset and enemiesSpawned == []:
            enemiesMoving = False
            resetCount += 1
            fireFrequency = 10*resetCount
            enemyLaserSpeed += 1*resetCount
            if fireFrequency > 40:
                fireFrequency = 40
            if enemyLaserSpeed > 4:
                enemyLaserSpeed = 4
            if fireFrequency == 40 and enemyLaserSpeed == 4:
                shipHealth = 1
            wave = 1
            phase = 1
        if enemiesMoving and not enemiesSpawned == []:
                for enemyindex,enemy in enumerate(enemiesData):
                    enemyMovement(enemyMoveType,enemyindex,enemyindex%2)
                    warpTicker += 1
                    if isBorderCollision(enemiesData[enemyindex]):
                        enemyMoveSpeed *= -1
                        
        for index,enemy in enumerate(enemiesSpawned):
            if isCollision(ship,enemiesSpawned[index],shipCoor,enemiesData[index]):
                shipHealth -= 1
                kaBoom(shipCoor[0],shipCoor[1])
                del enemiesSpawned[index]
                del enemiesData[index]
                scoreMultiplier = 1
                score += 100
        scoreText = spaceFont.render('Score: '+str(score),True,(255,255,255))
        healthText = spaceFont.render('Health: '+str(shipHealth),True,(255,255,255))
        powerupsText = spaceFont.render('Power-Ups Active: None',True,(255,255,255))
        enemyLaserFire(enemyLaserSpeed,fireFrequency)
        ship = shipStateCheck()
        heartPickup()
        energyCorePickup()
        waveTimer(waveTime)
        explosionRemoval()
        updateDisplay()
        pygame.time.delay(5)
    gameOver(score)
    button = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif button[pygame.K_r]:
            score = 0
