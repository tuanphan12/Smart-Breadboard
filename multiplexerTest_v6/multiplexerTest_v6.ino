elapsedMillis timeElapsed;

int centralPins[] = {12,11,10,9};
int auxPins[] = {8,7,6,5};
int SIG_pin = A0;
int EN_pin = 4;
int mode;
int values[50];
int average;
int sum;

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

String commandString;
boolean stringComplete = false;

String upstreamStr;

void setup() {
  for (int i = 0; i < 4; i++)
  {
    pinMode(centralPins[i],OUTPUT);
    pinMode(auxPins[i],OUTPUT);
    digitalWrite(centralPins[i],LOW);
    digitalWrite(auxPins[i],LOW);
  }
  pinMode(EN_pin,OUTPUT);  //EN pin
  digitalWrite(EN_pin,LOW); //EN pin 
  Serial.begin(9600);
  commandString.reserve(200);
}

int readChannel(int channel){
  for (int j = 0; j < 4; j++){
    digitalWrite(centralPins[j],myChannel[channel][j]);
  }
  int SIG_value = analogRead(SIG_pin);
  return SIG_value;
}

void serialEvent() {
  String temp;
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '*') {
      stringComplete = true;
    }
    else{
      commandString += inChar;
    }
  }
}

//variables to setup loop control:
int loopCounter = 0;
int maxSkip = 1000;

void loop() {
  if (loopCounter == maxSkip){
    Serial.println(upstreamStr);
    Serial.println(timeElapsed);
    loopCounter = 0;
    timeElapsed = 0;
    upstreamStr = "";   //empty the sent string so no addition information will be overlap
  }
  else{
    loopCounter += 1;
    delay(1);
  }
  //delay(2000);  //must have a delay here for communication....
  //Serial.print(upstreamStr);
  serialEvent();   
  if (stringComplete){
    if (commandString.equalsIgnoreCase("all")){
        mode = 0;
        Calculation(mode,0,0); 
    }

    else if (commandString.equalsIgnoreCase("off")){
      digitalWrite(EN_pin,HIGH);
    }

    else if (commandString.equalsIgnoreCase("on")){
      digitalWrite(EN_pin,LOW);
    }
  
//    //format of reading a single node for a lengt of time: nodeindex,samplingrate; + "single"
//    else if (commandString.substring(0) == "single"){
//        int node_pos;
//        int sampling_rate;
//        String temp;
//        mode = 2;
//        for (int h = 0; h < commandString.length(); h++) {
//          if (commandString[h] == '#'){
//            break;
//          }
//          else if (commandString[h] == ','){
//            node_pos = sampling_rate;
//            temp = ""; //empty
//          }
//          else{
//            temp += commandString[h];
//            sampling_rate = (temp.toInt());
//          }
//        }
//        Calculation(mode,node_pos,sampling_rate);
//    }

    //format of reading a range of nodes: nodeindex,samplingrate
    else{
      int lRange = 0;
      int hRange = 0;
      String temp;
      for (int h = 0; h < commandString.length(); h++){
        if (commandString[h] == ','){
          lRange = hRange;
          temp = ""; //empty    
        }
        else{
          temp += commandString[h];
          hRange = (temp.toInt());
        }
      }
      mode = 1;
      Calculation(mode,lRange,hRange);
    }
    commandString = "";
    stringComplete = false;
  }
}

void Calculation(int mode1, int low, int high){
    //Serial.println(low);
    //Serial.println(high);
    int pin = low;
    if (mode1 == 0){
      for (int i = 0; i < 8; i++){ //Read channel 0-7 of the central mux
        for (int j = 0; j < 16; j++){
          for (int sel = 0; sel < 4; sel++){ //Control the channel of the connecting mux
            digitalWrite(auxPins[sel],myChannel[j][sel]);
          }
          for (int k = 0; k < 50; k++){ //Take reading of the value 50 times and take the average
            values[k] = (readChannel(i));
            sum += values[k];
          }
          average = sum/50;
          sum = 0; //clear the sum
          upstreamStr += pin;
          upstreamStr += ":";
          upstreamStr += average;
          upstreamStr += "&";       
          pin++;    
        }
      }  
    }

    //high is the sampling rate
    //low is the index of the node
    if (mode1 = 1){
      //Serial.println(low);
      int central_mux_channel, aux_mux_channel,delay_step;
      int duration = 2; //for 2 seconds
      delay_step = 1000/high;
      central_mux_channel = low/16;
      aux_mux_channel = low - (central_mux_channel*16);
      //Serial.println(central_mux_channel);
      //Serial.println(aux_mux_channel);
      for (int sel = 0; sel < 4; sel++){ //Control the channel of the connecting mux
         digitalWrite(auxPins[sel],myChannel[aux_mux_channel][sel]);
      }
      for (int t = 0; t <= duration; t++){
        for (int s = 0; s < (high); s++){
          //Serial.println(low);
          average = readChannel(central_mux_channel);
          upstreamStr += low;
          upstreamStr += ":";
          upstreamStr += average;
          upstreamStr += "&";
          //Serial.println(upstreamStr);
          delay(delay_step);
        }
      } 
    }
}

