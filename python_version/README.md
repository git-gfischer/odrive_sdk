# odrive_sdk python version 



## Configuration Backup
You can use odrivetool to back up and restore device configurations or transfer the configuration of one ODrive to another one. <\br>
We provide the default odrive configuration json file in the ```config``` folder in case you need to reset your board.

To save the configuration to a file on the PC, run
```
odrivetool backup-config <PATH_TO_CONFIG>.json
```

To restore the configuration form such a file, run
```
odrivetool restore-config <PATH_TO_CONFIG>.json
```
