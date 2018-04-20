import pygame
import random
import time
import math
import socket
import pickle
import os
clear = lambda: os.system('cls')



serverSock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.bind(('0.0.0.0', 16000))
print('Listening... ')
serverSock.listen(1)
clientSock, clientIP = serverSock.accept()
print('connection from ' +str(clientIP))
clientSock.send('NONE'.encode('utf-8'))



#Version notes: they're all on the client side. See ya there!





pygame.init()
screen = pygame.display.set_mode((900, 400)) #Sets display as horizontal, want it vertical? You can suck a dick buddy.
clock = pygame.time.Clock() #game ticks

pygame.display.set_caption('Cattwalk Server') #Title of the window
CTboard = pygame.image.load('CattwalkBoard.png') #Board image
shortMover = None
lost = False
won = False
#---------------------------------------------------------------------
redturn = pygame.image.load('red turn.png')
blueturn = pygame.image.load('blue turn.png')
pieceImages = {
'B1': pygame.image.load('BLUE CALLISTO.png'),
'B2': pygame.image.load('BLUE EUROPA.png'),


'B3': pygame.image.load('BLUE LUNA.png'),
'B4': pygame.image.load('BLUE DEIMOS.png'),
'B5': pygame.image.load('BLUE TITAN.png'),
'B6': pygame.image.load('BLUE SOL.png'),
'R1': pygame.image.load('RED CALLISTO.png'),
'R2': pygame.image.load('RED EUROPA.png'),


'R3': pygame.image.load('RED LUNA.png'),
'R4': pygame.image.load('RED DEIMOS.png'),
'R5': pygame.image.load('RED TITAN.png'),
'R6': pygame.image.load('RED SOL.png'),
'CR': pygame.image.load('cursor.png'),
'LL': pygame.image.load('LongLine.png'),
'SX': pygame.image.load('STYX.png'),
'PH': pygame.image.load('PlaceHolder.png'),
'SC': pygame.image.load('ShortLine.png')}
#----------------------------------------------------------------------- global functions I need
def roundf(x):
    if x%50 < 25:            #I stole the idea for this function from stack overflow! 
        return x - x%50
    else:
        return x + (50 - x%50)

def dist(p1, p2):
    return int(math.ceil(math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)))
#----------------------------------------------------------------------- global data I need
pieceList = {}
stopped = False
bridges = []
gameStage = 'CONSIDERING MOVE'
#==============Beginning Server Networking Data

starmap = [None, None, None, None, None,] #list of past 5 comets
nasa = [None, None, None, None, None,] #list of past 5 rockets
clientIP = clientIP
networkQ = [None, None, None, None, None,] #A queue of all the messages various parts of the program want to send
networkCount = 0
networkStage = 'SETUP'
turn = 'SERVER'
setupPhase = [False, False]  # First is Client, second is Server.
setupPhase = [False, False]  # First is Client, second is Server.
#---------------- Setup Data
setupData = [0,0]
#Setup data records, for both the client and the server, whether they are set up,
#and how many pieces are left for them to place.
#---------------- Setup Data


#==============Ending Server Networking Data

#------------------------------------------------------------------------end of global data

#BEGINNING NETWORKING FUNCTIONS--------------------------------- (FOR THE SERVER) (clientSock)

def updateData():
    sendData = []
    for i in pieceList:
        sendData.append(pieceList[i])
    return pickle.dumps(sendData)

def updateProcess(data):
    pieceList = {}
    data = pickle.loads(data)
    for i in data:
        info = i.info
        placeHolderPiece = Piece([info[0], info[1],  info[0][0] == 'B', info[3], info[4]], movingData=i.isMoving, moveQ = i.moveQ)
        #Don't use placeHolderPiece as a variable, access the object through pieceList like everyone else
    return 'NONE'

