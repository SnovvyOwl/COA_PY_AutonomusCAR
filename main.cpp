#include<RasPi.h>
#include<iostream>
#include<string>
#include<wiringPi.h>
using namespace std;
int main(){
    if(wiringPiSetup()==-1){
        return 1;
    }
    car=RasPi("192.168.0.42",8080);
    return 0;
}