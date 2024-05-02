#=======================================================
# Usage: python3 speed_controller.py --setpoint [float] --serial [str][optional] --reduction [float][optional] --axis [int][optional] --cpr [int][optional] --KV [int][optional]
#=======================================================
import sys
import argparse
sys.path.insert(0,"..")
from odrive_sdk import Odrive_ctrl

def main():
    # parse command line
    parser = argparse.ArgumentParser(description='''test speed controller from odrive board  ''')
    parser.add_argument('--version', type=str, default = "0.6.8", choices= ["0.5.3","0.5.4","0.6.8"], help='Odrive version')
    parser.add_argument('--KV', type=int, default=150, help='motor KV')
    parser.add_argument('--reduction', type=int, default=1, help='motor gear box reduction')
    parser.add_argument('--axis', type=int, default=0, help='motor axis')
    parser.add_argument('--Nocalibration',action_store = "false", help='Dont calibrate the motor')
    parser.add_argument('--cpr', type=int, default=8192, help='encoder counts per revolutions')
    parser.add_argument('--serial', type=str, default="", help='odrive serial number')
    parser.add_argument('--setpoint', type=float, required=True, help='speed setpoint in rad/s')
    args = parser.parse_args()

    print("test odrive speed control")

    odrv = odrive_sdk("speed",args.Nocalibration,args.axis,args.reduction,args.cpr,args.KV,args.version,args.serial)
    odrv.speed_controller(args.setpoint)

    print("done")
#==============================================================
if __name__=="__main__": main()