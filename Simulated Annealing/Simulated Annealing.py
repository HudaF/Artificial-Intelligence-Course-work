import math
import random
import matplotlib.pyplot as plt


def f1(x,y):
    return (x**2) + (y**2)


def f2(x,y):
    return (100 * ((x**2) - (y**2))) + ((1 - x)**2)


def f3(x,y):
    return ((x**2 + y**2)/4000) - (math.cos(x) * math.cos(y/math.sqrt(2))) + 1


def calculate_probability(delta_f,temp):
    return math.e ** (delta_f / temp)


def get_successors(point,diff):
    succ = [None]*8
    succ[0] = ((point[0] + diff), (point[1]+0))
    succ[1] = ((point[0] + diff), (point[1] + diff))
    succ[2] = ((point[0] + 0), (point[1] + diff))
    succ[3] = ((point[0] - diff), (point[1] + diff))
    succ[4] = ((point[0] - diff), (point[1] + 0))
    succ[5] = ((point[0] - diff), (point[1] - diff))
    succ[6] = ((point[0] + 0), (point[1] - diff))
    succ[7] = ((point[0] + diff), (point[1] - diff))
    return  succ


def check_bounds(point,point_range):
    if point[0]>=point_range[0] and point[0]<=point_range[1]:
        if point[1]>=point_range[2] and point[1]<=point_range[3]:
            return  True
    return False

def Simulated_Annealing(f,point_range = (-math.inf, math.inf, -math.inf, math.inf) ,to_find_max = True, up_to = 0, diff = 0.1):
    #point_range = (min x, max x, min y, max y)
    path = []

    point = (round((random.uniform(point_range[0], point_range[1])), up_to), round((random.uniform(point_range[2], point_range[3])), up_to))
    path.append(point)

    temp = 10000
    threshold = 1
    alpha = 0.99 #tempetaure decay value

    while (temp>threshold):
        neighbours = []
        for i in get_successors(point,diff):
            if check_bounds(i,point_range):
                neighbours.append(i)

        rand_point = neighbours[random.randint(0,len(neighbours)-1)]
        delta_f = f(rand_point[0],rand_point[1]) - f(point[0],point[1])

        if to_find_max: # if we are looking for max value
            if delta_f > 0:
                point = rand_point
                path.append(point)
            elif calculate_probability(delta_f,temp) > (random.randint(0,100))/100:
                point = rand_point
                path.append(point)

        if not to_find_max: # if we are looking for min value
            if delta_f < 0:
                point = rand_point
                path.append(point)
            elif calculate_probability(-delta_f,temp) > (random.randint(0,100))/100:
                point = rand_point
                path.append(point)

        temp = temp * alpha
    return path


def visualize_path(func, path):
    x = [i[0] for i in path]
    y = [j[1] for j in path]
    z = [func(k[0],k[1]) for k in path]

    # Point plot
    fig, (ax1, ax2) = plt.subplots(2,1)
    ax1.set_xlabel("number of iterations")
    ax1.set_title("Value of point w.r.t time")
    ax1.plot(range(len(x)), x, 'r', label = 'x')
    ax1.plot(range(len(x)), y, 'g', label = 'y')
    ax1.legend()

    # Function plot
    ax2.plot(range(len(x)), z, label = 'f(x,y)')
    ax2.set_xlabel("number of iterations")
    ax2.set_ylabel("f(x,y)")
    ax2.set_title("Value of f(x,y) w.r.t time")

    fig.tight_layout()
    plt.show()

sphere = Simulated_Annealing(f1,(-5,5,-5,5),True,0,0.2)
rosenbrock = Simulated_Annealing(f2,(-2,2,-1,3),True)
griewank = Simulated_Annealing(f3,(-30,30,-30,30),True)


#visualize_path(f1, Simulated_Annealing(f1,sphere))
#visualize_path(f2,rosenbrock)
visualize_path(f3, griewank)


