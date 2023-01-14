from odrive_sdk import Odrive_ctrl
import time
import math

def main():
    print("Testing odrive...")

    odrv = Odrive_ctrl()

    # Testing speed controller
    odrv.setup(mode="pos",reduction = 17 ,version="0.5.4", serial = "207C378A3548")
    odrv.set_dc_max_negative_current(-10.0)
    time.sleep(0.1)
   
    speed= 10.0 # rad/s 
    pos = 17.0
    print(f"pos {pos}")
    p = odrv.get_encoder_position()
    print(f"res {p}")
    #odrv.actionP(pos,speed)
    #odrv.actionV(speed)

    # Keep the code running 
    while (True): pass
    print("done")
#===============================================
if __name__=="__main__": main()
