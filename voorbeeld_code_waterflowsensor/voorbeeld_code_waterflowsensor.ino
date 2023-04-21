/*
Liquid flow rate sensor -DIYhacking.com Arvind Sanjeev

Measure the liquid/water flow rate using this code. 
Connect Vcc and Gnd of sensor to arduino, and the 
signal line to arduino digital pin 2.
 
 */



byte sensorInterrupt = 0;  // 0 = digital pin 2
byte sensorPin       = 8;


float calibratieFactor = 4.5;

volatile byte pulsenGeteld;  

float debiet;
unsigned int flowMl;
unsigned long totaalMl;

unsigned long oudeTijd;

void setup()
{
  
  // Initialize a serial connection for reporting values to the host
  Serial.begin(9600);
  
  pinMode(sensorPin, INPUT);
  digitalWrite(sensorPin, HIGH);

  
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
/**
 * Main program loop
 */
void loop()
{
   
   if((millis() - oudeTijd) > 1000){ 

      detachInterrupt(sensorInterrupt);
      
      debiet = ((1000.0/(millis() - oudeTijd)) * pulsenGeteld) / calibratieFactor;  //  l/min

      oudeTijd = millis();
      flowMl = (debiet/60) * 1000;
      totaalMl += flowMl;

      Serial.println(debiet);
      pulsenGeteld = 0;
      attachInterrupt(sensorInterrupt, pulsTeller, FALLING);
    }
  
}
