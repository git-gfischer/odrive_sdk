import odrive
from odrive.enums import *
import numpy as np
import sys,tty,termios,time
import math 

import signal

#==========================================================
#->By Odrive 0.5.4
#-->pos in turn
#-->vel in turn/s
#-->ac in turn/s²
#-->Torque in Nm
#==================================================

class Odrive_ctrl:
	def __init__(self):
		self.original_sigint = signal.getsignal(signal.SIGINT)
		signal.signal(signal.SIGINT, self.exit_gracefully)
		self.KV_rad=28.27 #rad/Vs
		self.vel_max=250000
	#----------------------------------------------------------
	def exit_gracefully(self,signum, frame):
		signal.signal(signal.SIGINT, self.original_sigint)
		try:
			if self.mode=="speed":
				self.actionV(0)
			elif self.mode=="torque":
				self.actionT(0)
			sys.exit(1)
		except KeyboardInterrupt:
			print("Quit")
			sys.exit(1)

		signal.signal(signal.SIGINT, self.exit_gracefully)
	#----------------------------------------------------------
	def setup_cpp(self,mode,calibration,axis,reduction,cpr,KV,version):
		print("setup_cpp")
		motor = odrive.find_any()
		self.mode=mode
		self.reduction=reduction
		self.cpr=cpr
		self.version = version
		self.KV=KV #RPM/V

		if(axis==0):   self.m = motor.axis0
		elif(axis==1): self.m = motor.axis1

		self.m.motor.config.current_lim = 60

		self.m.controller.config.vel_limit = 25000

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
			if(self.version == "0.5.3"):
				#self.m.motor.config.torque_constant = 8.23 / self.KV
				self.m.controller.config.control_mode= CONTROL_MODE_TORQUE_CONTROL
			elif(self.version == "0.5.4"):
				#self.m.controller.config.control_mode= ControlMode.TORQUE_CONTROL
				self.m.motor.config.torque_constant = 8.23 / self.KV
				self.m.controller.config.control_mode= CONTROL_MODE_TORQUE_CONTROL
		elif(mode=="pos"):
			print("Position Controller Selected")
			if(self.version=="0.5.4"):
				self.m.controller.config.input_filter_bandwidth = 2.0
				self.m.controller.config.input_mode = INPUT_MODE_POS_FILTER
		else:
			print("Invalid Mode")
			print("Avalable Modes are : pos, speed, torque")
		
		self.m.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL    
			#t0 = time.monotonic()
			#torque = abs(motor.axis0.motor.current_control.Iq_measured)
			#print('odrive setup was sucessful')
	#----------------------------------------------------------
	def setup(self,mode="pos",calibration=True,axis=0,reduction=1,cpr=8192,KV=150,version="0.5.4"):
		motor = odrive.find_any()
		self.mode=mode
		self.reduction=reduction
		self.cpr=cpr
		self.version = version
		self.KV=KV #RPM/V

		if(axis==0):   self.m = motor.axis0
		elif(axis==1): self.m = motor.axis1

		self.m.motor.config.current_lim = 60

		self.m.controller.config.vel_limit = 25000

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
			if(self.version == "0.5.3"):
				#self.m.motor.config.torque_constant = 8.23 / self.KV
				self.m.controller.config.control_mode= CONTROL_MODE_TORQUE_CONTROL
			elif(self.version == "0.5.4"):
				#self.m.controller.config.control_mode= ControlMode.TORQUE_CONTROL
				self.m.motor.config.torque_constant = 8.23 / self.KV
				self.m.controller.config.control_mode= CONTROL_MODE_TORQUE_CONTROL
		elif(mode=="pos"):
			print("Position Controller Selected")
			if(self.version=="0.5.4"):
				self.m.controller.config.input_filter_bandwidth = 2.0
				self.m.controller.config.input_mode = INPUT_MODE_POS_FILTER
		else:
			print("Invalid Mode")
			print("Avalable Modes are : pos, speed, torque")
		
		self.m.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL    
			#t0 = time.monotonic()
			#torque = abs(motor.axis0.motor.current_control.Iq_measured)
			#print('odrive setup was sucessful')
	#--------------------------------------------------------------
	def actionP(self,pos,vel=150): # position control	   
		# [Input]: pos in degree
		#          vel in RPM
		if(self.mode=="pos"):
			pos_enc=pos*self.cpr*self.reduction/360 #Input Angular #TODO: 
			speed_enc= (vel*self.cpr*self.reduction)/60 #Input RPM   #TODO:
			if speed_enc>self.vel_max: speed_enc=self.vel_max
	 	   
			self.m.controller.config.vel_limit = speed_enc

			if(self.version=="0.5.3"):
				self.m.controller.pos_setpoint = pos_enc
			elif(self.version =="0.5.4"):
				self.m.controller.input_pos = pos_enc
		else:
			print("Odrive Error: Position control not configured")
		
	#--------------------------------------------------------------
	def actionV(self,vel): # velocity control
		if(self.mode=="speed"):
			#[Input]: vel in RPM
			speed_conv = (self.cpr*vel*self.reduction)/60 
			# acceleration ramp

			if(self.version == "0.5.3"):
				self.m.controller.vel_setpoint= speed_conv  # turn/s
			elif(self.version=="0.5.4"):
				self.m.controller.input_vel = speed_conv # turn/s 
		else:
			print("Odrive Error: Velocity control not configured")
	#--------------------------------------------------------------
	def actionT(self,Torque): #Torque control
		#[input]: Torque in Nm
		if(self.mode=="torque"):
			#I=Torque*self.KV_rad/(8.27*self.reduction)
			I=Torque
			#print(str(I)+' A')
			
			if(self.version=="0.5.3"): #TODO: Not Working
				self.m.controller.current_setpoint=I
			elif(self.version == "0.5.4"):
				self.m.controller.input_torque=I
			
		else:
			print("Odrive Error: Torque control not configured")
