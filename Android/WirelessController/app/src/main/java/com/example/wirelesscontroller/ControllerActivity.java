package com.example.wirelesscontroller;

import android.app.Activity;
import android.os.Bundle;
import android.view.MotionEvent;
import android.view.View;
import android.widget.RelativeLayout;
import android.widget.TextView;

public class ControllerActivity extends Activity implements View.OnTouchListener {

    RelativeLayout layout_ctrSpeed, layout_ctrDirection;
    SwipeController speedController, directionController;

    TextView txtSpeed;
    TextView txtDir;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_controller);

        txtSpeed = (TextView) findViewById(R.id.text);
        txtDir = (TextView) findViewById(R.id.text2);

        layout_ctrSpeed = (RelativeLayout)findViewById(R.id.layout_ctrSpeed);
        layout_ctrDirection = (RelativeLayout)findViewById(R.id.layout_ctrDirection);
        layout_ctrSpeed.setOnTouchListener(this);
        layout_ctrDirection.setOnTouchListener(this);

        speedController = new SwipeController(getApplicationContext(), layout_ctrSpeed,R.drawable.stick2,true,70);
        directionController = new SwipeController(getApplicationContext(), layout_ctrDirection,R.drawable.stick3,false,70);

        speedController.setStickSize(140,140);
        speedController.setStickCenter();

        directionController.setStickSize(150,150);
        directionController.setStickCenter();

    }

    @Override
    public boolean onTouch(View view, MotionEvent motionEvent) {
        if (view == layout_ctrSpeed){
            speedController.drawStick(motionEvent);
            txtSpeed.setText((100 - speedController.percent)+"");
            return true;
        }
        if (view == layout_ctrDirection){
            directionController.drawStick(motionEvent);
            txtDir.setText(directionController.percent+"");
            return true;
        }
        return false;
    }
}
