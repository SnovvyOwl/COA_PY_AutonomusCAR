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
#include<sstream>
#include<netdb.h>
#define  BUFF_SIZE 8

using namespace std;
class SRasPi{
    private:
        char *ip;
        int port=13000;
        int server = 0;
        int client = 0;
        Arduino Nano;
        struct sockaddr_in client_addr;
        socklen_t client_addr_len=sizeof(client_addr);
        struct sockaddr_in server_addr;
        string sock_receive=""; //received data for Clinet socket
        string sock_send="";
        float Loop_time = 0.02;
        
    public:
        SRasPi(const char* _ip,int _port, const char *serial,int baud)
        {   
            Nano.Start_setup((char*)serial,baud);//Arduino Serial port open
            ip=(char*)_ip;
            port=_port;
            //Socket init..
            server = socket( AF_INET, SOCK_STREAM, 0);
            if(server==-1){
                cerr<< "\n Socket creation error \n";
                sock_receive="quit";
				exit(1);
            }
            server_addr.sin_family = AF_INET;
            server_addr.sin_port = htons(port);
            server_addr.sin_addr.s_addr=htonl(INADDR_ANY);
            startServer();
        };
        
        void startServer(){
            cout<<"[start server]\n";
            cout<<"Server ip ->"<<ip<<endl;
            cout<<"Server port->"<<port<<endl;
            if(bind(server,(struct sockaddr*)&server_addr,sizeof(server_addr))<0){
                cerr<<"Bind ERROR"<<endl;
                sock_receive="quit";
				exit(1);
            }
            if(listen(server,1)<0){
                cerr<<"Listen ERROR"<<endl;
                sock_receive="quit";
				exit(1);
            }

            cout<<"wait\n";
            client_addr_len=sizeof(client_addr);
            client=accept(server, (struct sockaddr *)&client_addr,&client_addr_len);
            printf("Connection from: %s\n",inet_ntoa(client_addr.sin_addr));   
            char buffer[BUFF_SIZE]={0};
            read(client,buffer,BUFF_SIZE);
            sock_receive=buffer;
            cout<<sock_receive<<endl;
            runServer();
            
        }
        
        void stopServer(){
            cout<<"[stop server]\n"<<"- Thank you -\n";
            close(client);
            close(server);
            Nano.quit();
            cout<<"OFF";
			exit(1);
        }
        
        void runServer(){
            stringstream ss(sock_receive);//for parsing sock_recive 
            int Start_point=0;
            int End_point=0;
            int BF=0;
            int LR=0;
            string R_data="";
            if (sock_receive == "c"){
				//Controller Thread Generate;
                cout<<"controller is connected.\n";
                thread receive_thread([&](){receiving();});
                receive_thread.detach(); 
            }

            while(1){
                if(sock_receive=="quit"){
                    cout<<"Illegal connection has detected.\n";
                    break;
					exit(1);
                }
                                
                else if (sock_receive=="Test"){
                    Nano.Set_BF_position(255);
                    Nano.Set_LR_position(0);
                }                  
                else if (sock_receive=="call"){
                    Nano.Set_BF_position(-255);
                    Nano.Set_LR_position(0);
                }

                else{
                    Start_point=millis();
                    ss>>BF;
                    ss>>LR;
                    //Nano.Set_BF_position(BF);
                    //Nano.Set_LR_position(LR);
                    ss.str("");
                    //R_data=Nano.get_R_data();
                    //cout<<R_data<<endl;
                    End_point = millis();
                    //delay(Loop_time-((float)End_point/1000-(float)Start_point/1000)); 
                }
            }
            stopServer();
        }
    
        void receiving(){
            char buffer[BUFF_SIZE]={0};
            while(1){
                read(client,buffer,BUFF_SIZE);
                sock_receive=buffer;
                if (sock_receive.size()){
                    cout<<"controller: "<<sock_receive<<endl;
                    buffer[0]={0,};
                }
				Nano.Serial_read();
            }
        }
};
