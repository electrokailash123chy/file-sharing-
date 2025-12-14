#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "Engineer boys";
const char* password = "khwop@9800";
const char* serverURL = "http://192.168.18.139:5000/data";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected");
}

void loop() {
  float temperature = random(200, 350) / 10.0; // 20.0 – 35.0 °C
  float humidity = random(400, 800) / 10.0;    // 40 – 80 %

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");

    String payload = "{";
    payload += "\"temperature\":" + String(temperature) + ",";
    payload += "\"humidity\":" + String(humidity);
    payload += "}";

    http.POST(payload);
    http.end();
  }

  delay(5000); // send every 5 sec
}
