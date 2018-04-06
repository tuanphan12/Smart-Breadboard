//order: S0,S1,S2,S3
int centralPins[] = {12,11,10,9};
int auxPins[] = {8,7,6,5};

int myChannel[16][4] = {
  {0,0,0,0}, //channel 0
  {1,0,0,0}, //channel 1
  {0,1,0,0}, //channel 2
  {1,1,0,0}, //channel 3
  {0,0,1,0}, //channel 4
  {1,0,1,0}, //channel 5
  {0,1,1,0}, //channel 6
  {1,1,1,0}, //channel 7
  {0,0,0,1}, //channel 8
  {1,0,0,1}, //channel 9
  {0,1,0,1}, //channel 10
  {1,1,0,1}, //channel 11
  {1,0,1,1}, //channel 12
  {1,0,1,1}, //channel 13
  {0,1,1,1}, //channel 14
  {1,1,1,1}  //channel 15
};

void setup() {
  // put your setup code here, to run once:
  for (int i = 0; i < 4; i++)
  {
    pinMode(centralPins[i],OUTPUT);
    pinMode(auxPins[i],OUTPUT);
    digitalWrite(centralPins[i],LOW);
    digitalWrite(auxPins[i],LOW);
  }
  pinMode(4,OUTPUT);   //EN pin
  digitalWrite(4,LOW);
  
  digitalWrite(12,HIGH);  //S0
  digitalWrite(11,HIGH);  //S1
  digitalWrite(10,HIGH);  //S2
  digitalWrite(9,LOW);  //S3
  
  digitalWrite(8,HIGH);  //S0
  digitalWrite(7,LOW);  //S1
  digitalWrite(6,HIGH);  //S2
  digitalWrite(5,HIGH);  //S3
  
  Serial.begin(9600);

}

void loop() {
  int SIG_pin;
  SIG_pin = analogRead(A0);
  Serial.println(SIG_pin);
  delay(1500);
}
