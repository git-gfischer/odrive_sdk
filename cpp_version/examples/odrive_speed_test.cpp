//===============================
//Title: odrive test
//Date: 11/9/2022
//Author: Fischer
//Usage: ./odrive_speed_test
//===============================

#include "odrive_sdk.h"
#include <iostream>
#include <string>
#include <math.h>

#define CONFIG "../config/config.yaml"

int main()
{
    std::cout<<"Starting odrive test \n";
    Odrive_SDK *odrv;
    odrv = new Odrive_SDK(CONFIG);

    //setup
    std::string mode = "pos";
    int axis = 0;
    bool calibration = true;
    float reduction = 17;
    std::string version = "0.5.4";
    int cpr = 8192;
    int KV = 150;
    std::string serial = "207C378A3548";

    odrv->odrv_setup(mode,calibration,axis,reduction,cpr,KV,version,serial);
    
    double speed = 15.71; //rad/s  (150 rpm)
    double pos = 5*(2*M_PI); //rad
    //odrv->odrv_actionP(pos,speed);

    //print position
    //double enc_pos = odrv->odrv_get_encoder_pos();
    double enc_vel = odrv->odrv_get_encoder_vel();
    std::cout<<"pos "<<enc_vel<<"\n";

    std::cout<<"done \n";
    return 0;
}