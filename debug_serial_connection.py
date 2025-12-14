import serial
import time

# ==================================================================================
# CONFIGURATION
COM_PORT = 'COM6'  # <--- CHANGE THIS to your actual COM port
BAUD_RATE = 115200
# ==================================================================================

def debug_serial():
    print(f"Attempting to connect to {COM_PORT} at {BAUD_RATE} baud...")
    
    try:
        ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
        print("Connection successful!")
        
        # Give the connection a moment to settle
        time.sleep(2)
        
        print("Sending test data: '10,10\\n'")
        ser.write(b"10,10\n")
        
        print("Listening for response from ESP32 (if any)...")
        start_time = time.time()
        while time.time() - start_time < 3:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                print(f"[ESP32 RESPONSE]: {line}")
            time.sleep(0.1)
            
        print("Test finished.")
        ser.close()
        
    except serial.SerialException as e:
        print(f"Serial Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Ensure pyserial is installed
    try:
        import serial
        debug_serial()
    except ImportError:
        print("Error: 'pyserial' library is missing.")
        print("Please run: pip install pyserial")
