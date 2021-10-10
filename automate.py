import os
import sys
import subprocess
import time

def main():
	#dir = '/Users/sneha/Library/Android/sdk/platform-tools/Communication'
        aapt = '/Users/snehasudhakaran/Applications/Contents/MacOS/tools/aapt'
	dir = sys.argv[1]
	for apk in os.listdir(dir):
		if not apk.startswith("."):
			apk_name = dir + '/'  + apk
			print(apk_name)
			pkg = subprocess.check_output('./aapt dump badging '+apk_name + ' | grep \"package\"', shell = True).split("'")[1]
			print("Package name "+pkg)
			count = 4
			automate =False
			while (count!=0):
				try:
					raw_input('Start Clean Genymotion Device from Snapshot')
					raw_input('Check Device Network')
					print ("Installing "+apk_name)
					subprocess.check_output('./adb install -r ' + apk_name, shell = True)
					print ("Granting permissions for "+apk_name)
					grantPerm(apk_name, pkg)
					print ("Starting the Application "+pkg)
					os.system('./adb shell monkey -p '+pkg+' -c android.intent.category.LAUNCHER 1 ')
					time.sleep(10) #Use time for process to start
					print ("Getting PID ")
					pid = getPid(pkg)
					if (pid):
						print ("Process "+ pkg+" started with PID "+pid)
						# if GC adb shell am dumpheap com.test.test /sdcard/test.hprof
						print ("Checking Process if is in Foreground")
						procApp = getProc()
						while pkg not in procApp[0:procApp.rfind(".")]:
							time.sleep(5) #App hasn't started yet
							procApp = getProc()
						raw_input('RUN APP')
												[state, gc] = switch(count, pid, pkg, procApp)
						runMem(pid)
						getMem(apk, state, gc)
						clean(pkg)
					else:
						print("Error starting application "+apk_name)
				except subprocess.CalledProcessError as e:
					print "Installation failed due to "+e.output
				count = count-1
			
			
def runMonkey(pkg):
	
	monkey =subprocess.check_output('./adb shell monkey -p '+pkg+ ' -v --pct-syskeys 0 500 -s 5 --throttle 1000', shell = True)
	print monkey
	if "NOT RESPONDING" in monkey:
		raw_input('App is not responding try restarting and manual processing')
		raw_input('Hit enter when done running app')	
		
def runMem(pid):
	os.system('./adb push ./memfetch /data/local/')
	os.system('./adb push our_shell.sh /data/local')
	os.system('./adb shell sh /data/local/our_shell.sh ' +pid)


def getMem(apk, state, gc):
	os.system('mkdir all_memfetch')
	os.system('mkdir all_memfetch/'+apk)
	os.system('mkdir all_memfetch/'+apk+'/'+state+'-'+gc)
	os.system('./adb pull /data/local/memory_dump/ ./all_memfetch/'+apk+'/'+state+'-'+gc+'/')
	os.system('./adb pull /system/lib/libart.so ./all_memfetch/'+apk+'/'+state+'-'+gc+'/memory_dump/')
				
def clean(pkg):
	os.system('./adb shell rm -r /data/local/memory_dump/')	
	os.system('./adb uninstall '+pkg)	
	
def getPid(pkg):
	pid=subprocess.check_output('./adb shell ps -A | grep '+pkg, shell = True).split(" ")
	pid = filter(None, pid)[1].encode()
	return pid
	
def switch(count, pid, pkg, procApp):
	if count ==4: 
		state = "F"
		gc = "NGC"
		checkState(pkg, procApp, state)
		print "App in Foreground and No GC"
	elif count ==3:
		state = "F"
		gc = "GC"
		os.system('./adb shell kill -10 '+pid) # force GC
		checkState(pkg, procApp, state)
		print "App in Foreground and with GC"
	elif count ==2:
		state = "B"
		gc = "NGC"
		checkState(pkg, procApp, state)
		print "App in Background and No GC"
	elif count ==1:
		state = "B"
		gc = "GC"
		os.system('./adb shell kill -10 '+pid)
		checkState(pkg, procApp, state)
		print "App in Background and with GC"
	return [state, gc]
	
def getProc():
	proc = subprocess.check_output('./adb shell dumpsys window windows | grep mCurrentFocus',shell = True).rstrip("}\n").split("/")
	print proc
	return proc[len(proc) -1]
	
def checkState(pkg, procApp, state):
	proc = getProc()
	if "F" in state and not proc[0:proc.rfind(".")] in procApp[0:procApp.rfind(".")]: # if app not in foreground
		activity = procApp[procApp.rfind(".")+1:]
		os.system('./adb shell am start --activity-single-top '+procApp) # put it in foreground
	if "B" in state and proc[0:proc.rfind(".")] in procApp[0:procApp.rfind(".")]: # if app not in background
		os.system('./adb shell monkey -p com.android.messaging -c android.intent.category.LAUNCHER 1 ')		
		
def getPerm(apk):
	permlist=[]
	list = subprocess.check_output('./aapt dump permissions '+apk ,shell = True).split("\n")
	for i in list:
		if "android.permission" in i:
			permlist.append(i[i.rfind("=")+1:].strip("'"))
	return permlist
	
def grantPerm(apk, pkg):
	permlist = getPerm(apk)
	for perm in permlist:
		os.system('./adb shell pm grant '+pkg+' '+  perm)
	print "Done granting permissions"
	
main()
