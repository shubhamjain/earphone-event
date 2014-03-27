import threading

class mini_event:
    BUTTON_DOWN = 1
    BUTTON_UP = 2
    BUTTON_HOLD = 3

    subscribers = { BUTTON_DOWN: [], BUTTON_UP : [],  BUTTON_HOLD: [] }
    trigger_hold_stop = False # This value should be turned to True if the hold event callback needs to be stopped.

    def add_subscriber( self, callback, event ):
        self.subscribers[event].append( callback )

    def fire_event( self, event ):

        if( event == self.BUTTON_UP ):
            self.trigger_hold_stop = True

        if( event == self.BUTTON_DOWN ):
            self.trigger_hold_stop = False
    
        for callback in self.subscribers[event]:

            if( event == self.BUTTON_HOLD ):
                thread = threading.Thread(target=callback, args=[self.BUTTON_HOLD, self])
                thread.start()
            else:
                callback(event)

