#include <ros/ros.h>
#include <std_msgs/Int16.h>
#include <darknet_ros_msgs/BoundingBox.h>

void NumberCallback(const darknet_ros_msgs::BoundingBox &bbox)
{
    ROS_INFO("box_info %d", bbox.xmax-bbox.xmin);
}

int main(int argc, char** argv)
{
    ros::init(argc, argv, "cam_sub_node");
    ros::NodeHandle nh;

    ros::Subscriber sub_number = nh.subscribe("max_bbox", 10, NumberCallback);
    ros::spin();
}
