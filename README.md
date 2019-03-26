# autoBOF
# Nathan Gorman's automated buffer overflow project

Files:

restart.py - this is the script that manages the debugger. It mainly serves to restart the debugger at appropriate times and dump information about the program.

autoBOF.py - Where the magic happens. Currently fuzzes the service and overwrites the EIP. Takes one input variable, the maximum amount of data that will be sent to the target (int).


This is a project that attempts to automate OSCP-style buffer overflows. 
Currently it has achieved all of the minimum requirements to be considered a prototype

1. Fuzz and crash service [X]
2. Overwrite EIP [X]
3. Control EIP [X]
4. Determine valid characters [X]
5. Code execution [X]
6. Generate and send Shellcode [X]
7. Catch Shell [X]

The final stages of this project as it nears completion will involve a large influx of user control over the overflow testing process, as well as a handful of quality of life improvements. This includes the ability to save a standalone exploit for later use, as well as the ability to specify the initial buffer content in order to make this tool less theoretical and more practical
