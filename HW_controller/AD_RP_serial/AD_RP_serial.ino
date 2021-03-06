#include <Servo.h>

//Configuration

String R_data;
String T_data;

int BF_position = 0;
int LR_position = 0;

int servo_min_pos = -255;
int servo_max_pos = 255;
int servo_min_deg = 30;
int servo_max_deg = 150;
int servo_pin = 3;

//DC controlldr pin info
int IN3 = 9;
int IN4 = 10;
int ENB = 11;

//Connected with raspberry pi GPIO pin
int flag_pin = 12;

int Loop_time = 20;
unsigned long point = 0;

Servo servo;

void setup() {
  //Serial setting
  Serial.begin(115200);
  
  //Servo setting
  servo.attach(servo_pin);

  //DC controller digital pin setting
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);

  pinMode(flag_pin, INPUT);
  
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
  Serial.println('@' + T_data + '#');
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
    BF_position = value.toInt();
  } else if(Command[i] == 'B'){
    i++;
    while ((Command[i] != 'L') && (Command[i] != 'R')){
      value = value + Command[i];
      i++;
    }
    BF_position = value.toInt()*-1;
  }
  value = "";
  if (Command[i] == 'R'){
    i++;
    while (i < Command.length()){
      value = value + Command[i];
      i++;
    }
    LR_position = value.toInt();
  } else if (Command[i] == 'L'){
    i++;
    while (i < Command.length()){
      value = value + Command[i];
      i++;
    }
    LR_position = value.toInt()*-1;
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

void Servo_position(int val){
  //Input data is servo_min_pos to servo_max_pos (probably -255 to 255 initially I set)
  val = map(val, servo_min_pos, servo_max_pos, servo_min_deg, servo_max_deg);
  servo.write(val);
}

void DC_position(int val){
  if(val>0){
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    analogWrite(ENB, val);
  }
  else if(val<0){
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    analogWrite(ENB, -val);
  }
  else if(val == 0){
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
    analogWrite(ENB, val);
  }
}

void Start_setup(){
  //Check serial communication and servo position set 0
  Servo_position(0);  
  bool flag = false;
  while (!flag){
    Serial_read();
    flag = Serial_check();
  }
}

void loop() {

  Serial_read();
  if (R_data != "" && R_data != "TEST"){
    Catch_value(R_data);
    Servo_position(LR_position);
    DC_position(BF_position);
    T_data = String(BF_position) + ", " + String(LR_position);
    Serial_write();
    point = 0;
  }
  else if (point == 0 && R_data == ""){
    point = millis();
  }
  if (millis() - point > 3 * Loop_time && point != 0){
    point = 0;
    Servo_position(0);
    DC_position(0);
  }
}
