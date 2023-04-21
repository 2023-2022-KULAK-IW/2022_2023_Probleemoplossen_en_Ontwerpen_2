int motorHin1 = 2;
int motorHin2 = 3;

int motorVin1 = 4;
int motorVin2 = 5;

int pomp = 6;

String msg = "";

float relatieveSnelheidH = 100;

float maxSnelheidV = 150; //zelf te bepalen na testen [in rpm]
float relatieveSnelheidV = 100; //zelf te bepalen na testen
float msPerGraadV = ((1000)/(maxSnelheidV*6*relatieveSnelheidV))*255;

void setup() {
  Serial.begin(9600);

  pinMode(motorHin1, OUTPUT);
  pinMode(motorHin2, OUTPUT);

  pinMode(motorVin1, OUTPUT);
  pinMode(motorVin2, OUTPUT);

  pinMode(pomp, OUTPUT);

  
  
}
void loop(){
  while (Serial.available() == 0) {}
  String msg = Serial.readString();
  
  if (msg == "start") {
    digitalWrite(motorHin1, HIGH);
    digitalWrite(motorHin2, LOW);
    analogWrite(motorHin1, relatieveSnelheidH);    
  }

  if (msg != "start" and msg != "") {
    digitalWrite(motorHin1, LOW);
    digitalWrite(motorHin2, LOW);
    analogWrite(motorHin1,0);
    
    float hoekV = msg.toFloat();
    
    digitalWrite(motorVin1, HIGH);
    digitalWrite(motorVin2, LOW);
    analogWrite(motorVin1,relatieveSnelheidV);

    delay(hoekV*msPerGraadV*10);

    digitalWrite(motorVin1, LOW);
    digitalWrite(motorVin2, LOW);
    analogWrite(motorVin1,0);

    digitalWrite(pomp, HIGH);
    delay(2000);
    digitalWrite(pomp, LOW);

    digitalWrite(motorHin1, HIGH);
    digitalWrite(motorHin2, LOW);
    analogWrite(motorHin1, relatieveSnelheidH);
    
    msg = "";
    }




  

}
Schrijven naar P&O 2