def networkProcess(comet):


    #ugh. this is so awful. weird try/except in the middle of the thing. It works I guess. --------------------------
    try:
        turn = turn
    except:
        turn = 'SERVER'
    #ugh. this is so awful. weird try/except in the middle of the thing. It works I guess. --------------------------





    if nasa[-1] == 'UPDATEREQ':
        updateProcess(comet)
        return 'NONE'

    elif nasa[-1] == 'UPDATEGIV':
        return updateData()

    if networkQ[-1] == None:
        if comet == 'NONE':
            return 'NONE'
        elif comet == 'PIECE PLACED':
            networkQ.append('UPDATEREQ')


    else:
        if networkQ[-1] == 'UPDATEREQ' and nasa[-1] != 'UPDATEREQ' and nasa[-1] != 'UPDATEGIV':
            del networkQ[-1]
            return 'UPDATEREQ'

        elif networkQ[-1] == 'UPDATEGIV' and nasa[-1] != 'UPDATEGIV' and nasa[-1] != 'UPDATEREQ':
            del networkQ[-1]
            return 'UPDATEGIV'

        if turn == 'SERVER' and networkQ[-1] == 'TURN CHANGE' and nasa[-1] != 'TURN CHANGE':
            turn = 'CLIENT'
            print('Server made their turn, client has their turn now.')
            return 'TURN CHANGE'


        del networkQ[-1]
        networkQ.insert(0, None)

    return 'NONE'



        # if pygame.key.get_pressed()[pygame.K_COMMA] and nasa[-1] != 'UPDATEREQ' and nasa[-1] != 'UPDATEGIV':  # R E M O V E  - B E F O R E  - L A U N C H
        #     return 'UPDATEREQ'
        #
        # elif pygame.key.get_pressed()[pygame.K_PERIOD] and nasa[-1] != 'UPDATEGIV' and nasa[-1] != 'UPDATEREQ':  # R E M O V E  - B E F O R E  - L A U N C H
        #     return 'UPDATEGIV'



     #this function determines a proper response to the comet.

#     comet = comet.decode('utf-8').split('-----')  # FIVE(5) DASHES SEPARATES COMET PARTS
#     cometLabel = comet[0]
#     cometData = comet[1]
#
#     if cometData == 'NONE':
#         cometData = None
#
#     if cometLabel == 'UPDATE DELIVERY':
#         updateEat(cometData)
#         return  'CORRE-----NONE'.encode('utf-8')
#
#     if cometLabel == 'UPDATE REQUEST':
#
#     if cometLabel = 'CORRE':
#         return 'CORRE-----NONE'.encode('utf-8')
#         # rocket goes out packaged and encoded


#ENDING NETWORKING FUNCTIONS---------------------------------------






