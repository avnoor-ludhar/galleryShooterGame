#Avnoor Ludhar
#galleryshooterfinalgame1.py
#----------------------------------------------------------------------------------
#This program is a gallery shooter type game in which you move a cursor and shoot
#at enemies that are on the screen. There are many types of enemies with different
#point values and attributes. There is also a menu screen that can cycles between 4
#different views. In the game there is a pause menu included as well. Highscores in
#the highscorer menu can be entered at the end of a game if your score is high enough
#it will be put in the menu. The main parts of this program is how the information is held
#and the while True loop at the end of the code to cycle between pages.



from pygame import *
from random import *

init()

#timesnewromanfont1-5 are different sizes of the times new roman font used throughout the program.
timesnewromanfont = font.SysFont("Times New Roman", 50)
timesnewromanfont2 = font.SysFont("Times New Roman", 30)
timesnewromanfont3 = font.SysFont("Times New Roman", 80)
timesnewromanfont4 = font.SysFont("Times New Roman", 40)
timesnewromanfont5 = font.SysFont("Times New Roman", 68)

#All the sizes I used for Arial font.
arialfont1 = font.SysFont("Arial", 50)
arialfont2 = font.SysFont("Arial", 30)

BASEURL = "/Users/avnoorludhar/Desktop/computer sceince/high school projects/galleryShooterGame/"

#Loads the different sound effects
shotsound = mixer.Sound(BASEURL + "RealisticGunshotSoundEffect.wav")
gameoversound = mixer.Sound(BASEURL + "Evil game over sound effect for video games.wav")
deathsound = mixer.Sound(BASEURL + "pubgdeath1.wav")
noammosound = mixer.Sound(BASEURL + "Gun click - Sound effect.wav")


#Channels for the sounds so they overlap
shotsoundChannel = mixer.Channel(1)
deathsoundChannel = mixer.Channel(2)

ammo = 20
points = 0
#TYPE is the badguyslists type.
#STATUS, FRAME, DELAY, and TIMER are all positions in badguys.
TYPE = 1
STATUS = 2
FRAME = 3
DELAY = 4
TIMER = 5
#Alivepics is the pictures for the soldier TYPE being alive.
alivepics = [image.load(BASEURL + "commadosprite/commadosprite0.png"), image.load(BASEURL + "commadosprite/commadosprite1.png"),image.load(BASEURL + "commadosprite/commadosprite2.png")]
#Nothing is a list so that nothing is displayed when badguys aren't on the screen.
nothing = [0,0,0,0,0,0]
#badguys is a list of lists that holds the data for each badguy enitity.
#It has a rect position on the screen, a type, a status, a frame, a delay and a timer.
badguys = [[Rect(250,400,55,55), "soldier", "off", 0, 0, 0], [Rect(670,260,55,55),"soldier","off", 0, 0, 0],[Rect(370,250,55,55),"soldier", "off", 0, 0, 0], [Rect(0,485,50,50), "enemydoctor", "off", 0, 0, 0], [Rect(625,255,45,45), "civilian", "off", 0, 0, 0]]
shootpics = [image.load(BASEURL + "commandoshoot1/commandoshoot0.png"), image.load(BASEURL + "commandoshoot1/commandoshoot10.png"), image.load(BASEURL + "commandoshoot1/commandoshoot10.png")]
lives = 3

#2 lists of the 2 types of pictures for the doctor TYPE.
doctorpics = [image.load(BASEURL + "doctormoveleft/doctormoveleft0.png"),image.load(BASEURL + "doctormoveleft/doctormoveleft1.png"),image.load(BASEURL + "doctormoveleft/doctormoveleft2.png"),image.load(BASEURL + "doctormoveleft/doctormoveleft3.png")]
doctordead = [image.load(BASEURL + "doctordead1/doctordead10.png"),image.load(BASEURL + "doctordead1/doctordead11.png"),image.load(BASEURL + "doctordead1/doctordead12.png"),image.load(BASEURL + "doctordead1/doctordead13.png"),image.load(BASEURL + "doctordead1/doctordead14.png")]

