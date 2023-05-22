int pomp = 6; // pin pomp

byte sensorInterrupt = 7;  // 0 = digital pin 2
byte sensorPin       = 7;

float calibrationFactor = 4.5;

volatile byte pulseCount;  

float flowRate;
unsigned int flowMilliLitres;
unsigned long totalMilliLitres;

unsigned long oldTime;

void setup() {
  Serial.begin(9600);
  
  pinMode(pomp, OUTPUT);

  pinMode(sensorPin, INPUT);
  digitalWrite(sensorPin, HIGH);

  pulseCount        = 0;
  flowRate          = 0.0;
  flowMilliLitres   = 0;
  totalMilliLitres  = 0;
  oldTime           = 0;

  attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
  
  digitalWrite(pomp, HIGH);
}
void pulseCounter()
{

  pulseCount++;
}

void loop(){
  
  if((millis() - oldTime) > 1000)   
  { 
 
  detachInterrupt(sensorInterrupt);

  flowRate = ((1000.0 / (millis() - oldTime)) * pulseCount) / calibrationFactor;

  oldTime = millis();

  flowMilliLitres = (flowRate / 60) * 1000;

  totalMilliLitres += flowMilliLitres;
  
  Serial.print(flowRate);
  Serial.print(totalMilliLiters);
  unsigned int frac;

  pulseCount = 0;
  attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
  }

  if(totalMilliLitres > 200){
    digitalWrite(pomp, LOW);
    delay(3000);
    totalMilliLitres = 0;

  }

}