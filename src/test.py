from constants import *
import game as g

roles = [MEDIC, RESEARCHER, OE, CP]

game = g.Game(roles, 5)
game.fillPlayerDeck()
game.setPlayerDeck()
game.fillInfectDeck()

c1 = JAK
c2 = BAN
print(c1, c2)
game.infect(c1, c1//12, 3)
game.resetOutbreaks()
game.infect(c2, c2//12, 4)
game.resetOutbreaks()

def success():
    jak = game.cubes[JAK][RED] == 3
    ban = game.cubes[BAN][RED] == 3
    che = game.cubes[CHE][RED] == 2
    hcm = game.cubes[HCM][RED] == 2
    syd = game.cubes[SYD][RED] == 1
    hk = game.cubes[HK][RED] == 1
    kol = game.cubes[KOL][RED] == 1
    return jak and ban and che and hcm and syd and hk and kol

game.cures[RED] = True

def setResearcher():
    game.players[1].getCard(LA)

def setOE():
    game.players[2].getCard(JAK)
    game.players[2].move(JAK)

def setQS():
    game.players[3].move(JAK)
    game.quarantineCities(game.players[3])


setResearcher()
setOE()
setQS()

game.canShare(LA, game.players[1], game.players[0])
game.share(LA, game.players[1], game.players[0])

game.players[0].move(JAK)
game.medicWithCure(game.players[0])


print(game.canShare(JAK, game.players[2], game.players[0]))
game.share(JAK, game.players[2], game.players[0])

game.players[2].move(BAG)
game.buildStation(BAG, game.players[2])

game.infect(BA, BA // 12, 4)

if game.players[0].hasCard(JAK) and game.players[0].hasCard(LA):
    print("TRADING SUCCESS!")
else:
    print("TRADING uh-oh")

for card in game.players[0].hand:
    print (card)


print (game.quarantined)
if game.cubes[BA][YELLOW] == 0 and game.cubes[SP][YELLOW] == 0 and game.cubes[BOG][YELLOW] == 0:
    print ("QUARANTINE SUCCESS!")
else:
    print ("QUARANTINE uh-oh")