#Pictures for the civilian TYPE.
civilianpics = [image.load(BASEURL + "civilianman/civilianman0.png"),image.load(BASEURL + "civilianman/civilianman1.png"),image.load(BASEURL + "civilianman/civilianman2.png")]

#position of the crosshair.
crosshairX = 400
crosshairY = 300

#Position of the doctor.
doctorsx = 1000

#Variable at 0,0 to blit background pictures at.
loc = 0,0
background = image.load(BASEURL + "armybase.png")

#Pictures of the death animation for soldier TYPE.
deadguys = []
deadguys.append(image.load(BASEURL + "commandodead1/commando dead10.png"))
deadguys.append(image.load(BASEURL + "commandodead1/commando dead11.png"))
deadguys.append(image.load(BASEURL + "commandodead1/commando dead12.png"))
deadguys.append(image.load(BASEURL + "commandodead1/commando dead13.png"))
deadguys.append(image.load(BASEURL + "commandodead1/commando dead15.png"))

#Pictures of ammocrate
ammopics = [image.load(BASEURL + "ammocratepics1/ammocratepics13.png"), image.load(BASEURL + "ammocratepics1/ammocratepics12.png"),image.load(BASEURL + "ammocratepics1/ammocratepics11.png"),image.load(BASEURL + "ammocratepics1/ammocratepics10.png")]
    
#A dictionary with each corresponding string to its list of pictures. 
allPics = {"alive":alivepics, "dead":deadguys, "off":nothing, "shoot":shootpics, "enemydoctor":doctorpics, "doctordead":doctordead, "civilian":civilianpics, "opened":ammopics}


AMOUNT = 0
SPOT = 1
SPAWN = 2
#This is a list of the ammo crate position and all the aspects of badguys.
ammocrate = [[15, Rect(510,290, 55,55), "off", 0, 0, 0],[15, Rect(200,520, 55,55), "off", 0, 0, 0],[15, Rect(800,520, 55,55), "off", 0, 0, 0]]

def movedoctor():
    '''The movedoctor function moves the doctors
    X position across the screen if he's alive. If he's dead it sets
    the right image and spot for the doctor to respawn.'''
    global doctorsx
    global points
    global lives
    
    if doctorsx <= 1000 and badguys[3][STATUS] == "alive":
        doctorsx -= 8

    if doctorsx <= 0 and lives > 0:
        doctorsx = 1000
        points -= 500
        badguys[3][STATUS] = "off"
        badguys[3][FRAME] = 0

    if badguys[3][STATUS] == "doctordead":
        if badguys[3][FRAME] == 4:
            doctorsx = 1000
            badguys[3][STATUS] = "off"
            badguys[3][FRAME] = 0

            
    badguys[3][0].x = doctorsx
    
    

def music():
    '''Plays different music at different menu screens.'''

    #Chooses song out of 2 songs
    gamesongchoice = randint(0,1)
    
    if musicscreen == "Menu":
        mixer.music.stop()
        mixer.music.unload()
        mixer.music.load(BASEURL + "Jeopardy Theme.mp3")
        
    if musicscreen == "Game" and gamesongchoice == 0:
        mixer.music.stop()
        mixer.music.unload()
        mixer.music.load(BASEURL + "Runnin.wav")

    if musicscreen == "Game" and gamesongchoice == 1:
        mixer.music.stop()
        mixer.music.unload()
        mixer.music.load(BASEURL + "Jay-Z - Empire State Of Mind (Clean Edit).mp3")
                         
    if musicscreen == "Pause":
        mixer.music.stop()
        mixer.music.unload()
        mixer.music.load(BASEURL + "Jeopardy Theme.mp3")
    if musicscreen == "Highscore":
        mixer.music.stop()
        mixer.music.unload()
        mixer.music.load(BASEURL + "All I Do Is Win (clean).mp3")
        

    mixer.music.set_volume(0.45)  
    mixer.music.play() 
    

