package com.example.wirelesscontroller;

import android.util.Log;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.URL;

public class SocketCommunication {

    Socket socket;
    String ip = "10.0.2.2";
    int port = 5001;

    void startClient() {

        Thread thread = new Thread() {
            @Override
            public void run() {
                try {
                    socket = new Socket();
                    socket.connect(new InetSocketAddress(ip, port));
                } catch(Exception e) {
                    if(!socket.isClosed()) { stopClient(); }
                    return;
                }
            }


        };
        thread.start();
    }

    void stopClient() {
        try {
            if(socket!=null && !socket.isClosed()) {
                socket.close();
            }
        } catch (IOException e) {}
    }

    void receive() {
        while(true) {
            try {
                byte[] byteArr = new byte[100];
                InputStream inputStream = socket.getInputStream();

                //������ ������������ �������� ��� IOException �߻�
                int readByteCount = inputStream.read(byteArr);

                //������ ���������� Socket�� close()�� ȣ������ ���
                if(readByteCount == -1) { throw new IOException(); }

                String data = new String(byteArr, 0, readByteCount, "UTF-8");

            } catch (Exception e) {
//                Platform.runLater(()->displayText("[���� ��� �ȵ�]"));
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
                    outputStream.flush();
                } catch(Exception e) {
                    stopClient();
                }
            }
        };
        thread.start();
    }
}
