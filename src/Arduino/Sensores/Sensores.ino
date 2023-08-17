#include <ros.h>
#include <std_msgs/Float32MultiArray.h>

//US Sensors
const int US[8] = {0, 1, 2, 3, 4, 5, 6, 7};
float sensor_data[8];
//ROS
ros::NodeHandle nh;
std_msgs::Float32MultiArray msg;
//Publisher
ros::Publisher pub("/sensor_data", &msg);

volatile unsigned long TimeBackup=0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(57600);
  nh.initNode();
  nh.getHardware()->setBaud(57600);
  nh.advertise(pub);
}

void loop() {
  // put your main code here, to run repeatedly:
  for (int i=0; i<=7; i++) {
      sensor_data[i] = read_US(i);
  }
  if(millis()-TimeBackup>=100){
    // Set the message data
    msg.data_length = 8;
    msg.data = sensor_data;
      
    // Publish the message
    pub.publish(&msg);
    TimeBackup=millis();
  }
  nh.spinOnce();
  
  /*Serial.print("US1 :");
  Serial.print(sensor_data[0]);
  Serial.print("US2 :");
  Serial.print(sensor_data[1]);
  Serial.print("US3 :");
  Serial.print(sensor_data[2]);
  Serial.print("US4 :");
  Serial.print(sensor_data[3]);
  Serial.print("US5 :");
  Serial.print(sensor_data[4]);
  Serial.print("US6 :");
  Serial.print(sensor_data[5]);
  Serial.print("US7 :");
  Serial.print(sensor_data[6]);
  Serial.print("US8 :");
  Serial.println(sensor_data[7]);
  */
  
}
float read_US(int sensor) {
    float raw = 0, distance = 0;
    raw = analogRead(US[sensor]);
    distance = raw*0.5;
    
    //Return in meters
    return distance/100;
}
