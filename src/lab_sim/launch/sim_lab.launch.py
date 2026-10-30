import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg = get_package_share_directory('lab_sim')
    tb3 = get_package_share_directory('turtlebot3_gazebo')
    gz = get_package_share_directory('gazebo_ros')

    use_sim_time = LaunchConfiguration('use_sim_time')
    world = LaunchConfiguration('world')
    gui = LaunchConfiguration('gui')
    rviz = LaunchConfiguration('rviz')
    autonomy = LaunchConfiguration('autonomy')
    model_sdf = LaunchConfiguration('model_sdf')
    x_pose = LaunchConfiguration('x_pose')
    y_pose = LaunchConfiguration('y_pose')

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('world', default_value=os.path.join(
            pkg, 'worlds', 'lab_arena.world')),
        DeclareLaunchArgument('gui', default_value='true'),
        DeclareLaunchArgument('rviz', default_value='true'),
        DeclareLaunchArgument('autonomy', default_value='true'),
        DeclareLaunchArgument('model_sdf', default_value=os.path.join(
            tb3, 'models', 'turtlebot3_burger', 'model.sdf')),
        DeclareLaunchArgument('x_pose', default_value='-1.5'),
        DeclareLaunchArgument('y_pose', default_value='0.0'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(gz, 'launch', 'gzserver.launch.py')),
            launch_arguments={'world': world}.items()),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(gz, 'launch', 'gzclient.launch.py')),
            condition=IfCondition(gui)),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(tb3, 'launch', 'robot_state_publisher.launch.py')),
            launch_arguments={'use_sim_time': use_sim_time}.items()),

        Node(package='gazebo_ros', executable='spawn_entity.py',
             arguments=['-entity', 'burger', '-file', model_sdf,
                        '-x', x_pose, '-y', y_pose, '-z', '0.01'],
             output='screen'),

        Node(package='rviz2', executable='rviz2',
             arguments=['-d', os.path.join(pkg, 'rviz', 'lab_sim.rviz')],
             parameters=[{'use_sim_time': use_sim_time}],
             condition=IfCondition(rviz), output='screen'),

        Node(package='lab_sim', executable='obstacle_stop',
             name='obstacle_stop',
             parameters=[{'use_sim_time': use_sim_time,
                          'stop_distance': 0.35}],
             condition=IfCondition(autonomy), output='screen'),
    ])
