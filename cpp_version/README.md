# Odrive_sdk C++ version
This is the C++ version from odrive sdk. Since there is no oficial C++ implementation, this project uses Python/C api to call the python version methods. Just a remainder for each controller selected, there is a specific actuation function that must be called.  

## Build
To build the project, run the commands:
```
mkdir build 
cd build
cmake ..
make
```

## Run Speed test
To run an example using speed controller to drive a motor with constant 150 rpm, exceute the following commands.
```
cd build 
./odrive_speed
```