def soundeffects():
    '''Plays different sounds for different things that happen.'''
    
    keys = key.get_pressed()
    
    if keys[K_SPACE] and ammo > 0:
        shotsoundChannel.stop()
        shotsoundChannel.play(shotsound)

    if keys[K_SPACE] and ammo == 0:
        shotsoundChannel.stop()
        shotsoundChannel.play(noammosound)
        
    if lives == 0:
        mixer.Sound.play(gameoversound)
        
    if badguys[3][STATUS] == "doctordead" and badguys[3][FRAME] == 1:
        deathsoundChannel.play(deathsound)
        

def text():
    '''The text function renders and returns text according to if the game is over or
    still in play.'''
    global points
    global lives

    blitPic = timesnewromanfont2.render("You have % d points and have % d lives." % (points, lives), True, (47,131,31), 1)
    losePic = timesnewromanfont5.render("GAME OVER, you had %d points." % points , True, (47,131,31), 1)
    
    # Adds a life according to there points and how many lives they currently have.
    if points == 15000 and lives == 1:
        lives = 3
    elif points == 15000 and lives == 3:
        lives = 3
        
    elif points == 15000 and lives == 2:
        lives = 3

    if lives > 0:
        return blitPic
    if lives <= 0:
        return losePic

def crosshair():
    '''The crosshair function checks for if the cursor centre and checks for if its killing
    an enemy and changes the points lives and frame of the badguys accordingly.'''
    global points
    global crosshairX
    global crosshairY
    global lives
    global ammo
    
    mx, my = mouse.get_pos()
    keys = key.get_pressed()

    if keys[K_SPACE] == 1 and ammo > 0:
        ammo -= 1
        
    for i in range(len(badguys)):
        if badguys[i][0].collidepoint(crosshairX,crosshairY) and ammo > 0:
            if keys[K_SPACE] == 1 and badguys[i][STATUS] == "alive" and badguys[i][TYPE] == "soldier" or keys[K_SPACE] == 1 and badguys[i][STATUS] == "shoot":
                badguys[i][STATUS] = "dead"
                badguys[i][FRAME] = 0
                if lives > 0:
                    points += 500
                    
            elif keys[K_SPACE] == 1 and badguys[i][STATUS] == "alive" and badguys[i][TYPE] == "enemydoctor":
                badguys[i][STATUS] = "doctordead"
                badguys[i][FRAME] = 0
                if lives > 0:
                    points += 1000
                
            elif keys[K_SPACE] == 1 and badguys[i][STATUS] == "alive" and badguys[i][TYPE] == "civilian":
                badguys[i][STATUS] = "off"
                badguys[i][FRAME] = 0
                points -= 500





def frames():

    '''This function changes the frame and delays when showing th picture
    by getting into the FRAME and DELAY in the badguys list.'''
    
    for i in range(len(badguys)):

        if badguys[i][STATUS] == "shoot":
            badguys[i][DELAY] += 1
            if badguys[i][DELAY] == 6:
                badguys[i][DELAY] = 0
                badguys[i][FRAME] += 1
                if badguys[i][FRAME] == 3:
                    badguys[i][FRAME] = 0

        elif badguys[i][STATUS] == "alive" and badguys[i][TYPE] == "civilian" or badguys[i][STATUS] == "alive" and badguys[i][TYPE] == "soldier":
            badguys[i][DELAY] += 1
            if badguys[i][DELAY] == 6:
                badguys[i][DELAY] = 0
                badguys[i][FRAME] += 1
                if badguys[i][FRAME] == 3:
                    badguys[i][FRAME] = 0
     
                
        elif badguys[i][STATUS] == "dead":
            badguys[i][DELAY] += 1
            if badguys[i][DELAY] == 6:
                badguys[i][DELAY] = 0
                badguys[i][FRAME] += 1
                if badguys[i][FRAME] == 5 or badguys[i][FRAME] == 6:
                    badguys[i][FRAME] = 0
                    badguys[i][STATUS] = "off"
                    
        elif badguys[i][STATUS] == "doctordead":
            badguys[i][DELAY] += 1
            if badguys[i][DELAY] == 6:
                badguys[i][DELAY] = 0
                badguys[i][FRAME] += 1
                if badguys[i][FRAME] == 5 or badguys[i][FRAME] == 6:
                    badguys[i][FRAME] = 0
                    badguys[i][STATUS] = "off"

        elif badguys[i][STATUS] == "alive" and badguys[i][TYPE] == "enemydoctor":
            badguys[i][DELAY] += 1
            if badguys[i][DELAY] == 4:
                badguys[i][DELAY] = 0
                badguys[i][FRAME] += 1
                if badguys[i][FRAME] == 3:
                    badguys[i][FRAME] = 0

    for i in range(len(ammocrate)):
        if ammocrate[i][SPAWN] == "opened":
            ammocrate[i][DELAY] += 1
            if ammocrate[i][DELAY] == 6:
                ammocrate[i][DELAY] = 0
                ammocrate[i][FRAME] += 1
                if ammocrate[i][FRAME] == 3:
                    ammocrate[i][FRAME] = 0
                    ammocrate[i][STATUS] = "off"

