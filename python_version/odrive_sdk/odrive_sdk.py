import numpy as np
import sys,tty,termios,time
import math 

import signal
from odrive_v53 import Odrive_v53
from odrive_v54 import Odrive_v54
from odrivepro import Odrive_pro


# references links
#https://docs.odriverobotics.com/v/latest/manual/overview.html
#https://docs.odriverobotics.com/v/latest/fibre_types/com_odriverobotics_ODrive.html
#https://docs.odriverobotics.com/v/latest/guides/odrivetool-setup.html
#https://docs.odriverobotics.com/v/latest/manual/control.html#control-modes


class Odrive_ctrl:
	def __init__(self,mode="pos",calibration=True,axis=0,reduction=1,cpr=8192,KV=150,version="0.6.8", serial = " "):
		self.original_sigint = signal.getsignal(signal.SIGINT)
		signal.signal(signal.SIGINT, self.exit_gracefully)

		version = int(version.replace(".",""))
		if(version==53):
			self.odrv = Odrive_v53()
			self.odrv.setup(mode, calibration, axis, reduction, cpr, KV, serial)
		elif(version==54):
			self.odrv = Odrive_v54() 
			self.odrv.setup(mode, calibration, axis, reduction, cpr, KV, serial)
		elif (version>= 60):
			self.odrv = Odrive_pro()
			self.odrv.setup(mode, calibration, axis, reduction, cpr, KV, serial)

	#----------------------------------------------------------
	def exit_gracefully(self,signum, frame):
		signal.signal(signal.SIGINT, self.original_sigint)
		try:
			if self.mode=="speed":
				self.odrv.speed_controller(0)
			elif self.mode=="torque":
				self.odrv.torque_controller(0)
			sys.exit(1)
		except KeyboardInterrupt:
			print("Quit")
			sys.exit(1)

		signal.signal(signal.SIGINT, self.exit_gracefully)
	#----------------------------------------------------------
	# def setup_cpp(self,mode,calibration,axis,reduction,cpr,KV,version,serial):
	# 	print("setup_cpp")
	# 	motor = odrive.find_any(serial_number = serial)
	# 	self.odrv = motor
	# 	self.mode=mode
	# 	self.reduction=reduction
	# 	self.cpr=cpr
	# 	self.version = version
	# 	self.KV=KV #RPM/V

	# 	if(serial == " "):
	# 		print("Error: Please input odrive serial string, check under odrivetool command")
	# 		return 

	# 	if(axis==0):   self.m = motor.axis0
	# 	elif(axis==1): self.m = motor.axis1

	# 	self.m.motor.config.current_lim = self.current_max

	# 	self.m.controller.config.vel_limit = self.vel_max

	# 	self.m.motor.config.motor_type = MOTOR_TYPE_HIGH_CURRENT

	# 	if(calibration):
	# 		print("Calibrating...")
	# 		self.m.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
	# 		time.sleep(1)
	# 	while self.m.current_state != AXIS_STATE_IDLE:
	# 		time.sleep(0.1)
	# 	print("done calibration")

	
	# 	if(mode=="speed"):
	# 		print("Speed Controller Selected")
	# 		self.m.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
	# 		self.m.controller.config.vel_ramp_rate = 0.5 
	# 	elif(mode=="torque"):
	# 		print("Torque Controller Selected")
	# 		if(self.version == "0.5.3"):
	# 			#self.m.motor.config.torque_constant = 8.23 / self.KV
	# 			self.m.controller.config.control_mode= CONTROL_MODE_TORQUE_CONTROL
	# 		elif(self.version == "0.5.4"):
	# 			#self.m.controller.config.control_mode= ControlMode.TORQUE_CONTROL
	# 			self.m.motor.config.torque_constant = 8.23 / self.KV
	# 			self.m.controller.config.control_mode= CONTROL_MODE_TORQUE_CONTROL
	# 	elif(mode=="pos"):
	# 		print("Position Controller Selected")
	# 		if(self.version=="0.5.4"):
	# 			self.m.controller.config.input_filter_bandwidth = 2.0
	# 			self.m.controller.config.input_mode = INPUT_MODE_POS_FILTER
	# 	else:
	# 		print("Invalid Mode")
	# 		print("Avalable Modes are : pos, speed, torque")
		
	# 	self.m.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL    
	# 		#t0 = time.monotonic()
	# 		#torque = abs(motor.axis0.motor.current_control.Iq_measured)
	# 		#print('odrive setup was sucessful')
	#----------------------------------------------------------
	#--------------------------------------------------------------
	def pos_controller(self,pos,vel=150): # position control	   
		self.odrv.pos_controller(pos,vel)		
	#--------------------------------------------------------------
	def speed_controller(self,vel): # velocity control
		self.odrv.speed_controller(vel)
	#--------------------------------------------------------------
	def torque_controller(self,Torque): #Torque control
		self.odrv.torque_controller(Torque)
	#--------------------------------------------------------------
	def set_dc_max_negative_current(self,current=-15.0):
		self.odrv.set_dc_max_negative_current(current)
	#--------------------------------------------------------------
	def set_max_regen_current(self,current=10.0):
		self.odrv.set_max_regen_current(current)
	#--------------------------------------------------------------
	def set_current_max_limit(self,curr:int):
		self.odrv.set_current_max_limit(curr)
	#--------------------------------------------------------------
	def set_speed_max_limit(self,vel:int):
		self.odrv.set_speed_max_limit(vel)
	#-------------------------------------------------------------
	def set_motor_pole_pair(self,poles:int):
		self.odrv.set_motor_pole_pair(poles)
	#--------------------------------------------------------------
	def set_thermistor(self,state:bool):
		self.odrv.set_thermistor(state)
	#----------------------------------------------------------------
	def get_dbus_voltage(self):
		return self.odrv.get_vbus_voltage()
	