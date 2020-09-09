package com.example.wirelesscontroller;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import java.net.Socket;

public class ConnectActivity extends AppCompatActivity implements View.OnClickListener {

    Socket socket;

    Button btn1, btn2;
    EditText edt1, edt2;
    TextView txt1;

    SocketCommunication socketCommunication;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_test);

        btn1 = (Button)findViewById(R.id.btn1);
        btn2 = (Button)findViewById(R.id.btn2);
        edt1 = (EditText)findViewById(R.id.edt1);
        edt2 = (EditText)findViewById(R.id.edt2);
        txt1 = (TextView)findViewById(R.id.text1);

        btn1.setOnClickListener(this);
        btn2.setOnClickListener(this);

    }

//    void startClient() {
//        Thread thread = new Thread() {
//            @Override
//            public void run() {
//                try {
//                    socket = new Socket();
//                    String ip = "10.0.2.2";
//                    String rasp = "bluetank.iptime.org";
//                    socket.connect(new InetSocketAddress("localhost", 5001));
//                    txt1.setText("[연결 완료: "  + socket.getRemoteSocketAddress() + "]");
//                    btn1.setText("stop"); //connect
//                    btn2.setClickable(true); //send
//                } catch(Exception e) {
//                    txt1.setText("[서버 통신 안됨]");
//                    if(!socket.isClosed()) { stopClient(); }
//                    return;
//                }
//            }
//        };
//        thread.start();
//    }
//
//    void stopClient() {
//        try {
//            txt1.setText("[연결 끊음]");
//            btn1.setText("CONNECT"); //connect
//            btn2.setClickable(false); //send
//            if(socket!=null && !socket.isClosed()) {
//                socket.close();
//            }
//        } catch (IOException e) {}
//    }
//
//
//    void send(final String data) {
//        Thread thread = new Thread() {
//            @Override
//            public void run() {
//                try {
//                    byte[] byteArr = data.getBytes("UTF-8");
//                    OutputStream outputStream = socket.getOutputStream();
//                    outputStream.write(byteArr);
//                    outputStream.flush();
//                    txt1.setText("[전송 완료]");
//                } catch(Exception e) {
//                    txt1.setText("[서버 통신 안됨]");
//                    stopClient();
//                }
//            }
//        };
//        thread.start();
//    }

    @Override
    public void onClick(View view) {
        socketCommunication = new SocketCommunication();

        if(view == btn1){
            if (btn1.getText().equals("CONNECT")){
                socketCommunication.ip = edt1.getText().toString();
                socketCommunication.port = Integer.parseInt(edt2.getText().toString());
                socketCommunication.startClient();
                txt1.setText("연결 성공");
                btn1.setText("STOP");
            } else if (btn1.getText().equals("STOP")){
                socketCommunication.stopClient();
                txt1.setText("연결 종료");
                btn1.setText("CONNECT");
            }
        }
        if (view == btn2){

        }
    }

    @Override
    public void onBackPressed() {
        super.onBackPressed();
        socketCommunication.stopClient();
    }
}