def movecursor():
    '''The movecursor function does exactly that it moves the cursor position on the screen and returns it.'''
    global crosshairX
    global crosshairY
    mx, my = mouse.get_pos()
    keys = key.get_pressed()
    if keys[K_RIGHT] and crosshairX <= 1000:
        crosshairX += 11
    if keys[K_LEFT] and crosshairX >= 0:
        crosshairX -= 11
    if keys[K_UP] and crosshairY >= 0:
        crosshairY -= 11
    if keys[K_DOWN] and crosshairY <= 600:
        crosshairY += 11

    return crosshairX,crosshairY


def ammofun():
    '''The ammofun function just increases and decreases ammo and sets a timer for the ammo to be on screen for.'''
    global ammo
    keys = key.get_pressed()
    
    for i in range(len(ammocrate)):
        ammocrate[i][TIMER] +=1
        
        if ammocrate[i][SPAWN] == "alive" and ammocrate[i][SPOT].collidepoint(crosshairX,crosshairY):
            if keys[K_SPACE] == 1:
                ammo += ammocrate[i][AMOUNT]
                ammocrate[i][SPAWN] = "opened"

        if ammocrate[i][TIMER] == 240:
            ammocrate[i][SPAWN] == "off"
    
                       
def graphics():
    '''The graphics function blits every thing on the screen and draws anything that is in the actual game, pictures, text everything.'''
    global background
    global ammo
    
    screen.blit(background,(0,0))
    
    for guy in badguys:
        #frame is the exact frame the badguy is at
        frame = guy[FRAME]
        #pic is the picture corresponding to that frame.
        pic = allPics[guy[STATUS]][frame]
        if guy[STATUS] == "alive" and guy[TYPE] == "soldier" or guy[STATUS] == "dead" and guy[TYPE] == "soldier" or guy[STATUS] == "shoot" and guy[TYPE] == "soldier":
            screen.blit(pic,guy[0])

    for crate in ammocrate:
        frame = crate[FRAME]
        pic = allPics[crate[SPAWN]][frame]
        if crate[SPAWN] == "opened":
            screen.blit(pic, crate[1])
    
    draw.circle(screen, (255,0,0), movecursor(), 3)
    draw.circle(screen, (255,0,0), movecursor(), 15,2)
    
    if badguys[3][TYPE] == "enemydoctor" and badguys[3][STATUS] == "alive":
        frame = badguys[3][FRAME]
        pic = allPics[badguys[3][TYPE]][frame]
        screen.blit(pic,badguys[3][0])
        
    elif badguys[3][1] == "enemydoctor" and badguys[3][STATUS] == "doctordead":
        frame = badguys[3][FRAME]
        pic = allPics[badguys[3][STATUS]][frame]
        screen.blit(pic,badguys[3][0])

    if badguys[4][TYPE] == "civilian" and badguys[4][STATUS] == "alive":
        frame = badguys[4][FRAME]
        pic = allPics[badguys[4][TYPE]][frame]
        screen.blit(pic,badguys[4][0])

    ammotxt = timesnewromanfont2.render("AMMO: %i" % ammo, True, (47,131,31), 1)


    for i in range(len(ammocrate)):
        if ammocrate[i][SPAWN] == "alive":
            screen.blit(ammopics[0], ammocrate[i][SPOT])
    
    if lives > 0:  
        screen.blit(text(), (50,50))
        screen.blit(ammotxt,(50,90))
        
    if lives <= 0:
        screen.blit(text(), (0,250))
        
    
       

