#=======================================================
# Example for OdrivePro board
# Usage: python3 pos_controller.py --setpoint [float] --serial [str][optional] --reduction [float][optional] --axis [int][optional] --cpr [int][optional] --KV [int][optional]
#=======================================================

import sys
import argparse
sys.path.insert(0,"..")
from odrive_sdk.odrive_sdk import odrive_ctrl

def main():
    # parse command line
    parser = argparse.ArgumentParser(description='''test position controller from odrive board  ''')
    parser.add_argument('--version', type=str, default = "0.6.8", choices= ["0.5.3","0.5.4","0.6.8"], help='Odrive version')
    parser.add_argument('--KV', type=int, default=150, help='motor KV')
    parser.add_argument('--reduction', type=int, default=1, help='motor gear box reduction')
    parser.add_argument('--axis', type=int, default=0, help='motor axis')
    parser.add_argument('--Nocalibration',action = "store_false", help='Dont calibrate the motor')
    parser.add_argument('--Enc_calibration',action = "store_true", help='calibrate the encoder')
    parser.add_argument('--cpr', type=int, default=8192, help='encoder counts per revolutions')
    parser.add_argument('--serial', type=str, default="", help='odrive serial number')
    parser.add_argument('--setpoint', type=float, required=True, help='position setpoint in rad')
    args = parser.parse_args()

    print("test odrive postion control")

    odrv = odrive_ctrl(axis= args.axis, version = args.version, serial = args.serial)
    odrv.setup (mode = "pos", 
                calibration =args.Nocalibration,
                enc_calibration = args.Enc_calibration,
                reduction = args.reduction,
                cpr = args.cpr,
                KV = args.KV)
    odrv.pos_controller(args.setpoint)

    print("done")
#==============================================================
if __name__=="__main__": main()

    def setup(self,mode="pos",calibration=True,axis=0,reduction=1,cpr=8192,KV=150, calibration_current=5, serial = " "):