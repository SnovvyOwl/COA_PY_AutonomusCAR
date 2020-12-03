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
    char *hostname ="bluetank.iptime.org";
    RasPi  car(hostname,13000);

    return 0;
}
