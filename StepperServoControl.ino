
#include <Stepper.h>

const int stepsPerRevolution = 2048;

Stepper myStepper = Stepper(stepsPerRevolution, 8, 10, 9, 11);

char move[3];

void setup() {
  Serial.begin(9600);

}

void loop() {

  while(Serial.available() > 0)
  {

    int size = Serial.readBytes(move, 2);
    move[2] = '\0';

    if(move[0] == 'D')
    {
      if(move[1] == '1') {
        myStepper.setSpeed(15);
	      myStepper.step(-stepsPerRevolution/4);
      } else if(move[1] == '2') {
        myStepper.setSpeed(15);
	      myStepper.step(-stepsPerRevolution/2);
      } else {
        myStepper.setSpeed(15);
	      myStepper.step(stepsPerRevolution/4);
      }
    }

  }
}
