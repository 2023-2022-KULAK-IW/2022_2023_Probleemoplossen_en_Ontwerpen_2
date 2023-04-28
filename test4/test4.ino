int motorHin1 = 2;
int motorHin2 = 3;

int motorVin1 = 4;
int motorVin2 = 5;

int pomp = 6;

String msg = "";

float relatieveSnelheidH = 75;

float maxSnelheidV = 310; //zelf te bepalen na testen [in rpm]
float relatieveSnelheidV = 150; //zelf te bepalen na testen
float msPerGraadV = (1000*255)/(maxSnelheidV*6*relatieveSnelheidV);

float oudeTijd = -1;

byte sensorInterrupt = 9;  // 0 = digital pin 2
byte sensorPin       = 9;

int branden = 0;

float calibratieFactor = 4.5;

volatile byte pulsenGeteld;  

float debiet;
unsigned int flowMl;
unsigned long totaalMl;
float hoekV;
void setup() {
  Serial.begin(9600);

  pinMode(motorHin1, OUTPUT);
  pinMode(motorHin2, OUTPUT);

  pinMode(motorVin1, OUTPUT);
  pinMode(motorVin2, OUTPUT);

  pinMode(pomp, OUTPUT);

  

  pinMode(sensorPin, INPUT);
  digitalWrite(sensorPin, HIGH);
  hoekV = 0;
  pulsenGeteld = 0;
  debiet = 0.0;
  flowMl  = 0;
  totaalMl = 0;
  oudeTijd = 0;

  attachInterrupt(sensorInterrupt, pulsTeller, FALLING);
  
}
void pulsTeller()
{
  pulsenGeteld++;
}

void loop(){
  while (Serial.available() == 0) {}
  String msg = Serial.readString();
  if(msg == "start"){
    digitalWrite(motorHin1, HIGH);
    digitalWrite(motorHin2, LOW);
    analogWrite(motorHin1, relatieveSnelheidH);
    msg = "";
  }

  if (msg != "" and msg != "start") {

    branden++;
    digitalWrite(motorHin1, LOW);
    digitalWrite(motorHin2, LOW);
    analogWrite(motorHin1, 0);
    
    hoekV = msg.toFloat();
    
    digitalWrite(motorVin1, HIGH);
    digitalWrite(motorVin2, LOW);
    analogWrite(motorVin1,relatieveSnelheidV);

    delay(hoekV*msPerGraadV);

    digitalWrite(motorVin1, LOW);
    digitalWrite(motorVin2, LOW);
    analogWrite(motorVin1,0);

    digitalWrite(pomp, HIGH);
    oudeTijd = millis();
    msg = "";
    }
    if((millis() - oudeTijd) > 1000 and oudeTijd > 0){ 

      detachInterrupt(sensorInterrupt);
      
      debiet = ((1000.0/(millis() - oudeTijd)) * pulsenGeteld) / calibratieFactor;  //  l/min

      oudeTijd = millis();
      flowMl = (debiet/60) * 1000;
      totaalMl += flowMl;

      pulsenGeteld = 0;
      attachInterrupt(sensorInterrupt, pulsTeller, FALLING);
    }
    if(totaalMl > 400 and hoekV != 0){
      digitalWrite(pomp, LOW);
      totaalMl = 0;
      oudeTijd = -1;

      digitalWrite(motorVin1, LOW);
      digitalWrite(motorVin2, HIGH);
      analogWrite(motorVin2,relatieveSnelheidV);

      delay(hoekV*msPerGraadV);

      digitalWrite(motorVin1, LOW);
      digitalWrite(motorVin2, LOW);
      analogWrite(motorVin2,0);
      if(branden < 3){
        digitalWrite(motorHin1, HIGH);
        digitalWrite(motorHin2, LOW);
        analogWrite(motorHin1, relatieveSnelheidH);
      } 
    }
}
