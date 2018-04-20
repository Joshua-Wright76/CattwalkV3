import pygame
import random
import time
import math
import socket
import pickle
import os
clear = lambda: os.system('cls')

serverIP = input('IP?: ')
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.connect((serverIP, 16000))
print('Connection made with '+str(serverIP))


#Version notes: The pushing works nicely in all directions! the solution wasn't very "elegant" but it will work. probably.
#The left and right transpositions work nicely! I've been stuck for two days on this weird glitch with the dying logic.
#The rounding function worked wrong. I fixed it, but it didn't solve the dying problem...
#I've made some severe changes to the way dying works, and everything is fucked. Death is a myth. nothing is real.
#I did it! Kind of... I solved the dying problem, but now the dead piece blits OVER the living piece. Which is probably an ez fix so hooray for me
#I've now added a moves queue, and did some stuff to allow the pushing of multiple pieces, but it's a bit wonky. Half the time it doesn't work right and throws no error messages. Gotta investigate that.
#Now I have to work on top-bottom edge transposition! I'll work on the double pushing later. Probably a bug that I can hack away somehow.
#I now have finished top-bottom edge transposition! Now I have to try to fix that other bug
#Fixed it by reworking the push a bit, but now the death thing doesn't work, and I am rready to die
#fixed death, apparently boolean algebra doesn't quite work the way I thought it did
#Begun working on long move function.
#Long move almost done! I need to do two things: Test y negative, and translate "prime moves" to all possible moves and consolidate it in one return!
#THE LONG MMMOVES ARE OVER, THE LONG MOVES ARE (nearly, because kings) DONE
#time for short moves now!
#finished short moves, and tried to do some stuff with networking... Should probably sit on that one for a bit.
#I think the networking is all ready on this side, need to do server side now
#fuck everything was wrong the whole time
#why has god forsaken me
#note to self: read the documentation of a library before you start using it
#I FUCKKEBN DID IT! HAHAHAHHAHQHHA
#Jesus fuck there are so many bugs
#here are some bugs to remember:
#that thing where all the pieces move at once
#that thing where one player just fucken ctrl-z's the other players pieces
#that good meme where the pieces just move 200 times slower than normal
#The thing where updates dont include the moveQ
#these need to go
#Ive decided to just remake the networking process. Instead of having the
#Server and client cooperate, the server is gonna control the updating process entirely.
#server will have a request and a send information process.
#Alright! I've set up a framework, cleared out all (I hope) of the preexisting setup and networking systems,
#and now im gonna start filling it up.
#somewhere, the rocket is turning into a NoneType object????
#Alright, that solution was pretty hacky, ill have to remember this.
#Cool, the framework works fine, I need to test updating now.
#SO, the updating function breaks if the server sends it an empty piecelist. This probably wont ever be a problem, right?
#yeah, i guess there will never be a necessary update for no pieces on the board. Probably. Unless there are hackers...
#oh, wait, that wasn't the problem lmao.
#Okay, so there's an issue with the server's UPDATEGIV. it doesn't work.
#maybe something to do with the past comet/rocket checking.
#it was! The fuck? that was so weird. hold on.
#FUCKIGN finally. Okay, so i was adding new rockets to nasa and new comets to starmap at opposite times around
#processing a response. Dicks. well, it works now.
#I've given the server a queue of commands to handle for network updates and stuff.
#somehow, multiple updategivs end up in the queue at once, fucking literally all of it up
#I'm not finished with server setup business, my chair got too hot.
#halfway through setting up the turns system, I realized I don't have a solid plan, and decided to call it a night. fix that.
#got rid of the setup system, drew up a plan for turn handling, and implemented it (still needs testing)
# ? ? ? ? it's been throwing me a "referenced before assigned" error for the turn data. What the fuck. It's assigned right there.
# I'm literally assigning and referencing like five other variables that are exactly in the same place. What the hell
#I just hacked away the problem with a try/except thing. tf. I hate that that actually worked.
#this try/except bullshit really needs to go. I gotta just fix that bug some reasonable way.
#......................I ended up doing the try/except bullshit anyway.
#Alright, I took a two week break from this, tried to start working on grapevine/lichtenstein/whatever the fuck that was,
#came back and fixed the turns problem (as far as I know) in a few hours. A testament to the power of vacations.

#Jesus fuck this bug in the setup: I have no idea what is going on. It's throwing a keyError "R" whenever I long move request any piece after any have been
#set up. None of the pieces are ever just named "R", in fact that variable doesn't pop up anywhere??? Maybe I'm wrong about what keyError means exactly...
#Because stack overflow said it happens when you request a value from a dictionary with a key that isn't in it, but that doesn't seem relevant to my problem?
#It probably shows up for some other errortypes too. Now, there, future me, don't start getting suspicious at that poor pickling function over there, he has done
#nothing wrong and doesn't deserve this. Anyway, fix that and the game is like, an inch from done. Honestly I'm so excited!!! Good luck!

#I'm back, and nope, keyError is only for that. Maybe a long stretch of wait is what I need to fix this problem.

