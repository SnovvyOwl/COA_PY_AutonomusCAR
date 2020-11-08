#pragma once
#include<wiringPi.h>
#include<wiringSerial.h>
#include<Arduino.h>
#include<iostream>
#include<thread>
#include <stdio.h>
#include <string>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include<sstream>
#define  BUFF_SIZE 8
using namespace std;
class RasPi{
    private:
        string ip ="192.168.35.125";
        int port=8080;
        int client=0;
        Arduino nano("/dev/ttyACM0" ,115200);
        struct sockaddr_in server_addr;
        string sock_receive="";
        string sock_send="";
        
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
            if(inet_pton(AF_INET,ip, &serv_addr.sin_addr)<=0){ 
                cerr<<"\nInvalid address/ Address not supported \n";
                sock_receive="quit";
            } 
           if (connect(client, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0){    
                cerr<<"\nConnection Failed \n"; 
                sock_receive="quit";
            }
            startClient();
        };
        void receiving(string &msg){
            char buffer[BUFF_SIZE]={0};
            while(true){
                read(client,buffer,BUFF_SIZE);
                sock_receive=buffer;
                cout<<sock_receive<endl;
                nano.arduino.Serial_read();
                if (msg=="quit"){
                    break;
                }
            }
        }
        void sending(string &msg){
            while(true){
                send(client,sock_send.c_str(), strlen(sock_send.c_str()),0);
                nano.Value_to_T_data();
                nano.arduino.Serial_write();
                if (msg=="quit"){
                    break;
                }
            }   
        }
        void startClient(){
            cout<<"start\n";
            string message = "r";
            cout<<"sending "<<message<<endl;
            send(client,message.c_str(), strlen(message.c_str()),0); 
            printf("run Client");
            runClient();
        }
        void runClient(){
            thread receive_thread(&receiving,ref(sock_receive));
            thread send_thread(&sending,ref(sock_receive));
            receive_thread.detach();
            send_thread.detach();
            stringstream ss(sock_receive);
            int Start_point=0;
            int End_point=0;
            while(1){
                cout<<sock_receive<<endl;
                if (sock_receive=="Test"){
                    nano.LR_desire=255;
                    nano.BF_desire=0;
                }                  
                else if (sock_receive=="call"){
                    nano.LR_desire=-255;
                    nano.BF_desire=0;
                }
                else if(sock_receive=="quit"){
                    break;
                }
                else{
                    Start_point=millis();
                    ss>>nano.BF_desire;
                    ss>>nano.LR_desire;
                    sout.str("");
                    if (nano.R_data){
                      cout<<nano.R_data<<endl;
                    }
                    End_point = millis();
                    delay(nano.Loop_time-((float)End_point/1000-(float)Start_point/1000);                
                }
            }
            printf("OFF\n");
            serialClose(nano.arduino);
        }
};
