from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
import os


def generate_launch_description():
    # Get package share directory
    pkg_share = get_package_share_directory('elevation_mapping_cupy')

    # Launch arguments
    rviz_config = LaunchConfiguration('rviz_config')

    declare_rviz_config = DeclareLaunchArgument(
        'rviz_config',
        default_value=os.path.join(pkg_share, 'rviz', 'turtle_example_rviz2.rviz'),
        description='Path to the RViz config file'
    )

    # Include turtlesim_init.launch.py
    turtlesim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'turtlesim_init.launch.py')
        ),
        launch_arguments={'rviz_config': rviz_config}.items()
    )

    # Elevation mapping node
    elevation_mapping_node = Node(
        package='elevation_mapping_cupy',
        executable='elevation_mapping_node',
        name='elevation_mapping',
        output='screen',
        parameters=[
            os.path.join(pkg_share, 'config', 'core', 'core_param.yaml'),
            os.path.join(pkg_share, 'config', 'core', 'example_setup.yaml')
        ]
    )

    return LaunchDescription([
        declare_rviz_config,
        turtlesim_launch,
        elevation_mapping_node
    ])