#fucking what ? ? ? Well I learned something new today. Let me explain:
#So keyError really was telling the truth about what was going on. In the part of longMove where I split
#concurrent pieces into positive and negative x and y concurrents, I added the indeces of the pieces (in piecelist)
#to those lists, xpos ypos xneg and yneg, so I could manipulate them later on. the problem was,
#that I was using += to do that, instead of .append! Which meant that if the index of the piece was multiple chars,
#it would put each char into the list independently, instead of just adding the whole string as one item, fucking up literally everything.
#this wasn't a problem when all the indeces of my pieces were only one character, but the setup
#process instantiates them with mutiple character indeces. Fuck me.

#oh dude, its like, done.

#not yet though, I still have to fix a few things. Also theres a new mechanic in the game that showed up on accident, and I'm not sure how I feel about it.
#so like, while the setup is happening, you can choose to spend your turn moving one of your pieces or you can place a peice, they both take a turn.
#weird. not sure how I feel about that.

#postalpha bug list:
#some fuckery going on in shortmoves
#lmao the X sides falling is weird sometimes-
#I think it has something to do with updates-
#bungling the team attribute.
#also there are no win conditions so I gotta do that


pygame.init()
screen = pygame.display.set_mode((900, 400)) #Sets display as horizontal, want it vertical? You can suck a dick buddy.
clock = pygame.time.Clock() #game ticks
pygame.display.set_caption('Cattwalk Client') #Title of the window
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
    if x%50 < 25:
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

#==============Beginning Client Networking Data

starmap = [None, None, None, None, None,] #list of past 5 comets
nasa = [None, None, None, None, None,] #list of past 5 rockets
serverIP = serverIP #The server's IP
networkQ = [None, None, None, None, None]
turn = 'SERVER'
turnChange = False
setupData = [0,0]
setupPhase = [False, False] #First is Client, second is Server.
#--------------------Client Setup Data

networkStage = 'SETUP'

#--------------------Client Setup Data




#==============Ending Client Networking Data

#------------------------------------------------------------------------end of global data



    
#BEGINNING NETWORKING FUNCTIONS--------------------------------- (FOR THE CLIENT) (serverSock)

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
        placeHolderPiece = Piece([info[0], info[1],  info[0][0]=='R', info[3], info[4]], movingData=i.isMoving, moveQ = i.moveQ)
        #Don't use placeHolderPiece as a variable, access the object through pieceList like everyone else
    return 'NONE'

def networkProcess(comet):
     #this function determines a proper response to the comet.

    netQTop = networkQ[-1]
    del networkQ[-1]
    networkQ.insert(0, None)

        # ugh. this is so awful. weird try/except in the middle of the thing. if It works I guess. --------------------------
    try:
        turn = turn
    except:
        turn = 'SERVER'
        pass
        # ugh. this is so awful. weird try/except in the middle of the thing. if It works I guess. --------------------------

    if comet == 'UPDATEREQ':
        return updateData()

    elif comet == 'UPDATEGIV':
        return 'NONE'
    elif starmap[-1] == 'UPDATEGIV':
        updateProcess(comet)
        return 'NONE'


    if netQTop == 'TURN CHANGE':
        turn = 'SERVER'
        return 'TURN CHANGE'

    if comet == 'NONE':
         return 'NONE'

    if comet == 'TURN CHANGE':
        turn = 'CLIENT'
        return 'NONE'



#     comet = comet.decode('utf-8').split('-----') #FIVE(5) DASHES SEPARATES COMET PARTS
#     cometLabel = comet[0]
#     cometData = comet[1]
#
#     if cometData == 'NONE':
#         cometData = None
#
#     if cometLabel == 'UPDATE DELIVERY':
#         updateEat(cometData)
#         return #some corre thing
#
#     if cometLabel = 'CORRE':
#         return 'CORRE-----NONE'
#     #rocket goes out packaged and encoded



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

    
    for i in pieceList: #Finding all x and y concurrents
        if pieceList[i].position[0] == me.position[0]:
            yLine.append(i)
        if pieceList[i].position[1] == me.position[1]:
            xLine.append(i)

    for i in xLine: #Splitting x concurrents into greater and lesser
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



    #I'm thinking of having all the pieces clear off the board and do a little dance for the winner.
    #Too much? ;) No, of course it isn't.

