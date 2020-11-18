package com.example.wirelesscontroller;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;


public class ControllerActivity extends Activity implements View.OnTouchListener, View.OnClickListener {

    RelativeLayout layout_ctrSpeed, layout_ctrDirection;
    SwipeController speedController, directionController;

    TextView txtSpeed;
    TextView txtDir;

    Button btnSet,btnConnect;
    TextView txtConnect;

    SocketCommunication socketCommunication;
    SharedPreferences appData;

    int state_speed = 2;
    int state_direction = 2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_controller);
        socketCommunication = new SocketCommunication(
                PreferenceManager.getString(this,"IP"),
                PreferenceManager.getInt(this,"PORT"));

        txtSpeed = (TextView) findViewById(R.id.text);
        txtDir = (TextView) findViewById(R.id.text2);

        layout_ctrSpeed = (RelativeLayout)findViewById(R.id.layout_ctrSpeed);
        layout_ctrDirection = (RelativeLayout)findViewById(R.id.layout_ctrDirection);
        layout_ctrSpeed.setOnTouchListener(this);
        layout_ctrDirection.setOnTouchListener(this);

        speedController = new SwipeController(getApplicationContext(), layout_ctrSpeed,R.drawable.stickl,true,70);
        directionController = new SwipeController(getApplicationContext(), layout_ctrDirection,R.drawable.stickr,false,70);

        speedController.setStickSize(140,100);
        speedController.setStickCenter();

        directionController.setStickSize(100,140);
        directionController.setStickCenter();

        txtConnect = (TextView)findViewById(R.id.text3);
        btnSet = (Button)findViewById(R.id.btn_set);
        btnConnect = (Button)findViewById(R.id.btn_connect);
        btnSet.setOnClickListener(this);
        btnConnect.setOnClickListener(this);
    }

    @Override
    public boolean onTouch(View view, MotionEvent motionEvent) {
        if (view == layout_ctrSpeed){
            speedController.drawStick(motionEvent);

            if (state_speed != checkState(100 - speedController.percent)){
                state_speed = checkState(100 - speedController.percent);
                socketCommunication.send(makeData(Integer.toString(state_speed),Integer.toString(state_direction)));
            }


            txtSpeed.setText((100 - speedController.percent)+"");

//            socketCommunication.send(makeData(Integer.toString(200 - speedController.percent),Integer.toString(directionController.percent + 100)));


//            socketCommunication.send(txtSpeed.getText().toString() + "속도");
//            try {
//                socketCommunication.send(socketCommunication.socket.getSendBufferSize() + "");
//            } catch (SocketException e) {
//                e.printStackTrace();
//            }
            return true;
        }
        if (view == layout_ctrDirection){
            directionController.drawStick(motionEvent);

            if (state_direction != checkState(directionController.percent)){
                state_direction = checkState(directionController.percent);
                socketCommunication.send(makeData(Integer.toString(state_speed),Integer.toString(state_direction)));
            }

            txtDir.setText(directionController.percent+"");
//            socketCommunication.send(makeData(Integer.toString(200 - speedController.percent),Integer.toString(directionController.percent + 100)));

//            socketCommunication.send(makeData(txtSpeed.getText().toString(),txtDir.getText().toString()));
//            socketCommunication.send(txtDir.getText().toString() + "방향");
            return true;
        }
        return false;
    }

    @Override
    public void onClick(View view) {
        if (view == btnSet){
            if (btnSet.getText().equals("SET")){
                if (socketCommunication.socket != null && socketCommunication.socket.isConnected()){
                    btnSet.setText("ING");
                }
                socketCommunication.startClient();

            } else if (btnSet.getText().equals("ING")){
                socketCommunication.stopClient();
                if (socketCommunication.socket.isClosed()){
                    btnSet.setText("SET");
                }

            }
        }
        if (view == btnConnect){
            if (socketCommunication.socket != null && socketCommunication.socket.isConnected() && !socketCommunication.socket.isClosed()){
                Toast.makeText(this,"socket is connected",Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(this,"socket is not connected",Toast.LENGTH_SHORT).show();
            }
        }
    }

    private String makeData(String str1, String str2){
        return ("#" + str1 + "%" + str2);
    }

    private int checkState(int state){
        if (state > 50 && state <= 100){
            return 3;
        } else if (state == 50){
            return 2;
        } else  {       // 0 < state < 50
            return 1;
        }
    }

    @Override
    public void finish() {
        super.finish();
        if (socketCommunication.socket != null && socketCommunication.socket.isConnected() && !socketCommunication.socket.isClosed()){
            socketCommunication.stopClient();
        }
    }
}
