int centralPins[] = {12,11,10,9};
int auxPins[] = {8,7,6,5};
int SIG_pin = A0;
int EN_pin = 4;
int mode;
int data[256];
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
    if (inChar == '\n') {
      stringComplete = true;
    }
    else{
      commandString += inChar;
    }
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(1500);  //must have a delay here for communication....?????
  serialEvent();   
  if (stringComplete){
    if (commandString.equalsIgnoreCase("all")){
        mode = 0;
        Calculation(mode,0,0); 
    }

    //format of reading a single node for a lengt of time: nodeindex,timeinsec; + "single"
    else if (commandString.substring(0) == "single"){
        int node_pos;
        int t;
        String temp;
        mode = 2;
        for (int h = 0; h < commandString.length(); h++) {
          if (commandString[h] == ';'){
            break;
          }
          else if (commandString[h] == ','){
            node_pos = t;
            temp = ""; //empty
          }
          else{
            temp += commandString[h];
            t = (temp.toInt());
          }
        }
        Calculation(mode,node_pos,t);
    }

    //format of reading a range of nodes: firstnodeindex,secondnodeindex
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
      //Serial.println(lRange);
      //Serial.println(hRange);
    }
    //Serial.println(commandString);
    commandString = "";
    stringComplete = false;
  }
}

void Calculation(int mode1, int low, int high){
    int count = 0;
    int pin = low;
    String upstreamStr;
    if (mode1 == 0){
      for (int i = 0; i < 8; i++){ //Read channel 0-7 of the central mux
        for (int j = 0; j < 16; j++){
          for (int sel = 0; sel < 4; sel++){ //Control the channel of the connecting mux
            digitalWrite(auxPins[sel],myChannel[j][sel]);
          }
          //Serial.print("Pin ");
          upstreamStr += pin;
          upstreamStr += ":";
          for (int k = 0; k < 50; k++){ //Take reading of the value 50 times and take the average
            values[k] = (readChannel(i));
            sum += values[k];
          }
          average = sum/50;
          sum = 0; //clear the sum
          upstreamStr += (average);
          upstreamStr += "&";        
          data[count] = pin;          //format of the data: [PIN#,average,PIN#,average,etc...]
          data[count+1] = average;
          count = count + 2;
          pin++;    
        }
      }  
    }
        
    if (mode1 == 1){
      int tempInt;
      int setLow;
      int cycle = int(high/16);  //total number of cycle 
      int start_mux = int(low/16); //initial starting mux
      if (high < 16){
        tempInt = high;
      }
      else{
        tempInt = 15;
      }

      if (low < 16){
        setLow = low;
      }
      else{
        setLow = low - (start_mux*16);
      }
          
      int turn = start_mux + 1;  //keep track of how many times the function loop
      //   Serial.print(start_mux);
      //   Serial.println(cycle);
      for (int i = start_mux; i < (cycle+1); i++){ //Read channel 0-7 of the central mux
         for (int j = setLow; j < (tempInt+1); j++){ //Read channels from 0 - 15
            for (int sel = 0; sel < 4; sel++){ //Control the channel of the connecting mux
              digitalWrite(auxPins[sel],myChannel[j][sel]);
            }
            for (int k = 0; k < 50; k++){ //Take reading of the value 50 times and take the average
              values[k] = (readChannel(i));
              sum += values[k];
            }
            Serial.print(pin);
            Serial.print(":");
            average = sum/50;
            sum = 0;
            Serial.print(average);
            Serial.print("&");                 
            data[count] = pin;          //format of the data: [PIN#,average,PIN#,average,etc...]
            data[count+1] = average;
            count = count + 2;
            pin++;    
         }
         setLow = 0;
         if (turn == cycle){
           tempInt = high-(cycle*16);
         }
         else{
            turn += 1;
            tempInt = 15;
         }
      }
    }

    if (mode1 = 2){
      int central_mux_channel, aux_mux_channel;
      central_mux_channel = low/16;
      aux_mux_channel = low - (central_mux_channel*16);
      //Serial.println(central_mux_channel);
      //Serial.println(aux_mux_channel);
      for (int sel = 0; sel < 4; sel++){ //Control the channel of the connecting mux
         digitalWrite(auxPins[sel],myChannel[aux_mux_channel][sel]);
      }
      for (int t = 0; t < (high*1000); t++){
        for (int k = 0; k < 50; k++){ //Take reading of the value 50 times and take the average
           values[k] = (readChannel(central_mux_channel));
           sum += values[k];
        }
        average = sum/50;
        sum = 0;
        upstreamStr += pin;
        upstreamStr += ":";
        upstreamStr += average;
        upstreamStr += "&";
        delay(1);
      } 
    }

    Serial.print(upstreamStr);
}

