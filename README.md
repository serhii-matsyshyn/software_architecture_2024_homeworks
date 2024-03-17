# Software architecture 2024 homeworks

Author: Serhii Matsyshyn (https://github.com/serhii-matsyshyn) <br>

## Protocols / research papers
See protocols and research papers attached at CMS homework assignment.  
Homeworks are saved in separate branches in this repository.

## Additional information
Homeworks are implemented in Python programming language. Use requirements.txt to install dependencies.

## Useful commands
Below, some useful commands can be found.  
You should have hazelcast on Windows in `hazelcast\hazelcast-5.3.6\` folder.  


```shell
./hz-start.bat
\management-center\bin> ./start.bat
```

### To run homework 4

In `logging_controller.py` set `hazelcast_path` to Hazelcast bin folder (Hazelcast for Windows). That folder should contain `hz-start.bat`.  

```shell
cd logging_service
python logging_controller.py -p 8003
python logging_controller.py -p 8004
python logging_controller.py -p 8005
```

```shell
cd messages_service
python messages_controller.py -p 8001
python messages_controller.py -p 8002
```

```shell
cd facade_service
python facade_controller.py
```

Use Requests.http to send requests.