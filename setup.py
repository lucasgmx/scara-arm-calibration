from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="scara_arm_calibration",
    version="0.1.0",
    author="Lucas Marques",
    author_email="lucas@marques.llc",
    description="A Python package for calibrating a SCARA robotic arm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # Replace with your repo URL
    url="https://github.com/lucasgmx/scara-arm-calibration",
    packages=find_packages(),
    install_requires=[
        'numpy>=2.1.1',
        'scipy>=1.14.1',
    ],
    entry_points={
        'console_scripts': [
            'scara_calibrate=scara_arm_calibration.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Robotics',
    ],
    python_requires='>=3.6',
    license="MIT",
)
