#include<SRasPi.h>
#include<iostream>
#include<string>
#include<wiringPi.h>
#include<Arduino.h>
using namespace std;
int main(){
    if(wiringPiSetup()==-1){
        return 1;
    }
    SRasPi  car("10.42.0.53",13000,"/dev/ttyACM0",115200);

    return 0;
}
