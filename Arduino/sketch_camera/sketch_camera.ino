int in2 = 2;
int in3 = 3;
String msg = "";
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);


}

void loop() {
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  while (Serial.available() == 0) {}
  String msg = Serial.readString();

  if (msg != "") {
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    delay(3000);
    String msg = "";
  }
}
