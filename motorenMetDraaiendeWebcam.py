
/*
We hebben hiervoor de CYTRON 20A 6V-30V Dual DC Motor Driver (kostprijs = 150) nodig. We moeten ook de maximale snelheid van de motor nog weten.
*/

//https://dronebotworkshop.com/dc-motors-l298n-h-bridge/
//https://arduinogetstarted.com/tutorials/arduino-controls-pump?utm_content=cmp-true


int motorHorizontaal = 9;
int in1 = 8;
int in2 = 7;

int motorVerticaal = 10;
int in3 = 6;
int in4 = 5;

int pomp = 11;

//gegevens nodig
//verticaal:
float aantalGradenV = -1;//te krijgen van berekening na meting afstand en waterflow

float aantalGradenH = -50; //te krijgen van webcam
//wachten:
float tijdBlussen = -1; //te krijgen na berekening na meting afstand en waterflow [ms]

void setup(){
  pinMode(motorHorizontaal, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  pinMode(motorVerticaal, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  pinMode(pomp, OUTPUT);

  //horizontaal:
  float maxSnelheidH = 320; //zelf te bepalen na testen [in rpm]
  float relatieveSnelheidH = 1; //zelf te bepalen na testen
  float msPerGraadH = 1000/6 * (maxSnelheidH*relatieveSnelheidH)/255;

  //verticaal:
  maxSnelheidV = 310; //zelf te bepalen na testen [in rpm]
  relatieveSnelheidV = 1; //zelf te bepalen na testen
  msPerGraadV = 1000/6 * (maxSnelheidV*relatieveSnelheidV)/255;

void draaienH(richting){

  //richting: True = met de klok mee, False = tegen de klok in

  if (richting){
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
  }
  else {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
  }

  analogWrite(motorHorizontaal, relatieveSnelheidH);
}


void draaienV(richting){
      //richting: True = met de klok mee, False = tegen de klok in
      float tijdDraaienV = aantalGradenV*msPerGraadV;

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
void correctieV(nieuweHoek){

    float correctieGraden = aantalGradenV - nieuweHoek;

    if(correctieGraden <= 0){
        digitalWrite(in3, LOW);
        digitalWrite(in4, HIGH);
        correctieGraden = - correctieGraden;
    }
    else{
        digitalWrite(in3, HIGH);
        digitalWrite(in4, LOW);
    }
    analogWrite(motorVerticaal, relatieveSnelheidV);
    delay(correctieGraden*msPerGraadV);
    analogWrite(motorVerticaal, 0);
}
void gevonden(){
        analogWrite(motorHorizontaal, 0);

        delay(1000); //tijd om te berekenen van aantalGradenV en tijdBlussen
        draaienV(True);
        delay(1000); //extra pauze uit voorzorg
        digitalWrite(pomp, HIGH);
        delay(500);
        float debietWater = 0; //te krijgen van waterflowsensor
        float nieuweHoek = hoekV(debietWater, afstandBeker)//nieuweHoek krijgen
        correctieV(nieuweHoek);
}
void loop(){
    draaienH(True);
    if(aantalGradenH <= 0.5 and aantalGradenH >= -0.5){

        float afstandBeker = 0 // te krijgen van webcam
        aantalGradenV = hoekV(3.95, afstandBeker);

        delay(1000); //tijd om te berekenen van aantalGradenV en tijdBlussen
        draaienV(True);
        delay(1000); //extra pauze uit voorzorg
        digitalWrite(pomp, HIGH);
        delay(500);
        //nieuweHoek krijgen
        correctieV(nieuweHoek);
}

