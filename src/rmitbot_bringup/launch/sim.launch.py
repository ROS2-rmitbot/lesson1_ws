import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node


# Launch the file
# ros2 launch rmitbot_bringup sim.launch.py

def generate_launch_description():
    rviz_launch =       os.path.join(get_package_share_directory("rmitbot_description"),"launch", "rviz.launch.py")
    rsp_launch =        os.path.join(get_package_share_directory("rmitbot_description"),"launch", "rsp.launch.py")
    gsim_launch =       os.path.join(get_package_share_directory("rmitbot_description"),"launch", "gazebo.launch.py")
    
    rviz =      IncludeLaunchDescription(rviz_launch, launch_arguments={'is_sim': 'true',}.items())
    rsp =       IncludeLaunchDescription(rsp_launch, launch_arguments={'is_sim': 'true',}.items())
    gz_sim =    IncludeLaunchDescription(gsim_launch, launch_arguments={'is_sim': 'true',}.items())
    
    # Publish the joint state TF - Not needed with a controller
    jsp_gui = Node(
        package=    'joint_state_publisher_gui',
        executable= 'joint_state_publisher_gui',
    )

    
    return LaunchDescription([
        rviz, 
        rsp,
        gz_sim, 
        jsp_gui, 
    ])