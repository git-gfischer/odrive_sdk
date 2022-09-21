#pragma once

#include <Python.h>
#include <string>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <iostream>
#include <vector>
#include <cstdio>
#include <yaml-cpp/yaml.h>

//#include <boost/thread.hpp>
//#include "include/Conversion.h"

class Odrive_SDK
{
    public:
        Odrive_SDK(std::string config_file);
        ~Odrive_SDK();

        void odrv_actionP(double pos, double speed);
        void odrv_actionV(double speed);
        void odrv_actionT(double torque);
        void odrv_setup(std::string mode,bool calibration,int axis,float reduction,int cpr,int KV,std::string version);

    private:
        PyObject *odrv_module;
        PyObject *odrv_class;
        PyObject *odrv_instance;
        PyObject *odrv_setup_obj;
        PyObject *odrv_actionP_obj;
        PyObject *odrv_actionV_obj;
        PyObject *odrv_actionT_obj;

        std::string odrv_module_path;
        std::string odrv_class_path;
    
        void setup_env();
        void py_error(std::string msg);
        bool py_check(PyObject *in);
        void PrintPyObject(PyObject *obj);
        void Import_Settings(std::string config_file);

        
};