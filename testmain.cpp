#include<iostream>
#include <string>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include<sstream>
#include<thread>
#include<netdb.h>
#define BUFF_SIZE 8
using namespace std;

void receiving(int &client,string &sock_receive){
    char buffer[BUFF_SIZE]={0};
    while(true){
        read(client,buffer,BUFF_SIZE);
        sock_receive=buffer;
        cout<<sock_receive<<endl;
        cout<<sock_receive<<endl;
        if (sock_receive=="quit"){
            break;
        }
        if (sock_receive==""){
            break;
        }
    }
}
void sending(int &client, string &sock_send,string &sock_receive){
    while(true){
        send(client,sock_send.c_str(), sock_send.size(),0);
        if (sock_receive=="quit"){
            break;
        }
    }   
}
void runClient(int &client, string& sock_send, string &sock_receive){
    thread receive_thread(&receiving, ref(client),ref(sock_receive));
    thread send_thread(&sending, ref(client),ref(sock_send),ref(sock_receive));
    receive_thread.detach();
    send_thread.detach();
    while(1){
        cout<<sock_receive<<endl;     
    }
}
void startClient(int &client,string &sock_receive,string &sock_send){
    cout<<"start\n";
    string message = "r";
    cout<<"sending "<<message<<endl;
    send(client,message.c_str(),message.size(),0); 
    printf("run Client");
    runClient(client,sock_send,sock_receive);
}


int main(){
    int client =0;
    string sock_receive="";
    client = socket( AF_INET, SOCK_STREAM, 0);
    int port=8080;
    struct sockaddr_in server_addr;
    string sock_send="";
    struct hostent *he;
    const char *hostname="bluetank.iptime.org";
    he=gethostbyname(hostname);
    client = socket( AF_INET, SOCK_STREAM, 0);
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    server_addr.sin_addr.s_addr=*(long*)(he->h_addr_list[0]);
    if(client==-1){
        cerr<< "\n Socket creation error \n";
        sock_receive="quit";
    }
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);

    if (connect(client, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0){    
        cerr<<"\nConnection Failed \n"; 
        sock_receive="quit";
    }
    startClient(client,sock_receive,sock_send);
    return 0;
}