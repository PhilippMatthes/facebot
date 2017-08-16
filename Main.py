from FacebookDriver import Driver
from Mailer import Mailer
from time import sleep
import traceback
import sys

if __name__=="__main__":
    session = Driver()
    mailer = Mailer()
    mailer.sendMessage("Facebook Bot started. Please send >>Start<< to start")
    while True:
        message = mailer.getCurrentMessage()
        if (message == "Start" or message == "Continue"):
            try:
                session.doSomeMagic()
            # except Exception as err:
            #     for frame in traceback.extract_tb(sys.exc_info()[2]):
            #         fname, lineno, fn, text = frame
            #     error = "Error in "+str(fname)+" on line "+str(lineno)+": "+str(err)
            #     print(error)
            #     mailer.sendMessage(error)
            #     pass
            except KeyboardInterrupt:
                mailer.sendMessage("Keyboard Interrupt. Bot will exit now.")
                print("Exiting...")
                break
        else:
            if (message == "Stop" or message == "Exit"):
                mailer.sendMessage("Facebook Bot will exit now.")
                break
            sleep(1)
