int enA = 9;
int in1 = 8;
int in2 = 7;

"""
We hebben hiervoor de CYTRON 20A 6V-30V Dual DC Motor Driver (kostprijs = 150) nodig. We moeten ook de maximale snelheid van de motor nog weten.
"""
#https://dronebotworkshop.com/dc-motors-l298n-h-bridge/

maxSnelheid = 310 #nog niet bekend [in rpm]
aantalGraden = 10 #te krijgen van webcam
tijdWachten = 1000 #nog te bepalen, hangt af van draaien verticaal en tijd blussen [in ms]


relatieveSnelheid = 1

snelheid = (maxSnelheid*relatieveSnelheid)/255
msPerGraad = 1000/6 * snelheid
tijdDraaien = aantalGraden*msPerGraad

void setup(){
pinMode(motor1, OUTPUT);
pinMode(in1, OUTPUT);
pinMode(in2, OUTPUT);
}

void loop(){
  #start motor1
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);

  #snelheid meegeven (0-255)
  analogWrite(motor1, relatieveSnelheid);

  #laten draaien (milliseconden)
  delay(msPerGraad);

  #stoppen
  analogWrite(motor1, 0);

  delay(tijdWachten);


  #andere richting uit draaien
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(motor1, relatieveSnelheid);


  #laten draaien (milliseconden)
  delay(tijdDraaien);

  #motor1 uitzetten
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
}