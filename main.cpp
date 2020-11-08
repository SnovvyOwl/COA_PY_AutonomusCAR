#include<RasPi.h>
#include<iostream>
#include<string>
#include<wiringPi.h>
#include<Arduino.h>
using namespace std;
int main(){
    if(wiringPiSetup()==-1){
        return 1;
    }
    /*Arduino Nano;
    Nano.Start_setup();
    float Start_point;
    float End_point;
    int speed[4]={200,0,-200,0};
    while(1){
        Start_point=millis();
        Nano.Set_BF_position(speed[0]);
        Nano.Set_LR_position(speed[1]);
        Nano.Value_to_T_data();
        Nano.Serial_write();
        Nano.Serial_read();
    }*/
    RasPi  car("localhost",13000);

    return 0;
}
