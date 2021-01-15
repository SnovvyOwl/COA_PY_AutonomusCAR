#pragma once
#include<wiringPi.h>
#include<wiringSerial.h>
#include<Arduino.h>
#include<iostream>
#include<stdio.h>
#include <string>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include<thread>
#include<netdb.h>
#define  BUFF_SIZE 8

using namespace std;
class RasPi{
    private:
        int client=0;
        Arduino Nano;
        struct sockaddr_in server_addr;
        string sock_receive="";
        string sock_send="";
        float Loop_time = 0.02;
        struct hostent *he;
        int BF=0;
        int LR=0;
        
    public:
        RasPi(const char *hostname, const int _port, const char *serial,int baud)
        {   
            Nano.Start_setup((char*)serial,baud);//Arduino Serial port open
            he=gethostbyname(hostname); // server url
            client = socket( AF_INET, SOCK_STREAM, 0);
            server_addr.sin_family = AF_INET;
            server_addr.sin_port = htons(_port);
            server_addr.sin_addr.s_addr=*(long*)(he->h_addr_list[0]);
            
            if(client==-1){
                cerr<< "\n Socket creation error \n";
                sock_receive="quit";
				exit(1);
            }
           if (connect(client, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0){    
                cerr<<"\nConnection Failed \n"; 
                sock_receive="quit";
				exit(1);
            }
            startClient();
        };
        void receiving(){
            char buffer[BUFF_SIZE]={0};
            while(true){
                read(client,buffer,BUFF_SIZE);
                sock_receive=buffer;
                if (sock_receive.size()){
                    if (sock_receive=="quit"){
                        quitClient();
                    }
                    cout<<"controller: "<<sock_receive<<endl;
                    BF=stoi(sock_receive.substr(1,3));
                    LR=stoi(sock_receive.substr(5));
                    buffer[0]={0,};
                    Nano.Set_BF_position(BF);
                    Nano.Set_LR_position(LR);
                    Nano.Value_to_T_data();

                }
            }
        }
        void quitClient(){
            cout<<"Close.."<<endl;
            Nano.quit();
            close(client);
            cout<<"OFF"<<endl;
            exit(1);
        
        }
        void sending(){
            while(true){
                Nano.Value_to_T_data();
                Nano.Serial_write();
                if (sock_receive=="quit"){
					exit(1);
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

            int Start_point=0;
            int End_point=0;
            //int BF=0;
            //int LR=0;
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
                    
                    Nano.Serial_read();
                    Start_point=millis();
                    Nano.Set_BF_position(BF);
                    Nano.Set_LR_position(LR);
                    R_data=Nano.get_R_data();
                    //cout<<R_data<<endl;

                    End_point = millis();
                    //delay(Loop_time-((float)End_point/1000-(float)Start_point/1000));                
                }
            }
            quitClient();
        }
};
