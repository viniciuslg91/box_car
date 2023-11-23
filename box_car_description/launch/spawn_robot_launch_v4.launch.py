import os
from ament_index_python.packages import get_package_prefix
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

import xacro

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    pkg_box_car_description = get_package_share_directory('box_car_description')
    xacro_file = os.path.join(get_package_share_directory('box_car_description'), 'robot/', 'box_bot.xacro')    
    assert os.path.exists(xacro_file), "The box_bot.xacro doesnt exist in "+str(xacro_file)

    install_dir = get_package_prefix('box_car_description')

    if 'GAZEBO_MODEL_PATH' in os.environ:
        os.environ['GAZEBO_MODEL_PATH'] =  os.environ['GAZEBO_MODEL_PATH'] + ':' + install_dir + '/share'
    else:
        os.environ['GAZEBO_MODEL_PATH'] =  install_dir + "/share"

    if 'GAZEBO_PLUGIN_PATH' in os.environ:
        os.environ['GAZEBO_PLUGIN_PATH'] = os.environ['GAZEBO_PLUGIN_PATH'] + ':' + install_dir + '/lib'
    else:
        os.environ['GAZEBO_PLUGIN_PATH'] = install_dir + '/lib'


    robot_description_config = xacro.process_file(xacro_file)
    robot_desc = robot_description_config.toxml()

    print(robot_desc)
    
    start_steering_control = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_box_car_description, 'launch', 'steering_control.launch.py'),
        )
    ) 

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),
        Node(package='box_car_description', executable='spawn_box_bot.py', arguments=[robot_desc], output='screen'),
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            parameters=[
                {"robot_description": robot_desc}],
            output="screen"),
        #start_steering_control,
    ])

