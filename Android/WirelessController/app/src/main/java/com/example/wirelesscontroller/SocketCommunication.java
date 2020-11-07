package com.example.wirelesscontroller;

import android.content.Context;
import android.util.Log;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketException;
import java.net.URL;

public class SocketCommunication {

    Socket socket;
    String ip ;
    int port ;

    SocketCommunication(){
        this.ip = "10.0.2.2";
        this.port = 5005;
    }

    SocketCommunication(String ip, int port){
        if (ip.isEmpty()) this.ip = "10.0.2.2";
        if (port == 0) this.port = 5005;

        this.ip = ip;
        this.port = port;
    }



    void startClient() {
        final boolean check = false;
        Thread thread = new Thread() {
            @Override
            public void run() {
                try {
                    socket = new Socket();
                    socket.connect(new InetSocketAddress(ip, port));
                    send("c");
                } catch (SocketException e){
                    stopClient();
                    System.out.println(e);
                } catch(Exception e) {
                    if(!socket.isClosed()) { stopClient(); }
                    System.out.println(e);
                }
            }
        };
        thread.start();
    }

    void stopClient() {
        try {
            if(socket!=null && socket.isConnected()) {
                socket.close();
            }
        } catch (IOException e){
            System.out.println(e);
        }
    }

    void receive() {
        while(true) {
            try {
                byte[] byteArr = new byte[100];
                InputStream inputStream = socket.getInputStream();

                int readByteCount = inputStream.read(byteArr);

                if(readByteCount == -1) { throw new IOException(); }

                String data = new String(byteArr, 0, readByteCount, "UTF-8");

            } catch (Exception e) {
                stopClient();
                break;
            }
        }
    }

    void send(final String data) {
        Thread thread = new Thread() {
            @Override
            public void run() {
                try {
                    byte[] byteArr = data.getBytes("UTF-8");
                    OutputStream outputStream = socket.getOutputStream();
                    outputStream.write(byteArr);
                    System.out.println(byteArr.length);
                    outputStream.flush();
                } catch(Exception e) {
                    stopClient();
                }
            }
        };
        thread.start();
    }
}
