#include "mmWaveDataHdl.hpp"
#include "DataHandlerClass.h"

namespace node1_radarinterface
{

PLUGINLIB_EXPORT_CLASS(node1_radarinterface::mmWaveDataHdl, nodelet::Nodelet);

mmWaveDataHdl::mmWaveDataHdl() {}

void mmWaveDataHdl::onInit()
{
   ros::NodeHandle private_nh = getPrivateNodeHandle();
   
   std::string mySerialPort;
   int myBaudRate;
   int myMaxAllowedElevationAngleDeg;
   int myMaxAllowedAzimuthAngleDeg;
   
   private_nh.getParam("/node1_radarinterface/data_port", mySerialPort);
   
   private_nh.getParam("/node1_radarinterface/data_rate", myBaudRate);
   
   if (!(private_nh.getParam("/node1_radarinterface/max_allowed_elevation_angle_deg", myMaxAllowedElevationAngleDeg)))
   {
      myMaxAllowedElevationAngleDeg = 90;  // Use max angle if none specified
   }

   if (!(private_nh.getParam("/node1_radarinterface/max_allowed_azimuth_angle_deg", myMaxAllowedAzimuthAngleDeg)))
   {
      myMaxAllowedAzimuthAngleDeg = 90;  // Use max angle if none specified
   }

   ROS_INFO("mmWaveDataHdl: data_port = %s", mySerialPort.c_str());
   ROS_INFO("mmWaveDataHdl: data_rate = %d", myBaudRate);
   ROS_INFO("mmWaveDataHdl: max_allowed_elevation_angle_deg = %d", myMaxAllowedElevationAngleDeg);
   ROS_INFO("mmWaveDataHdl: max_allowed_azimuth_angle_deg = %d", myMaxAllowedAzimuthAngleDeg);
   
   DataUARTHandler DataHandler(&private_nh);
   DataHandler.setUARTPort( (char*) mySerialPort.c_str() );
   DataHandler.setBaudRate( myBaudRate );
   DataHandler.setMaxAllowedElevationAngleDeg( myMaxAllowedElevationAngleDeg );
   DataHandler.setMaxAllowedAzimuthAngleDeg( myMaxAllowedAzimuthAngleDeg );
   DataHandler.start();
   
   NODELET_DEBUG("mmWaveDataHdl: Finished onInit function");
}

}



