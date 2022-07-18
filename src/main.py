import terminal_color
import solver

###############################################################################
# ENTER HERE THE COORDINATES OF THE CALIBRATION POINTS:
###############################################################################
class points:
    target = [[49.85, 44.03], # [x, y]
              [49.85, 258.84],
              [257.5, 258.84],
              [400.99, 44.03]]

    measured = [[50.3, 45], # [x, y]
                [50.3, 258],
                [257.3, 258],
                [400.7, 44]]

###############################################################################
# ENTER HERE THE INITIAL/DESIGN VALUES FOR THE ARM:
###############################################################################
class initial:
    P_length = 220 # proximal arm length in mm
    D_length = 220 # proximal arm length in mm
    P_angle = -49 # position of the proximal endstop in degrees
    D_angle = 166 # position of the distal endstop in degrees
    P_positionX = 150 # position of the proximal joint in mm
    P_positionY = -50 # position of the proximal joint in mm
    
###############################################################################

# convert each point from cartesian coordinates to joint angles
NUM_OF_POINTS = len(points.target)
def solve(NUM_OF_POINTS, points, initial):
    class offset:
        P = [[0] for i in range(NUM_OF_POINTS)]
        D = [[0] for i in range(NUM_OF_POINTS)]
    offset = solver.calculate_offset(NUM_OF_POINTS, points, initial, offset)
    # return the results containing the new values for all 6 variables
    return solver.solve_for_all_variables(NUM_OF_POINTS, points, initial, offset)

# print the results
def print_results():
    terminal_color.yellow()
    print("\n initial error:", '{:4.1f}'.format(solver.initial_error), "mm ")
    terminal_color.red()
    for point in range(0, NUM_OF_POINTS):
        print("point " + str(point+1) + ":  " +
            str('{:7.3f}'.format(solver.errorX[point])) + str('{:7.3f}'.format(solver.errorY[point])))
    terminal_color.reverse()
    print(" final error:" + str('{:7.4f}'.format(solver.final_error)) + " mm ")
    terminal_color.cyan()
    print("\n results:               ")
    terminal_color.reset()
    terminal_color.cyan()
    print("P length:", '{:14.10f}'.format(results[0]))
    print("D length:", '{:14.10f}'.format(results[1]))
    print("P angle: ", '{:14.10f}'.format(results[2]))
    print("D angle: ", '{:14.10f}'.format(results[3]))
    print("P pos X: ", '{:14.10f}'.format(results[4]))
    print("P pos Y: ", '{:14.10f}'.format(results[5]))
    terminal_color.reverse()
    print(" iteration cycles:" + str('{:5.0f}'.format(solver.iteration_cycles)) + " ")
    terminal_color.reset()
    #print gcode line
    gcode = str("M669 K4 P" + str('{:.5f}'.format(results[0])) + " D" +
        str('{:.5f}'.format(results[1])) + " A" + str('{:.5f}'.format(results[2])) +
        ":100 B20:" + str('{:.5f}'.format(results[3])) + " X" +
        str('{:.5f}'.format(-results[4])) + " Y" + str('{:.5f}'.format(-results[5])) + "\n")
    print("\n" + "Updated G-code calibration command:")
    print(gcode)
    terminal_color.reset()

if __name__=="__main__":
    # solve and store the new values for all 6 variables
    results = solve(NUM_OF_POINTS, points, initial)
    print_results()