package com.example.wirelesscontroller;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    Button btn1, btn2, btn3;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        btn1 = (Button)findViewById(R.id.main_btn1);
        btn2 = (Button)findViewById(R.id.main_btn2);
        btn3 = (Button)findViewById(R.id.main_btn3);

        btn1.setOnClickListener(this);
        btn2.setOnClickListener(this);
        btn3.setOnClickListener(this);
    }

    @Override
    public void onClick(View view) {
        if (view == btn1){
            Intent intent = new Intent(getApplicationContext(), ConnectActivity.class);
            startActivity(intent);
            overridePendingTransition(R.anim.slide_in_right,R.anim.slide_out_left);
        }
        if (view == btn2){
            Intent intent = new Intent(getApplicationContext(),ControllerActivity.class);
            startActivity(intent);
        }
        if (view == btn3){
            Intent intent = new Intent(getApplicationContext(),SettingsActivity.class);
            startActivity(intent);
            overridePendingTransition(R.anim.slide_in_right,R.anim.slide_out_left);
        }
    }
}
