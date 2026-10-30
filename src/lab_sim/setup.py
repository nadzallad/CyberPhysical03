import os
from glob import glob
from setuptools import setup

package_name = 'lab_sim'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'worlds'),
            glob('worlds/*.world')),
        (os.path.join('share', package_name, 'rviz'),
            glob('rviz/*.rviz')),
        (os.path.join('share', package_name, 'models', 'turtlebot3_burger_lab'),
            glob('models/turtlebot3_burger_lab/*.*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kelompok',
    maintainer_email='kelompok@lab.ac.id',
    description='Modul 3: simulasi TurtleBot3 di Gazebo dan RViz2',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'obstacle_stop = lab_sim.obstacle_stop:main',
            'square_driver = lab_sim.square_driver:main',
        ],
    },
)
