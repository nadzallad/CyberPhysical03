from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    threshold = LaunchConfiguration('threshold')

    return LaunchDescription([
        DeclareLaunchArgument(
            'threshold',
            default_value='0.5',
            description='Threshold untuk processing_node',
        ),

        Node(
            package='lab_comm',
            executable='sensor_publisher',
            name='sensor_publisher',
            output='screen',
        ),

        Node(
            package='lab_comm',
            executable='sensor_subscriber',
            name='sensor_subscriber',
            output='screen',
        ),

        Node(
            package='lab_comm',
            executable='processing_node',
            name='processing_node',
            parameters=[{
                'threshold': ParameterValue(threshold, value_type=float)
            }],
            output='screen',
        ),

        Node(
            package='lab_comm',
            executable='reset_service',
            name='reset_service',
            output='screen',
        ),

        Node(
            package='lab_comm',
            executable='motion_action_server',
            name='motion_action_server',
            output='screen',
        ),
    ])
