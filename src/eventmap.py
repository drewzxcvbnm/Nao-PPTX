import qi
from services import mem


def handle_event(event):
    eventname = event.split('_')[0]
    args = event.split('_')[1:]
    print "HANDLING " + eventname
    if eventname not in eventmap.keys():
        print "ERROR: eventmap cannot handle event:" + eventname
    mem.insertData("event", None)
    eventmap[eventname](*args)


def crash():
    raise Exception("some exeption")


mem.declareEvent("event")
subscriber = mem.subscriber("event")
disconnect = subscriber.signal.connect(handle_event)

eventmap = {
    "crash": crash
}
