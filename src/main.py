from scipy.optimize import minimize
from math import cos, sin, acos, asin, radians, degrees, sqrt, fabs, fsum
from time import sleep, time
import sys

###############################################################################
# calibration points
target_points = [[49.85, 44.03],
                 [49.85, 258.84],
                 [257.5, 258.84],
                 [400.99, 44.03]]

measured_points = [[50.3, 45],
                   [50.3, 258],
                   [257.3, 258],
                   [400.7, 44]]

NUM_OF_POINTS = len(target_points)

###############################################################################
# initial values (from the config file)
P_length_initial = 220 #proximal arm length in mm
D_length_initial = 220 #proximal arm length in mm
P_angle_initial = -49 #position of the proximal endstop in degrees
D_angle_initial = 166 #position of the distal endstop in degrees
P_positionX_initial = 150 #position of the proximal joint in mm
P_positionY_initial = -50 #position of the proximal joint in mm

###############################################################################
# convert each point from cartesian coordinates to joint angles
P_offset = [[0] for i in range(NUM_OF_POINTS)]
D_offset = [[0] for i in range(NUM_OF_POINTS)]

for point in range(0, NUM_OF_POINTS):
    if measured_points[point][0] < P_positionX_initial:
        P_offset[point] = 180-(degrees(acos((P_length_initial**2+(sqrt((measured_points[point][1]-
            P_positionY_initial)**2+(P_positionX_initial-measured_points[point][0])**
            2))**2-D_length_initial**2)/(2*P_length_initial*(sqrt((measured_points[point][1]-
            P_positionY_initial)**2+(P_positionX_initial-measured_points[point][0])**
            2))))))-degrees(asin((measured_points[point][1]-P_positionY_initial)/
            (sqrt((measured_points[point][1]-P_positionY_initial)**2+(P_positionX_initial-
            measured_points[point][0])**2))))
    else:
        P_offset[point] = degrees(asin((measured_points[point][1]-P_positionY_initial)/
            (sqrt((measured_points[point][1]-P_positionY_initial)**2+
            (P_positionX_initial-measured_points[point][0])**2))))-(degrees(
            acos((P_length_initial**2+(sqrt((measured_points[point][1]-
            P_positionY_initial)**2+(P_positionX_initial-measured_points[point][0])**
            2))**2-D_length_initial**2)/(2*P_length_initial*
            (sqrt((measured_points[point][1]-P_positionY_initial)**2+
            (P_positionX_initial-measured_points[point][0])**2))))))
    D_offset[point] = 180-(degrees(acos((P_length_initial**2+D_length_initial**2-
        (sqrt((measured_points[point][1]-P_positionY_initial)**2+
        (P_positionX_initial-measured_points[point][0])**2))**2)/
        (2*P_length_initial*D_length_initial))))

###############################################################################
# solver
T = 10 # tolerance -> math solver attempt range (+/- T)
boundaries = ([P_length_initial-T, P_length_initial+T], [D_length_initial-T,
    D_length_initial+T], [P_angle_initial-T, P_angle_initial+T],
    [D_angle_initial-T, D_angle_initial+T], [P_positionX_initial-T,
    P_positionX_initial+T], [P_positionY_initial-T, P_positionY_initial+T])
initial_guess = [P_length_initial, D_length_initial, P_angle_initial, D_angle_initial,
    P_positionX_initial, P_positionY_initial]
    # P_length, D_length, P_angle, D_angle, P_positionX, P_positionY
initial_error = 0
errorX = [[0] for i in range(NUM_OF_POINTS)]
errorY = [[0] for i in range(NUM_OF_POINTS)]
final_error = 0
iteration_cycles = 0

def cumulative_error(params):
    P_length, D_length, P_angle, D_angle, P_positionX, P_positionY = params
    global final_error, errorX, errorY, iteration_cycles
    error = 0
    iteration_cycles += 1
    for point in range(0, NUM_OF_POINTS):
        errorX[point] = (((P_length*cos(radians(P_angle+(P_offset[point]-P_angle_initial))))+
            P_positionX)-D_length*cos(radians(180-(P_angle+(P_offset[point]-P_angle_initial))-
            (D_angle+(D_offset[point]-D_angle_initial))))) - target_points[point][0]
        errorY[point] = ((D_length*sin(radians(180-(P_angle+(P_offset[point]-P_angle_initial))-
            (D_angle+(D_offset[point]-D_angle_initial))))+((P_length*sin(radians(P_angle+
            (P_offset[point]-P_angle_initial))))+P_positionY))) - target_points[point][1]
        #error += (fabs(errorX[point]) + fabs(errorY[point]))
        error += sqrt((errorX[point]**2) + (errorY[point]**2))
    #print('{:14.10f}'.format(error))
    final_error = error
    return error

sys.stdout.write("\033[93m") #yellow
print("\ncalculating...")
sys.stdout.write("\033[0m") #reset
print("")
initial_error = cumulative_error(initial_guess) # RUN SOLVER
result = minimize(cumulative_error, initial_guess, method='trust-constr', bounds=boundaries)

###############################################################################
# organize results
errors = [[0,0] for i in range(NUM_OF_POINTS)] # store the error for each point
for point in range(0, NUM_OF_POINTS):
    errors[point][0] = errorX[point]
    errors[point][1] = errorY[point]

results = [[0] for i in range(6)] # store the solver result for each variable
for x in range(0, 6):
    results[x] = result.x[x]

###############################################################################
# print results
if result.success:
    sys.stdout.write("\033[93m") #yellow
    sys.stdout.write("\033[7m") #reverse
    print("\n initial error:", '{:4.1f}'.format(initial_error), "mm ")
    sys.stdout.write("\033[0m") #reset
    sys.stdout.write("\033[91m") #red
    for point in range(0, NUM_OF_POINTS):
        print("point " + str(point+1) + ":  " +
            str('{:7.3f}'.format(errorX[point])) + str('{:7.3f}'.format(errorY[point])))
    sys.stdout.write("\033[7m") #reverse
    print(" final error:" + str('{:7.4f}'.format(final_error)) + " mm ")
    sys.stdout.write("\033[96m") #cyan
    print("\n results:               ")
    sys.stdout.write("\033[0m") #reset
    sys.stdout.write("\033[96m") #cyan
    print("P length:", '{:14.10f}'.format(results[0]))
    print("D length:", '{:14.10f}'.format(results[1]))
    print("P angle: ", '{:14.10f}'.format(results[2]))
    print("D angle: ", '{:14.10f}'.format(results[3]))
    print("P pos X: ", '{:14.10f}'.format(results[4]))
    print("P pos Y: ", '{:14.10f}'.format(results[5]))
    sys.stdout.write("\033[7m") #reverse
    print(" iteration cycles:" + str('{:5.0f}'.format(iteration_cycles)) + " ")
    sys.stdout.write("\033[0m") #reset
    #print gcode line
    sys.stdout.write("\033[0m") #reset
    sys.stdout.write("\033[2m") #dim
    gcode = str("M669 K4 P" + str('{:.5f}'.format(results[0])) + " D" +
        str('{:.5f}'.format(results[1])) + " A" + str('{:.5f}'.format(results[2])) +
        ":100 B20:" + str('{:.5f}'.format(results[3])) + " X" +
        str('{:.5f}'.format(-results[4])) + " Y" + str('{:.5f}'.format(-results[5])) + "\n")
    print("\n" + gcode)
    sys.stdout.write("\033[0m") #reset
else:
    raise ValueError(result.message)

    #M98 P"0:/macros/CALIBRATION_GRID" # call g-code file