#------------------------------------------------------------------------piece class
class Piece(): #Instantiate with a list of the string name of the image, the LIST of the position, a boolean of the team, and the piece name, and whether it's a king
    def __init__(self, args, movingData = [False, None], moveQ = []):
        self.info = args
        self.args = args
        self.imageName = args[0]
        self.image = pieceImages[args[0]]
        self.position = args[1]
        self.isThisTeam = args[2]
        self.name = args[3]
        self.isMoving = movingData
        self.moveQ = moveQ
        self.isKing = args[4]
        pieceList[str(self.name)] = self

    def move(self, direction, pixels):
        self.moveQ.append([str(direction), pixels])
        
    def update(self):
        screen.blit(self.image, (self.position[0], self.position[1]))



        
        if self.moveQ != [] and not self.isMoving[0]:
            self.isMoving[0] = True
            self.isMoving[1] = self.moveQ[0]
            self.moveQ.remove(self.moveQ[0])

        
        if self.isMoving[0]: #UPDATE MOVE
            if self.isMoving[1][0] == 'up':
                self.position[1] -= math.ceil(math.sqrt(self.isMoving[1][1])/2)
                self.isMoving[1][1] -= math.ceil(math.sqrt(self.isMoving[1][1])/2)
            if self.isMoving[1][0] == 'down':
                self.position[1] += math.ceil(math.sqrt(self.isMoving[1][1])/2)
                self.isMoving[1][1] -= math.ceil(math.sqrt(self.isMoving[1][1])/2)
            if self.isMoving[1][0] == 'right':
                self.position[0] += math.ceil(math.sqrt(self.isMoving[1][1])/2)
                self.isMoving[1][1] -= math.ceil(math.sqrt(self.isMoving[1][1])/2)
            if self.isMoving[1][0] == 'left':
                self.position[0] -= math.ceil(math.sqrt(self.isMoving[1][1])/2)
                self.isMoving[1][1] -= math.ceil(math.sqrt(self.isMoving[1][1])/2)
            if self.isMoving[1][1] <= 0:
                self.isMoving = [False, None]
                for i in list(pieceList):
                    pieceList[i].position[0] = roundf(pieceList[i].position[0])
                    pieceList[i].position[1] = roundf(pieceList[i].position[1])
        

        if self.position[1] == 7*50 or self.position[1] == 0: #DYING
            if not self.position in bridges and not self.isMoving[0]:
                print('Death be upon '+str(self.name)+", for their position was "+str(self.position)+", and that is not in the bridges list! "+str(bridges))
                if self.isKing:
                    if not self.isThisTeam:
                        win()
                    else:
                        lose()
                bridges.append([int(roundf(self.position[0])),int(roundf(self.position[1]))])
                del pieceList[self.name]

        if self.position[0] <= -50 and not self.isMoving[0]: #FALLING OFF LEFT SIDE
            if [17*50, self.position[1]] in longMoves(18*50, self.position[1], hyp = True)[0]:
                if self.isThisTeam:
                    self.isThisTeam = False
                    self.image = pieceImages[self.imageName.replace('R', 'B')]
                else:
                    self.isThisTeam = True
                    self.image = pieceImages[self.imageName.replace('B', 'R')]
                self.position[0] = 18*50
                self.isMoving = [True, ['left', 50]]
            else:
                self.isMoving = [True, ['right', 50]]

        if self.position[0] >= 18*50 and not self.isMoving[0]: #FALLING OFF RIGHT SIDE
            if [0, self.position[1]] in longMoves(-50, self.position[1], hyp = True)[0]:            
                if self.isThisTeam:
                    self.isThisTeam = False
                    self.image = pieceImages[self.imageName.replace('R', 'B')]
                else:
                    self.isThisTeam = True
                    self.image = pieceImages[self.imageName.replace('B', 'R')]
                self.position[0] = -50
                self.isMoving = [True, ['right', 50]]
            else:
                self.isMoving = [True, ['left', 50]]

        if self.position[1] <= -50 and not self.isMoving[0] and not self.position[1] <= -500: #FALLING OFF THE TOP
            self.position[1] = 8*50
            self.isMoving = [True, ['up', 50]]

        if self.position[1] >= 8*50 and not self.isMoving[0]: #FALLING OFF THE BOTTOM
            self.position[1] = -50
            self.isMoving = [True, ['down', 50]]


        for i in list(pieceList): #BEING PUSHED
            if pieceList[i].name != self.name:
                if abs(pieceList[i].position[0] - self.position[0]) < 50 and pieceList[i].position[1] == self.position[1] and not self.isMoving[0] and pieceList[i].isMoving[0]:
                    self.move(pieceList[i].isMoving[1][0], pieceList[i].isMoving[1][1])
                    
                    print('something is too close!')
                    if pieceList[i].position[0] - self.position[0] < 0:
                        self.position[0] += 50 - abs(pieceList[i].position[0] - self.position[0])
                    else:
                        self.position[0] -= 50 - abs(pieceList[i].position[0] - self.position[0])

                if abs(pieceList[i].position[1] - self.position[1]) < 50 and pieceList[i].position[0] == self.position[0] and not self.isMoving[0]:
                    if pieceList[i].position[1] - self.position[1] < 0:
                        self.position[1] += 50 - abs(pieceList[i].position[1] - self.position[1])
                    else:
                        self.position[1] -= 50 - abs(pieceList[i].position[1] - self.position[1])
                        
#---------------------------------------------------------------------------end of piece Class and update method

