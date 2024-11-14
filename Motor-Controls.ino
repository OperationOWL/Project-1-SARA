// Motor pins
const int motor1Pin1 = 27; // Motor 1, Pin 1
const int motor1Pin2 = 26; // Motor 1, Pin 2
const int motor2Pin1 = 25; // Motor 2, Pin 1
const int motor2Pin2 = 33; // Motor 2, Pin 2

void setup() {
  // Initialize motor pins as outputs
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(motor2Pin1, OUTPUT);
  pinMode(motor2Pin2, OUTPUT);
}

void loop() {
  // Example: Call the functions here to control the motor movement
  front();
  delay(1000);  // Move forward for 1 second

  back();
  delay(1000);  // Move backward for 1 second

  turnRight();
  delay(500);   // Turn right for 0.5 seconds

  turnLeft();
  delay(500);   // Turn left for 0.5 seconds

  stopMotors();
  delay(1000);  // Stop for 1 second
}

// Function to move forward
void front() {
  digitalWrite(motor1Pin1, HIGH);
  digitalWrite(motor1Pin2, LOW);
  digitalWrite(motor2Pin1, HIGH);
  digitalWrite(motor2Pin2, LOW);
}

// Function to move backward
void back() {
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, HIGH);
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, HIGH);
}

// Function to turn right
void turnRight() {
  digitalWrite(motor1Pin1, HIGH);
  digitalWrite(motor1Pin2, LOW);
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, HIGH);
}

// Function to turn left
void turnLeft() {
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, HIGH);
  digitalWrite(motor2Pin1, HIGH);
  digitalWrite(motor2Pin2, LOW);
}

// Function to stop the motors
void stopMotors() {
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, LOW);
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, LOW);
}
