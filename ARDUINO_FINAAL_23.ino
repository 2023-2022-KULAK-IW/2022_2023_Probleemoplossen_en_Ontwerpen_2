int motorHin1 = 2; // pins horizontale motor
int motorHin2 = 3;

int motorVin1 = 4; // pins verticale motor
int motorVin2 = 5;

int pomp = 6; // pin pomp

bool isEersteLoop = true; // houdt loop bij zodat geswitched kan worden tussen manueel en automatisch

String msg = ""; // initialisatie van mogelijke inkomende serial input

float relatieveSnelheidHaut = 225; // wordt verzonden naar de driver die de snelheid van de horizontale motor controlleert
float relatieveSnelheidHman = 100;
int branden = 0; // tel bijhouden van aantal gebluste branden
float maxSnelheidV = 50; //zelf te bepalen na testen [in rpm]
float relatieveSnelheidVaut = 90; // wordt verzonden naar de driver die de snelheid van de verticale motor controlleert
float relatieveSnelheidVman = 50;
float msPerGraadV = (1000*255)/(maxSnelheidV*6*relatieveSnelheidVaut); //tijd die de verticale motor nodig heeft om zich te richten per graad

byte sensorInterrupt = 7;  // 0 = digital pin 2
byte sensorPin = 7;

float calibrationFactor = 3.3; //calibratieconstante va de waterflowsensor

volatile byte pulseCount; // initialisatie van de variabele voor pulsentelling van de waterflowsensor

float flowRate;
unsigned int flowMilliLitres;
unsigned long totalMilliLitres;

unsigned long oldTime;
float hoekV;


void setup(){
  Serial.begin(9600);
  
  pinMode(motorHin1, OUTPUT);
  pinMode(motorHin2, OUTPUT);

  pinMode(motorVin1, OUTPUT);
  pinMode(motorVin2, OUTPUT);

  pinMode(pomp, OUTPUT);

  pinMode(LED_BUILTIN, OUTPUT);

  pinMode(sensorPin, INPUT);
  digitalWrite(sensorPin, HIGH);

  pulseCount        = 0;
  flowRate          = 0.0;
  flowMilliLitres   = 0;
  totalMilliLitres  = 0;
  oldTime           = 0;

  attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
}



void pulseCounter(){
  pulseCount++;
}



void loop(){
  String msg = Serial.readString();
  //Serial.print("De Arduino kreeg volgende input: ");
  //Serial.println(msg);
  if(isEersteLoop){ //zorgt ervoor dat kan switchen tussen manueel en automatische werking
    digitalWrite(LED_BUILTIN, LOW);
    if(msg == "switch"){
      isEersteLoop = !isEersteLoop;
      Serial.println(isEersteLoop);
      msg = "";
    }
    if(msg == "n"){
      digitalWrite(motorHin1, LOW);
        digitalWrite(motorHin2, LOW);
        analogWrite(motorHin1, 0);
      digitalWrite(motorVin1, LOW);
        digitalWrite(motorVin2, LOW);
        analogWrite(motorVin1, 0);   
      digitalWrite(pomp, LOW);
      Serial.println(msg);
      msg = ""; 
    }  
    if(msg == "start"){
      digitalWrite(motorHin1, HIGH);
      digitalWrite(motorHin2, LOW);
      analogWrite(motorHin1, relatieveSnelheidHaut);
      msg = "";
    }
    if (msg != "" and msg != "start" and msg != "n" and msg != "switch"){
      branden++;
      digitalWrite(motorHin1, LOW);
      digitalWrite(motorHin2, LOW);
      analogWrite(motorHin1, 0);
      
      hoekV = msg.toFloat();
      
      digitalWrite(motorVin1, HIGH);
      digitalWrite(motorVin2, LOW);
      analogWrite(motorVin1,relatieveSnelheidVaut);

      delay(hoekV*msPerGraadV);

      digitalWrite(motorVin1, LOW);
      digitalWrite(motorVin2, LOW);
      analogWrite(motorVin1,0);

      digitalWrite(pomp, HIGH);
      delay(10000);
      digitalWrite(pomp, LOW);
      digitalWrite(motorVin1, LOW);
      digitalWrite(motorVin2, HIGH);
      analogWrite(motorVin2,relatieveSnelheidVaut-50);

      delay(hoekV*msPerGraadV);

      digitalWrite(motorVin1, LOW);
      digitalWrite(motorVin2, LOW);
      analogWrite(motorVin2,0);
      if(branden < 3){
        digitalWrite(motorHin1, HIGH);
        digitalWrite(motorHin2, LOW);
        analogWrite(motorHin1, relatieveSnelheidHaut);
      } 
      msg = "";
    }
    if((millis() - oldTime) > 1000 and oldTime > 0){
      detachInterrupt(sensorInterrupt);
      flowRate = ((1000.0 / (millis() - oldTime)) * pulseCount) * calibrationFactor;
      oldTime = millis();
      totalMilliLitres += flowRate;
      unsigned int frac;
      Serial.println(flowRate);
      Serial.println(totalMilliLitres);
      pulseCount = 0;
      attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
    }
  }
  else{ //manuele werking
    digitalWrite(LED_BUILTIN, HIGH);
    if(msg == "switch"){
      isEersteLoop = !isEersteLoop;
      Serial.println(isEersteLoop);
      msg = "";
    }
    if(msg == "w"){
      digitalWrite(motorVin1, LOW);
        digitalWrite(motorVin2, HIGH);
        analogWrite(motorVin2, relatieveSnelheidVman);
        Serial.println(msg);
        msg = "";
    } 
    if(msg == "a"){
      digitalWrite(motorHin1, LOW);
        digitalWrite(motorHin2, HIGH);
        analogWrite(motorHin2, relatieveSnelheidHman);
        Serial.println(msg);
        msg = "";
    }
    if(msg == "s"){
      digitalWrite(motorVin1, HIGH);
        digitalWrite(motorVin2, LOW);
        analogWrite(motorVin1, relatieveSnelheidVman);
        Serial.println(msg);
        msg = "";
    } 
    if(msg == "d"){
      digitalWrite(motorHin1, HIGH);
        digitalWrite(motorHin2, LOW);
        analogWrite(motorHin1, relatieveSnelheidHman);
        Serial.println(msg);
        msg = "";
    } 
    if(msg == "p"){
      digitalWrite(pomp, HIGH);
      Serial.println(msg);
      msg = "";
    }
    if(msg == "n"){
      digitalWrite(motorHin1, LOW);
        digitalWrite(motorHin2, LOW);
        analogWrite(motorHin1, 0);
      digitalWrite(motorVin1, LOW);
        digitalWrite(motorVin2, LOW);
        analogWrite(motorVin1, 0);   
      digitalWrite(pomp, LOW);
      Serial.println(msg);
      msg = ""; 
    }   
  }
}

