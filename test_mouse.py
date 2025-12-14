import time
from mouse_driver.MouseMove import mouse_move

def test_movement():
    print("Starting mouse movement test in 3 seconds...")
    time.sleep(3)
    
    print("Moving mouse...")
    # Move in a small square
    for _ in range(4):
        print("Moving Right")
        mouse_move(50, 0)
        time.sleep(0.5)
        
        print("Moving Down")
        mouse_move(0, 50)
        time.sleep(0.5)
        
        print("Moving Left")
        mouse_move(-50, 0)
        time.sleep(0.5)
        
        print("Moving Up")
        mouse_move(0, -50)
        time.sleep(0.5)
        
    print("Test complete.")

if __name__ == "__main__":
    test_movement()
