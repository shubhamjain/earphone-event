from vlc_http import vlc_http
from earphone_event import earphone_event
import time

# trigger_hold_stop variable in earphone_event_object instructs
# the callback to stop seeking.

def seek_handler(event, earphone_event_object):
    instance = vlc_http()

    while( not(earphone_event_object.trigger_hold_stop) ):
	# seek 5s in every 1s
        instance.seek(5)
        time.sleep(1)

def play_handler(event):
    instance = vlc_http()
    instance.play_pause()

EE = earphone_event()
EE.print_e = True
EE.add_subscriber( play_handler, EE.BUTTON_UP)
EE.add_subscriber( seek_handler, EE.BUTTON_HOLD)

EE.init()
