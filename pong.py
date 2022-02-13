import cv2
import numpy as np
from pynput.keyboard import Key, Listener, KeyCode






velikost_y = 720    # vyska
velikost_x = 1280   # sirka
velikost_micek = 15
rychlost = 1
barva_micku = (255,255,255)     #BGR
barva_skore = (120, 220, 0)
barva_palka = (255,0,0)

##############################################
posun_x = 1
posun_y = 1
predchozi_x = int(velikost_x/2)
predchozi_y = int(velikost_y/2)
predchozi_bot = int(velikost_y/2)
skore1 = 0
skore2 = 0
palka = 75  # polovina velikosti palky
predchozi_palka = 360
posun_palka = 0
keycode = None


def on_press(key):
    global keycode
    keycode = key

def on_release(key):
    global keycode
    keycode = None

def reset():
    image=np.zeros((velikost_y,velikost_x,3),np.uint8)
    cv2.putText(image, "press any key to continue", (int(velikost_x/2-200),int(velikost_y/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, [255,255,255], 2, cv2.LINE_AA)
    cv2.putText(image, str(skore1), (280,100), cv2.FONT_HERSHEY_SIMPLEX, 1, barva_skore, 2, cv2.LINE_AA)                #skore2
    cv2.putText(image, str(skore2), (1000,100), cv2.FONT_HERSHEY_SIMPLEX, 1, barva_skore, 2, cv2.LINE_AA)               #skore1
    global predchozi_palka
    predchozi_palka = 360
    global predchozi_x
    predchozi_x = int(velikost_x/2)
    global predchozi_y 
    predchozi_y = int(velikost_y/2)
    cv2.imshow('Pong',image)
    cv2.waitKey(0)

def bot(predchozi_y,predchozi_bot):
    if predchozi_y > predchozi_bot:
        posun_bot = 1
    else:
        posun_bot = -1
    if predchozi_bot+palka > 720:     #checkovani bota(pozice aby nevyjela ven)
        predchozi_bot=720-palka
        posun_bot = 0
    if predchozi_bot-palka < 0:
        predchozi_bot=0+palka
        posun_bot=0
    cv2.rectangle(image, (1265,predchozi_bot+posun_bot-palka), (1270,predchozi_bot+posun_bot+palka), [0,0,255], -1)
    predchozi_bot += posun_bot
    return(predchozi_bot)


with Listener(on_press=on_press, on_release=on_release) as listener:
    while(True):
        
        image=np.zeros((velikost_y,velikost_x,3),np.uint8)
        cv2.putText(image, str(skore1), (280,100), cv2.FONT_HERSHEY_SIMPLEX, 1, barva_skore, 2, cv2.LINE_AA)                # skore2
        cv2.putText(image, str(skore2), (1000,100), cv2.FONT_HERSHEY_SIMPLEX, 1, barva_skore, 2, cv2.LINE_AA)               # skore1

        if predchozi_palka+palka > 720:     # checkovani palky(pozice aby nevyjela ven)
            predchozi_palka=720-palka
            posun_palka = 0
        if predchozi_palka-palka < 0:
            predchozi_palka=0+palka
            posun_palka=0
        cv2.circle(image,(int(predchozi_x+posun_x),int(predchozi_y+posun_y)),velikost_micek,barva_micku,-1)                       # micek
        cv2.rectangle(image, (10,predchozi_palka+posun_palka-palka), (15,predchozi_palka+posun_palka+palka), barva_palka, -1)     # palka
        predchozi_palka += posun_palka
        posun_palka = 0
        predchozi_x += posun_x
        predchozi_y += posun_y
        if predchozi_x > int(velikost_x/2):
            predchozi_bot = bot(predchozi_y,predchozi_bot)
        cv2.rectangle(image, (1265,predchozi_bot-palka), (1270,predchozi_bot+palka), [0,0,255], -1)


        if predchozi_y > 720 - velikost_micek:      # odrazeni od stropu a podlahy
            posun_y *= -1
        if predchozi_y < 0 + velikost_micek:
            posun_y *= -1

        if predchozi_x > 1280 - velikost_micek:     # naraz u bota
            if predchozi_y > predchozi_bot-palka and predchozi_y < predchozi_bot + palka:
                posun_x *= -1
            else:
                skore1 += 1
                reset()

        if predchozi_x < 0 + velikost_micek:        # naraz u hrace
            if predchozi_y > predchozi_palka-palka and predchozi_y < predchozi_palka + palka:
                posun_x *= -1
            else:
                skore2 += 1
                reset()

        if keycode == Key.esc or keycode == KeyCode.from_char('q'):
            break
        if keycode == KeyCode.from_char('w'):
            posun_palka = -rychlost
        if keycode == KeyCode.from_char('s'):
            posun_palka = rychlost
        cv2.waitKey(1)
        cv2.imshow('Pong',image)
