package sec07.exam03_chatting;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Iterator;
import java.util.List;
import java.util.Vector;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class ServerExCh2 {

    ExecutorService executorService;
    ServerSocket serverSocket;
    List<Client> connections = new Vector<Client>();


    void startServer() {
        executorService = Executors.newFixedThreadPool(
                Runtime.getRuntime().availableProcessors()
        );

        try {
            serverSocket = new ServerSocket();
            serverSocket.bind(new InetSocketAddress("localhost", 5001));
        } catch(Exception e) {
            if(!serverSocket.isClosed()) { stopServer(); }
            return;
        }

        Runnable runnable = new Runnable() {
            @Override
            public void run() {
                System.out.println("[Server Start]");
                while(true) {
                    try {
                        Socket socket = serverSocket.accept();
                        String message = "[accept: " + socket.getRemoteSocketAddress()  + ": " + Thread.currentThread().getName() + "]";
                        System.out.println(message);

                        Client client = new Client(socket);
                        connections.add(client);
                        System.out.println("[number: " + connections.size() + "]");
                    } catch (Exception e) {
                        if(!serverSocket.isClosed()) { stopServer(); }
                        break;
                    }
                }
            }
        };
        executorService.submit(runnable);
    }

    void stopServer() {
        try {
            Iterator<Client> iterator = connections.iterator();
            while(iterator.hasNext()) {
                Client client = iterator.next();
                client.socket.close();
                iterator.remove();
            }
            if(serverSocket!=null && !serverSocket.isClosed()) {
                serverSocket.close();
            }
            if(executorService!=null && !executorService.isShutdown()) {
                executorService.shutdown();
            }
            System.out.println("[Server Stop]");
        } catch (Exception e) { }
    }

    class Client {
        Socket socket;

        Client(Socket socket) {
            this.socket = socket;
            receive();
        }

        void receive() {
            Runnable runnable = new Runnable() {
                @Override
                public void run() {
                    try {
                        while (true) {
                            byte[] byteArr = new byte[100];
                            InputStream inputStream = socket.getInputStream();

                            //????????? ?????? ???? ???? ??? IOException ???
                            int readByteCount = inputStream.read(byteArr);

                            //????????? ?????????? Socket?? close()?? ??????? ???
                            if (readByteCount == -1) {
                                throw new IOException();
                            }

                            String message = "[Success: " + socket.getRemoteSocketAddress() + ": " + Thread.currentThread().getName() + "]";
//							Platform.runLater(()->displayText(message));
                            System.out.println(message);

                            String data = new String(byteArr, 0, readByteCount, "UTF-8");
                            System.out.println(data);

//                            Platform.runLater(()->displayText("[받기 완료] "  + data));

                            for (Client client : connections) {
                                client.send(data);
                            }
                        }
                    } catch (Exception e) {
                        try {
                            connections.remove(Client.this);
                            String message = "[클라이언트 통신 안됨: "
                                    + socket.getRemoteSocketAddress()
                                    + ": " + Thread.currentThread().getName() + "]";
//                            Platform.runLater(()->displayText(message));
                            System.out.println(message);
                            socket.close();
                        } catch (IOException e2) {
                        }
                    }
                }
            };
            executorService.submit(runnable);
        }

        void send(String data) {
            Runnable runnable = new Runnable() {
                @Override
                public void run() {
                    try {
                        byte[] byteArr = data.getBytes("UTF-8");
                        OutputStream outputStream = socket.getOutputStream();
                        outputStream.write(byteArr);
                        outputStream.flush();
                    } catch(Exception e) {
                        try {
                            String message = "[클라이언트 통신 안됨: "
                                    + socket.getRemoteSocketAddress()
                                    + ": " + Thread.currentThread().getName() + "]";
//                            Platform.runLater(()->displayText(message));
                            connections.remove(Client.this);
                            socket.close();
                        } catch (IOException e2) {}
                    }
                }
            };
            executorService.submit(runnable);
        }

    }



}