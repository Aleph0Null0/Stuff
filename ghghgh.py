from graphics import *
import random
win = GraphWin('uy',1200,1200)
win.setBackground(color_rgb(204,255,204))

for i in range(100):
    r = random.randrange(10,50)
    x = random.randrange(1200)
    y = random.randrange(1200)
    b,a = x,y
    h = random.randrange(20,400)
    k = random.randrange(20,400)
    red = random.randrange(200,255)
    green = random.randrange(200,255)
    blue = random.randrange(200,255)
    circle = Circle(Point(x,y),r)
    rect = Rectangle(Point(x,y),Point(a,b))
    Line(Point(x,y),Point(a,b)).draw(win)
    rect.draw(win)
    rect.setFill(color_rgb(red,green,blue))
    circle.draw(win)
    circle.setFill(color_rgb(int(red*x/1200),int(green*y/1200),int(blue*0.8)))
