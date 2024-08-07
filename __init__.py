import fractions
import matplotlib.pyplot as plt
import numpy as np

F_OTF = 0xC
F_PF = 0xD
class OneTimeFunction:
    def __init__(self,k,b):
        self.IC_I = 0x0
        self.IC_D = 0x1
        self.SUB_X = 0x2
        self.SUB_Y = 0x3
        self.RET_AUTO = 0x4
        self.RET_INT = 0x5
        self.RET_FLOAT = 0x6
        self.RET_FRACTION = 0x7
        self.D_U = 0x8
        self.D_D = 0x9
        self.D_L = 0xA
        self.D_R = 0xB
        if k == 0:
            raise ValueError("The coefficient of the primary function is not 0.")
        elif type(k) not in (int,float,fractions.Fraction):
            raise ValueError("The coefficient of the primary function must be an integer/floating-point number.")
        elif type(b) not in (int,float,fractions.Fraction):
            raise ValueError("The primary function b value must be an integer/floating-point number.")
        else:
            self.k = k
            self.b = b
    def getStr(self):
        if self.b == 0:
            if self.k > 0:
                if self.k == 1:
                    return f"y = x"
                else:
                    return f"y = {self.k}x"
            else:
                if self.k == -1:
                    return f"y = -x"
                else:
                    return f"y = {self.k}x"
        else:
            if self.b > 0:
                if self.k > 0:
                    if self.k == 1:
                        return f"y = x+{self.b}"
                    else:
                        return f"y = {self.k}x+{self.b}"
                else:
                    if self.k == -1:
                        return f"y = -x+{self.b}"
                    else:
                        return f"y = {self.k}x+{self.b}"
            else:
                if self.k > 0:
                    if self.k == 1:
                        return f"y = x{self.b}"
                    else:
                        return f"y = {self.k}x{self.b}"
                else:
                    if self.k == -1:
                        return f"y = -x{self.b}"
                    else:
                        return f"y = {self.k}x{self.b}"

    def showStr(self):
        print(self.getStr())

    def is_proportional_function(self):
        if self.b == 0:
            return True
        else:
            return False

    def setK(self,k):
        if k == 0:
            raise ValueError("The coefficient of the primary function is not 0.")
        elif type(k) not in (int,float,fractions.Fraction):
            raise ValueError("The coefficient of the primary function must be an integer/floating-point number.")
        else:
            self.k = k

    def setB(self,b):
        if type(b) not in (int,float,fractions.Fraction):
            raise ValueError("The primary function b value must be an integer/floating-point number.")
        else:
            self.b = b

    def incrementality(self):
        if self.k > 0:
            return self.IC_I
        else:
            return self.IC_D

    def is_increasing(self):
        if self.incrementality() == self.IC_I:
            return True
        else:
            return False

    def is_degression(self):
        if self.incrementality() == self.IC_D:
            return True
        else:
            return False

    def substitution(self,value,category,ret=0x4):
        if category == self.SUB_X:
            if ret == self.RET_AUTO:
                return value*self.k+self.b
            elif ret == self.RET_INT:
                return int(value * self.k + self.b)
            elif ret == self.RET_FLOAT:
                return float(value * self.k + self.b)
            elif ret == self.RET_FRACTION:
                f = value * self.k + self.b
                return fractions.Fraction(*f.as_integer_ratio())
        elif category == self.SUB_Y:
            if ret == self.RET_AUTO:
                return (value-self.b)/self.k
            elif ret == self.RET_INT:
                return int((value - self.b) / self.k)
            elif ret == self.RET_FLOAT:
                return float((value - self.b) / self.k)
            elif ret == self.RET_FRACTION:
                return fractions.Fraction((value-self.b), self.k)

    def is_across(self,point):
        if self.substitution(point[0], self.SUB_X, ret=self.RET_FRACTION) == fractions.Fraction(*point[1].as_integer_ratio()):
            return True
        else:
            return False

    def quadrant(self):
        if self.is_proportional_function():
            if self.k > 0:
                return (1,3)
            elif self.k < 0:
                return (2,4)
        else:
            if self.k > 0:
                if self.b > 0:
                    return (1,2,3)
                else:
                    return (1,3,4)
            else:
                if self.b > 0:
                    return (1,2,4)
                else:
                    return (2,3,4)

    def parse(self):
        return f"({self.k}) * x + ({self.b})"

    def move(self, value, direction):
        if direction == self.D_U:
            self.setB(self.b+value)
        elif direction == self.D_D:
            self.setB(self.b-value)
        elif direction == self.D_L:
            self.setB(self.k*value+self.b)
        elif direction == self.D_R:
            self.setB(-(self.k*value)+self.b)

    def is_parallel_to(self,other):
        if self.k == other.k:
            return True
        else:
            return False

    def is_perpendicular_to(self,other):
        if self.k * other.k == -1:
            return True
        else:
            return False

    def perpendicular(self):
        self.setK((-1)/self.k)

    def copy(self):
        other = OneTimeFunction(self.k,self.b)
        return other

    def getIntersection(self,other,ret=0x4):
        x = (other.b-self.b)/(self.k-other.k)
        y = self.substitution(x,self.SUB_X,ret=ret)
        return (x,y)





    def __repr__(self):
        return self.getStr()

def create(function,x_from,x_to,x_step,y_from,y_to,y_step,hide_y_origin=True):
    x = np.linspace(x_from, x_to, x_step)
    y = eval(function.parse())
    plt.plot(x, y)
    new_ticks = np.linspace(y_from, y_to, y_step)
    plt.yticks(new_ticks)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data', 0))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data', 0))
    yticks = ax.yaxis.get_major_ticks()
    if hide_y_origin == True:
        if int((y_step-1)/2) == (y_step-1)/2:
            yticks[int((y_step-1)/2)].label1.set_visible(False)
    return plt

def function(points,category):
    if category == F_OTF:
        point1 = points[0]
        point2 = points[1]
        x1 = fractions.Fraction(*point1[0].as_integer_ratio())
        y1 = fractions.Fraction(*point1[1].as_integer_ratio())
        x2 = fractions.Fraction(*point2[0].as_integer_ratio())
        y2 = fractions.Fraction(*point2[1].as_integer_ratio())
        k = (y2 - y1) / (x2 - x1)
        b = y1-k*x1
        return OneTimeFunction(fractions.Fraction(*k.as_integer_ratio()),fractions.Fraction(*b.as_integer_ratio()))
    elif category == F_PF:
        point1 = points[0]
        point2 = (0,0)
        x1 = fractions.Fraction(*point1[0].as_integer_ratio())
        y1 = fractions.Fraction(*point1[1].as_integer_ratio())
        x2 = fractions.Fraction(*point2[0].as_integer_ratio())
        y2 = fractions.Fraction(*point2[1].as_integer_ratio())
        k = (y2 - y1) / (x2 - x1)
        b = y1 - k * x1
        return OneTimeFunction(fractions.Fraction(*k.as_integer_ratio()), fractions.Fraction(*b.as_integer_ratio()))
