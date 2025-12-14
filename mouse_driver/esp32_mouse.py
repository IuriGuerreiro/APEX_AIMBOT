import serial
import time

# ==================================================================================
# CONFIGURATION
# Check your Device Manager to find the correct COM port for your ESP32
COM_PORT = 'COM6'  # <--- CHANGE THIS to your actual COM port (e.g., 'COM3', 'COM4')
BAUD_RATE = 115200 # Ensure this matches your ESP32's Serial.begin(115200)
# ==================================================================================

try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=0.01)
    print(f"[INFO] Serial port {COM_PORT} opened successfully.")
except Exception as e:
    print(f"[ERROR] Could not open serial port {COM_PORT}: {e}")
    print("Make sure the device is connected and you have the correct COM port.")
    ser = None

def mouse_xy(x, y):
    """
    Sends relative x, y coordinates to the ESP32 via Serial.
    Format: "x,y\n" (e.g., "10,-5\n")
    """
    if ser and ser.is_open:
        try:
            # Format the string. Adjust this if your ESP32 expects a different format.
            # Common formats: "x,y\n" or "MOVE:x,y\n"
            command = f"{int(x)},{int(y)}\n"
            
            # Send the data
            ser.write(command.encode('utf-8'))
            
            # Optional: Print what we sent for debugging
            # print(f"[DEBUG] Sent Serial: {command.strip()}")
            
        except Exception as e:
            print(f"[ERROR] Failed to write to serial: {e}")

def mouse_down(key=1):
    # Implement click logic if your ESP32 supports it
    pass

def mouse_up(key=1):
    # Implement release logic if your ESP32 supports it
    pass

def mouse_close():
    if ser and ser.is_open:
        ser.close()
