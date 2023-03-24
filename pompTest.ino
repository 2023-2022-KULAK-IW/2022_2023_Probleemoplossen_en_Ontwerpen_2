int pomp = 11;
void setup() {
  pinMode(pomp, OUTPUT);
}

void loop() {
  digitalWrite(pomp, HIGH);
  delay(10000);
  digitalWrite(pomp, LOW);
}
