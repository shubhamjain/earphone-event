Earphone Events
==============

This is a small module which can be used to detect earphone button presses. I was aroused by curiousity on how [these buttons](http://i01.i.aliimg.com/img/pb/410/506/487/487506410_866.jpg) worked. I hacked around and found, they emit a certain noise like [this](http://i.imgur.com/CqIwRiv.png). So there went my afternoon to detect the clipping part and make the button presses meaningful. It is explained more succintly in my [blog post](https://shubhamjain.co/2014/03/30/making-earphone-presses-useful-with-pyaudio-and-vlc-http-api/)

How can this be used?
====================

I originally made it to control VLC player from button presses but the module is of feeble use, as of now. For using this, you must have a way detect the noise, implying you have a machine with a combo jack [mic + headphone combined jack]. Secondly, I have only tried my pair of samsung earphones; I am not sure how the other pairs would work on this. The `example.py` shows an example on using the module. 


