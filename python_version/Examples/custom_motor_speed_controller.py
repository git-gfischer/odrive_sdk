#=======================================================
# Usage: python3 custom_motor_speed_controller.py --setpoint [float] --serial [str][optional] --reduction [float][optional] --axis [int][optional] --cpr [int][optional] --KV [int][optional]
#=======================================================

import sys
import argparse
sys.path.insert(0,"..")
from odrive_sdk import Odrive_ctrl

def main():
    # parse command line
    parser = argparse.ArgumentParser(description='''test position controller from odrive board in a custom motor/encoder setup  ''')
    parser.add_argument('--version', type=str, default = "0.6.8", choices= ["0.5.3","0.5.4","0.6.8"], help='Odrive version')
    parser.add_argument('--KV', type=int, default=300, help='custom motor KV')
    parser.add_argument('--reduction', type=int, default=1, help='motor gear box reduction')
    parser.add_argument('--axis', type=int, default=0, help='motor axis')
    parser.add_argument('--Nocalibration',action_store = "false", help='Dont calibrate the motor')
    parser.add_argument('--cpr', type=int, default=20000, help='encoder counts per revolutions')
    parser.add_argument('--serial', type=str, default="", help='odrive serial number')
    parser.add_argument('--setpoint', type=float, required=True, help='position setpoint in rad')
    args = parser.parse_args()

    print("test odrive postion control")

    # setup for custom motor
    odrv = odrive_sdk(version = args.version, serial = args.serial)
    
    #configure custom motor 
    odrv.set_calibration_current(10.0)
    odrv.set_motor_pole_pair(12)
    odrv.set_vel_gain(0.02)
    odrv.set_vel_integrator_gain(0)
    odrv.set_pos_gain(50)
    odrv.set_dc_max_negative_current(-15)
    odrv.set_dc_max_positive_current(30) 
    odrv.set_encoder_index_search(True)

    odrv.setup(mode = "speed",
               calibration = args.Nocalibration,
               axis = args.axis,
               reduction = args.reduction,
               cpr = args.cpr,
               KV = args.KV)

    odrv.speed_controller(args.setpoint)

    print("done")
#==============================================================
if __name__=="__main__": main()