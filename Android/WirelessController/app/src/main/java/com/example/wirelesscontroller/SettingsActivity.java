package com.example.wirelesscontroller;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.content.DialogInterface;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public class SettingsActivity extends AppCompatActivity implements View.OnClickListener {

    Button btnSave, btnChange;
    EditText edtIpDlg, edtPortDlg;
    TextView txtIp, txtPort;
    View dialogView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);

        btnSave = (Button) findViewById(R.id.btn_save);
        btnChange = (Button) findViewById(R.id.btn_change);

        txtIp = (TextView) findViewById(R.id.txt_ip);
        txtPort = (TextView) findViewById(R.id.txt_port);

        txtIp.setText(PreferenceManager.getString(this,"IP"));
        txtPort.setText(PreferenceManager.getInt(this,"PORT") + "");

        btnSave.setOnClickListener(this);
        btnChange.setOnClickListener(this);
    }

    @Override
    public void onClick(View view) {
        if (view == btnSave){
            onBackPressed();
        }
        if (view == btnChange){
            dialogView = (View) View.inflate(this,R.layout.item_settingdlg,null);
            AlertDialog.Builder dlg = new AlertDialog.Builder(this);
            dlg.setTitle("Setting change");
            dlg.setView(dialogView);
            dlg.setPositiveButton("확인",
                    new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialogInterface, int i) {
                            edtIpDlg = (EditText) dialogView.findViewById(R.id.edt_ip_dlg);
                            edtPortDlg = (EditText) dialogView.findViewById(R.id.edt_port_dlg);

                            if (edtIpDlg.length() == 0 || edtPortDlg.length() == 0){
                                Toast.makeText(dialogView.getContext(),"입력을 바르게 해주세요!",Toast.LENGTH_SHORT).show();
                                return;
                            }

                            txtIp.setText(edtIpDlg.getText());
                            txtPort.setText(edtPortDlg.getText());
                        }
                    });
            dlg.setNegativeButton("취소",null);
            dlg.show();
        }
    }

    @Override
    public void onBackPressed() {
        super.onBackPressed();
        finish();
    }

    @Override
    public void finish() {
        super.finish();
        PreferenceManager.setString(this,"IP",txtIp.getText().toString());
        PreferenceManager.setInt(this,"PORT",Integer.parseInt(txtPort.getText().toString()));
        overridePendingTransition(R.anim.slide_in_left,R.anim.slide_out_right);
    }
}