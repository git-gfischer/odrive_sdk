#include "odrive_sdk.h"

Odrive_SDK::Odrive_SDK(std::string config_path)
{
    std::cout<<"Importing Odrive settings... \n";
    setup_env();
    Import_Settings(config_path);

    Py_Initialize();
    std::cout<<odrv_module_path.c_str()<<std::endl;
    this->odrv_module = PyImport_ImportModule(odrv_module_path.c_str()); //config_path.c_str()
    if (!py_check(this->odrv_module)) // check load py_Name 
    {
        py_error("python error: Cannot load module");
        return;
    }
    
    this->odrv_class = PyObject_GetAttrString(this->odrv_module, odrv_class_path.c_str());
    if (!py_check(this->odrv_class)) // check load py_module 
    {
        py_error("python error: Cannot load class");
        return;
    }
    
    //Check if PyObject is callable
    if(this->odrv_class && PyCallable_Check(this->odrv_class))
    {
        

        this->odrv_instance = PyEval_CallObject(this->odrv_class,NULL); //call class __init__
        if (!py_check(this->odrv_instance)) // check load py_instance
        {
            py_error("python error: Cannot load class");
            return;
        }

        //load class methods
        this->odrv_setup_obj =  PyObject_GetAttrString(this->odrv_instance, (char*)"setup"); 
        if (!py_check(this->odrv_setup_obj)) // check load py_method
        {
            py_error("python error: Cannot load setup method");
            return;
        }

        this->odrv_actionP_obj =  PyObject_GetAttrString(this->odrv_instance, (char*)"actionP"); 
        if (!py_check(this->odrv_actionP_obj )) // check load py_method
        {
            py_error("python error: Cannot load actionP method");
            return;
        }

        this->odrv_actionV_obj =  PyObject_GetAttrString(this->odrv_instance, (char*)"actionV"); 
        if (!py_check(this->odrv_actionV_obj)) // check load py_method
        {
            py_error("python error: Cannot load actionV method");
            return;
        }

        this->odrv_actionT_obj =  PyObject_GetAttrString(this->odrv_instance, (char*)"actionT"); 
        if (!py_check(this->odrv_actionT_obj)) // check load py_method
        {
            py_error("python error: Cannot load actionT method");
            return;
        }

        this->odrv_encoder_pos_obj =  PyObject_GetAttrString(this->odrv_instance, (char*)"get_encoder_position"); 
        if (!py_check(this->odrv_encoder_pos_obj)) // check load py_method
        {
            py_error("python error: Cannot load get_encoder_position method");
            return;
        }

        this->odrv_encoder_vel_obj =  PyObject_GetAttrString(this->odrv_instance, (char*)"get_encoder_speed"); 
        if (!py_check(this->odrv_encoder_vel_obj)) // check load py_method
        {
            py_error("python error: Cannot load get_encoder_speed method");
            return;
        }

        std::cout<<"odrive Ready" <<std::endl;

    }
    else
    {
        py_error("python error: Module is not callable");
        return;
    }

}
//====================================
Odrive_SDK::~Odrive_SDK()
{
    delete this->odrv_module;
    delete this->odrv_class;
    delete this->odrv_instance;
    delete this->odrv_setup_obj;
    delete this->odrv_actionP_obj;
    delete this->odrv_actionV_obj;
    delete this->odrv_actionT_obj;
    delete this->odrv_encoder_pos_obj;
    delete  this->odrv_encoder_vel_obj;
    Py_Finalize();
}

