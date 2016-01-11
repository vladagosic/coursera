import  math

a = 1

def s():
    print "|", a

s()

def project_to_distance(point_x, point_y, distance):
    dist_to_origin = (point_x ** 2 + point_y ** 2) ** (1.0 / 2)
    scale = distance / dist_to_origin
    print point_x * scale, point_y * scale

print project_to_distance(2, 7, 4)

print("********")

#

def c(sides, length):
    return  1.0 / 4 * sides * length ** 2 / math.tan(math.pi / sides)

print( c(5,7))
print( c(7,3))

print("**************")

def future_value(present_value, annual_rate, periods_per_year, years):
    rate_per_period = annual_rate / periods_per_year
    periods = periods_per_year * years

    # Put your code here.
    return  present_value * (1 + rate_per_period) ** periods

print "$1000 at 2% compounded daily for 3 years yields $", future_value(1000, .02, 365, 3)

print( future_value(500, .04, 10, 10))

print("********************")
__author__ = 'Vlada'

p = False
q = True

print not (p or not q)

n = 123
n1 = 123.4

print((n / 10) % 10)
print((n1 / 10) % 10)


## f(x) = -5 x^5 + 69 x^2 - 47

def f(x):
    return -5 * x ** 5 + 69 * x ** 2 - 47

print f(0)
print f(1)
print f(2)
print f(3)

print math.log(10000, 10)
