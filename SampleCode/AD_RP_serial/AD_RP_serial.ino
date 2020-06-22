#include <Servo.h>

String R_data;
String T_data;

int BF_value = 0;
int LR_value = 0;
int LR_value_history = 0;

bool flag = false;

int servo_min_pos = -500;
int servo_max_pos = 500;
int servo_min_deg = 30;
int servo_max_deg = 150;
float servo_speed = 0.0028333333; // (sec/deg)


Servo servo;

void setup() {
  //Serial setting
  Serial.begin(115200);

  //Servo setting
  int servo_pin = 3;
  servo.attach(servo_pin);

  Start_setup();
}

void Serial_read(){
  //Serial read and decode(remove @ and #)
  char Temp;
  
  Temp = Serial.read();
  
  if (Temp == '@'){
    
    while (Temp != '#'){
      if (Temp != '@' && Temp != '#'){
        R_data = R_data + Temp;
      }
      while (true){
        if (Serial.available() > 0){
          Temp = Serial.read();
          break;
        }
      }
    }
    
  } 
  else{
    R_data = "";
  }
}

void Serial_write(){
  Serial.println(T_data);
  T_data = "";
}

void Catch_value(String Command){
  //interpret decoded data to BF & LR data
  int i=0;
  String value = "";
  if (Command[i] == 'F'){
    i++;
    while ((Command[i] != 'L') && (Command[i] != 'R')){
      value = value + Command[i];
      i++;
    }
    BF_value = value.toInt();
  } else if(Command[i] == 'B'){
    i++;
    while ((Command[i] != 'L') && (Command[i] != 'R')){
      value = value + Command[i];
      i++;
    }
    BF_value = value.toInt()*-1;
  }
  value = "";
  if (Command[i] == 'R'){
    i++;
    while (i < Command.length()){
      value = value + Command[i];
      i++;
    }
    LR_value_history = LR_value;
    LR_value = value.toInt();
  } else if (Command[i] == 'L'){
    i++;
    while (i < Command.length()){
      value = value + Command[i];
      i++;
    }
    LR_value_history = LR_value;
    LR_value = value.toInt()*-1;
  }
}

bool Serial_check(){
  if (R_data == "TEST"){
    T_data = "TEST";
    Serial_write();
    return true;
  }
  return false;
}

void servo_position(int val){
  //Servo speed : 0.17sec/60deg(0.0028333333sec/deg)
  val = map(val, servo_min_pos, servo_max_pos, servo_min_deg, servo_max_deg);

  //Calculate servo delay in milliseconds
  float servo_delay = float(servo_max_deg-servo_min_deg)/float(servo_max_pos-servo_min_pos)*float(abs(LR_value-LR_value_history))*servo_speed*1000;
  servo.write(val);
  delay(servo_delay);
}

void Start_setup(){
  //Check serial communication and servo position set 0
  servo_position(0);
  while (!flag){
    Serial_read();
    flag = Serial_check();
  }
}

void loop() {
  
  Serial_read();
  if (R_data != "" && R_data != "TEST"){
    Catch_value(R_data);
    servo_position(LR_value);
    T_data = String(BF_value) + ", " + String(LR_value);
    Serial_write(); 
  }
}
