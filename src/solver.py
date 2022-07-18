from scipy.optimize import minimize
from math import cos, sin, acos, asin, radians, degrees, sqrt, fabs, fsum
import main

# calculate the offset between the end-stops and the arm at each of the calibration points
def calculate_offset(NUM_OF_POINTS, points, initial, offset):
    for point in range(0, NUM_OF_POINTS):
        if points.measured[point][0] < initial.P_positionX: # if the point is on the LEFT side
            offset.P[point] = 180-(degrees(acos((initial.P_length**2+(sqrt((points.measured[point][1]-
                                initial.P_positionY)**2+(initial.P_positionX-points.measured[point][0])**
                                2))**2-initial.D_length**2)/(2*initial.P_length*(sqrt((points.measured[point][1]-
                                initial.P_positionY)**2+(initial.P_positionX-points.measured[point][0])**
                                2))))))-degrees(asin((points.measured[point][1]-initial.P_positionY)/
                                (sqrt((points.measured[point][1]-initial.P_positionY)**2+(initial.P_positionX-
                                points.measured[point][0])**2))))
        else: # if the point is on the RIGHT side
            offset.P[point] = degrees(asin((points.measured[point][1]-initial.P_positionY)/
                                (sqrt((points.measured[point][1]-initial.P_positionY)**2+
                                (initial.P_positionX-points.measured[point][0])**2))))-(degrees(
                                acos((initial.P_length**2+(sqrt((points.measured[point][1]-
                                initial.P_positionY)**2+(initial.P_positionX-points.measured[point][0])**
                                2))**2-initial.D_length**2)/(2*initial.P_length*
                                (sqrt((points.measured[point][1]-initial.P_positionY)**2+
                                (initial.P_positionX-points.measured[point][0])**2))))))
          
        offset.D[point] = 180-(degrees(acos((initial.P_length**2+initial.D_length**2-
                            (sqrt((points.measured[point][1]-initial.P_positionY)**2+
                            (initial.P_positionX-points.measured[point][0])**2))**2)/
                            (2*initial.P_length*initial.D_length))))
    return offset

# use the math solver to find the optimal values for the 6 variables
def solve_for_all_variables(NUM_OF_POINTS, points, initial, offset):
    def cumulative_error(params):
        P_length, D_length, P_angle, D_angle, P_positionX, P_positionY = params
        global final_error, errorX, errorY, iteration_cycles
        current_error = 0
        iteration_cycles += 1
        for point in range(0, NUM_OF_POINTS):
            errorX[point] = (((P_length*cos(radians(P_angle+(offset.P[point]-initial.P_angle))))+
                            P_positionX)-D_length*cos(radians(180-(P_angle+(offset.P[point]-initial.P_angle))-
                            (D_angle+(offset.D[point]-initial.D_angle))))) - points.target[point][0]
            errorY[point] = ((D_length*sin(radians(180-(P_angle+(offset.P[point]-initial.P_angle))-
                            (D_angle+(offset.D[point]-initial.D_angle))))+((P_length*sin(radians(P_angle+
                            (offset.P[point]-initial.P_angle))))+P_positionY))) - points.target[point][1]
            current_error += sqrt((errorX[point]**2) + (errorY[point]**2))
        # print('{:14.10f}'.format(current_error))
        final_error = current_error
        return current_error

    T = 10 # tolerance -> math solver attempt range (+/- T)
    boundaries = ([initial.P_length-T, initial.P_length+T], [initial.D_length-T,
                    initial.D_length+T], [initial.P_angle-T, initial.P_angle+T],
                    [initial.D_angle-T, initial.D_angle+T], [initial.P_positionX-T,
                    initial.P_positionX+T], [initial.P_positionY-T, initial.P_positionY+T])
    initial_guess = [initial.P_length, initial.D_length, initial.P_angle, initial.D_angle,
                    initial.P_positionX, initial.P_positionY]

    # RUN SOLVER
    print("\ncalculating...")
    global initial_error
    initial_error = cumulative_error(initial_guess)
    result = minimize(cumulative_error, initial_guess, method='trust-constr', bounds=boundaries)

    # organize results
    errors = [[0,0] for i in range(NUM_OF_POINTS)] # store the error for each point
    for point in range(0, NUM_OF_POINTS):
        errors[point][0] = errorX[point]
        errors[point][1] = errorY[point]

    results = [[0] for i in range(6)] # store the solver result for each variable
    for x in range(0, 6):
        results[x] = result.x[x]

    return results

if __name__=="__main__":
    print("Please call this code from main.py only")
else:
    # global variables
    initial_error = 0
    errorX = [[0] for i in range(main.NUM_OF_POINTS)]
    errorY = [[0] for i in range(main.NUM_OF_POINTS)]
    final_error = 0
    iteration_cycles = 0