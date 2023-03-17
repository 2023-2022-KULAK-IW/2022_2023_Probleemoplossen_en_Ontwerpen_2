
"""
We hebben hiervoor de CYTRON 20A 6V-30V Dual DC Motor Driver (kostprijs = 150) nodig. We moeten ook de maximale snelheid van de motor nog weten.
"""
#https://dronebotworkshop.com/dc-motors-l298n-h-bridge/

int motorHorizontaal = 9;
int in1 = 8;
int in2 = 7;

int motorVerticaal = 10
int in3 = 6
int in4 = 5

#horizontaal:
maxSnelheidH = 310 #nog niet bekend [in rpm]
aantalGradenH = 0 #te krijgen van webcam

relatieveSnelheidH = 1 #zelf te bepalen na testen
msPerGraadH = 1000/6 * (maxSnelheidH*relatieveSnelheidH)/255
tijdDraaienH = aantalGradenH*msPerGraadH

#verticaal:
maxSnelheidV = 310 #nog niet bekend [in rpm]
aantalGradenV = 0 #te krijgen van berekening na meting afstand en waterflow

relatieveSnelheidV = 1 #zelf te bepalen na testen
msPerGraadV = 1000/6 * (maxSnelheidV*relatieveSnelheidV)/255
tijdDraaienV = aantalGradenV*msPerGraadV

#wachten:
tijdBlussen = 0 #te krijgen na berekening na meting afstand en waterflow [ms]


void setup(){
  pinMode(motorHorizontaal, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  pinMode(motorVerticaal, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
}

void draaienH(richting){
  #richting: True = met de klok mee, False = tegen de klok in
  if (richting){
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
  }
  else {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
  }

  analogWrite(motorHorizontaal, relatieveSnelheidH);
  delay(tijdDraaienH);
  analogWrite(motorHorizontaal, 0);
}


void draaienV(richting){
  #richting: True = met de klok mee, False = tegen de klok in
  if (richting)  {
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
  }
  else {
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
  }
  analogWrite(motorVerticaal, relatieveSnelheidV);
  delay(tijdDraaienV);
  analogWrite(motorVerticaal, 0);
}

void loop(){
  if (tijdBlussen != 0){
    draaienH(True);
    draaienV(True);

    delay(tijdBlussen);

    draaienH(False);
    draaienV(False);
  }
}

