#pragma once
#include<wiringPi.h>
#include<wiringSerial.h>
#include<string>
#include<iostream>
#define  Channel_reset 0  
using namespace std;
class Arduino{
    private:
        int arduino;
        string T_data = "";
        string R_data = "";        
        float Loop_time = 0.02;
        string port="dev/ttyACM0";
        int baud=115200;
    
        //BF, LR value range is -255 to 255
        int BF_desire = 100;
        int LR_desire = 0;

    public:
        Arduino(string port,int _baud) //Generater
            
        {   port=port;
            baud=_baud;
            if((arduino = serialOpen(port.c_str(),baud))<0){
                cerr<<"Unable to open Arduino Nano"<<endl;
            }
            Start_setup();
        };
        void Set_BF_position(int value){
            BF_desire = value;
        }
        void Set_LR_position(int value){
            LR_desire = value;
        }
        void Start_setup(){
            //GPIO.setmode(GPIO.BCM)
            //GPIO.setwarnings(False)
            pinMode(Channel_reset, OUTPUT);
            digitalWrite(Channel_reset, LOW);        //Reset arduino
            delay(1000);
            digitalWrite(Channel_reset,HIGH);
            Serial_check(5);
        }   
        int Serial_check(int timeout){
            int i = 0;
            while (1){
                T_data = "TEST";
                Serial_write();
                delay(1000);
                cout<<"Waiting connection.\n";
                Serial_read();
                if (R_data == "TEST"){
                    return 0;
                    break;
                }  
                else if(i == timeout) {
                    cout<<"Test fail\n";
                    return 1;
                    break;
                }
                else{ 
                    i += 1;
                }        
            }
        }
        void Serial_write(){
            string msg="@" + T_data + '#';
            serialPuts(arduino,msg.c_str());
        } 
        void Serial_read(){
            char Temp = char(serialGetchar(arduino));
            if (Temp == '@'){
                R_data = "";
                while (1){
                    Temp = char(serialGetchar(arduino));
                    if (Temp == '#'){
                        break;
                    }
                    if(Temp != '@' & Temp != '#' & Temp){
                    R_data = R_data + Temp;
                    }
                }
            }           
            else{
                R_data = "";
            }   
        } 
        void Value_to_T_data(){
            string BF_position = "";
            string LR_position = "";
            if (BF_desire>= 0){
                BF_position = "F" + to_string(BF_desire);
            }  
            else{
                BF_position = "B" + to_string(-1*BF_desire);
            }
            if (LR_desire>= 0){
                LR_position = "R" + to_string(LR_desire);
            }  
            else{
                LR_position = "L" + to_string(-1*LR_desire);
            }
            T_data = BF_position + LR_position;
        }
};
