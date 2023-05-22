int motorHin1 = 2; // pins horizontale motor
int motorHin2 = 3;

int motorVin1 = 4; // pins verticale motor
int motorVin2 = 5;

int pomp = 6; // pin pomp

String msg = "";

float relatieveSnelheidH = 75;
int branden = 0;
float maxSnelheidV = 150; //zelf te bepalen na testen [in rpm]
int relatieveSnelheidV = 100; //zelf te bepalen na testen
float msPerGraadV = (1000*255)/(maxSnelheidV*6*relatieveSnelheidV);

byte sensorInterrupt = 9;  // 0 = digital pin 2
byte sensorPin       = 9;

float calibrationFactor = 4.5;

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

  if(msg == "w"){
     digitalWrite(motorVin1, LOW);
      digitalWrite(motorVin2, HIGH);
      analogWrite(motorVin2, relatieveSnelheidV);
      msg = "";
    } 
  
  if(msg == "a"){
    digitalWrite(motorHin1, LOW);
      digitalWrite(motorHin2, HIGH);
      analogWrite(motorHin2, relatieveSnelheidH);
      msg = "";
    }

  if(msg == "s"){
     digitalWrite(motorVin1, HIGH);
      digitalWrite(motorVin2, LOW);
      analogWrite(motorVin1, relatieveSnelheidV);
      msg = "";
    } 

  if(msg == "d"){
     digitalWrite(motorHin1, HIGH);
      digitalWrite(motorHin2, LOW);
      analogWrite(motorHin1, relatieveSnelheidH);
      msg = "";
    } 

  if (msg != "" and msg != "start" and msg != "w" and msg != "a" and msg != "s" and msg != "d") { //nog python code veranderen en deze voorwaarde dat hij rekening houdt met een begincharacter, zo kunnen we ook van de laptop stuff sturen

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
    
    msg = "";
    }
    if((millis() - oldTime) > 1000)   
  { 
 
    detachInterrupt(sensorInterrupt);

    flowRate = ((1000.0 / (millis() - oldTime)) * pulseCount) / calibrationFactor;

    oldTime = millis();

    flowMilliLitres = (flowRate / 60) * 1000;

    totalMilliLitres += flowMilliLitres;
      
    unsigned int frac;

    pulseCount = 0;
    attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
  }

    if(totalMilliLitres > 10 and hoekV != 0){
      digitalWrite(pomp, LOW);
      totalMilliLitres = 0;

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