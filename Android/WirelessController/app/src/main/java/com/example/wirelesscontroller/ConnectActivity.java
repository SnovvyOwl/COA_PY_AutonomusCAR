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
        setContentView(R.layout.activity_connect);

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