def spawning():
    global points
    '''The spawning function spawns all entitys by a random chance. If the player is above 20 000 points they spawn faster'''
    global doctorsx
    
    for i in range(len(badguys)):
        if points >= 20000:
            if randint(0,100) == 1 and badguys[i][STATUS] == "off":
                badguys[i][STATUS] = "alive"
            
        elif randint(0,125) == 1 and badguys[i][STATUS] == "off":
            badguys[i][STATUS] = "alive"

        if points >= 20000:
            if randint(0,350) == 1 and badguys[i][STATUS] == "off" and badguys[i][TYPE] == "enemydoctor":
                badguys[i][STATUS] = "alive"
            
        elif randint(0,400) == 1 and badguys[i][STATUS] == "off" and badguys[i][TYPE] == "enemydoctor":
            badguys[i][STATUS] = "alive"
            #Resets doctors X position back to the start.
            doctorsx = 1000

    for i in range(len(ammocrate)):
        if randint(0, 150) == 1  and ammocrate[i][SPAWN] == "off":
            ammocrate[i][TIMER] = 0
            ammocrate[i][SPAWN] = "alive"

            

def trans():
    '''The trans function transforms all the sizes of the enemies to look bigger.'''
    for i in range(len(alivepics)):
        alivepics[i] = transform.smoothscale(alivepics[i], (55,55))
        
    for i in range(len(deadguys)):
        deadguys[i] = transform.smoothscale(deadguys[i], (55,55))
        
    for i in range(len(doctorpics)):
        doctorpics[i] = transform.smoothscale(doctorpics[i], (55,55))
        
    for i in range(len(doctordead)):
        doctordead[i] = transform.smoothscale(doctordead[i], (55,55))

    for i in range(len(ammopics)):
        ammopics[i] = transform.smoothscale(ammopics[i], (50,50))


        
def shooting():
    '''This uses the TIMER position in the badguys list to either make the soldiers shoot or the civilians go off screen and come back.'''
    global lives
    
    for i in range(len(badguys)):
        badguys[i][TIMER] += 1
        
    for i in range(len(badguys)):
        
        if badguys[i][TIMER] == 105 and badguys[i][STATUS] == "alive" and badguys[i][1] == "soldier":
            badguys[i][STATUS] = "shoot"
            lives -= 1
            
        if badguys[i][TIMER] == 150 and badguys[i][STATUS] == "shoot":
            badguys[i][STATUS] = "off"
        elif badguys[i][STATUS] == "off":
            badguys[i][TIMER] = 0

    if badguys[4][TIMER] >= 90 and badguys[4][STATUS] == "alive":
        badguys[4][STATUS] = "off"

