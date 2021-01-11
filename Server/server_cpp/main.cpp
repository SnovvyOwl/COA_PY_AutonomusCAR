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
    RasPi  car("bluetank.iptime.org",13000,"/dev/ttyACM0",115200);

    return 0;
}
