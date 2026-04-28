import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration

# Launch the file
# ros2 launch rmitbot_description rviz.launch.py is_sim:=true

def generate_launch_description():
    # ==========================================
    # 1. Capture the 'is_sim' configuration
    is_sim = LaunchConfiguration('is_sim')
    
    # ==========================================
    # 2. Declare the launch argument (this shows up in --help)
    declare_is_sim_arg = DeclareLaunchArgument(
        'is_sim',
        default_value='false',
        description='Use Gazebo or hardware interface'
    )
  
    # ==========================================
    # 3. Rviz launch
    rmit_dir = get_package_share_directory("rmitbot_description")
    rviz_config = os.path.join(rmit_dir, 'rviz', 'display.rviz')
       
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config],
        parameters=[{"use_sim_time": is_sim}],
    )
    
    # ==========================================
    return LaunchDescription([
        declare_is_sim_arg,
        rviz, 
    ])