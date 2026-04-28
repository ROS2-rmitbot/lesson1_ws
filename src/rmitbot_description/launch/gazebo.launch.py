import os
from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch_ros.actions import Node


# Launch the file
# ros2 launch rmitbot_description gazebo.launch.py

def generate_launch_description():
    pkg_dir = get_package_share_directory("rmitbot_description")
    gz_dir = os.path.join(get_package_share_directory("ros_gz_sim"), "launch"), "/gz_sim.launch.py"
    
    # Resource path for gazebo. Required while using stl (robot CAD), and sdf (world)
    gz_resource_path = SetEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH",
        value=[str(Path(pkg_dir).parent.resolve())]
    )

    # Launch Gazebo 
    gazebo = IncludeLaunchDescription(gz_dir, 
        launch_arguments=[("gz_args", [" -v 4", " -r", " empty.sdf", " --render-engine", " ogre"])]
    )
    
    # Spawn the robot in Gazebo
    gz_spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=["-topic", "robot_description","-name", "rmitbot"],
    )

    # Bridge between ROS2 and Gazebo
    gz_ros2_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=["/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock"], 
    )

    return LaunchDescription([
        gz_resource_path,
        gazebo,
        gz_spawn_entity,
        gz_ros2_bridge,
    ])