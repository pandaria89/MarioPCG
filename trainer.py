import os
from random import randint
#from reverend.thomas import Bayes
#trainer = Bayes()

probs = {}
def _train(inp, outp):
    global probs
    if inp not in probs.keys():
        probs[inp] = {}
        probs[inp][outp] = 1
        return
    elif outp not in probs[inp].keys():
        probs[inp][outp] = 1
        return
    probs[inp][outp] += 1

def _guess(inp):
    global probs
    total = 0
    for key in probs[inp].keys():
        total += probs[inp][key]
    choice = randint(0,total)
    for key in probs[inp].keys():
        if choice - probs[inp][key] <= 0:
            return key
        choice = choice - probs[inp][key]


def get_next_lowest_block_ind(y,x,mparr):
    column = ""
    for horiz in mparr:
        column += horiz[x]
    
    for ind, block in enumerate(column[y:]):
        if block != "-":
            return ind
        return 

def get_rel_surfaces(y,x,mparr):
    column = ""
    for horiz in mparr:
        colummn += horiz[x]
    surfaces = []
#    for ind, block in enumerate(column):
#        if block != "-":

def is_jumping(mario):
    if mario["jump"] or mario["ypos"] not in [ind for ind, block in enumerate(mario["curr"][::-1]) if block == "#" or block == "?"]:
        return True
    return False

def train(parsed_ticks): # mario, nextblock, currblock, nbindex):
    #global trainer
    prev_xpos = 0
    prev_ypos = 0
    inp = ""
    keys = ["left", "right", "down", "jumping", "speed"]
    for key in keys:
        inp += str(parsed_ticks[0][key])
    for ticknum, mario in enumerate(parsed_ticks):
        if ticknum == len(parsed_ticks)-1:
            continue
        
        if mario["xpos"] != prev_xpos:
            mario_offset = mario["ypos"] - prev_ypos
            #trainer.
            _train(inp, mario["curr"]+":"+str(mario_offset)+":"+str(mario["ypos"]))
            prev_xpos = mario["xpos"]
            prev_ypos = mario["ypos"]
            inp = ""
        else:
            continue
        for key in keys:
            inp += str(mario[key])



for fn in os.listdir("./"):
    if fn == "trainer.py" or fn == "classifier":
        continue
    cf = ""
    with open(fn,"r") as f:
        cf = f.read()
    ticks = cf.split("\n")
    print fn
    parsed_ticks = []
    for tick in ticks[1:]:
        if tick == "":
            print "empty"
        else:
            tickarr = tick.split("\t")
            mario = {"ticknum":int(tickarr[0]),
                    "left":int(tickarr[1][0]),
                     "right":int(tickarr[1][1]),
                     "down":int(tickarr[1][2]),
                     "jump":int(tickarr[1][3]),
                     "speed":int(tickarr[1][4]),
                     "xpos":int(tickarr[2]),
                     "ypos":int(tickarr[3]),
                     "2prev":tickarr[4],
                     "prev":tickarr[5],
                     "curr":tickarr[6],
                     "next":tickarr[7]}
            mario["jumping"] = int(is_jumping(mario))
            parsed_ticks.append(mario)
    train(parsed_ticks)
#trainer.save("classifier")

f = open("astar_01.tsv","r")
sample = f.read().split("\n")
inp = []
for line in sample:
    if line != "":
        inp.append(line.split("\t")[1])

curry = 10
seed = "-----------#"
columns = [[seed, 0]]
mn = 0
mx = 0
tmpctr = 0
curryoff = 10
globalshift = 0
for keym in inp[15:]:
    guess = _guess(keym)
    guess = guess.split(":")
    shift = curry - int(guess[2]) - int(guess[1])
    globalshift += shift
    columns.append([guess[0], globalshift])
    curry = int(guess[2])
    if globalshift > mx:
        mx = globalshift
    if globalshift < mn:
        mn = globalshift
    if tmpctr < 10:
        print "shift: ", shift
        print "globalshift: ", globalshift
        print "guess[2]: ", guess[2]
        print "guess[1]: ", guess[1]
        print guess[0]
        print "======="
        tmpctr += 1
colheight = len(columns[0][0])
mx += colheight
height = (mx) - (mn)
height = height
print "mapheight: ", height
maparr = ["" for i in range(height)]
currx = 0
for column in columns:
    offset = column[1] + (mn*-1)
    ptr = offset+colheight-1
    #print "height: ", height
    #print "ptr: ", ptr
    for ind, char in enumerate(column[0][::-1]):
        maparr[ptr-ind] += char
    currx += 1
    pit = False
    hitgen = False
    lastchar = ""
    for ind, line in enumerate(maparr):
        if ind == 0:
            hitgen = False
            pit = False
            lastchar = ""
        if len(line) == currx:
            hitgen = True
            lastchar = line[-1]
            continue
        if lastchar == "-":
            pit = True
        if pit or not hitgen:
            maparr[ind] += "-"
        else:
            maparr[ind] += "#"

with open("genmap","w+") as f:
    for row in maparr:
        f.write(row + "\n")

