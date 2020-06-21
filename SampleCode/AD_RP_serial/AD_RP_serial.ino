#include <Servo.h>

String R_data;
String T_data;
int BF_value;
int LR_value;
bool flag;

Servo servo;

void setup() {
  Serial.begin(115200);
  int servo_pin = 9;
  servo.attach(servo_pin);
}

void Serial_read(){
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
    LR_value = value.toInt();
  } else if (Command[i] == 'L'){
    i++;
    while (i < Command.length()){
      value = value + Command[i];
      i++;
    }
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
  val = map(val, -500, 500, -180, 180);
  servo.write(val);
}

void loop() {
  Serial_read();
  if (R_data != ""){
    flag = Serial_check();
    if (not flag){
      Catch_value(R_data);
      servo_position(LR_value);
      T_data = String(BF_value) + ", " + String(LR_value);
      Serial_write();
    } 
  }
  delay(1);
}
