int motorHin1 = 2; // pins horizontale motor
int motorHin2 = 3;

int motorVin1 = 4; // pins verticale motor
int motorVin2 = 5;

int pomp = 6; // pin pomp

int knopje = 8; // voorlopig is dit een random getal
volatile int staatKnopje = LOW; // initialisatie van knopje
bool isEersteLoop = true; // houdt loop bij zodat geswitched kan worden tussen manueel en automatisch

String msg = ""; // initialisatie van mogelijke inkomende serial input

float relatieveSnelheidH = 75; // wordt verzonden naar de driver die de snelheid van de horizontale motor controlleert
int branden = 0; // tel bijhouden van aantal gebluste branden
float maxSnelheidV = 150; //zelf te bepalen na testen [in rpm]
float relatieveSnelheidV = 100; // wordt verzonden naar de driver die de snelheid van de verticale motor controlleert
float msPerGraadV = (1000*255)/(maxSnelheidV*6*relatieveSnelheidV); //tijd die de verticale motor nodig heeft om zich te richten per graad

byte sensorInterrupt = 7;  // 0 = digital pin 2
byte sensorPin       = 7;

float calibrationFactor = 4.5; //calibratieconstante va de waterflowsensor

volatile byte pulseCount; // initialisatie van de variabele voor pulsentelling van de waterflowsensor

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

  pinMode(knopje, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(knopje), knopjeIngedrukt, FALLING); 
}

void knopjeIngedrukt() {
  isEersteLoop = !isEersteLoop; // iedere keer de knop wordt ingedrukt verandert de boolean van waarde
  staatKnopje = LOW; // zet waarde van knop weer naar LOW, zodat opnieuw ingedrukt kan worden
}

void pulseCounter()
{
  pulseCount++;
}


void loop(){
  String msg = Serial.readString();
  
  if((millis() - oldTime) > 1000) { 
      detachInterrupt(sensorInterrupt);
      flowRate = ((1000.0 / (millis() - oldTime)) * pulseCount) / calibrationFactor;
      oldTime = millis();
      flowMilliLitres = (flowRate / 60) * 1000;
      totalMilliLitres += flowMilliLitres;
      unsigned int frac;
      pulseCount = 0;
      attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
    }

  if (isEersteLoop) { //zorgt ervoor dat kan switchen tussen manueel en automatische werking
    Serial.println("Dit is de automatische loop");  
    

  }
  else { //manuele werking
    Serial.println("Dit is de manuele loop");
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
    
    if(msg == "p"){
      digitalWrite(pomp,HIGH);
      msg = "";
    }

    if(msg == "b"){
      digitalWrite(motorHin1, LOW);
      digitalWrite(motorHin2, LOW);
      analogWrite(motorHin2, 0);
      digitalWrite(motorVin1, LOW);
      digitalWrite(motorVin2, LOW);
      analogWrite(motorVin1, 0);
      digitalWrite(pomp, LOW);



    }
  }
}

