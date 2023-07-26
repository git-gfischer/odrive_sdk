from odrive_sdk import Odrive_ctrl
import time
import math

def main():
    print("Testing odrive...")

    odrv = Odrive_ctrl()
    # Testing speed controller
    odrv.setup(mode="speed",reduction = 17 ,version="0.5.4", serial = "207C378A3548",axis=1)
    #odrv.set_dc_max_negative_current(-20.0)
    #odrv.set_max_regen_current(20.0)
    time.sleep(0.1)
   
    speed= 5.0 # rad/s 
    pos = 16*3.14
    print(f"pos {pos}")
    while(True):
        odrv.actionV(speed)
        p = odrv.get_encoder_position()
        print(f"res {p}")
        print(f"vbus {odrv.get_dbus_voltage()}")
        #odrv.actionV(speed)

    # Keep the code running 
    while (True): pass
    print("done")
#===============================================
if __name__=="__main__": main()