def posToOb(position):
    for i in pieceList:
        if pieceList[i].position == position:
            return pieceList[i]
    else:
        return 'Nothing to see here!'

#---------------------------------------------------------------------------Beginning move functions
def longMoves(x, y, hyp = False, kingHyp = False):
    me = None
    crown = None
    for i in pieceList:
        if pieceList[i].position == [x, y]:
            me = pieceList[i]
    if me == None and not hyp:
        return "Nothing to see here!"

    if hyp and me == None:
        #Well, I don't see a better way, if there are any bugs that randomly spawn a piece that tells you
        #angrily in big red font to STOP HACKING, This is probably where it is.
        me = Piece(['PH', [x, y], True, 'P', kingHyp])
    
    xLine = []
    yLine = []
    xlinepos = []
    xlineneg = []
    ylinepos = []
    ylineneg = []

    if me.isKing:
        crown = 1
    else:
        crown = 0
    
    for i in pieceList: #Finding all x and y concurrents
        print(str(i))
        if pieceList[i].position[0] == me.position[0]:
            yLine.append(i)
        if pieceList[i].position[1] == me.position[1]:
            xLine.append(i)

    for i in xLine: #Splitting x concurrents into greater and lesser
        print(str(xLine))
        if pieceList[i].position[0] > me.position[0]:
            xlinepos.append(i)
        if pieceList[i].position[0] < me.position[0]:
            xlineneg.append(i)

    for i in yLine: #Splitting y concurrents into greater and lesser
        if pieceList[i].position[1] > me.position[1]:
            ylinepos.append(i)
        if pieceList[i].position[1] < me.position[1]:
            ylineneg.append(i)

                        #sorting all the greater and lesser x and y concurrents in descending order
    xlinepos.sort(key=lambda x: pieceList[x].position[0], reverse=True)
    xlineneg.sort(key=lambda x: pieceList[x].position[0], reverse=True)
    ylinepos.sort(key=lambda x: pieceList[x].position[1], reverse=True)
    ylineneg.sort(key=lambda x: pieceList[x].position[1], reverse=True)

    moves = []

    PrimeMoves = {'xpos': None, 'xneg': None, 'ypos': None, 'yneg': None}

    xposmoves = []
    
    #BEGIN X POSITIVE
    if len(xlinepos) == 1:
        PrimeMoves['xpos'] = pieceList[xlinepos[-1]].position[0]
    elif len(xlinepos) == 0:
        PrimeMoves['xpos'] = 850
    else:
        if pieceList[xlinepos[-2]].position[0] - pieceList[xlinepos[-1]].position[0] != 50:
            PrimeMoves['xpos'] = pieceList[xlinepos[-1]].position[0]
        else:

            
            if me.isKing:
                #BEGIN XPOS KING
                if len(xlinepos) >= 3:
                    if pieceList[xlinepos[-3]].position[0] - pieceList[xlinepos[-2]].position[0] != 50:
                        PrimeMoves['xpos'] = pieceList[xlinepos[-1]].position[0]
                    else:
                        PrimeMoves['xpos'] = pieceList[xlinepos[-1]].position[0] - 50
                else:
                    PrimeMoves['xpos'] = pieceList[xlinepos[-1]].position[0]
                #END XPOS KING
            else:
                PrimeMoves['xpos'] = pieceList[xlinepos[-1]].position[0] - 50

                
        #END X POSITIVE

    while PrimeMoves['xpos'] > me.position[0]:
        moves.append([PrimeMoves['xpos'], me.position[1]])
        PrimeMoves['xpos'] -= 50
        
    #BEGIN X NEGATIVE
    if len(xlineneg) == 1:
        PrimeMoves['xneg'] = pieceList[xlineneg[0]].position[0]
    elif len(xlineneg) == 0:
        PrimeMoves['xneg'] = 0
    else:
        if pieceList[xlineneg[0]].position[0] - pieceList[xlineneg[1]].position[0] != 50:
            PrimeMoves['xneg'] = pieceList[xlineneg[0]].position[0]
        else:

            
            if me.isKing:
                if len(xlineneg) >= 3:
                    if pieceList[xlineneg[1]].position[0] - pieceList[xlineneg[2]].position[0] != 50:
                        PrimeMoves['xneg'] = pieceList[xlineneg[0]].position[0]
                    else:
                        PrimeMoves['xneg'] = pieceList[xlineneg[0]].position[0] + 50
                else:
                    PrimeMoves['xneg'] = pieceList[xlineneg[0]].position[0]
            else:
                PrimeMoves['xneg'] = pieceList[xlineneg[0]].position[0] + 50

                
        #END X NEGATIVE

    while PrimeMoves['xneg'] < me.position[0]:
        moves.append([PrimeMoves['xneg'], me.position[1]])
        PrimeMoves['xneg'] += 50
    
    yposmoves = []
    
    #BEGIN Y POSITIVE
    if len(ylinepos) == 1:
        PrimeMoves['ypos'] = pieceList[ylinepos[-1]].position[1]
    elif len(ylinepos) == 0:
        PrimeMoves['ypos'] = 350
    else:
        if pieceList[ylinepos[-2]].position[1] - pieceList[ylinepos[-1]].position[1] != 50:
            PrimeMoves['ypos'] = pieceList[ylinepos[-1]].position[1]
        else:
            
            if me.isKing:
                if len(ylinepos) >= 3:
                    if pieceList[ylinepos[-3]].position[1] - pieceList[ylinepos[-2]].position[1] != 50:
                        PrimeMoves['ypos'] = pieceList[ylinepos[-1]].position[1]
                    else:
                        PrimeMoves['ypos'] = pieceList[ylinepos[-1]].position[1] -50
                else:
                    PrimeMoves['ypos'] = pieceList[ylinepos[-1]].position[1]
            else:
                PrimeMoves['ypos'] = pieceList[ylinepos[-1]].position[1] - 50
            #END Y POSITIVE

    while PrimeMoves['ypos'] > me.position[1]:
        moves.append([me.position[0], PrimeMoves['ypos']])
        PrimeMoves['ypos'] -= 50
        

    ynegmoves = []
    
    #BEGIN Y NEGATIVE
    if len(ylineneg) == 1:
        PrimeMoves['yneg'] = pieceList[ylineneg[0]].position[1]
    elif len(ylineneg) == 0:
        PrimeMoves['yneg']= 0
    else:
        if pieceList[ylineneg[0]].position[1] - pieceList[ylineneg[1]].position[1] != 50:
            PrimeMoves['yneg'] = pieceList[ylineneg[0]].position[1]
        else:

            if me.isKing:
                if len(ylineneg) >= 3:
                    if pieceList[ylineneg[1]].position[1] - pieceList[ylineneg[2]].position[1] != 50:
                        PrimeMoves['yneg'] = pieceList[ylineneg[0]].position[1]
                    else:
                        PrimeMoves['yneg'] = pieceList[ylineneg[0]].position[1] + 50
                else:
                    PrimeMoves['yneg'] = pieceList[ylineneg[0]].position[1]
            else:
                PrimeMoves['yneg'] = pieceList[ylineneg[0]].position[1] + 50
    #END Y NEGATIVE

    while PrimeMoves['yneg'] < me.position[1]:
        moves.append([me.position[0], PrimeMoves['yneg']])
        PrimeMoves['yneg'] += 50

    if me.name == 'P':
        del pieceList[me.name]

    return [moves, me]

    
