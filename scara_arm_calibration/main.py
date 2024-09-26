import utils
import solver
from utils import TerminalColor

###############################################################################
# ENTER HERE THE COORDINATES OF THE CALIBRATION POINTS:
###############################################################################


class Points:
    target = [
        [50, 50],  # [x, y]
        [50, 250],
        [250, 250],
        [250, 50],
    ]

    measured = [
        [50.4, 49.2],  # [x, y]
        [49.1, 248.7],
        [249.1, 249.7],
        [250.6, 49.3],
    ]

###############################################################################
# ENTER HERE THE INITIAL/DESIGN VALUES FOR THE ARM:
###############################################################################


class Initial:
    P_length = 220  # proximal arm length in mm
    D_length = 220  # distal arm length in mm
    P_angle = -49  # position of the proximal endstop in degrees
    D_angle = 166  # position of the distal endstop in degrees
    P_positionX = 150  # position of the proximal joint in mm
    P_positionY = -50  # position of the proximal joint in mm

###############################################################################


def solve(num_of_points, points, initial):
    offset = {
        'P': [[0] for _ in range(num_of_points)],
        'D': [[0] for _ in range(num_of_points)]
    }
    offset = solver.calculate_offset(num_of_points, points, initial, offset)
    return solver.solve_for_all_variables(num_of_points, points, initial, offset)


def print_results(results, num_of_points):
    TerminalColor.yellow()
    print(f"\n initial error: {solver.initial_error:4.1f} mm ")
    TerminalColor.red()
    for point in range(num_of_points):
        print(
            f"point {point + 1}:  {solver.errorX[point]:7.3f} {solver.errorY[point]:6.3f}")
    TerminalColor.reverse()
    print(f" final error: {solver.final_error:6.4f} mm ")
    TerminalColor.cyan()
    print("\n results:               ")
    TerminalColor.reset()
    TerminalColor.cyan()
    print(f"P length: {results[0]:14.10f}")
    print(f"D length: {results[1]:14.10f}")
    print(f"P angle:  {results[2]:14.10f}")
    print(f"D angle:  {results[3]:14.10f}")
    print(f"P pos X:  {results[4]:14.10f}")
    print(f"P pos Y:  {results[5]:14.10f}")
    TerminalColor.reverse()
    print(f" iteration cycles: {solver.iteration_cycles:4.0f} \n")
    TerminalColor.reset()


if __name__ == "__main__":
    num_of_points = len(Points.target)
    results = solve(num_of_points, Points, Initial)
    print_results(results, num_of_points)
