#!/usr/bin/python
import pyaudio
import sys
import thread
import wave
from time import sleep,time,asctime
from array import array

flag = 0
exitFlag = False
summa=0
peaks=0
theend = 0
#{{{ function waitSomeTime()
def waitSomeTime(threadName):
    global summa
    global flag
    global peaks
    interval = 15 # seconds
    sleep(interval)
    print "--- %s : peaks = %s : summa = %s ---"%(asctime(),peaks,summa)
    flag=0
    summa=0
    peaks=0
#}}}
#{{{ main()
def main():
    global summa
    global flag
    global peaks

    flag = 0
    noise=1500
    threshold=5000
    chunk = 4096 # gut
#   chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
#   RATE = 44100
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            output=True,
            frames_per_buffer=chunk)
    try:
      while True:
        integral=0
        data = stream.read(chunk)
        as_ints = array('h', data)
        max_value = max(as_ints)
        if max_value > noise:
            peaks += 1
            if flag == 0:
                thread.start_new_thread( waitSomeTime, ("waitThread",) )
                flag = 1
            else:
                #reduce(lambda x,y: x+(0,(y,5)[y>5]-3)[(y,5)[y>5]>3], a)
                integral = reduce(lambda x,y: x+\
                        (0,(y,threshold)[y>threshold]-\
                        noise)[(y,threshold)[y>threshold]>noise], as_ints)
            summa += integral
            #print "%s\t%s\t%s"%(max_value-noise, integral, summa)
            if exitFlag:
                sys.exit(0)
    except (KeyboardInterrupt, SystemExit):
        print "\rExiting"
        stream.stop_stream()
        stream.close()
        p.terminate()
#}}}
if __name__ == '__main__':
  main()



