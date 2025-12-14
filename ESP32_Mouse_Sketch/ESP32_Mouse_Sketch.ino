/**
 * ESP32 BLE Mouse with Serial Control and Smoothing
 * 
 * Requirements:
 * 1. Install ESP32 board support in Arduino IDE.
 * 2. Install "ESP32 BLE Mouse" library by T-vK (https://github.com/T-vK/ESP32-BLE-Mouse).
 * 
 * Usage:
 * - Upload to ESP32.
 * - Pair ESP32 with PC via Bluetooth.
 * - Send "x,y\n" via Serial (115200 baud) to move mouse.
 */

#include <BleMouse.h>

// Create BleMouse instance
// You can change the name "ESP32 Mouse" to whatever you want to appear in Bluetooth settings
BleMouse bleMouse("ESP32 Aim Assist", "Espressif", 100);

void setup() {
  Serial.begin(115200);
  Serial.println("Starting BLE Mouse...");
  bleMouse.begin();
}

// Function to move mouse smoothly by breaking large moves into smaller steps
void smoothMove(int targetX, int targetY) {
  // CONFIGURATION
  // Higher steps = smoother but slower
  // Lower delay = faster
  int steps = 10; 
  int stepDelay = 2; // milliseconds

  // If movement is very small, don't smooth it, just move instantly
  // This prevents small adjustments from feeling laggy
  if (abs(targetX) < 5 && abs(targetY) < 5) {
    bleMouse.move(targetX, targetY);
    return;
  }

  float stepX = (float)targetX / steps;
  float stepY = (float)targetY / steps;
  
  float accumulatedX = 0;
  float accumulatedY = 0;
  
  for (int i = 0; i < steps; i++) {
    accumulatedX += stepX;
    accumulatedY += stepY;
    
    // We can only move integer pixels
    int moveX = (int)accumulatedX;
    int moveY = (int)accumulatedY;
    
    if (moveX != 0 || moveY != 0) {
      bleMouse.move(moveX, moveY);
      accumulatedX -= moveX;
      accumulatedY -= moveY;
    }
    
    delay(stepDelay);
  }
  
  // Ensure we reach the exact target by moving any remaining float remainder
  // (Though usually accumulatedX/Y will be < 1 here, but good for correctness)
  if ((int)round(accumulatedX) != 0 || (int)round(accumulatedY) != 0) {
     bleMouse.move((int)round(accumulatedX), (int)round(accumulatedY));
  }
}

void loop() {
  if (Serial.available() > 0) {
    // Read incoming data until newline
    String data = Serial.readStringUntil('\n');
    data.trim(); // Remove any whitespace/newlines
    
    if (data.length() > 0) {
      int commaIndex = data.indexOf(',');
      
      if (commaIndex > 0) {
        // Parse X and Y
        String xStr = data.substring(0, commaIndex);
        String yStr = data.substring(commaIndex + 1);
        
        int x = xStr.toInt();
        int y = yStr.toInt();
        
        if (bleMouse.isConnected()) {
          // Apply smoothing
          smoothMove(x, y);
          
          // Optional: Send confirmation back
          // Serial.println("OK");
        } else {
          Serial.println("BLE not connected");
        }
      }
    }
  }
}
