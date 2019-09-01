import Draw
import random
import time

#Draws the screen size
Draw.setCanvasSize(400, 500)

#Creates a variable which keeps track of how long the game has been playing
#Want the game to be 20 seconds
gameEnd = time.time()+20

#Creates a variable that keeps track of how many 
#keys have been pressed correctly
KeysInMotion = 0

#Creates a variable that keeps track of penalty time if user
#clicks the incorrect key
resumeTime = 0

#Creates a variable that keeps track of the correct keys the used has pressed
score = 0 

#Creates the list of keys!
allButtons =["a","s","d","f"]
#Makes a list of the keys that need to be pressed
keys=[random.choice(allButtons) for i in range(1000)] 

#Draws 16 keys (4 x 4)
#Select through each row and draw the one filled
#As the selected key in the list that the user must touch!
def drawBoard(score, keys):#, keysInMotion):
    Draw.clear() #Clears the canvas
    
    #Sets the color of the keys
    Draw.setColor("RED")
    for i in range(4): 
        for j in range(4):
            Draw.rect(100*i, 125*j, 100, 125)
            
    for i in range(4):
        Draw.setColor("RED")
        if keys[i]=="a":
            number=0
        elif keys[i]=="s":
            number=1
        elif keys[i]=="d":
            number=2
        elif keys[i]=="f":
            number=3
        Draw.filledRect(100*number, 125*abs(i-3), 100, 125) #Draws the respective key that need to be pressed
        Draw.setColor("WHITE") #Set the color for the letter to be seen on the red key
        Draw.setFontSize(20)
        Draw.setFontBold(True)
        Draw.string(keys[i], 100*number+40, 125*abs(i-3)+45)
        
    #show the score
    Draw.setFontSize(15)        
    Draw.setColor("BLACK")
    Draw.string("Score: " + str(score), 10, 10)
    Draw.show(.30)

#Play the game
def playGame(gameEnd, keys, score, resumeTime):
    
    while gameEnd != time.time() and len(keys)>0: 
        #Creates a while loop that says game will keep running while time isn’t up and there are keys left to press (The code is made so that the number of keys should never run out because game should end based on time)
        
        if Draw.hasNextKeyTyped(): #checks to see if the user times a letter
            
            if Draw.nextKeyTyped()==keys[0]: #Checks to see if the user typed the correct letter corresponding to the highlighted key
                
                score+=1 #Increments score
                keys = keys[1:] #removes zeroth position of keys
                #keysInMotion += 1 #Keeps track of how many keys need to "moved down"' because pressed correctly
           
            else:
                
                resumeTime = time.time() + 1.5 #Creates a penalty of 1.5 seconds if user incorrectly clicks key
            
            if Draw.mousePressed(): #Also checks to see if the mouse touched the correct key and that also works!
                x=Draw.mouseX()
                y=Draw.mouseY()
                if keys[0]=="a":
                    if x>0 and x<=100 and y>375:
                        keys = keys[1:]
                        score+=1
                if keys[0]=="s":
                    if x>100 and x<=200 and y>=375:
                        keys = keys[1:]
                        score+=1
                if keys[0]=="d":
                    if x>200 and x<=300 and y>375:
                        keys = keys[1:]
                        score+=1
                if keys[0]=="f":
                    if x>300 and x<=400 and y>375:
                        keys = keys[1:]
                        score+=1        
    
        if resumeTime and time.time()>resumeTime: #this means penaltly is over so can resume game
            resumeTime = 0
        
        drawBoard(score, keys)
        
def main():
    drawBoard(score, keys)
    playGame(gameEnd, keys, score, resumeTime)
    if gameEnd==time.time():
        Draw.clear()
        Draw.string("Congratulations! You tapped" + str(score)+ "tiles!") 
        #When game is over, clear the screen and display the score

main()