#ENDING LONG MOVES FUNCTION, BEGINNING SHORT MOVES FUNCTION-----------
def shortMoves(x, y):
    me = None
    moves = []
    for i in pieceList:
        if pieceList[i].position == [x, y]:
            me = pieceList[i]
    if me == None:
        return 'Nothing to see here!'
    #CHECKING SHORT MOVES A&B--------------------
    if [me.position[0], me.position[1]-50] in longMoves(me.position[0], me.position[1])[0]:
        if [me.position[0] - 50, me.position[1] - 50] in longMoves(me.position[0], me.position[1]- 50, hyp = True, kingHyp = me.isKing)[0]:
            moves.append('A')
        if [me.position[0] + 50, me.position[1] - 50] in longMoves(me.position[0], me.position[1]- 50, hyp = True, kingHyp = me.isKing)[0]:
            moves.append('B')
    #CHECKING SHORT MOVES C&D--------------------
    if [me.position[0]+50, me.position[1]] in longMoves(me.position[0], me.position[1])[0]:
        if [me.position[0] + 50, me.position[1] - 50] in longMoves(me.position[0] + 50, me.position[1], hyp = True, kingHyp = me.isKing)[0]:
            moves.append('C')
        if [me.position[0] + 50, me.position[1] + 50] in longMoves(me.position[0] + 50, me.position[1], hyp = True, kingHyp = me.isKing)[0]:
            moves.append('D')
    #CHECKING SHORT MOVES E&F--------------------
    if [me.position[0], me.position[1]+50] in longMoves(me.position[0], me.position[1])[0]:
        if [me.position[0] + 50, me.position[1] + 50] in longMoves(me.position[0] , me.position[1] + 50, hyp = True, kingHyp = me.isKing)[0]:
            moves.append('E')
        if [me.position[0] - 50, me.position[1] + 50] in longMoves(me.position[0] , me.position[1] + 50, hyp = True, kingHyp = me.isKing)[0]:
            moves.append('F')
    #CHECKING SHORT MOVES G&H--------------------
    if [me.position[0]-50, me.position[1]] in longMoves(me.position[0], me.position[1])[0]:
        if [me.position[0] - 50, me.position[1] + 50] in longMoves(me.position[0] - 50, me.position[1], hyp = True, kingHyp = me.isKing)[0]:
            moves.append('G')
        if [me.position[0] - 50, me.position[1] - 50] in longMoves(me.position[0] - 50, me.position[1], hyp = True, kingHyp = me.isKing)[0]:
            moves.append('H')
    return [moves, me]


    # Instantiate with a list of the string name of the image, the LIST of the position, a boolean of the team, and the piece name, and whether it's a king
    #this is the spot where you artificially make pieces, remember?

