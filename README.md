# autoBOF
# Nathan Gorman's automated buffer overflow project

autoBOF is a project that can search for and create traditional buffer overflow exploits given certain starting parameters. It is currently only capable of running in local laboratory environments on Linux, where a vulnerable service is managed by gdb debugger and the supplied python script. However, I believe with some modification it could without much difficulty be made functional on Windows devices as well, so long as a python script that interfaces with ImmunityDB is made to mirror my restart.py.

# Files:

restart.py - this is the script that manages the debugger. It mainly serves to restart the debugger at appropriate times and dump information about the program.

autoBOF.py - Where the magic happens. Currently fuzzes the service and overwrites the EIP. Takes one input variable, the maximum amount of data that will be sent to the target (int).

autoBOFConfig.txt - sample configuration file for usage with autoBOF.py


This is a project that attempts to automate OSCP-style buffer overflows. 
Currently it has achieved all of the minimum requirements to be considered a prototype

1. Fuzz and crash service [X]
2. Overwrite EIP [X]
3. Control EIP [X]
4. Determine valid characters [X]
5. Code execution [X]
6. Generate and send Shellcode [X]
7. Catch Shell [X]

Additionally, this project has achieved the following post-protoype stretch goals:

1. User-customizable input flags [x]
2. minimization of static variables to maximize functionality against a wide variety of targets [x]
3. Generation of standalone exploit [x]

