//===============================
//Title: odrive test
//Date: 11/9/2022
//Author: Fischer
//Usage: ./odrive_speed_test
//===============================

#include "odrive_sdk.h"
#include <iostream>
#include <string>

#define CONFIG "config/config.yaml"

int main()
{
    std::cout<<"Starting odrive test \n";
    Odrive_SDK *odrv;
    odrv = new Odrive_SDK(CONFIG);

    //setup
    odrv->odrv_setup("speed");

    float speed = 150.0; //rpm
    odrv->odrv_actionV(speed);

    std::cout<<"done \n";
    return 0;
}