def win():
    won = True
    bridges = []
    for i in list(pieceList):
        pieceList[i].move("up", 1000)
        pieceList[i].move("right", 1000)


def lose():
    lost = True
    bridges = []
    for i in list(pieceList):
        pieceList[i].move("up", 1000)
        pieceList[i].move("right", 1000)


turn = 'SERVER'
#----------------------------------------------------------------------------
while not stopped:                              #Main Loop!
#----------------------------------------------------------------------------
    events = pygame.event.get()
    screen.blit(CTboard, (0, 0))
    mousePosX = int(str(pygame.mouse.get_pos()).split(',')[0][1:])
    mousePosX -= mousePosX%50
    mousePosY = int(str(pygame.mouse.get_pos()).split(',')[1][:-1])
    mousePosY -= mousePosY%50

    #STARTING SERVER NETWORKING
    comet = clientSock.recv(2048)
    if isinstance(comet, bytes) and not nasa[-1] == 'UPDATEREQ':
        comet = comet.decode('utf-8')

    if comet == 'TURN CHANGE':
        turn = 'SERVER'
        networkQ.append('UPDATEREQ')

    rocket = networkProcess(comet)

    # if networkCount%5 == 0:
    #     if serverTurn:
    #         networkQ.append('UPDATEGIV')
    #     else:
    #         networkQ.append('UPDATEREQ')
    # networkCount += 1

    if rocket == 'TURN CHANGE':
        turn = 'CLIENT'


    starmap.append(comet)
    if len(starmap) >= 5:
        del starmap[0]

    nasa.append(rocket)
    if len(nasa) >= 5:
        del nasa[0]

        #NETWORKING SETUP START-----------------------------------------------------


        #NETWORKING SETUP END-----------------------------------------------------------

    if rocket == None:
        rocket = 'NONE'



    if not isinstance(rocket, bytes):
        rocket = rocket.encode('utf-8')
    clientSock.send(rocket)

    #ENDING SERVER NETWORKING



    for event in events:                         #For loop through all events
        if event.type == pygame.QUIT:  #if quit boolean is true, quit the thing
            stopped = True
            pygame.display.set_caption(gameStage)
            
            print(str(event))                           #print each event to the console

            print(str(mousePosX))
            print(str(mousePosY))

        if pygame.key.get_pressed()[pygame.K_RETURN] and turn == 'SERVER': #R E M O V E  - B E F O R E  - L A U N C H
            gameStage = 'CONSIDERING MOVE'

        #STARTING CLICK TREE
        if event.type == pygame.MOUSEBUTTONUP:
            print('client clicked on '+str(mousePosX)+', '+str(mousePosY))


            if gameStage == 'CONSIDERING LONG MOVE' and posToOb([mousePosX, mousePosY]) == lngmvcons[1]:
                print('double click!')
                gameStage = 'CONSIDERING SHORT MOVE'
                shrtmvcons = shortMoves(mousePosX, mousePosY)
                shortMover = shrtmvcons[1]

            elif gameStage == 'CONSIDERING SHORT MOVE' and posToOb([mousePosX, mousePosY]) == shortMover:
                print('double click!')
                gameStage = 'CONSIDERING LONG MOVE'

            elif gameStage == 'CONSIDERING MOVE' and longMoves(mousePosX, mousePosY) != 'Nothing to see here!' and turn == 'SERVER':
                if posToOb([mousePosX, mousePosY]).isThisTeam:
                    lngmvcons = longMoves(mousePosX, mousePosY)
                    print('Player is considering a long move')
                    gameStage = 'CONSIDERING LONG MOVE'

            elif gameStage == 'CONSIDERING MOVE' and longMoves(mousePosX, mousePosY) == 'Nothing to see here!' and turn == 'SERVER' and not setupPhase[1]:
                if mousePosX <= 4 * 50:
                    if setupData[1] == 6:
                        setupPhase[1] = True
                    else:
                        setupData[1] += 1
                        networkQ.append('TURN CHANGE')
                        networkQ.append('UPDATEGIV')
                        networkQ.append('PIECE PLACED')
                        Piece(['B'+str(setupData[1]), [mousePosX, mousePosY], True, 'B'+str(setupData[1]), setupData[1]==6])
                        gameStage = 'CONSIDERING MOVE'


            elif gameStage == 'CONSIDERING LONG MOVE':
                if [mousePosX, mousePosY] in lngmvcons[0] and turn == 'SERVER':
                    networkQ.append('TURN CHANGE')
                    networkQ.append('UPDATEGIV')
                    print('Piece has been given a directive to move!')

                    if mousePosY == lngmvcons[1].position[1] and mousePosX > lngmvcons[1].position[0]:
                        lngmvcons[1].move('right', mousePosX - lngmvcons[1].position[0])
                    elif mousePosY == lngmvcons[1].position[1] and mousePosX < lngmvcons[1].position[0]:
                        lngmvcons[1].move('left', lngmvcons[1].position[0] - mousePosX)
                    elif mousePosX == lngmvcons[1].position[0] and mousePosY < lngmvcons[1].position[1]:
                        lngmvcons[1].move('up', lngmvcons[1].position[1] - mousePosY)
                    elif mousePosX == lngmvcons[1].position[0] and mousePosY > lngmvcons[1].position[1]:
                        lngmvcons[1].move('down', mousePosY - lngmvcons[1].position[1])
                        #move 
                    gameStage = 'CONSIDERING MOVE'
                    lngmvcons = None

            elif gameStage == 'CONSIDERING SHORT MOVE' and posToOb([mousePosX, mousePosY]) != shortMover and turn == 'SERVER':
                if dist([mousePosX, mousePosY], [shortMover.position[0], shortMover.position[1]]) <= 175:
                    madeMove = ''
                    networkQ.append('TURN CHANGE')
                    networkQ.append('UPDATEGIV')


                    if mousePosY > shortMover.position[1]:
                        madeMove += 'A'
                    else:
                        madeMove += 'B'
                    
                    if mousePosX > shortMover.position[0]:
                        madeMove += 'C'
                    else:
                        madeMove += 'D'
                    
                    if mousePosX - shortMover.position[0] > mousePosY - shortMover.position[1]:
                        madeMove += 'E'
                    else:
                        madeMove += 'F'

                    if - mousePosX + shortMover.position[0] > mousePosY - shortMover.position[1]:
                        madeMove += 'G'
                    else:
                        madeMove += 'H'
                if madeMove == 'BDEG' and 'A' in shrtmvcons[0]:
                    shortMover.move('up', 50)
                    shortMover.move('left', 50)
                elif madeMove == 'BCEG' and 'B' in shrtmvcons[0]:
                    shortMover.move('up', 50)
                    shortMover.move('right', 50)
                elif madeMove == 'BCEH' and 'C' in shrtmvcons[0]:
                    shortMover.move('right', 50)
                    shortMover.move('up', 50)
                elif madeMove == 'ACEH' and 'D' in shrtmvcons[0]:
                    shortMover.move('right', 50)
                    shortMover.move('down', 50)
                elif madeMove == 'ACFH' and 'E' in shrtmvcons[0]:
                    shortMover.move('down', 50)
                    shortMover.move('right', 50)
                elif madeMove == 'ADFH' and 'F' in shrtmvcons[0]:
                    shortMover.move('down', 50)
                    shortMover.move('left', 50)
                elif madeMove == 'ADFG' and 'G' in shrtmvcons[0]:
                    shortMover.move('left', 50)
                    shortMover.move('down', 50)
                elif madeMove == 'BDFG' and 'H' in shrtmvcons[0]:
                    shortMover.move('left', 50)
                    shortMover.move('up', 50)

            elif gameStage == 'CONSIDERING LONG MOVE' or gameStage == 'CONSIDERING SHORT MOVE':
                if longMoves(mousePosX, mousePosY) == 'Nothing to see here!':
                    gameStage = 'CONSIDERING MOVE'
                    
                
        
            #ENDING CLICK TREE


                        
    


