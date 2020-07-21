package com.example.wirelesscontroller;

import android.app.Activity;
import android.os.Bundle;
import android.view.MotionEvent;
import android.view.View;
import android.widget.RelativeLayout;
import android.widget.TextView;

public class ControllerActivity extends Activity {

    RelativeLayout layout_controller;
    RelativeLayout layout_controller2;
    SwipeController swipeController;
    SwipeController swipeController2;

    TextView sample_text;
    TextView sample_text2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_controller);

        sample_text = (TextView) findViewById(R.id.text);
        sample_text2 = (TextView) findViewById(R.id.text2);

        layout_controller = (RelativeLayout)findViewById(R.id.layout_controller);
        layout_controller2 = (RelativeLayout)findViewById(R.id.layout_controller2);
        swipeController = new SwipeController(getApplicationContext(),layout_controller,R.drawable.stick2,true);
        swipeController2 = new SwipeController(getApplicationContext(),layout_controller2,R.drawable.stick3,false);

        swipeController.setStickSize(140,140);
        swipeController.setStickCenter();
        swipeController.setOffset(70);

        swipeController2.setStickSize(150,150);
        swipeController2.setStickCenter();
        swipeController2.setOffset(70);

        layout_controller.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View view, MotionEvent motionEvent) {

                swipeController.drawStick(motionEvent);
                sample_text.setText(swipeController.percent+"");
                return true;
            }
        });
        layout_controller2.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View view, MotionEvent motionEvent) {

                swipeController2.drawStick(motionEvent);
                sample_text2.setText((int)motionEvent.getX()+"");
                return true;
            }
        });
    }
}
