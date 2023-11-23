# box_car
ROS2 Humble

#Second The Construct:
  # Here we place usefull commands for many things in ROS2 used for the tutorials
  
  # Tutorial 1: Creation of your car
  # We create a CMake version for the description package
    ros2 pkg create --build-type ament_cmake box_car_description
    cd box_car_description
    mkdir launch robot
  
    ros2 pkg create --build-type ament_cmake box_car_gazebo
    cd box_car_gazebo
    mkdir launch worlds
  
    ros2 pkg create --build-type ament_cmake box_car_tutorials
    cd box_car_tutorials
    mkdir launch scripts
  
  # We add dependencies for python to have a hibrid package to be used for C++ and python for the future
  
  # Start sim
    reset;ros2 launch box_car_gazebo box_bot_launch.py
  # Move the Car
    ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args --remap cmd_vel:=/box_bot/cmd_vel
  # Turn Wheels
    ros2 control load_controller --set-state start joint_state_broadcaster
    ros2 control load_controller --set-state start joint_trajectory_controller
    ros2 launch box_car_description steering.launch.py
