import fastapi as fAPI
import threading
import serial
import re

def initRobot():
    com = input("Insert serial port that arduino is connected")
    speed = int(input("Insert speed of serial port"))
    commonsSpeeds = [9600, 19200, 38400, 57600, 115200]
    pattern = r'^com[1-9]$'
    newRobot = None
    if speed in commonsSpeeds and re.match(pattern, com):
        newRobot = Robot((com, speed))
    else:
        newRobot = Robot()
    return newRobot


class Robot:
    def __init__(self, comPort=('COM4', 9600)):
        self.stack = []
        self.serialConnection = serial.Serial(comPort[0], comPort[1])
        self.moveThread = threading.Thread(target=self.moveRobot)
        self.moveThread.start()

    def addToStack(self, side):
        self.stack.append(side)

    def moveRobot(self):
        while True:
            if len(self.stack) > 0:
                temp = self.stack.pop(0)
                print(f"Stack not empty next move: {temp}")
                self.sendData(temp)

    def sendData(self, data: str):
        possibleSides = {'forward':'w', 'back':'s', 'left':'a', 'right':'d','stop':'c'}
        self.serialConnection.write(possibleSides[data].encode())


myRobot = initRobot()
app = fAPI.FastAPI()


@app.get("/move-robot")
async def callMove(side: str):
    possibleSides = ['forward', 'back', 'left', 'right','stop']
    if side not in possibleSides:
        return {"Message": "Bad parameter" + side}
    myRobot.addToStack(side)
    return {"Message": "Operation OK"}