//====================================
void Odrive_SDK::setup_env()
{
    //pwd get current folder
    char buff[FILENAME_MAX]; //create string buffer to hold path
    if(getcwd( buff, FILENAME_MAX ) ==NULL)
    {
        std::cerr<<"Error: cannot get current working folder \n";
        return;
    }
    std::string pwd(buff);
    pwd=pwd.erase(pwd.length()-5,pwd.length()); // erase "build" from path

    //setting automatic PYTHONPATH environment variable
    std::string python_path = "PYTHONPATH=" + pwd + "../python_version/";
    //std::cout<<python_path<<std::endl;
    char * py_path = new char[python_path.size() + 1];
    std::copy(python_path.begin(), python_path.end(), py_path);
    py_path[python_path.size()] = '\0'; // don't forget the terminating 0
    
    putenv(py_path);
}
//====================================
void Odrive_SDK::Import_Settings(std::string config_path)
{
    YAML::Node config = YAML::LoadFile(config_path);

    odrv_module_path = config["py_module"].as<std::string>();
    odrv_class_path = config["py_class"].as<std::string>();

}
//=========================================================
bool Odrive_SDK::py_check(PyObject *in)
{
    if (in == nullptr) {return false;}
    return true;
}
//==========================================================
void Odrive_SDK::py_error(std::string msg)
{
    PyErr_Print();
    std::cerr << msg << std::endl;
}
//=========================================================
void Odrive_SDK::PrintPyObject(PyObject *obj)
{
    PyObject* objectsRepresentation = PyObject_Repr(obj);
    const char* s = PyUnicode_AsUTF8(objectsRepresentation);
    std::cout<<s<<std::endl;
}
//=========================================================
void Odrive_SDK::odrv_setup(std::string mode,bool calibration,int axis,float reduction,int cpr,int KV,std::string version, std::string serial)
{
    PyObject *pargs = Py_BuildValue("(sbifiiss)",mode.c_str(),calibration,axis,reduction,cpr,KV,version.c_str(),serial.c_str());
    PyObject *pValue = PyEval_CallObject(this->odrv_setup_obj,pargs);
    if(!py_check(pargs)) {std::cerr<<"Error:setup args has an error \n"; return; }
    if(!py_check(pValue)) {std::cerr<<"Error:setup did not excecute \n"; return; }
}
//=========================================================
void Odrive_SDK::odrv_actionP(double pos, double speed)
{
    PyObject *pargs = Py_BuildValue("(dd)",pos,speed);
    PyObject *actionP_Value = PyEval_CallObject(this->odrv_actionP_obj,pargs);
    if(!py_check(pargs)) {std::cerr<<"Error:actionP args has an error \n";        return;} 
    if(!py_check(actionP_Value)) {std::cerr<<"Error:actionP did not excecute \n"; return;}
}
//=========================================================
void Odrive_SDK::odrv_actionV(double speed)
{
    PyObject *pargs = Py_BuildValue("(d)",speed);
    PyObject *actionV_Value = PyEval_CallObject(this->odrv_actionV_obj,pargs);
    if(!py_check(pargs)) {std::cerr<<"Error:actionV args has an error \n"; return;}
    if(!py_check(actionV_Value)) {std::cerr<<"Error:actionV did not excecute \n"; return;}
}
//=========================================================
void Odrive_SDK::odrv_actionT(double torque)
{
    PyObject *pargs = Py_BuildValue("(d)",torque);
    PyObject *actionT_Value = PyEval_CallObject(this->odrv_actionT_obj,pargs);
    if(!py_check(pargs)) {std::cerr<<"Error:actionT args has an error \n"; return;}
    if(!py_check(actionT_Value)) {std::cerr<<"Error:actionT did not excecute \n"; return;}
}
//=========================================================
double Odrive_SDK::odrv_get_encoder_pos()
{
    PyObject *encoder_pos_Value = PyEval_CallObject(this->odrv_encoder_pos_obj,NULL);

    if(!py_check(encoder_pos_Value)) 
    {
        std::cerr<<"Error:get_encoder_pos did not excecute \n"; 
        return std::numeric_limits<double>::quiet_NaN();
    }
    return PyFloat_AsDouble(encoder_pos_Value);
}
//=========================================================
double Odrive_SDK::odrv_get_encoder_vel()
{
    PyObject *encoder_vel_Value = PyEval_CallObject(this->odrv_encoder_vel_obj,NULL);
    if(!py_check(encoder_vel_Value)) 
    {
        std::cerr<<"Error:get_encoder_vel did not excecute \n"; 
        return std::numeric_limits<double>::quiet_NaN();
    }
    return PyFloat_AsDouble(encoder_vel_Value);
}