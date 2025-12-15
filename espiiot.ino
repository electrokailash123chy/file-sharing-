#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

#define SSID "Engineer boys"
#define PASS "khwop@9800"
#define BASE_URL "https://esp32-led-ed9ea-default-rtdb.asia-southeast1.firebasedatabase.app/pins.json"

// Maximum number of GPIO pins to monitor
#define MAX_PINS 10
int activePins[MAX_PINS];
int activePinCount = 0;

void reconnectWiFi() {
  Serial.println("\nWiFi Disconnected! Reconnecting...");
  WiFi.disconnect();
  WiFi.begin(SSID, PASS);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    Serial.print(".");
    delay(500);
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi Reconnected!");
    Serial.println("IP: " + WiFi.localIP().toString());
  } else {
    Serial.println("\nReconnection failed!");
  }
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(SSID, PASS);
  Serial.print("Connecting WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  } 
  Serial.println("\nWiFi Connected!");
  Serial.println("IP: " + WiFi.localIP().toString());
}

void loop() {
  HTTPClient http;
  http.begin(BASE_URL);
  http.setTimeout(5000); // 5 second timeout
  
  int httpCode = http.GET();
  
  // Check if HTTP request failed due to WiFi issue
  if (httpCode == HTTPC_ERROR_CONNECTION_REFUSED || 
      httpCode == HTTPC_ERROR_CONNECTION_LOST || 
      httpCode <= 0) {
    
    // Only now check WiFi status
    if (WiFi.status() != WL_CONNECTED) {
      reconnectWiFi();
    }
  } 
  else if (httpCode > 0) {
    String payload = http.getString();
    
    // Parse JSON response
    StaticJsonDocument<2048> doc;
    DeserializationError error = deserializeJson(doc, payload);
    
    if (!error) {
      // Clear active pins tracking
      activePinCount = 0;
      
      // Loop through all pins in Firebase
      JsonObject pins = doc.as<JsonObject>();
      for (JsonPair kv : pins) {
        int pin = atoi(kv.key().c_str());
        JsonObject device = kv.value().as<JsonObject>();
        
        if (device.containsKey("status")) {
          int status = device["status"];
          String name = device.containsKey("name") ? device["name"].as<String>() : "Unknown";
          
          // Initialize pin if not already done
          if (!isPinActive(pin)) {
            pinMode(pin, OUTPUT);
            activePins[activePinCount++] = pin;
            Serial.printf("Initialized GPIO %d (%s)\n", pin, name.c_str());
          }
          
          // Set pin state
          digitalWrite(pin, status);
          Serial.printf("GPIO %d (%s): %s\n", pin, name.c_str(), status ? "ON" : "OFF");
        }
      }
    } else {
      Serial.println("JSON Parse Error: " + String(error.c_str()));
    }
  }
  
  http.end();
  delay(500); // Check every 500ms
}

// Check if pin is already initialized
bool isPinActive(int pin) {
  for (int i = 0; i < activePinCount; i++) {
    if (activePins[i] == pin) return true;
  }
  return false;
}
