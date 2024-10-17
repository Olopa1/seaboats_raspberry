import fastapi as fAPI
import threading
import serial
import uvicorn

def initRobot():
    com = input("Insert serial port that arduino is connected")
    speed = int(input("Insert speed of serial port"))
    commonsSpeeds = [9600, 19200, 38400, 57600, 115200]
    newRobot = None
    if speed in commonsSpeeds:
        newRobot = Robot((com, speed))
    else:
        newRobot = Robot()
    return newRobot


class Robot:
    def __init__(self, comPort=('COM4', 9600)):
        self.stack = []
        self.serialConnection = serial.Serial(comPort[0], comPort[1])
        self.moveThread = threading.Thread(target=self.moveRobot)
        self.readThread = threading.Thread(target=self.readDataFromRobot)
        self.moveThread.start()

    def addToStack(self, side):
        self.stack.append(side)

    def moveRobot(self):
        while True:
            if len(self.stack) > 0:
                temp = self.stack.pop(0)
                print(f"Stack not empty next move: {temp}")
                self.sendData(temp)

    def startReadingData(self):
        self.readThread.start()

    def readDataFromRobot(self):
        while True:
            try:
                print("Arduino response:")
                self.serialConnection.readlines()
            except:
                continue

    def sendData(self, data: str):
        possibleSides = {'forward': 'w', 'back': 'x', 'left': 'a', 'right': 'd', 'stop': 's',
                         'diagonalleft':'e','diagonalright':'q','diagonalbackleft':'z','diagonalbackright':'c','turnleft':'f','turnright':'r'}
        self.serialConnection.write(possibleSides[data].encode())


#myRobot = initRobot()
app = fAPI.FastAPI()


@app.get("/move-robot")
async def callMove(side: str):
    possibleSides = ['forward', 'back', 'left', 'right', 'stop'
        ,'diagonalleft','diagonalright','diagonabacklleft','diagonalbackright','turnleft','turnright']
    if side not in possibleSides:
        return {"Message": "Bad parameter: " + side}
    #myRobot.addToStack(side)
    return {"Message": "Operation OK"}

if __name__=="__main__":
    uvicorn.run(app,host="192.168.0.128",port=8000)