#UPDATING GAME STAGES STARTS
    for i in pieceList:
        if pieceList[i].isMoving[0]:
            gameStage = 'MOVING'
        if pieceList[i].name == 'P':
            del pieceList[i]
        if gameStage == 'MOVING':
            throw = False #stands for "throwaway variable"
            for i in pieceList:
                if pieceList[i].isMoving[0]:
                    throw = True
            if not throw:
                gameStage = 'CONSIDERING MOVE'

    clear()
    print('SERVER SIDE \n')
    print(gameStage)
    print('STARMAP IS: ' + str(starmap)+'\n')
    print('NASA IS: ' + str(nasa)+'\n')
    print('Comet: ' + str(comet)+'\n')
    print('Rocket: ' + str(rocket)+'\n')
    print('Network command Queue: ' + str(networkQ)+'\n')
    print(turn+' TURN')
    print('PieceList Is: '+str(pieceList))
    print('gameStage is: '+str(gameStage))

#UPDATING GAME STAGES DONE



    #BLITS!


    
    for i in bridges:
        screen.blit(pieceImages['SX'], (i[0], i[1]))
        print(str(bridges))

    for i in list(pieceList):
        pieceList[i].update()

    if turn == 'CLIENT':
        screen.blit(redturn, (0,0))
    else:
        screen.blit(blueturn, (0,0))
    
    if gameStage == 'CONSIDERING LONG MOVE':
        for i in lngmvcons[0]:
            screen.blit(pieceImages['LL'], i)

    if gameStage == 'CONSIDERING SHORT MOVE':
        screen.blit(pieceImages['SC'], [shortMover.position[0]-150, shortMover.position[1]-150])

    if lost:
        for i in list(pieceList):
            pieceList[i].move("up", 5000)


        lost = False

    if won:


        for i in range(5):
            print("CLIENT WINS!")

        won = False


    #NO MORE BLITS!


    pygame.display.flip()
    clock.tick(60)