def Game():
    global lives
    '''This game function draws the pause game and back to menu buttons
    and runs everything going on in the game when called. Also goes to the pause screen
    and back to the menu.'''

    #makes sure that the get name function is only called once.
    count = 0
    
    trans()

    #backmenu has the position and text for the back to menu button. 
    backmenu = [Rect(650,10,235,40), "Back to the Menu."]
    
    #pausemenu has the position and text for the pause button. 
    pausemenu = [Rect(650,60,235,40), "Pause game."]
    
    def backmenudraw():
        '''This function draws all the buttons on the screen.'''
        #backpic is the text for the back menu.
        backPic = timesnewromanfont2.render(backmenu[1], True, (255,255,255))
        draw.rect(screen, (0,0,0), backmenu[0])
        backPic = timesnewromanfont2.render(backmenu[1], True, (255,255,255))
        screen.blit(backPic,(backmenu[0].x+6,backmenu[0].y+4))

        #pausepic is the text for the pause menu.
        pausePic = timesnewromanfont2.render(pausemenu[1], True, (255,255,255))
        draw.rect(screen, (0,0,0), pausemenu[0])
        backPic = timesnewromanfont2.render(pausemenu[1], True, (255,255,255))
        screen.blit(pausePic,(pausemenu[0].x+6, pausemenu[0].y+4))

        

    running =True
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False
                
        myClock = time.Clock()
        
        mousepos = mouse.get_pos()
        mb = mouse.get_pressed()

        shooting()
    
        spawning()

        movedoctor()

        crosshair()
        
        frames()

        graphics()

        ammofun()
        

        backmenudraw()

        soundeffects()

        if lives == 0:
            count += 1
        if count == 1:
            textfileaddition()
        

        if backmenu[0].collidepoint(mousepos):
            draw.rect(screen,(0,255,0),backmenu[0],2)
            if mb[0]==1:
                return "Menu"
            
        if pausemenu[0].collidepoint(mousepos):
            draw.rect(screen,(0,255,0),pausemenu[0],2)
            if mb[0]==1:
                return "Pause"
        
        myClock.tick(30)
 
        display.flip()

    return "Exit"

def instructions():
    '''Draws and makes everything inside of the instruction page including the button to go back to the menu.'''
    loc = (0,0)
    running = True

    #The picture for the instructions page.
    picture = image.load(BASEURL + "instructionpage.png")
    backmenu = [Rect(620,520,235,40), "Back to the Menu."]
    
    def backmenudraw():
        backPic = timesnewromanfont2.render(backmenu[1], True, (255,255,255))
        draw.rect(screen, (0,0,0), backmenu[0])
        screen.blit(backPic,(backmenu[0].x+6,backmenu[0].y+4))
 
    
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                running = False

        mousepos = mouse.get_pos()
        mb = mouse.get_pressed()
        
        screen.blit(picture, loc)

        backmenudraw()

        if backmenu[0].collidepoint(mousepos):
            draw.rect(screen,(0,255,0),backmenu[0],2)
            if mb[0]==1:
                return "Menu"
                
        display.flip()

    return "Exit"
    
    
    
def credit():
    '''Draws and makes everything inside of the credit page including the button to go back to the menu.'''
    loc = (0,0)
    
    running = True
    
    #The picture for the credit page.
    picture = image.load(BASEURL + "credits.png")
    backmenu = [Rect(750,500,250,40), "Back to the Menu."]

    def backmenudraw():
        backPic = timesnewromanfont2.render(backmenu[1], True, (255,255,255))
        draw.rect(screen, (0,0,0), backmenu[0])
        screen.blit(backPic,(backmenu[0].x+6,backmenu[0].y+4))

    
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                running = False


        mousepos = mouse.get_pos()
        mb = mouse.get_pressed()
        
        screen.blit(picture, loc)
        
        backmenudraw()
        
        if backmenu[0].collidepoint(mousepos):
            draw.rect(screen,(0,255,0),backmenu[0],2)
            if mb[0]==1:
                return "Menu"
        

        display.flip()

    return "Exit"