#----------------------------------------------------------------------------
while not stopped:                              #Main Loop!
#----------------------------------------------------------------------------
    events = pygame.event.get()
    screen.blit(CTboard, (0, 0))
    mousePosX = int(str(pygame.mouse.get_pos()).split(',')[0][1:])
    mousePosX -= mousePosX%50
    mousePosY = int(str(pygame.mouse.get_pos()).split(',')[1][:-1])
    mousePosY -= mousePosY%50

    #STARTING CLIENT NETWORKING
    comet = serverSock.recv(2048)
    if isinstance(comet, bytes) and starmap[-1] != 'UPDATEGIV':
        comet = comet.decode('utf-8')

    if comet == 'TURN CHANGE':
        turn = 'CLIENT'

    rocket = networkProcess(comet)

    if rocket == 'TURN CHANGE':
        turn = 'SERVER'

    starmap.append(comet)
    if len(starmap) >= 5:
        del starmap[0]

    nasa.append(rocket)
    if len(nasa) >= 5:
        del nasa[0]



        #NETWORK SETUP START------------------------------------------------------------------


        #NETWORK SETUP END--------------------------------------------------------------------


    if rocket == None:
        rocket = 'NONE'

    if not isinstance(rocket, bytes):
        rocket = rocket.encode('utf-8')
    serverSock.send(rocket)

    #ENDING CLIENT NETWORKING


    
    for event in events:                         #For loop through all events
        if event.type == pygame.QUIT:  #if quit boolean is true, quit the thing
            stopped = True
            pygame.display.set_caption(gameStage)
            
            #print(str(event))                           #print each event to the console

            #print(str(mousePosX))
            #print(str(mousePosY))

        if pygame.key.get_pressed()[pygame.K_RETURN] and turn == 'CLIENT': #R E M O V E  - B E F O R E  - L A U N C H
            gameStage = 'CONSIDERING MOVE'

        #STARTING CLICK TREE
        if event.type == pygame.MOUSEBUTTONUP:
            print('client clicked on '+str(mousePosX)+', '+str(mousePosY))

            #STARTING SETUP BUSINESS--------------------------------------------------------------------

            #ENDING SETUP BUSINESS----------------------------------------------------------------------






            if gameStage == 'CONSIDERING LONG MOVE' and posToOb([mousePosX, mousePosY]) == lngmvcons[1]:
                print('double click!')
                gameStage = 'CONSIDERING SHORT MOVE'
                shrtmvcons = shortMoves(mousePosX, mousePosY)
                shortMover = shrtmvcons[1]

            elif gameStage == 'CONSIDERING SHORT MOVE' and posToOb([mousePosX, mousePosY]) == shortMover:
                print('double click!')
                gameStage = 'CONSIDERING LONG MOVE'

            elif gameStage == 'CONSIDERING MOVE' and longMoves(mousePosX, mousePosY) != 'Nothing to see here!' and turn == 'CLIENT':
                if posToOb([mousePosX, mousePosY]).isThisTeam:
                    lngmvcons = longMoves(mousePosX, mousePosY)
                    print('Player is considering a long move')
                    gameStage = 'CONSIDERING LONG MOVE'

            elif gameStage == 'CONSIDERING MOVE' and longMoves(mousePosX, mousePosY) == 'Nothing to see here!' and turn == 'CLIENT' and not setupPhase[0]:
                if mousePosX >= 13*50:
                    if setupData[0] == 6:
                        setupPhase[0] = True
                    else:
                        setupData[0] += 1
                        networkQ.append('TURN CHANGE')
                        networkQ.append('PIECE PLACED')
                        Piece(['R'+str(setupData[0]), [mousePosX, mousePosY], True, 'R'+str(setupData[0]), setupData[0]==6])
                        gameStage = 'CONSIDERING MOVE'


            elif gameStage == 'CONSIDERING LONG MOVE':
                if [mousePosX, mousePosY] in lngmvcons[0] and turn == 'CLIENT':
                    turnChange = True
                    print('Piece has been given a directive to move!')

                    networkQ.append('TURN CHANGE')


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

            elif gameStage == 'CONSIDERING SHORT MOVE' and posToOb([mousePosX, mousePosY]) != shortMover:
                if dist([mousePosX, mousePosY], [shortMover.position[0], shortMover.position[1]]) <= 175 and turn =='CLIENT':
                    madeMove = ''
                    networkQ.append('TURN CHANGE')


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
    #print('CLIENT SIDE \n')
    #print(gameStage)
    #print('STARMAP IS: ' + str(starmap)+'\n')
    #print('NASA IS: ' + str(nasa)+'\n')
    #print('Comet: ' + str(comet)+'\n')
    #print('Rocket: ' + str(rocket)+'\n')
    print(turn + ' TURN')
    print('PieceList Is: '+str(pieceList))
    print('gameStage is: '+str(gameStage))
    #print(networkStage)
    #print(setupStage)
#UPDATING GAME STAGES DONE



    #BLITS!

    if turn == 'CLIENT':
        screen.blit(redturn, (0, 0))
    else:
        screen.blit(blueturn, (0, 0))
    
    for i in bridges:
        screen.blit(pieceImages['SX'], (i[0], i[1]))
        #print(str(bridges))

    for i in list(pieceList):
        pieceList[i].update()

    print(setupPhase)

    if gameStage == 'CONSIDERING LONG MOVE':
        for i in lngmvcons[0]:
            screen.blit(pieceImages['LL'], i)

    if gameStage == 'CONSIDERING SHORT MOVE':
        screen.blit(pieceImages['SC'], [shortMover.position[0]-150, shortMover.position[1]-150])

    if lost:

        for i in range(5):
            print("SERVER WINS!")

        lost = False

    if won:

        for i in range(5):
            print("CLIENT WINS!")

        won = False

    #NO MORE BLITS!


    pygame.display.flip()
    clock.tick(60)

