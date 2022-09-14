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
    std::string python_path = "PYTHONPATH=" + pwd + "../python_version";
    std::cout<<python_path<<std::endl;
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
void Odrive_SDK::odrv_setup(std::string mode)
{
    PyObject *pargs = Py_BuildValue("(s)",mode);
    PyObject *pValue = PyEval_CallObject(this->odrv_setup_obj,pargs);
    if(!py_check(pValue)) {std::cerr<<"Error:actionP did not excecute \n";}
}
//=========================================================
void Odrive_SDK::odrv_actionP(float pos, float speed=150.0)
{
    PyObject *pargs = Py_BuildValue("(ff)",pos,speed);
    PyObject *pValue = PyEval_CallObject(this->odrv_actionP_obj,pargs);
    if(!py_check(pValue)) {std::cerr<<"Error:actionP did not excecute \n";}
}
//=========================================================
void Odrive_SDK::odrv_actionV(float speed)
{
    PyObject *pargs = Py_BuildValue("(f)",speed);
    PyObject *pValue = PyEval_CallObject(this->odrv_actionV_obj,pargs);
    if(!py_check(pValue)) {std::cerr<<"Error:actionV did not excecute \n";}
}
//=========================================================
void Odrive_SDK::odrv_actionT(float torque)
{
    PyObject *pargs = Py_BuildValue("(f)",torque);
    PyObject *pValue = PyEval_CallObject(this->odrv_actionT_obj,pargs);
    if(!py_check(pValue)) {std::cerr<<"Error:actionT did not excecute \n";}
}