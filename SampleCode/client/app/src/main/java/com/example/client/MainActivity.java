package com.example.client;
import android.os.Handler;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.net.Socket;
public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    Button connect_btn;                 // ip 받아오는 버튼
    Button send_btn;
    EditText ip_edit;               // ip 에디트
    TextView show_text;// 서버에서온거 보여주는 에디트
    TextView recv_text;
    TextView send_text;
    // 소켓통신에 필요한것
    private Handler mHandler;
    private Socket socket;
    private BufferedReader networkReader;
    private PrintWriter networkWriter;
    private DataOutputStream dos;
    //private String ip = "192.168.55.53";
    //private String ip = "192.168.42.72";  // IP 번호
    private int port = 8080;                          // port 번호
    private String CMD="vel, angle";
    private String data;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        connect_btn = (Button)findViewById(R.id.connect_btn);
        connect_btn.setOnClickListener(this);
        //send_btn.setOnClickListener(this);
        ip_edit = (EditText)findViewById(R.id.ip_edit);
        show_text = (TextView)findViewById(R.id.show_text);
        //recv_text= (TextView)findViewById(R.id.recv_text);
        //send_text=(TextView)findViewById(R.id.send_text);
    }

    @Override
    public void onClick(View v) {
        switch(v.getId()){
            case R.id.connect_btn:     // ip 받아오는 버튼
                try {
                    connect();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                /*
            case R.id.send_btn:
                data = String.valueOf(ip_edit.getText());
                }
                 */
            }
    }

    // 로그인 정보 db에 넣어주고 연결시켜야 함.
    void connect() throws IOException {
        mHandler = new Handler();


        Log.w("connect","연결 하는중");
        // 받아오는거
        Thread checkUpdate = new Thread() {
            public void run() {
                // ip받기
                String newip = String.valueOf(ip_edit.getText());

                // 서버 접속
                try {
                    socket = new Socket(newip, port);

                    //socket=new Socket(ip,port);
                    Log.w("서버 접속됨", "서버 접속됨");
                } catch (IOException e1) {
                    Log.w("서버접속못함", "서버접속못함");
                    e1.printStackTrace();
                }

                Log.w("edit 넘어가야 할 값 : ","안드로이드에서 서버로 연결요청");

                // Buffered가 잘못된듯.
                try {
                    dos = new DataOutputStream(socket.getOutputStream());   // output에 보낼꺼 넣음
                    dos.writeUTF("I'm client");
                    Log.d("ClientThread", "서버로 보냄.");
                    InputStream in = socket.getInputStream();
                    byte[] input = new byte[1024];
                    int b;
                    for (int i = 0; i <input.length; i++) {
                        b = in.read();
                        if (b == -1) break;
                        int j = b >= 0 ?b :256+b; //양수일 땐 그대로 b, 음수면 256+b
                        input [i] = (byte) j;
                    }
                    CMD= new String(input,"UTF-8");


                    Log.d("ClientThread","서버입니까? : "+CMD);
                } catch (IOException e) {
                    e.printStackTrace();
                    Log.w("버퍼", "버퍼생성 잘못됨");
                }
                Log.w("버퍼","버퍼생성 잘됨");
                mHandler.post(new Runnable() {
                    @Override
                    public void run() {
                        show_text.setText("서버입니까?: "+CMD);
                    }
                });
                /*
                while(true) {
                    // 서버에서 받아옴
                    try {
                        while (true) {
                            InputStream in = socket.getInputStream();
                            byte[] input = new byte[1024];
                            int b;
                            for (int i = 0; i <input.length; i++) {
                                b = in.read();
                                if (b == -1) break;
                                int j = b >= 0 ?b :256+b; //양수일 땐 그대로 b, 음수면 256+b
                                input [i] = (byte) j;
                            }
                            CMD= new String(input,"UTF-8");

                            Log.w("서버에서 받아온 값 ", "" + CMD);
                            //Log.w("서버에서 받아온 값 ", "" + line2);

                            if(CMD.length() > 0) {
                                Log.w("------서버에서 받아온 값 ", "" + CMD);
                                dos.writeUTF("령: " + data);
                                dos.flush();
                            }
                            if(data == "q") {
                                socket.close();
                                break;
                            }
                            mHandler.post(new Runnable() {
                                @Override
                                public void run() {
                                    recv_text.setText("받은 데이터: "+CMD);
                                    send_text.setText("보낸 데이터: "+data);
                                }
                            });
                        }
                    } catch (Exception e) {

                    }
                }*/
            }
        };
        // 소켓 접속 시도, 버퍼생성
        checkUpdate.start();
    }
}