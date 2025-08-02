from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    elevation_mapping_cupy_dir = get_package_share_directory('elevation_mapping_cupy')

    # Declare launch arguments
    rviz_config_arg = DeclareLaunchArgument(
        'rviz_config',
        default_value=PathJoinSubstitution([
            elevation_mapping_cupy_dir,
            'rviz',
            'turtle_example_rviz2.rviz'
        ]),
        description='Path to the RViz config file'
    )

    return LaunchDescription([
        # Declare arguments
        rviz_config_arg,

        # Include the turtlesim_init launch file
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    elevation_mapping_cupy_dir,
                    'launch',
                    'turtlesim_init.launch.py'
                ])
            ),
            launch_arguments={
                'rviz_config': LaunchConfiguration('rviz_config')
            }.items()
        ),

        # Elevation Mapping Node
        Node(
            package='elevation_mapping_cupy',
            executable='elevation_mapping_node',
            name='elevation_mapping',
            parameters=[
                PathJoinSubstitution([
                    elevation_mapping_cupy_dir,
                    'config',
                    'core',
                    'core_param.yaml'
                ]),
                PathJoinSubstitution([
                    elevation_mapping_cupy_dir,
                    'config',
                    'setups',
                    'turtle_bot',
                    'turtle_bot_simple.yaml'
                ])
            ],
            output='screen'
        )
    ]) 