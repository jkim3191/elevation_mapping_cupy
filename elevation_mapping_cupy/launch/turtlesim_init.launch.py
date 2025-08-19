
import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution, TextSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    try:
        elevation_mapping_cupy_dir = get_package_share_directory('elevation_mapping_cupy')
        print(f"elevation_mapping_cupy_dir: {elevation_mapping_cupy_dir}\n")
        turtlebot3_description_dir = get_package_share_directory('turtlebot3_description')
    except Exception as e:
        print(f"Error getting package directory: {e}\n")

    print(f"elevation_mapping_cupy_dir: {elevation_mapping_cupy_dir}\n")
    print(f"turtlebot3_description_dir: {turtlebot3_description_dir}\n")

    # Declare launch arguments
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )

    rviz_config_arg = DeclareLaunchArgument(
        'rviz_config',
        default_value=PathJoinSubstitution([
            elevation_mapping_cupy_dir, 'rviz', 'turtle_sim_laser.rviz'
        ]),
        description='Path to the RViz config file'
    )

    # print rviz config used
    print(f"rviz_config: {rviz_config_arg}")

    model_arg = DeclareLaunchArgument(
        'model',
        default_value='waffle',
        description='Model type [burger, waffle, waffle_pi]'
    )

    x_pos_arg = DeclareLaunchArgument(
        'x_pos',
        default_value='0.0',
        description='Initial X position of the robot'
    )

    y_pos_arg = DeclareLaunchArgument(
        'y_pos',
        default_value='2.0',
        description='Initial Y position of the robot'
    )

    z_pos_arg = DeclareLaunchArgument(
        'z_pos',
        default_value='0.0',
        description='Initial Z position of the robot'
    )

    # Launch configurations
    use_sim_time = LaunchConfiguration('use_sim_time')
    rviz_config = LaunchConfiguration('rviz_config')
    model = LaunchConfiguration('model')
    x_pos = LaunchConfiguration('x_pos')
    y_pos = LaunchConfiguration('y_pos')
    z_pos = LaunchConfiguration('z_pos')

    # Set the /use_sim_time parameter
    use_sim_time_param = Node(
        package='rclcpp_components',
        executable='parameter_server',
        name='use_sim_time_param',
        parameters=[{'use_sim_time': use_sim_time}]
    )

    static_tf_prefix_publisher = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='base_footprint_to_turtlebot3_base_footprint',
        arguments=[
            '0', '0', '0',  # x, y, z translation
            '0', '0', '0',  # roll, pitch, yaw rotation
            'base_footprint', 'turtlebot3_base_footprint'  # parent frame, child frame
        ],
        output='screen'
    )

    robot_description_content = Command([
            'xacro ',
            PathJoinSubstitution([
                turtlebot3_description_dir, 'urdf', 'turtlebot3_waffle.urdf'
            ]),
            ' namespace:=turtlebot3_'
        ])

    robot_description = {'robot_description': robot_description_content}

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            robot_description,
            {
                'use_sim_time': use_sim_time,
                'publish_frequency': 50.0,
                'ignore_timestamp': False
            }
        ]
    )

    ld = LaunchDescription()

    # Add the declared arguments
    ld.add_action(use_sim_time_arg)
    ld.add_action(rviz_config_arg)
    ld.add_action(model_arg)
    ld.add_action(x_pos_arg)
    ld.add_action(y_pos_arg)
    ld.add_action(z_pos_arg)

    ld.add_action(static_tf_prefix_publisher)  
    ld.add_action(robot_state_publisher)  
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )
    
    ld.add_action(rviz_node)

    return ld