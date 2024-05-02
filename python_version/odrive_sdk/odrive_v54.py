import odrive
from odrive.enums import *
import numpy as np
import sys,tty,termios,time
import math 
from odrive.utils import *

import signal

# references links
#https://docs.odriverobotics.com/v/latest/manual/overview.html
#https://docs.odriverobotics.com/v/latest/fibre_types/com_odriverobotics_ODrive.html
#https://docs.odriverobotics.com/v/latest/guides/odrivetool-setup.html
#https://docs.odriverobotics.com/v/latest/manual/control.html#control-modes

#==========================================================
#->By Odrive 0.5.4
#-->pos in turn
#-->vel in turn/s
#-->ac in turn/s²
#-->Torque in Nm
#==================================================

class Odrive_v54:
	def __init__(self):
		#self.KV_rad=28.27 #rad/Vs
		self.vel_max=25000  # turn/s
		self.current_max = 180 # Ampers
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
    #         #self.m.controller.config.control_mode= ControlMode.TORQUE_CONTROL
    #         self.m.motor.config.torque_constant = 8.23 / self.KV
    #         self.m.controller.config.control_mode= CONTROL_MODE_TORQUE_CONTROL
	# 	elif(mode=="pos"):
	# 		print("Position Controller Selected")
    #         self.m.controller.config.input_filter_bandwidth = 2.0
    #         self.m.controller.config.input_mode = INPUT_MODE_POS_FILTER
	# 	else:
	# 		print("Invalid Mode")
	# 		print("Avalable Modes are : pos, speed, torque")
		
	# 	self.m.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL    
	# 		#t0 = time.monotonic()
	# 		#torque = abs(motor.axis0.motor.current_control.Iq_measured)
	# 		#print('odrive setup was sucessful')
	#----------------------------------------------------------
	def setup(self,mode="pos",calibration=True,axis=0,reduction=1,cpr=8192,KV=150, serial = " "):
		self.motor = odrive.find_any(serial_number = serial)
		self.mode=mode
		self.reduction=reduction
		self.cpr=cpr
		self.KV=KV #RPM/V


		if(serial==" "):
			print("Error: Please input odrive serial string, check under odrivetool command")
			return 

		if(axis==0):   self.m = motor.axis0
		elif(axis==1): self.m = motor.axis1

		self.m.motor.config.current_lim = self.current_max

		self.m.controller.config.vel_limit = self.vel_max
		
	
		self.m.motor.config.motor_type = MOTOR_TYPE_HIGH_CURRENT

		if(calibration):
			print("Calibrating...")
			self.m.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
			time.sleep(1)
		while self.m.current_state != AXIS_STATE_IDLE:
			time.sleep(0.1)
		print("done calibration")

		if(mode=="speed"):
			print("Speed Controller Selected")
            self.m.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
            self.m.controller.config.vel_ramp_rate = 0.5 
		elif(mode=="torque"):
			print("Torque Controller Selected")
            #self.m.controller.config.control_mode= ControlMode.TORQUE_CONTROL
            self.m.motor.config.torque_constant = 8.23 / self.KV
            self.m.controller.config.control_mode= CONTROL_MODE_TORQUE_CONTROL
		elif(mode=="pos"):
			print("Position Controller Selected")
            self.m.controller.config.input_filter_bandwidth = 2.0
            self.m.controller.config.input_mode = INPUT_MODE_POS_FILTER
		else:
			print("Invalid Mode")
			print("Avalable Modes are : pos, speed, torque")
		
		
		self.m.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL    

			#t0 = time.monotonic()
			#torque = abs(motor.axis0.motor.current_control.Iq_measured)
			#print('odrive setup was successful')
	#--------------------------------------------------------------
	def pos_controller(self,pos,vel=150): # position control	   
		# [Input]: pos in rad
		#          vel in Rad/s
		if(self.mode=="pos"):
			pos_enc=float(pos*self.reduction/(2*3.14)) # rad to turn conversion 
			print(pos_enc)
			speed_enc=float((vel*self.reduction)/(2*3.14)) # rad/s to turn/s conversion
			print(speed_enc)
			if speed_enc>self.vel_max: speed_enc=self.vel_max
	 	   
			#self.m.controller.config.vel_limit = speed_enc
			self.m.controller.input_pos = pos_enc

			self.dump_error()
		else:
			print("Odrive Error: Position control not configured")
		
	#--------------------------------------------------------------
	def speed_controller(self,vel): # velocity control
		if(self.mode=="speed"):
			#[Input]: vel in Rad/s
			speed_conv = (vel*self.reduction)/(2*3.14) # rad/s to turn/s conversion
			# acceleration ramp
			self.m.controller.input_vel = speed_conv # turn/s 

			self.dump_error()
		else:
			print("Odrive Error: Velocity control not configured")
	#--------------------------------------------------------------
	def actionT(self,Torque): #Torque control
		#[input]: Torque in Nm
		if(self.mode=="torque"):
			#I=Torque*self.KV_rad/(8.27*self.reduction)
			I=Torque
			#print(str(I)+' A')
			self.m.controller.input_torque=I
		else:
			print("Odrive Error: Torque control not configured")
	#--------------------------------------------------------------
	def set_dc_max_negative_current(self,current=-15.0):
		self.motor.config.dc_max_negative_current = current
	#--------------------------------------------------------------
	def set_max_regen_current(self,current=10.0):
		self.motor.config.max_regen_current = current
	#--------------------------------------------------------------
	def set_current_max_limit(self,curr:int):
		self.m.motor.config.current_lim = curr
	#--------------------------------------------------------------
	def set_speed_max_limit(self,vel:int):
		self.m.controller.config.vel_limit = vel
	#-------------------------------------------------------------
	def set_motor_pole_pair(self,poles:int):
		self.m.config.motor.pole_pairs=poles
	#--------------------------------------------------------------
	def get_encoder_position(self,unit="rad"):
		pos = float(self.m.encoder.pos_estimate)
		if(unit=="rad"):      pos = (pos*2*math.pi)/self.reduction
		elif(unit=="degree"): pos = (pos*360)/self.reduction
		else: return None
		return pos 
	#--------------------------------------------------------------
	def get_encoder_speed(self,unit="rad/s"):
		speed = float(self.m.encoder.vel_estimate)
		if(unit=="rad/s"):   speed = (speed*2*math.pi)/self.reduction
		elif(unit=="rpm"):   speed = (speed*60)/self.reduction
		elif(unit=="hertz"): speed = speed / self.reduction
		else: return None
		return speed 
	#----------------------------------------------------------------
	def dump_error(self):
		dump_errors(self.motor)
	#----------------------------------------------------------------
	def get_dbus_voltage(self):
		return self.motor.vbus_voltage
	
