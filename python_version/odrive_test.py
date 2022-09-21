from odrive_sdk import Odrive_ctrl
import time

def main():
    print("Testing odrive...")

    odrv = Odrive_ctrl()

    # Testing speed controller
    odrv.setup(mode="torque",version="0.5.3")
    time.sleep(0.1)
   

    speed= 150 # rpm
    pos = 720
    torque = 0.5
    odrv.actionT(torque)

    # Keep the code running 
    while (True): pass
    print("done")
#===============================================
if __name__=="__main__": main()
