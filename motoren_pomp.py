
"""
We hebben hiervoor de CYTRON 20A 6V-30V Dual DC Motor Driver (kostprijs = 150) nodig. We moeten ook de maximale snelheid van de motor nog weten.
"""
#https://dronebotworkshop.com/dc-motors-l298n-h-bridge/
#https://arduinogetstarted.com/tutorials/arduino-controls-pump?utm_content=cmp-true

int motorHorizontaal = 9;
int in1 = 8;
int in2 = 7;

int motorVerticaal = 10;
int in3 = 6;
int in4 = 5;

int pomp = 11;

"""
gegevens nodig:
"""
#horizontaal:
aantalGradenH = -1; #te krijgen van webcam

#verticaal:
aantalGradenV = -1;#te krijgen van berekening na meting afstand en waterflow

#wachten:
tijdBlussen = -1; #te krijgen na berekening na meting afstand en waterflow [ms]


void setup(){
  pinMode(motorHorizontaal, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  pinMode(motorVerticaal, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  pinMode(pomp, OUTPUT);

  #horizontaal:
  maxSnelheidH = 310; #zelf te bepalen na testen [in rpm]
  relatieveSnelheidH = 1; #zelf te bepalen na testen

  msPerGraadH = 1000/6 * (maxSnelheidH*relatieveSnelheidH)/255;


  #verticaal:
  maxSnelheidV = 310; #zelf te bepalen na testen [in rpm]
  relatieveSnelheidV = 1; #zelf te bepalen na testen
  msPerGraadV = 1000/6 * (maxSnelheidV*relatieveSnelheidV)/255;

}

void draaienH(richting){
  #richting: True = met de klok mee, False = tegen de klok in
  tijdDraaienH = aantalGradenH*msPerGraadH;
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
  tijdDraaienV = aantalGradenV*msPerGraadV;
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
  #if éénmaal doorlopen wanneer alle 3 de gegevens zijn verkregen
  if (tijdBlussen >= 0 and aantalGradenH >= 0 and aantalGradenV >= 0 ){
    draaienH(True);
    draaienV(True);

    delay(1000); #extra pauze uit voorzorg

    digitalWrite(pomp, HIGH);
    delay(tijdBlussen);
    digitalWrite(pomp, LOW);

    delay(1000); #extra pauze uit voorzorg

    draaienH(False);
    draaienV(False);

    tijdBlussen = aantalGradenH = aantalGradenV = -1;
  }
}
