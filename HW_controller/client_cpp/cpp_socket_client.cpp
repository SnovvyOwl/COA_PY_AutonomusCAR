// socket server sample frome https://kevinthegrey.tistory.com/26
// 20200106
// jinwook_choi

#include <stdio.h>
#include <WinSock2.h>
#pragma comment(lib, "ws2_32")

#define PORT 5005
#define PACKET_SIZE 1024
#define SERVER_IP   "bluetank.iptime.org"

int main()
{
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2,2), &wsaData);

    SOCKET hSocket;
    hSocket = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);

    SOCKADDR_IN tAddr = {};
    tAddr.sin_family = AF_INET;
    tAddr.sin_port = htons(PORT);
    tAddr.sin_addr.s_addr = inet_addr(SERVER_IP);

    connect(hSocket, (SOCKADDR*)&tAddr, sizeof(tAddr));

    char cMsg[] = "Client Send";
    send(hSocket, cMsg, strlen(cMsg), 0);

    char cBuffer[PACKET_SIZE] = {};
    recv(hSocket, cBuffer, PACKET_SIZE, 0);

    printf("Recv Msg : %s\n",cBuffer);

    closesocket(hSocket);

    WSACleanup();

    WSACleanup();
    return 0;
}