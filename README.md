# SCARA Arm Calibration

A Python package to calibrate a SCARA robotic arm by optimizing six key parameters: the distal and proximal arm lengths, joint angles, and the X-Y Cartesian position of the proximal joint (the base of the arm).

## Features

- Calibrate arm parameters to minimize error between real-world and ideal model.
- Supports customizable arm configurations.
- Easy-to-use command-line interface for calibration.

## Installation

You can install this package using pip:

```bash
pip install git+https://github.com/your-username/scara-arm-calibration.git
```

## Usage

To calibrate the SCARA arm, run the following command in your terminal:

```bash
scara_calibrate --input angles.txt --output calibrated_params.txt
```

## Files

- **main.py**: Core logic for calibration.
- **solver.py**: Solver algorithms to minimize the error between real and model coordinates.
- **utils.py**: Utility functions for calculations and transformations.
- **cli.py**: Command-line interface handler.

## Testing

Run unit tests with:

```bash
pytest
```
