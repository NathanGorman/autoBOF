#!gdb
import sys
import gdb
import os
os.system("echo resetFile > eip.txt")
number_restarts = 100
def on_stop(sig):
  global number_restarts
  if isinstance(sig, gdb.SignalEvent): #and (sig.stop_signal != "SIGSEGV"):
    if (number_restarts > 0): #can add restart control if want
      os.system("rm eip.txt") #overwrite still appending for some reason, hot fix
      gdb.execute("set confirm off")
      gdb.execute("set logging file eip.txt")
      gdb.execute("set logging on")
      gdb.execute("set logging overwrite on")
      gdb.execute("info registers eip")
      gdb.execute("set logging off") #CAN LOG THE DUMP TO NEW FILE BY CHANGING LOG FILE AND USING DIFFERENT COMMAND
      gdb.execute("set logging overwrite off")
      gdb.execute("kill")
      gdb.execute("run")
gdb.events.stop.connect (on_stop)
gdb.execute("run")
#Maybe after each run kill this and start a new debugger instance? Or too slow.
#garbage idea but maybe work