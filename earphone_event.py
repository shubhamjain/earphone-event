import pyaudio
import struct
import sys
import time
from mini_event import mini_event

class earphone_event(mini_event):
    FORMAT = pyaudio.paInt32
    RATE = 22050 # Sampling rates

    print_e = False # True if you want to print events when fired. Useful for debugging
    listen = True # Should true for loop to execute

    # A click should emit a high frequency wave which
    # gets clipped to max / min value. Here we are considering
    # a margin of 15% from the absolute max / min.

    THRESHOLD_MAX = 2 ** 31 - .20 * 2 ** 31
    THRESHOLD_MIN = -2 ** 31 + .20 * 2 ** 31

    # Minimum no of clipped samples indicating a click
    THRESHOLD_SAMPLES = 800

    def init(self):

        stream = pyaudio.PyAudio().open(format=self.FORMAT,
                        channels=1,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=1)

        count_min = 0
        count_max = 0

        # time_fired is used to detect if the earphone button is held for prolong time by recording
        # time since button was pressed and not released.
        time_fired = 0
        button_down = False

        while(1):
            if self.listen == False:
                break
            
            data = stream.read(1) #read one sample
            int_sample = struct.unpack("i", data)[0] #convert string to 32 bit integer

            
            # Count no of clipped samples. The first condition 
            # makes sure double events don't fire after a long press.
            if( not(button_down) and int_sample <= self.THRESHOLD_MIN ):
                count_min += 1
                if count_min >= self.THRESHOLD_SAMPLES:
                    count_min = 0
                    button_down = True
                    if self.print_e : print "button_down"
                    self.fire_event( self.BUTTON_DOWN )
                    time_fired = time.time()
            else:
                count_min = 0

            if( time_fired ):
                if( (time.time() - time_fired) > 1.5 ): # Pressed for more than one and half second?
                    if self.print_e : print "button_up"
                    self.fire_event( self.BUTTON_HOLD )
                    time_fired = 0
                       
            if( button_down and int_sample >= self.THRESHOLD_MAX ):
                count_max += 1
                if count_max >= self.THRESHOLD_SAMPLES:
                    count_max = 0
                    button_down = False
                    if self.print_e : print "button_up"
                    self.fire_event( self.BUTTON_UP )
                    time_fired = 0
            else:
                count_max = 0

    def stop(self):
        self.listen = False

