# SCARA Arm Calibration

This repository provides a Python-based calibration algorithm for a SCARA (Selective Compliance Articulated Robot Arm). The algorithm adjusts key variables to align the physical arm's position with a virtual model by minimizing the error between the two systems using a mathematical solver.

![image](https://github.com/user-attachments/assets/a6e081bb-2251-45fe-9c38-5d8a8b95f794)

## Project Overview

The calibration adjusts the following six variables:

1. **Distal Arm Length**
2. **Proximal Arm Length**
3. **Distal Joint Angle**
4. **Proximal Joint Angle**
5. **Proximal Joint X Position**
6. **Proximal Joint Y Position**

![image](https://github.com/user-attachments/assets/bbb03fe7-335e-4b19-92b8-c6c5534de286)

The calibration process compares the real-world arm's X-Y coordinates with a virtual ideal model, then iteratively minimizes the difference (error) between the two by adjusting the six parameters. The goal is to ensure the SCARA arm positions accurately align with the virtual model.

## Features

- Iteratively calculates and adjusts joint positions and arm lengths.
- Uses four reference points on the SCARA arm’s workspace.
- Mathematical solver minimizes the error between real-world and virtual model coordinates.

## Installation

Clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/lucasgmx/scara-arm-calibration.git
cd scara-arm-calibration
pip install -r requirements.txt
```

## Usage

To run the calibration, use:

```bash
python3 main.py
```

## Parameter Adjustment Instructions

To customize the calibration points and initial design values for your SCARA arm, edit the following sections in `main.py`:

### Calibration Points

Locate the section for calibration points in `main.py`:

```python
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
```

- __target__: These are the ideal coordinates where the SCARA arm should reach.
- __measured__: These coordinates represent the actual positions the SCARA arm reaches. Adjust these values based on your measurements during calibration.

### Initial Design Values

Next, locate the section for initial design values:

```python
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
```

Make sure to save your changes in `main.py` before running the calibration script.

## More Information

For more information about this project, visit my website: [SCARA Arm Project](https://www.lucasgmarques.com/projects/scara)
