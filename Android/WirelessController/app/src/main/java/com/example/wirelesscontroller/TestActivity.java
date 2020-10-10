package com.example.wirelesscontroller;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.net.Socket;

public class TestActivity extends AppCompatActivity implements View.OnClickListener {

    Button btn1, btn2;
    EditText edt1, edt2;
    TextView txt1;

    SocketCommunication socketCommunication;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_test);

        socketCommunication = new SocketCommunication();

        btn1 = (Button)findViewById(R.id.btn1);
        btn2 = (Button)findViewById(R.id.btn2);
        edt1 = (EditText)findViewById(R.id.edt1);
        edt2 = (EditText)findViewById(R.id.edt2);
        txt1 = (TextView)findViewById(R.id.text1);

        btn1.setOnClickListener(this);
        btn2.setOnClickListener(this);

    }

    @Override
    public void onClick(View view) {

        if(view == btn1){
            if (btn1.getText().equals("CONNECT")){
                if (edt1.length() == 0 || edt2.length() == 0){
                    Toast.makeText(this,"입력을 하고 눌러라 인간!",Toast.LENGTH_SHORT).show();
                    return;
                }

                socketCommunication.ip = edt1.getText().toString();
                socketCommunication.port = Integer.parseInt(edt2.getText().toString());
                socketCommunication.startClient();

                if (socketCommunication.socket != null && socketCommunication.socket.isConnected()){
                    txt1.setText("연결 성공");
                    btn1.setText("STOP");
                }

            } else if (btn1.getText().equals("STOP")){
                socketCommunication.send("e");
                socketCommunication.stopClient();
                txt1.setText("연결 종료");
                btn1.setText("CONNECT");
            }
        }
        if (view == btn2){
            if (socketCommunication.socket != null && socketCommunication.socket.isConnected() && !socketCommunication.socket.isClosed()){
                socketCommunication.send("Test word!");
            } else {
                Toast.makeText(this,"Server is not connected.",Toast.LENGTH_SHORT).show();
            }
        }
    }

    @Override
    public void finish() {
        super.finish();
        if (socketCommunication.socket != null && socketCommunication.socket.isConnected() && !socketCommunication.socket.isClosed()){
            socketCommunication.stopClient();
        }
        overridePendingTransition(R.anim.slide_in_left,R.anim.slide_out_right);
    }
}
