// socket server sample frome https://kevinthegrey.tistory.com/26
// 20200106
// jinwook_choi

#include <stdio.h>
#include <WinSock2.h>
#pragma comment(lib, "ws2_32")

#define PORT 5005
#define PACKET_SIZE 1024

int main()
{
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2,2), &wsaData);

    SOCKET hListen;
    hListen = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);

    SOCKADDR_IN tListenAddr = {};
    tListenAddr.sin_family = AF_INET;
    tListenAddr.sin_port = htons(PORT);
    tListenAddr.sin_addr.s_addr = htonl(INADDR_ANY);

    bind(hListen, (SOCKADDR*)&tListenAddr, sizeof(tListenAddr));
    listen(hListen, SOMAXCONN);

    SOCKADDR_IN tClntAddr = {};
    int iClntSize = sizeof(tClntAddr);
    SOCKET hClient = accept(hListen, (SOCKADDR*)&tClntAddr, &iClntSize);

    char cBuffer[PACKET_SIZE] = {};
    recv(hClient, cBuffer, PACKET_SIZE, 0);
    printf("Recv Msg : %s\n", cBuffer);

    char cMsg[] = "Server Send";
    send(hClient, cMsg, strlen(cMsg), 0);

    closesocket(hClient);
    closesocket(hListen);

    WSACleanup();
    return 0;
}