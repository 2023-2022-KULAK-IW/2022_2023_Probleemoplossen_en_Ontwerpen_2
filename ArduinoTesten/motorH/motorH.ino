int motorHin1 = 2; // pins horizontale motor
int motorHin2 = 3;
float relatieveSnelheidH = 255;

void setup() {
  pinMode(motorHin1, OUTPUT);
  pinMode(motorHin2, OUTPUT);

}

void loop() {
    digitalWrite(motorHin1, HIGH);
    digitalWrite(motorHin2, LOW);
    analogWrite(motorHin1, relatieveSnelheidH);

}
