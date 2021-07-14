import qi
from services import mem


def handleEvent(x):
    print "HANDLING " + x
    if x not in eventmap.keys():
        print "ERROR: eventmap cannot handle event:" + x
    eventmap[x]()


def crash():
    raise Exception("some exeption")


mem.declareEvent("event")
subscriber = mem.subscriber("event")
disconnect = subscriber.signal.connect(handleEvent)

eventmap = {
    "crash": crash
}
