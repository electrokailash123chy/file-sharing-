/*
  Serial Communication Test
  Send data from Arduino to computer and vice versa
  Good for debugging and learning serial communication
*/

String inputString = "";
bool stringComplete = false;
int counter = 0;

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  
  // Wait for serial port to connect
  while (!Serial) {
    ; // Wait for serial port (needed for native USB boards)
  }
  
  Serial.println("\n=================================");
  Serial.println("Serial Communication Test");
  Serial.println("=================================");
  Serial.println("Commands:");
  Serial.println("  'ON'  - Turn LED ON");
  Serial.println("  'OFF' - Turn LED OFF");
  Serial.println("  'HELP' - Show this message");
  Serial.println("=================================\n");
  
  inputString.reserve(200);
}

void loop() {
  // Send counter value every 2 seconds
  static unsigned long lastTime = 0;
  if (millis() - lastTime > 2000) {
    lastTime = millis();
    counter++;
    Serial.print("Counter: ");
    Serial.println(counter);
  }
  
  // Check if data received
  if (stringComplete) {
    Serial.print("Received: ");
    Serial.println(inputString);
    
    // Process commands
    inputString.trim();
    inputString.toUpperCase();
    
    if (inputString == "ON") {
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println("✓ LED turned ON");
    } 
    else if (inputString == "OFF") {
      digitalWrite(LED_BUILTIN, LOW);
      Serial.println("✓ LED turned OFF");
    }
    else if (inputString == "HELP") {
      Serial.println("\nAvailable commands:");
      Serial.println("  ON, OFF, HELP");
    }
    else {
      Serial.println("✗ Unknown command. Type 'HELP' for commands.");
    }
    
    // Clear the string
    inputString = "";
    stringComplete = false;
  }
}

// Serial event handler
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    
    if (inChar == '\n') {
      stringComplete = true;
    } else {
      inputString += inChar;
    }
  }
}
