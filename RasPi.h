#pragma once
#include<wiringPi.h>
#include<wiringSerial.h>
#include<Arduino.h>
#include<iostream>
#include <stdio.h>
#include <string>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include<thread>
#include<sstream>
#define  BUFF_SIZE 8
using namespace std;
class RasPi{
    private:
        string ip ="";
        int port=8080;
        int client=0;
        string ser_port="/dev/ttyACM0";
        Arduino Nano;
        struct sockaddr_in server_addr;
        string sock_receive="";
        string sock_send="";
        float Loop_time = 0.02;
        
        
    public:
        RasPi(string server_ip,int _port)
        {   
            ip=server_ip;
            port=_port;
            
            client = socket( AF_INET, SOCK_STREAM, 0);
            if(client==-1){
                cerr<< "\n Socket creation error \n";
                sock_receive="quit";
            }
            server_addr.sin_family = AF_INET;
            server_addr.sin_port = htons(port);
            if(inet_pton(AF_INET,ip.c_str(), &server_addr.sin_addr)<=0){ 
                cerr<<"\nInvalid address/ Address not supported \n";
                sock_receive="quit";
            } 
           if (connect(client, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0){    
                cerr<<"\nConnection Failed \n"; 
                sock_receive="quit";
            }
            startClient();
        };
        void receiving(){
            char buffer[BUFF_SIZE]={0};
            while(true){
                read(client,buffer,BUFF_SIZE);
                sock_receive=buffer;
                cout<<sock_receive<<endl;
                cout<<sock_receive<<endl;
                Nano.Serial_read();
                if (sock_receive=="quit"){
                    break;
                }
                if (sock_receive==""){
                    break;
                }
            }
        }
        void sending(){
            while(true){
                send(client,sock_send.c_str(), sock_send.size(),0);
                Nano.Value_to_T_data();
                Nano.Serial_write();
                if (sock_receive=="quit"){
                    break;
                }
            }   
        }
        void startClient(){
            cout<<"start\n";
            string message = "r";
            cout<<"sending "<<message<<endl;
            send(client,message.c_str(),message.size(),0); 
            printf("run Client");
            runClient();
        }
        void runClient(){
            thread receive_thread([&](){receiving();});
            thread send_thread([&](){sending();});
            receive_thread.detach();
            send_thread.detach();

            stringstream ss(sock_receive);
            int Start_point=0;
            int End_point=0;
            int BF=0;
            int LR=0;
            string R_data="";
            while(1){
                cout<<sock_receive<<endl;
                if (sock_receive=="Test"){
                    Nano.Set_BF_position(255);
                    Nano.Set_LR_position(0);
                }                  
                else if (sock_receive=="call"){
                    Nano.Set_BF_position(-255);
                    Nano.Set_LR_position(0);
                }
                else if(sock_receive=="quit"){
                    break;
                }
                else{
                    Start_point=millis();
                    ss>>BF;
                    ss>>LR;
                    Nano.Set_BF_position(BF);
                    Nano.Set_LR_position(LR);
                    ss.str("");
                    R_data=Nano.get_R_data();
                    cout<<R_data<<endl;

                    End_point = millis();
                    delay(Loop_time-((float)End_point/1000-(float)Start_point/1000));                
                }
            }
            printf("OFF\n");
            Nano.quit();
        }
};
