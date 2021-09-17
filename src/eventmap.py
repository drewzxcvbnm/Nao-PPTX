import qi
from services import mem, EVENT_ARG_DELIMITER


def handle_event(event):
    eventname = event.split(EVENT_ARG_DELIMITER)[0]
    args = event.split(EVENT_ARG_DELIMITER)[1:]
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
