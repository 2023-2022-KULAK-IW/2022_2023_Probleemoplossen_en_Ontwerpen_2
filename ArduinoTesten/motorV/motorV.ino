int motorVin1 = 4; // pins verticale motor
int motorVin2 = 5;
<<<<<<< Updated upstream
float maxSnelheidV = 50; //zelf te bepalen na testen [in rpm]
int relatieveSnelheidV = 90; //zelf te bepalen na testen
=======
float maxSnelheidV = 80; //zelf te bepalen na testen [in rpm]
int relatieveSnelheidV = 75; //zelf te bepalen na testen
>>>>>>> Stashed changes
float msPerGraadV = (1000*255)/(maxSnelheidV*6*relatieveSnelheidV);


void setup() {
  pinMode(motorVin1, OUTPUT);
  pinMode(motorVin2, OUTPUT);
}

void loop() {
  delay(5000);
  int hoekV  = 45;
  digitalWrite(motorVin1, HIGH);
  digitalWrite(motorVin2, LOW);
  analogWrite(motorVin1,relatieveSnelheidV);

  delay(hoekV*msPerGraadV);

  digitalWrite(motorVin1, LOW);
  digitalWrite(motorVin2, LOW);
  analogWrite(motorVin1,0);
<<<<<<< Updated upstream


=======
  
>>>>>>> Stashed changes
  delay(10000);

  digitalWrite(motorVin1, LOW);
  digitalWrite(motorVin2, HIGH);
  analogWrite(motorVin2,relatieveSnelheidV-50);

  delay(hoekV*msPerGraadV);

  digitalWrite(motorVin1, LOW);
  digitalWrite(motorVin2, LOW);
  analogWrite(motorVin2,0);
  
  delay(10000);
  

  

  delay(5000);
}