from odrive_sdk import Odrive_ctrl
import time

def main():
    print("Testing odrive...")

    odrv = Odrive_ctrl()

    # Testing speed controller
    print("calibrating...")
    odrv.setup(mode="speed")
    time.sleep(0.1)
    print("done calibration")

    speed= 150 # rpm
    odrv.actionV(speed)

    # Keep the code running 
    while (True): pass
    print("done")
#===============================================
if __name__=="__main__": main()
