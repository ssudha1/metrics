# metrics
This is a partially automated script for metric evaluation
Experimental setup : 1. Install Genymotion emulator and Virtualbox
                     2. Download this code and save the memfetch (https://github.com/citypw/lcamtuf-memfetch) executable with in the code directory
                     3. Run the code python automateadb.py <folder containing the application executable used to acquire process dump for>
                     4. The code on execution asks the user to run the Genymotion emulator, turn on the network adapter in the emulator, adjust the process state of installed app 
 in the emulator. Once all the requiredparameteers are set by the user. The code with help of Memfetch automatically acquires the process dump in each runtime mode                   