def pause():
    '''Draws and makes everything inside of the pause page including the button to go back to the game.'''

    loc = (0,0)
    #picture is the background
    picture = image.load(BASEURL + "menubackground.png")
    picture = transform.smoothscale(picture, (1000, 601))

    #meme is the meme displayed.
    meme = image.load(BASEURL + "pausememe.png")

    backmenu = [Rect(750,500,250,40), "Back to the Game"]
    
    def writetext():
        '''The write text funciton writes out all the text in the pause menu.'''

        #pausemenu text is the text thats about to be blitted. Changed multiple times in the function.
        pausemenutext = arialfont1.render("Pause Menu.", True, (255,255,255))
        screen.blit(pausemenutext, (600,70))
        
        pausemenutext = arialfont2.render("Since this is an offline game", True, (255,255,255))
        screen.blit(pausemenutext, (550, 150))
    
        pausemenutext = arialfont2.render("you can pause!!!", True, (255,255,255))
        screen.blit(pausemenutext, (550, 190))
   
        pausemenutext = arialfont1.render("Woooooo Hoooooo!!!", True, (255,255,255))
        screen.blit(pausemenutext, (510, 350))


    def backmenudraw():
        backPic = timesnewromanfont2.render(backmenu[1], True, (255,255,255))
        draw.rect(screen, (0,0,0), backmenu[0])
        screen.blit(backPic,(backmenu[0].x+6,backmenu[0].y+4))
    
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                return "Exit"
            
        mousepos = mouse.get_pos()
        mb = mouse.get_pressed()
                
        screen.blit(picture, loc)
        
        draw.rect(screen, (0,0,0), backmenu[0])
        screen.blit(meme, loc)
        
        writetext()

        backmenudraw()

        if backmenu[0].collidepoint(mousepos):
            draw.rect(screen,(0,255,0),backmenu[0],2)
            if mb[0]==1:
                return "Play"
    
        display.flip()

def menu():
    '''The menu function displays all the boxes and text on the screen and when one of the boxes is clicked it returns that value
    thus sending you to that page.'''
    
    loc = (0,0)
    running = True
    myClock = time.Clock()

    #Menu text is the title for the menu.
    menutext = timesnewromanfont3.render("Army Base Invasion", True, (255,0,0))

    #boxes is the position of each button.

    boxes = []
    for y in range(2):
        boxes.append(Rect(150,y*180+200,300,100))
        boxes.append(Rect(550,y*180+200,300,100))

    #values is the text and where the page will be directed to.
    values = ["Play","Instructions","Credits", "Highscore"]

    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                return "Exit"

        mousepos = mouse.get_pos()
        mb = mouse.get_pressed()

        #pic is the background picture.
        pic = image.load(BASEURL + "menubackground.png")
        pic = transform.smoothscale(pic, (1000, 601))

        
        screen.blit(pic, loc)
        screen.blit(menutext, (170,60))
        
        for i in range(len(boxes)):
            #box and value is the position in boxes and values.
            box = boxes[i]
            value = values[i]
            draw.rect(screen,(0,0,0),box)
            if box.collidepoint(mousepos):
                draw.rect(screen,(0,255,0),box,2)
                if mb[0]==1:
                    return value
            else:
                draw.rect(screen,(255,0,0),box,2)
            #textpic is the rendering of value.
            textPic = timesnewromanfont.render(value, True, (255,255,255))
            screen.blit(textPic,(box.x+40,box.y+25))            
                
        display.flip()


def getName():
    '''Function made by Mr. Mckenzie with a few small changes. This function gets
    the player's name and lets them type it in and blits it on the screen.'''
    #contains the name of the player.
    name = ""                
    # copy screen so we can replace it when done
    back = screen.copy()
    #area of the box around the text
    textArea = Rect(385,450,120,50)
    
    typing = True
    while typing:
        for e in event.get():
            # puts QUIT back in event list so main quits
            if e.type == QUIT:
                event.post(e)   
                return ""
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    typing = False
                    name = ""
                # remove last letter
                elif e.key == K_BACKSPACE:   
                    if len(name)>0:
                        name = name[:-1]
                #if you click enter or return it stops typing
                elif e.key == K_KP_ENTER or e.key == K_RETURN : 
                    typing = False
                elif e.key < 256 and len(name) <= 6:
                    name += e.unicode 
                        

        titlepic = timesnewromanfont2.render("Enter your name: ", True, (255,255,255))
        txtPic = timesnewromanfont2.render(name, True, (0,0,0))   
        draw.rect(screen,(220,255,220),textArea)        
        draw.rect(screen,(0,0,0),textArea,2)            
        screen.blit(titlepic, (350,410))
        screen.blit(txtPic,(textArea.x+3,textArea.y+2))        
        display.flip()
        
    screen.blit(back,(0,0))
    return name

