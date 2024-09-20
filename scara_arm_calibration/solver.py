from scipy.optimize import minimize
from math import cos, sin, acos, asin, radians, degrees, sqrt
import main

# Calculate the offset between the end-stops and the arm at each of the calibration points


def calculate_offset(num_of_points, points, initial, offset):
    for point in range(num_of_points):
        x_diff = points.measured[point][0] - initial.P_positionX
        y_diff = points.measured[point][1] - initial.P_positionY
        distance = sqrt(x_diff**2 + y_diff**2)

        if points.measured[point][0] < initial.P_positionX:  # Point is on the LEFT side
            offset['P'][point] = 180 - degrees(acos((initial.P_length**2 + distance**2 - initial.D_length**2) / (
                2 * initial.P_length * distance))) - degrees(asin(y_diff / distance))
        else:  # Point is on the RIGHT side
            offset['P'][point] = degrees(asin(y_diff / distance)) - degrees(acos(
                (initial.P_length**2 + distance**2 - initial.D_length**2) / (2 * initial.P_length * distance)))

        offset['D'][point] = 180 - degrees(acos((initial.P_length**2 + initial.D_length **
                                                 2 - distance**2) / (2 * initial.P_length * initial.D_length)))

    return offset

# Use the math solver to find the optimal values for the 6 variables


def solve_for_all_variables(num_of_points, points, initial, offset):
    def cumulative_error(params):
        P_length, D_length, P_angle, D_angle, P_positionX, P_positionY = params
        global final_error, errorX, errorY, iteration_cycles
        current_error = 0
        iteration_cycles += 1

        for point in range(num_of_points):
            offset_p_angle = P_angle + (offset['P'][point] - initial.P_angle)
            offset_d_angle = D_angle + (offset['D'][point] - initial.D_angle)
            errorX[point] = ((P_length * cos(radians(offset_p_angle)) + P_positionX) - D_length * cos(
                radians(180 - offset_p_angle - offset_d_angle))) - points.target[point][0]
            errorY[point] = (D_length * sin(radians(180 - offset_p_angle - offset_d_angle)) + (
                P_length * sin(radians(offset_p_angle)) + P_positionY)) - points.target[point][1]
            current_error += sqrt(errorX[point]**2 + errorY[point]**2)

        final_error = current_error
        return current_error

    tolerance = 10  # Tolerance -> math solver attempt range (+/- tolerance)
    boundaries = [
        (initial.P_length - tolerance, initial.P_length + tolerance),
        (initial.D_length - tolerance, initial.D_length + tolerance),
        (initial.P_angle - tolerance, initial.P_angle + tolerance),
        (initial.D_angle - tolerance, initial.D_angle + tolerance),
        (initial.P_positionX - tolerance, initial.P_positionX + tolerance),
        (initial.P_positionY - tolerance, initial.P_positionY + tolerance)
    ]
    initial_guess = [
        initial.P_length, initial.D_length, initial.P_angle, initial.D_angle,
        initial.P_positionX, initial.P_positionY
    ]

    # Run solver
    print("\nCalculating...")
    global initial_error
    initial_error = cumulative_error(initial_guess)
    result = minimize(cumulative_error, initial_guess,
                      method='trust-constr', bounds=boundaries)

    # Organize results
    # Store the error for each point
    errors = [[0, 0] for _ in range(num_of_points)]
    for point in range(num_of_points):
        errors[point][0] = errorX[point]
        errors[point][1] = errorY[point]

    # Store the solver result for each variable
    results = [result.x[i] for i in range(6)]

    return results


if __name__ == "__main__":
    print("Please call this code from main.py only")
else:
    # Global variables
    initial_error = 0
    num_of_points = len(main.Points.target)
    errorX = [[0] for _ in range(num_of_points)]
    errorY = [[0] for _ in range(num_of_points)]
    final_error = 0
    iteration_cycles = 0
