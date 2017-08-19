from graphics import *
import math

PI = math.pi


class Plane:
    def __init__(self,center,width = 1200, heigth = 900, mode = 'not visible', flush=False, flushLaps=10): # center is a touple (x,y)
        self.win = GraphWin('grapher very cool', width, heigth,autoflush=False)
        self.center = center
        self.mode = mode
        self.drawPlane()
        self.win.setCoords(21.8, -102.4, 22.0, -102.25)

        self.memoryRect = []
        self.buffCount = 0
        self.flush = flush
        self.flushLaps = flushLaps

    def drawLine(self,coord1,coord2):
        ix = coord2[0] - coord1[0]
        iy = coord2[1] - coord1[1]
        x = coord1[0]
        y = coord1[1]
        dist = ix*ix + iy*iy

        if dist == 0:
            return

        dist = math.sqrt(dist)

        dx = ix/ dist
        dy = iy/ dist
        self.win.plot(x+self.center[0],y+self.center[1])
        for z in range(int(dist)):
            x += dx
            y += dy
            self.win.plot(x+self.center[0],y+self.center[1])
        self.flushBuffer()

    def isInside(self,point):
        if point[0] < -self.win.getWidth() or point[0]> self.win.getWidth():
            return False
        if point[1] < -self.win.getHeight() or point[1]> self.win.getHeight():
            return False
        return True

    def paramGraph(self, f, g, start = 0, end=1000, dt = 1):

        for i in range(start, end):
            p1 = (f(i*dt), g(i*dt))
            p2 = ( f( (i+1)*dt ), g( (i+1)*dt ) )

            if ( self.isInside(p1) and self.isInside(p2)):
                self.drawLine(p1, p2)

    def graph(self, f):
        for val in range(-self.center[0],self.win.getWidth()-self.center[0]):
            x = val
            p1 = (x + 1, f(x) )
            p2 = ( x + 1, f(x+1))

            if ( self.isInside(p1) and self.isInside(p2)):
                self.drawLine(p1, p2)

    def flushBuffer(self):
        if self.flush:
            self.buffCount += 1
            if self.buffCount%self.flushLaps == 0:
                self.win.update()


    '''def graph(self,f):
        for val in range(-self.center[0],self.win.getWidth()-self.center[0]):
            x = val
            y = f(x)
            x2 = val+1
            y2 = f(x2)
            if y < -self.win.getHeight() or y > self.win.getHeight():
                continue
            else:
                self.drawLine((x,y), (x2,y2))
            self.drawLine((x2,y2),(x,y))'''

    def drawPlane(self):
        for y in range(self.win.getHeight()):
            self.win.plot(self.center[0],y)

        for x in range(self.win.getWidth()):
            self.win.plot(x,self.center[1])

    def printBuffer(self):
        self.win.update()

    def riemanSum(self,f,n):
        dx = ((self.win.getWidth()-self.center[0]) +self.center[0])/n
        xi = 0
        y = 0
        for i in range(-self.center[0],self.win.getWidth()-self.center[0]):
            xi = self.center[0] + dx*i
            y = f(xi)
            coord1 = Point(xi +self.center[0],f(xi)+self.center[1])
            if y < -self.win.getHeight() or y > self.win.getHeight():
                continue
            coord2 = Point(xi+dx +self.center[0],self.center[1])
            rect = Rectangle(coord1,coord2)
            self.memoryRect.append(rect)
            rect.draw(self.win)


    def releaseMemo(self):
        for rect in self.memoryRect:
            rect.undraw()
        self.memoryRect = []

    def drawPoints(self, points, size = 1, color = "black"):
        center = Point(0,0)
        drawPoints = []
        for p in points:
            center = Point(p[0]+self.center[0], p[1]+self.center[1])
            circle = Circle(center, size)
            drawPoints.append(circle)
            circle.setFill(color)
            circle.draw(self.win)
            self.flushBuffer()
            #self.win.plot(p[0]+self.center[0],p[1]+self.center[1]) ## principal pixel
        return drawPoints


def f(x):
    return ((50-20)*math.cos(x) + 20*math.cos(((50-20)/20)*x))

def g(x):
    return ((50-20)*math.sin(x) + 20*math.sin(((50-20)/20)*x))


def h(x):
    if x > 0:
        return 46.83858314068624*math.log(x) + -80.10997338893367
    return 0


def j(x):
    return 30*math.sin(-x + (1/2)*math.pi) + 30

"""
hipocicloid
    #circle in a circle supouse
    def f(x):
        return (30-8)*math.cos(x) + 8*math.cos(x)


    def g(x):
        return (30-8)*math.sin(x) + 8*math.sin(x)


cool graph:

    def f(x):
        return 200*(math.sin(x) - math.sin(2.3*x))

    def g(x):
        return 200*math.cos(x)

Another cool graph
    def f(x):
        return 100*(math.sin(x) + (1/2)*math.sin(5*x)+ (1/4)*math.cos(2.3*x))

    def g(x):
        return 100*(math.cos(x) + (1/2)*math.cos(5*x)+ (1/4)*math.sin(2.3*x))

cycloid :
    def f(x):
        return 30*math.cos(-x + (1/2)*math.pi) + 30*x


    def g(x):
        return 30*math.sin(-x + (1/2)*math.pi) + 30

conchoids of Nicomedes
    def f(x):
        return 50*(-0.1 + math.cos(x))


    def g(x):
        return 50*(-0.1*math.tan(x) + math.sin(x))

broing exercise:
    def f(x):
        return x**2


    def g(x):
        return x**3 - 3*x
"""

if __name__ == "__main__":

    n = 20

    cartesian = Plane((450,450), flush=True, flushLaps=5)
    cartesian.paramGraph(f, g, start = 0, end = 10000, dt = 1/100)
    #cartesian.paramGraph(h, j, start = 0, end = 300, dt = 0.1)
    #cartesian.graph(g)
    #cartesian.riemanSum(f,n)

    """while True:
        cartesian.win.getMouse()
        n += 6
        cartesian.releaseMemo()
        cartesian.riemanSum(f,n)
    	cartesian.printBuffer()"""

    cartesian.win.getMouse()
    cartesian.win.close()