from setuptools import setup, find_packages


setup(
    name="gcode2scad",
    version=f"0.1",
    description=("Convert Cura gcode to scad"),

    # adding packages
    packages=find_packages(),
    package_data={
        '': ['template.scad'],
    },
    entry_points={
        "console_scripts": [
            "gcode2scad = gcode2scad:main",
        ]
    }
)