import os
import sys

## OBSOLETE ##
#Change audio pitch (replaces the source file)
def ChangePitch(inputFilename,pitchFactor):
    if pitchFactor != 1:
        print("Changing pitch to {}".format(pitchFactor))
    os.system(" ffmpeg -y -i {} -af asetrate=44100*{},aresample=44100,atempo={} pitchBuffer.mp3"
              .format(inputFilename,pitchFactor,1/pitchFactor))
    return "pitchBuffer.mp3"

### OBSOLETE ###
#Change audio speed (replaces the source file)
def ChangeSpeed(inputFilename,speedFactor):
    if speedFactor != 1:
        print("Changing speed to {}".format(speedFactor))
    os.system(" ffmpeg -y -i {} -af atempo={} speedBuffer.mp3"
              .format(inputFilename,speedFactor))
    return "speedBuffer.mp3"

# Find new name that is not taken
def FindName(newFilename,originalFilename,i):
    for filename in os.listdir(path):
        if (filename == newFilename+".mp3"):
            newFilename = originalFilename + "(" +str(i) + ")"
            i=i+1
            return FindName(newFilename,originalFilename,i)
    return newFilename + ".mp3"

def ProcessAudio(inputFilename,path,outputFilename,pitchFactor=1,speedFactor=1):
    print("Processing: {}. Output file: {}".format(inputFilename,outputFilename+".mp3"))
    # Change output name if there are duplicates
    outputFilename = FindName(outputFilename,outputFilename,1)        

    # Generate pitchProcessString
    pitchProcessString = ("asetrate=44100*{}".format(pitchFactor))
    pitchTempoOverhead = (1/pitchFactor)
    while(pitchTempoOverhead < 0.5):
        pitchProcessString = pitchProcessString + ",atempo={}".format(0.5)
        pitchTempoOverhead = pitchTempoOverhead/0.5
    pitchProcessString = pitchProcessString + ",atempo={}".format(pitchTempoOverhead)

    # Generate speedProcessString
    speedProcessString = ""
    speedTempoOverhead = speedFactor
    while(speedTempoOverhead < 0.5):
        speedProcessString = speedProcessString + ",atempo={}".format(0.5)
        speedTempoOverhead = speedTempoOverhead/0.5
    speedProcessString = speedProcessString + ",atempo={}".format(speedTempoOverhead)

    # Process
    #print(" ffmpeg -y -i {} -af {}{} out.mp3".format(inputFilename,pitchProcessString,speedProcessString))
    os.system(" ffmpeg -y -i {} -af {}{} out.mp3".format(inputFilename,pitchProcessString,speedProcessString))
    #os.startfile("out.mp3")

# Execute the script
path = "C:\\Users\\qkunder\\Desktop\\ffmpeg\\bin"
outputFilename = "out"
pitchFactor = .5
speedFactor =4
inputFilename = str(sys.argv[1])
if (len(sys.argv)==4):
    pitchFactor = float(sys.argv[2])
    speedFactor = float(sys.argv[3]) 
ProcessAudio(inputFilename,path,outputFilename,pitchFactor,speedFactor)
