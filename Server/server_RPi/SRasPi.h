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
        string sock_receive="";
        string sock_send="";
        float Loop_time = 0.02;
        
    public:
        SRasPi(const char* _ip,int _port, const char *serial,int baud)
        {   
            Nano.Start_setup((char*)serial,baud);//Arduino Serial port open
            ip=(char*)_ip;
            port=_port;
            
            server = socket( AF_INET, SOCK_STREAM, 0);
            if(server==-1){
                cerr<< "\n Socket creation error \n";
                sock_receive="quit";
            }
            //memset(&server_addr,0,sizeof(sever_addr));
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
            }
            if(listen(server,1)<0){
                cerr<<"Listen ERROR"<<endl;
                sock_receive="quit";
            }

            cout<<"wait\n";
            client_addr_len=sizeof(client_addr);
            client=accept(server, (struct sockaddr *)&client_addr,&client_addr_len);
            printf("Connection from: %s\n",inet_ntoa(client_addr.sin_addr));   
            char buffer[BUFF_SIZE]={0};
            read(client,buffer,BUFF_SIZE);
            sock_receive=buffer;
            cout<<sock_receive<<endl;

            if (sock_receive == "c"){
                cout<<"controller is connected.\n";
                //write(client,"Server is Connected");
                runServer();
            }
            else{
                cout<<"Illegal connection has detected.\n";
                stopServer();
            }
        }
        
        void stopServer(){
            cout<<"[stop server]\n"<<"- Thank you -\n";
            close(client);
            close(server);
            Nano.quit();
            cout<<"OFF";
        }
        
        void runServer(){
            thread receive_thread([&](){receiving();});
            //thread send_thread([&](){sending();});
            receive_thread.detach();//Command Recieve Thread
            //send_thread.detach();//current state send Thread
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
            stopServer();
        }

        void receiving(){
            char buffer[BUFF_SIZE]={0};
            while(true){
                read(client,buffer,BUFF_SIZE);
                sock_receive=buffer;
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
        
        /*void sending(){
            while(true){
                Nano.Value_to_T_data();
                Nano.Serial_write();
                write(Nano.T)
                if (sock_receive=="quit"){
                    break;
                }
            }   
        }*/
        

};
