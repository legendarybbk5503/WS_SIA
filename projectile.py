import os
import sys
import numpy
from matplotlib import pyplot
from typing import Literal

class projectile():
    
    def __init__(self, **kwargs):
        #mass
        self.__m = kwargs.get('m')
        #area
        self.__r = kwargs.get('r')
        self.__A = numpy.pi * (self.__r**2)
        #drag coefficient
        self.__C = kwargs.get('C', 0.5)
        #density of air
        self.__rho = kwargs.get("rho", 1.2)
        #gravitational acceleration
        self.__g = kwargs.get('g', 9.81)
        #constant D
        self.__D = self.__rho * self.__C * self.__A / 2
        #delta t
        self.__deltaT = kwargs.get("deltaT", 1/240) #30Hz*8slow mo
        #data in python list
        #data = [t, x, y, vx, vy, ax, ay]
        self.__datas = []
        
    def getData(self, fileName: str):
        with open(os.path.join(sys.path[0], fileName), encoding = "utf-8") as f:
            file = f.readlines()
            file.pop(0) #remove first row (title of each column)
            datas = [x[:-1].split(',') for x in file]
            for i, data in enumerate(datas):
                for j, num in enumerate(data):
                    if num == "":
                        data[j] = 0
                datas[i] = list(map(float, data))
            self.__datas = datas
        self.__adjust()
    
    def __adjust(self):
        for data in self.__datas:
            #t
            data[0] = data[0] / 8
            #v
            data[3] = data[3] * 8
            data[4] = data[4] * 8
            #a
            data[5] = data[5] * 64
            data[6] = data[6] * 64
        

    def __initialValue(self):
        t = self.__datas[0][0]
        x = numpy.mean([self.__datas[i][1] for i in range(1, 11)])
        y = numpy.mean([self.__datas[i][2] for i in range(1, 11)])
        vx = numpy.mean([self.__datas[i][3] for i in range(1, 11)])
        vy = numpy.mean([self.__datas[i][4] for i in range(1, 11)])
        return [t], [x], [y], [vx], [vy]
    
    def __calculateWithAir(self, data: tuple = None):
        t, x, y, vx, vy = tuple(map(lambda x: [x], data)) if data is not None else self.__initialValue()
        ax, ay = [], []
        deltaT = self.__deltaT

        r = range(60*30) if data is not None else range(len(self.__datas[:-1]))

        for _ in r:
            v = numpy.hypot(vx[-1], vy[-1])
            ax.append(-1 * (self.__D / self.__m) * v * vx[-1])
            ay.append(- self.__g - (self.__D / self.__m) * v * vy[-1])

            vx.append(vx[-1] + ax[-1] * deltaT)
            vy.append(vy[-1] + ay[-1] * deltaT)
            x.append(x[-1] + vx[-2] * deltaT + 0.5 * ax[-1] * (deltaT**2))
            y.append(y[-1] + vy[-2] * deltaT + 0.5 * ay[-1] * (deltaT**2))
            t.append(t[-1] + deltaT)

        ax.append(-1 * (self.__D / self.__m) * v * vx[-1])
        ay.append(- self.__g - (self.__D / self.__m) * v * vy[-1])
        
        return t, x, y, vx, vy, ax, ay
    
    def __calculateWithoutAir(self, data: tuple = None):
        t, x, y, vx, vy = tuple(map(lambda x: [x], data)) if data is not None else self.__initialValue()
        ax, ay = [], []
        deltaT = self.__deltaT
        
        r = range(60*30) if data is not None else range(len(self.__datas[:-1]))
        
        for _ in r:
            v = numpy.hypot(vx[-1], vy[-1])
            ax.append(0)
            ay.append(- self.__g)
            
            vx.append(vx[-1] + ax[-1] * deltaT)
            vy.append(vy[-1] + ay[-1] * deltaT)
            x.append(x[-1] + vx[-2] * deltaT + 0.5 * ax[-1] * (deltaT**2))
            y.append(y[-1] + vy[-2] * deltaT + 0.5 * ay[-1] * (deltaT**2))
            t.append(t[-1] + deltaT)
        
        ax.append(0)
        ay.append(- self.__g)

        return t, x, y, vx, vy, ax, ay

    def __actual(self):
        t = [data[0] for data in self.__datas]
        x = [data[1] for data in self.__datas]
        y = [data[2] for data in self.__datas]
        vx = [data[3] for data in self.__datas]
        vy = [data[4] for data in self.__datas]
        ax = [data[5] for data in self.__datas]
        ay = [data[6] for data in self.__datas]
        return t, x, y, vx, vy, ax , ay

    def draw(self, x:Literal['t', 'x', 'y', 'vx', 'vy', 'ax', 'ay'], y:Literal['t', 'x', 'y', 'vx', 'vy', 'ax', 'ay']):    
        t1, x1, y1, vx1, vy1, ax1, ay1 = self.__calculateWithAir()
        t2, x2, y2, vx2, vy2, ax2, ay2 = self.__calculateWithoutAir()
        t3, x3, y3, vx3, vy3, ax3, ay3 = self.__actual()
        
        data = [None] * 6
        data[0] = locals().get(f"{x}1")
        data[2] = locals().get(f"{x}2")
        data[4] = locals().get(f"{x}3")
        data[1] = locals().get(f"{y}1")
        data[3] = locals().get(f"{y}2")
        data[5] = locals().get(f"{y}3")
        
        line1, = pyplot.plot(data[0], data[1], color = 'r', label = 'calculated with air resistance')
        line2, = pyplot.plot(data[2], data[3], color = 'g', label = 'calculated without air resistance')
        line3, = pyplot.plot(data[4], data[5], color = 'b', label = 'actual')
        
        #pyplot.ylim(bottom = 0)
        #pyplot.xlim(left = 0)
        
        pyplot.xlabel(x)
        pyplot.ylabel(y)
        pyplot.title("Projectile Trajectory")
        
        pyplot.legend()
        pyplot.show()
        
        #print(line1.get_xydata())
        #numpy.savetxt("data.csv", line1.get_xydata(), delimiter=',')

def main():
    eg = (0, 0, 0, 50*numpy.cos(35*numpy.pi/180), 50*numpy.sin(35*numpy.pi/180))

    x = projectile(m = 15e-3, r = 0.01508, C = 0.75, rho = 1.293, g = 9.80665)

    x.getData("data.txt")
    x.draw('x', 'y')

if __name__ == "__main__":
    main()   