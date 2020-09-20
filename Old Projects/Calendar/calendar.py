#--------------------------------------------------------------------------------
#Program Name: Calendar
#Programmer: Arya Hosseini
#Date: March 7, 2019
#Input: Date from system
#Processing: The day of the week for the input date is determined as well as
#            whether the year is a leap year
#Output: A calendar displays the current month with the ability to cycle back
#        and forth through both months and years
# 
#--------------------------------------------------------------------------------
import pygame
import datetime
pygame.init()
win = pygame.display.set_mode((1000,1000))
pygame.display.set_caption('Calendar Generator by Arya')
CORAL = (255,155,107)
BLACK = (0,0,0)
sysDate = [i for i in str(datetime.datetime.now())[0:10].split('-')]
date = '/'.join([sysDate[1],sysDate[2],sysDate[0]])
def dayOfTheWeek(date):
    date = [int(i) for i in date.split('/')]
    month = date[0]+10 - 12 if date[0]+10>12 else date[0]+10
    day = date[1]
    year = date[2]
    year = date[2] -1 if date[0] < 3 else date[2]
    yearDig12 = int(''.join([digit for i,digit in enumerate(str(year)) if i < 2]))
    yearDig34 = int(''.join([digit for i,digit in enumerate(str(year)) if i > 1]))
    numZeller = day + int((13*month-1)/5)+yearDig34+int(yearDig34/4)+int(yearDig12/4)-(2*yearDig12)
    numWeekday = numZeller%7 if numZeller >= 0 else (numZeller%-7)+7
    return numWeekday

def isLeapYear(date):
    year = int(date.split('/')[2])
    if year%4 == 0 and not year%100 == 0 or year%400 == 0:
        return True
    else:
        return False
def drawGrid(rows,columns,surface,colour,width,height):
    for r in range(rows):
        for c in range(columns):
            x = (width/columns)*c
            y = (height/rows)*(r+(columns/10))
            pygame.draw.rect(surface,colour,(x,y,width/columns,height/rows),2)
def makeText(date,rows=6,columns=7):
    fonts = (pygame.font.SysFont('Comic Sans MS', 36),pygame.font.SysFont('Comic Sans MS', 20),pygame.font.SysFont('Comic Sans MS', 16))
    date = date.split('/')
    weekdaysText = [fonts[1].render(weekdays[weekday],False,(0,0,0)) for weekday in weekdays]
    title = fonts[0].render('Gregorian Calendar',True,(0,0,0))
    yearLabel = fonts[2].render('Year',False,(0,0,0))
    year = fonts[2].render(date[2],False,(0,0,0))
    monthLabel = fonts[2].render('Month',False,(0,0,0))
    month = fonts[2].render(months[int(date[0])],False,(0,0,0))
    numbersText = [fonts[0].render('{:0>2}'.format(str(i+1)),False,BLACK) for i in range(31)]
    index = -1
    dayOne = dayOfTheWeek('/'.join([date[0],'1',date[2]]))
    posX = (95,235,375,515,660,805,950)
    posY = (100,250,400,550,700,850,1000)
    for r in range(rows):
        for c in range(columns):
            if index < monthsLen[months[int(date[0])]]-1:
                index += 1
                win.blit(numbersText[index],(posX[c+dayOne if c+dayOne < 7 else c+dayOne-7],posY[r if c+dayOne < 7 else r+1]))
            else:
                pass
    win.blit(title,(3,3))
    win.blit(yearLabel,(700,10))
    win.blit(year,(700,27))
    win.blit(monthLabel,(600,10))
    win.blit(month,(600,27))
    for i in range(len(weekdaysText)):
        win.blit(weekdaysText[i],(1000/7*i+3,70))

def makeButtons():
    global leftbutton
    global rightbutton
    leftbutton = pygame.image.load('leftarrow.png')
    rightbutton = pygame.image.load('rightarrow.png')
    win.blit(leftbutton,(580,27))
    win.blit(leftbutton,(680,27))
    win.blit(rightbutton,(655,27))
    win.blit(rightbutton,(755,27))
def reDrawWin():
    win.fill(CORAL)
    drawGrid(6,7,win,BLACK,1000,900)
    makeText(date)
    makeButtons()
    pygame.display.update()
def checkButtons(date,mp):
    date = [int(i) for i in date.split('/')]
    buttonLM = leftbutton.get_rect(topleft=(580,27))
    buttonRM = rightbutton.get_rect(topleft=(655,27))
    buttonLY = leftbutton.get_rect(topleft=(680,27))
    buttonRY = rightbutton.get_rect(topleft=(755,27))
    if buttonLM.collidepoint(mp) and int(date[0]) > 1:
        date[0] -= 1
    elif buttonLM.collidepoint(mp) and int(date[0]) == 1:
        date[2] -= 1
        date[0] = 12
    if buttonRM.collidepoint(mp) and int(date[0]) < 12:
        date[0] += 1
    elif buttonRM.collidepoint(mp) and int(date[0]) == 12:
        date[2] += 1
        date[0] = 1
    if buttonLY.collidepoint(mp) and int(date[2]) > 1002:
        date[2] -= 1
    if buttonRY.collidepoint(mp) and int(date[2]) < 9998:
        date[2] += 1
    date = [str(i) for i in date]
    return '/'.join(date)
weekdays = {0:'Sunday',1:'Monday',2:'Tuesday',3:'Wednesday',4:'Thursday',5:'Friday',6:'Saturday'}
months = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
monthsLen = {"Jan":31,"Feb":28 if isLeapYear(date) == False else 29,"Mar":31,"Apr":30,"May":31,"Jun":30,"Jul":31,"Aug":31,"Sep":30,"Oct":31,"Nov":30,"Dec":31}
buttons = (pygame.Rect(580,27,15,15))
running = True
while running:
    pygame.time.delay(10)
    reDrawWin()
    monthsLen["Feb"] = 28 if isLeapYear(date) == False else 29
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False                  
        if event.type == pygame.MOUSEBUTTONDOWN:
            mp = pygame.mouse.get_pos()
            date = checkButtons(date,mp)
print('END')
pygame.quit()
