import argparse
import sys
import numpy as np
import itertools


parser = argparse.ArgumentParser(description='Calculate minimal partition for pythagorean triple')
parser.add_argument('x', metavar='x', type=int, nargs='+',
                                   help='x^2 + y^2 = z^2')
parser.add_argument('y', metavar='y', type=int, nargs='+',
                                   help='x^2 + y^2 = z^2')
parser.add_argument('z', metavar='z', type=int, nargs='+',
                                   help='x^2 + y^2 = z^2')

args = parser.parse_args()

class Triple:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
         return '('+str(self.x)+', '+str(self.y)+', '+str(self.z)+')'

class Rect:
    def __init__(self, picture, width, height):
        self.picture = picture
        self.width = width
        self.height = height

    def __str__(self):
        if self.picture.startswith('B'):
            return self.picture
        return self.picture+' (width: '+str(self.width)+', height: '+str(self.height)+')'

    def __repr(self):
        return str(self)

def is_finished(rects, val):
    # is sum(area(rect)) correct?
    tmp = 0
    for rect in rects:
            tmp+=rect.width*rect.height
    return val==tmp

def build_split_up(rest_of_c, rest_of_d):
    sol = []
    x,y = rest_of_d.width, rest_of_d.height
    while(not is_finished(sol, x*y)):
        if rest_of_c.width < rest_of_d.width:
            starter_width = rest_of_c.width
            if rest_of_c.height * 2 < rest_of_d.height:
                starter_height = rest_of_c.height
            else:
                starter_height = rest_of_d.height/2
            rest_of_d= Rect('dummy', rest_of_d.width-rest_of_c.width, rest_of_d.height)
            rest_of_c= Rect('dummy', rest_of_c.width, rest_of_c.height-starter_height)
        else:
            starter_width = rest_of_d.width
            if rest_of_c.height * 2 < rest_of_d.height:
                starter_height = rest_of_c.height
            else:
                starter_height = rest_of_d.height/2
            rest_of_d= Rect('dummy', rest_of_d.width, rest_of_d.height-rest_of_c.height*2)
            rest_of_c= Rect('dummy', rest_of_c.width-starter_width, rest_of_c.height)
        sol1 = Rect('Part of D from splitted Cs in Picture', starter_width, starter_height)
        sol.append(sol1)
        sol.append(sol1)
    return sol

def calc(triple):
    solution = []
    # append square with area=y^2 (PICTURE: A)
    solution.append(Rect('A in Picture', triple.y, triple.y))
    # append rect angle form (PICTURE: B)
    solution.append(Rect('B in Picture', triple.x, triple.z-triple.y))

    # missing pieces(2 equal forms with width m=z-x and height n=z-y (PICTURE: C)) which we have to split up to fill rest_of_d.size n^2 with n = x-(z-y))
    # together with rect angle form with minimal possible amount of pieces
    c = Rect('dummy', triple.z-triple.x, triple.z-triple.y)
    d_length = triple.x-(triple.z-triple.y)
    d = Rect('dummy', d_length, d_length)

    # do the minimal split up and append result to solution
    solution += build_split_up(c, d)

    return solution


x,y,z = vars(args).get('x')[0], vars(args).get('y')[0], vars(args).get('z')[0]
if pow(x,2) + pow(y,2) != pow(z, 2):
    print("x,y,z is not a pythagorean triple")
    sys.exit(0)
trip = Triple(x if x < y else y ,y if x < y else x,z)

res = calc(trip)
print("##########################")
print("# x="+str(x)+", y="+str(y)+", z="+str(z))
print("# x^2 + y^2 = z^2")
print("# _________________")
print("# |  C   |         |")
print("# |______|______ B |")
print("# |            |   |")
print("# |            |   |")
print("# |     A      |___|")
print("# |            |   |")
print("# |            | C |")
print("# |____________|___|")
print("#")
print("#  area(complete square = z^2 = " + str(pow(z,2)))
print("#  area(A) = y^2 = " + str(pow(y,2)))
print("#  length_out(B) = x = " +str(x))
print("#  length_inner(B) = x-(z-y) = " +str(x-(z-y)))
print("#  area(C) = z-x*z-y = "+str(z-x)+"*"+str(z-y)+" = "+str((z-x)*(z-y)))
print("#")
print("# Build D out of 2 Cs with minimum splitups")
print("#")
print("# square with size x^2 " + "square with size y^2")
print("# _________________ " + "   " + "_________________")
print("# |                |" + "   " + "|                |")
print("# |____________  B |" + "   " + "|                |")
print("# |            |   |" + "   " + "|                |")
print("# |            |   |" + "   " + "|       A        |")
print("# |     D      |   |" + "   " + "|                |")
print("# |            |   |" + "   " + "|                |")
print("# |            |   |" + "   " + "|                |")
print("# |____________|___|" + "   " + "|________________|")
print("#")
print("##########################")
print("Result Parts:")
for x in res:
    print(str(x))
print("total: "+ str(len(res)))
