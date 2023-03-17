
"""
We hebben hiervoor de CYTRON 20A 6V-30V Dual DC Motor Driver (kostprijs = 150) nodig. We moeten ook de maximale snelheid van de motor nog weten.
"""
<<<<<<< HEAD
//https://dronebotworkshop.com/dc-motors-l298n-h-bridge/
//https://arduinogetstarted.com/tutorials/arduino-controls-pump?utm_content=cmp-true
=======
#https://dronebotworkshop.com/dc-motors-l298n-h-bridge/
#https://arduinogetstarted.com/tutorials/arduino-controls-pump?utm_content=cmp-true
>>>>>>> codeMotorPomp

int motorHorizontaal = 9;
int in1 = 8;
int in2 = 7;

int motorVerticaal = 10;
int in3 = 6;
int in4 = 5;

int pomp = 11;

<<<<<<< HEAD

//gegevens nodig:


//verticaal:
float aantalGradenV = -1;//te krijgen van berekening na meting afstand en waterflow

//horizontaal
float aantalGradenH = -50; //te krijgen van webcam
//wachten:
float tijdBlussen = -1; //te krijgen na berekening na meting afstand en waterflow [ms]
=======
"""
gegevens nodig:
"""

#verticaal:
aantalGradenV = -1;#te krijgen van berekening na meting afstand en waterflow

#horizontaal
aantalGradenH = -50; #te krijgen van webcam
#wachten:
tijdBlussen = -1; #te krijgen na berekening na meting afstand en waterflow [ms]
>>>>>>> codeMotorPomp


void setup(){
  pinMode(motorHorizontaal, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  pinMode(motorVerticaal, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  pinMode(pomp, OUTPUT);

<<<<<<< HEAD
  //horizontaal:
  float maxSnelheidH = 320; //zelf te bepalen na testen [in rpm]
  float relatieveSnelheidH = 1; //zelf te bepalen na testen
  float msPerGraadH = 1000/6 * (maxSnelheidH*relatieveSnelheidH)/255;


  //verticaal:
  float maxSnelheidV = 310; //zelf te bepalen na testen [in rpm]
  float relatieveSnelheidV = 1; //zelf te bepalen na testen
  float msPerGraadV = 1000/6 * (maxSnelheidV*relatieveSnelheidV)/255;
}

void draaienH(richting){
  //richting: True = met de klok mee, False = tegen de klok in
=======
  #horizontaal:
  maxSnelheidH = 320; #zelf te bepalen na testen [in rpm]
  relatieveSnelheidH = 1; #zelf te bepalen na testen
  msPerGraadH = 1000/6 * (maxSnelheidH*relatieveSnelheidH)/255;


  #verticaal:
  maxSnelheidV = 310; #zelf te bepalen na testen [in rpm]
  relatieveSnelheidV = 1; #zelf te bepalen na testen
  msPerGraadV = 1000/6 * (maxSnelheidV*relatieveSnelheidV)/255;
}

void draaienH(richting){
  #richting: True = met de klok mee, False = tegen de klok in
>>>>>>> codeMotorPomp

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
<<<<<<< HEAD
  //richting: True = met de klok mee, False = tegen de klok in

      float tijdDraaienV = aantalGradenV*msPerGraadV;
=======
  #richting: True = met de klok mee, False = tegen de klok in

      tijdDraaienV = aantalGradenV*msPerGraadV;
>>>>>>> codeMotorPomp
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
<<<<<<< HEAD
    float correctieGraden = aantalGradenV - nieuweHoek;
=======
    correctieGraden = aantalGradenV - nieuweHoek;
>>>>>>> codeMotorPomp
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
<<<<<<< HEAD
        delay(1000); //tijd om te berekenen van aantalGradenV en tijdBlussen
        draaienV(True);
        delay(1000); //extra pauze uit voorzorg
        digitalWrite(pomp, HIGH);
        delay(500);
        waterDebiet = 0; //waarde van waterflowsensor
        aantalGradenV = hoekV(waterDebiet, afstandBeker)
        correctieV(nieuweHoek);
}
void loop(){

    draaienH(True);
    aantalGradenH = 0; //graden H krijgen van webcam
    if(aantalGradenH <= 0.5 and aantalGradenH >= -0.5){
        float afstandBeker = 0 // te krijgen van webcam
        aantalGradenV = hoekV(3.95, afstandBeker);
=======
        delay(1000); #tijd om te berekenen van aantalGradenV en tijdBlussen
        draaienV(True);
        delay(1000); #extra pauze uit voorzorg
        digitalWrite(pomp, HIGH);
        delay(500);
        #nieuweHoek krijgen
        correctieV(nieuweHoek);
}
void loop(){
    draaienH(True);
    if(aantalGradenH <= 0.5 and aantalGradenH >= -0.5){

>>>>>>> codeMotorPomp
        gevonden();
        if(stoppenPomp()){
            digitalWrite(pomp, LOW);
        }
<<<<<<< HEAD
        delay(1000); //extra pauze uit voorzorg
        draaienV(False);
=======

        delay(1000); #extra pauze uit voorzorg
        draaienV(False);
        tijdBlussen = aantalGradenV = -1;
>>>>>>> codeMotorPomp
    }
}
