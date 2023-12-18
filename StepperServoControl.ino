#include <Stepper.h>
#include <Servo.h>

Servo myservo;

const int stepsPerRevolution = 2048;

Stepper myStepper = Stepper(stepsPerRevolution, 8, 10, 9, 11);

char move[3];

void setup() {
  Serial.begin(115200);

  myservo.attach(5); 
  myservo.write(115); 

}

void loop() {

  while(Serial.available() > 0)
  {

    int size = Serial.readBytes(move, 2);
    move[2] = '\0';

    if(move[0] == 'D')
    {
      myservo.write(140); 
      delay(500); 
      if(move[1] == '1') {
        myStepper.setSpeed(15);
	      myStepper.step(-stepsPerRevolution/4 - 40);
      } else if(move[1] == '2') {
        myStepper.setSpeed(15);
	      myStepper.step(-stepsPerRevolution/2 - 40);
      } else {
        myStepper.setSpeed(15);
	      myStepper.step(stepsPerRevolution/4 + 40);
      }
      delay(500); 
      myservo.write(115); 
      
      if(move[1] == '1') {
        myStepper.setSpeed(15);
	      myStepper.step(40);
      } else if(move[1] == '2') {
        myStepper.setSpeed(15);
	      myStepper.step(40);
      } else {
        myStepper.setSpeed(15);
	      myStepper.step(-40);
      }
      
    } else if(move[0] == 'X') {

      for(int i = 0; i < move[1] - '0'; i++) {
        myservo.write(74); 
        delay(300); 
        myservo.write(115); 
        delay(500);
      }

    } else if(move[0] == 'Y') {

      if(move[1] == '1') {
        myStepper.setSpeed(15);
	      myStepper.step(stepsPerRevolution/4);
      } else if(move[1] == '2') {
        myStepper.setSpeed(15);
	      myStepper.step(stepsPerRevolution/2);
      } else {
        myStepper.setSpeed(15);
	      myStepper.step(-stepsPerRevolution/4);
      }
    }

    Serial.println("done");

  }
}
