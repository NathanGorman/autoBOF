# autoBOF
# Nathan Gorman's automated buffer overflow project

Files:

restart.py - this is the script that manages the debugger. It mainly serves to restart the debugger at appropriate times and dump information about the program.
autoBOF.py - Where the magic happens. Currently fuzzes the service and overwrites the EIP. Takes one input variable, the maximum amount of data that will be sent to the target (int).


This is a project that attempts to automate OSCP-style buffer overflows. 
Currently it is stage 3 of 7 before it can be considered a prototype.

1. Fuzz and crash service [X]
2. Overwrite EIP [X]
3. Control EIP [X]
4. Determine valid characters [ ]
5. Code execution [ ]
6. Generate and send Shellcode [ ]
7. Catch Shell [ ]
