int motorHin1 = 2;
int motorHin2 = 3;

int motorVin1 = 4;
int motorVin2 = 5;

int pomp = 6;

String msg = "";

float relatieveSnelheidH = 220;
int branden = 0;
float maxSnelheidV = 50; //zelf te bepalen na testen [in rpm]
float relatieveSnelheidV = 90; //zelf te bepalen na testen
float msPerGraadV = (1000*255)/(maxSnelheidV*6*relatieveSnelheidV);

float oudeTijd = -1;

byte sensorInterrupt = 9;  // 0 = digital pin 2
byte sensorPin       = 9;

float calibrationFactor = 3.33;

volatile byte pulseCount;  

float flowRate;
unsigned int flowMilliLitres;
unsigned long totalMilliLitres;

unsigned long oldTime;
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

  pulseCount        = 0;
  flowRate          = 0.0;
  flowMilliLitres   = 0;
  totalMilliLitres  = 0;
  oldTime           = 0;

  attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
  
}
void pulseCounter()
{

  pulseCount++;
}

void loop(){
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
    delay(30000);
    digitalWrite(pomp, LOW);
    digitalWrite(motorVin1, LOW);
      digitalWrite(motorVin2, HIGH);
      analogWrite(motorVin2,relatieveSnelheidV-50);

      delay(hoekV*msPerGraadV);

      digitalWrite(motorVin1, LOW);
      digitalWrite(motorVin2, LOW);
      analogWrite(motorVin2,0);
      if(branden < 3){
        digitalWrite(motorHin1, HIGH);
        digitalWrite(motorHin2, LOW);
        analogWrite(motorHin1, relatieveSnelheidH);
      } 
    
    msg = "";
    }
    if((millis() - oldTime) > 1000 and oldTime > 0)   
  { 
 
    detachInterrupt(sensorInterrupt);

    flowRate = ((1000.0 / (millis() - oldTime)) * pulseCount) * calibrationFactor;

    oldTime = millis();

    totalMilliLitres += flowRate;
      
    unsigned int frac;

    pulseCount = 0;
    attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
  }

}