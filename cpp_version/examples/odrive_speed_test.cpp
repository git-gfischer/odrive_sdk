//===============================
//Title: odrive test
//Date: 11/9/2022
//Author: Fischer
//Usage: ./odrive_speed_test
//===============================

#include "odrive_sdk.h"
#include <iostream>
#include <string>

#define CONFIG "../config/config.yaml"

int main()
{
    std::cout<<"Starting odrive test \n";
    Odrive_SDK *odrv;
    odrv = new Odrive_SDK(CONFIG);

    //setup
    std::string mode = "torque";
    int axis = 0;
    bool calibration = true;
    float reduction = 1.0;
    std::string version = "0.5.3";
    int cpr = 8192;
    int KV = 150;
    odrv->odrv_setup(mode,calibration,axis,reduction,cpr,KV,version);
    
    double speed = 150.0; //rpm
    double pos = 720; //rpm
    odrv->odrv_actionT(0.1);

    std::cout<<"done \n";
    return 0;
}