def textfileaddition():
    '''The textfileaddition adds the name and points to a text file if it is in
    the top ten. Used example of highscores and applied it.'''
    global points

    #newname is the return of the getName function
    newname = getName()
    if newname != "":
    #Scorefile is the file with all the scores and names
        scorefile = open(BASEURL + "score.txt")

    #list of tuples with the score and name of the person.
        scores = []

        for i in range(10):
            name = scorefile.readline().strip()
            score = int(scorefile.readline().strip())
            scores.append((score, name))

        if points > scores[-1][0]:
            scores.append((points, newname))
            scores.sort(reverse=True)

            out = open(BASEURL + "score.txt", "w")
            for s, n in scores[:10]:
                out.write(n+"\n" + str(s) + "\n")
            out.close()


def highscore():
    '''Displays and makes everything in the highscorer menu including the back button.'''
    loc = (0,0)
    
    backmenu = [Rect(750,500,250,40), "Back to the Game"]

    #scorefile is the .txt file with all the scores and namees
    scorefile = open(BASEURL + "score.txt")
    #pic is the background picture.
    pic = image.load(BASEURL + "menubackground.png")
    picture = transform.smoothscale(pic, (1000, 601))

    #hightitle is the title for the highscorers menu.
    hightitle = timesnewromanfont3.render("Highscorers", True, (255,255,255))

    def backmenudraw():
        backPic = timesnewromanfont2.render(backmenu[1], True, (255,255,255))
        draw.rect(screen, (0,0,0), backmenu[0])
        backPic = timesnewromanfont2.render(backmenu[1], True, (255,255,255))
        screen.blit(backPic,(backmenu[0].x+6,backmenu[0].y+4))

        
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                return "Exit"

        mousepos = mouse.get_pos()
        mb = mouse.get_pressed()

        screen.blit(picture, loc)

        screen.blit(hightitle, (310,20))
        
        backmenudraw()
        
        for i in range(11):
            #loc is the location of the names.
            loc = (350,45*i+120)
            #loc2 is the locations of the scores.
            loc2 =(550,45*i+120)
            #name is the name of the high scorers.
            name = scorefile.readline().strip()
            #score is the score of the high scorers.
            score = scorefile.readline().strip()
            #turns the name into text. 
            namerender = timesnewromanfont4.render(name, True, (255,0,0),2)
            screen.blit(namerender, loc)
            #turns the score into text. 
            scorerender = timesnewromanfont4.render(score, True, (255,0,0),2)
            screen.blit(scorerender, loc2)

        draw.line(screen, (255,0,0), (490, 120), (490,580), 2)
        
        if backmenu[0].collidepoint(mousepos):
            draw.rect(screen,(0,255,0),backmenu[0],2)
            if mb[0]==1:
                return "Menu"
        else:
            draw.rect(screen,(255,0,0),backmenu[0],2)
            
        display.flip()


screen = display.set_mode((1000, 601))
running = True

#screen1 is the screen you are on in the game.
screen1 = "Menu"
#musicscreen is the music playing at each screen.
musicscreen = "Menu"

#This part of the code calls the screen according to a string that is returned when buttons are clicked in the menus.
#Changes the music according to the screen as well.
while screen1 != "Exit":

    if screen1 == "Menu":
        ammo = 20
        for i in range(len(badguys)):
            badguys[i][STATUS] = "off"
        points = 0
        lives = 3
        musicscreen = "Menu"
        music()
        screen1 = menu()
        
    elif screen1 == "Play":
        musicscreen = "Game"
        music()
        screen1 = Game()
        
    elif screen1 == "Instructions":
        screen1 = instructions()
        
    elif screen1 == "Credits":
        screen1 = credit()
        
    elif screen1 == "Pause":
        musicscreen = "Pause"
        music()
        screen1 = pause()
        
    elif screen1 == "Highscore":
        musicscreen = "Highscore"
        music()
        screen1 = highscore()

    
quit()
