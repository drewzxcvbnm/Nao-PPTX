import qi
# ip = "192.168.253.155"
ip = "192.168.252.226"
# ip = "192.168.252.62"

session = qi.Session()
session.connect("tcp://" + ip + ":" + "9559")
# video = session.service( "ALVideoDevice" )   
memory = session.service( "ALMemory" )
tts = session.service("ALTextToSpeech")

def main():
    memory.declareEvent("event")
    memory.insertData("event", "my_func()")
    sub = memory.subscriber("event")
    # exec("my_func()")
    dis = sub.signal.connect(myexec)
    print "check1"
    memory.insertData("event", "my_func2()")
    print "check2"
    memory.insertData("event", "my_func3()")
    print "check3"
    memory.raiseEvent("event", "my_func4()")

def myexec(x):
    exec(x)
    return True

def my_func():
    print "suka"
def my_func2():
    print "suka2"
def my_func3():
    print "suka3"
def my_func4():
    print "suka4"

def pprint(a):
    print a


main()


