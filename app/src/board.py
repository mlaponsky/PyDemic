# -*- coding: utf-8 -*-

from .constants import *

class Board:
    def __init__(self):
        self.neighbors = []
        self.rows = []
        self.distance = 0
        for city in range(NUM_CITIES):
            self.neighbors.append([])
            self.rows.append([-1] * 4)
        self.fill_neighbors()

    def add_neighbor(self, n1, n2):
        self.neighbors[n1].append(n2)
        self.neighbors[n2].append(n1)

    def fill_neighbors(self):
        # BLUE
        self.add_neighbor(SF, TOK)
        self.add_neighbor(SF, MAN)
        self.add_neighbor(SF, LA)
        self.add_neighbor(SF, CHI)

        self.add_neighbor(CHI, ATL)
        self.add_neighbor(CHI, MON)
        self.add_neighbor(CHI, LA)
        self.add_neighbor(CHI, MC)

        self.add_neighbor(MON, WAS)
        self.add_neighbor(MON, NY)

        self.add_neighbor(NY, WAS)
        self.add_neighbor(NY, MAD)
        self.add_neighbor(NY, LON)

        self.add_neighbor(ATL, WAS)
        self.add_neighbor(ATL, MIA)

        self.add_neighbor(LON, PAR)
        self.add_neighbor(LON, ESS)
        self.add_neighbor(LON, MAD)

        self.add_neighbor(MAD, PAR)
        self.add_neighbor(MAD, ALG)
        self.add_neighbor(MAD, SP)

        self.add_neighbor(PAR, ESS)
        self.add_neighbor(PAR, MIL)
        self.add_neighbor(PAR, ALG)

        self.add_neighbor(ESS, MIL)
        self.add_neighbor(ESS, STP)

        self.add_neighbor(MIL, IST)

        self.add_neighbor(WAS, MIA)

        self.add_neighbor(STP, MOS)
        self.add_neighbor(STP, IST)

        # YELLOW
        self.add_neighbor(LA, SYD)
        self.add_neighbor(LA, MC)

        self.add_neighbor(MC, MIA)
        self.add_neighbor(MC, BOG)
        self.add_neighbor(MC, LIM)

        self.add_neighbor(MIA, BOG)

        self.add_neighbor(BOG, BA)
        self.add_neighbor(BOG, LIM)
        self.add_neighbor(BOG, SP)

        self.add_neighbor(LIM, SAN)
        self.add_neighbor(LIM, BA)

        self.add_neighbor(SP, BA)
        self.add_neighbor(SP, LAG)

        self.add_neighbor(LAG, KIN)
        self.add_neighbor(LAG, KHA)

        self.add_neighbor(KIN, KHA)
        self.add_neighbor(KIN, JOH)

        self.add_neighbor(KHA, JOH)
        self.add_neighbor(KHA, CAI)

        # BLACK
        self.add_neighbor(ALG, IST)
        self.add_neighbor(ALG, CAI)

        self.add_neighbor(MOS, TEH)
        self.add_neighbor(MOS, IST)

        self.add_neighbor(IST, CAI)
        self.add_neighbor(IST, BAG)

        self.add_neighbor(TEH, DEL)
        self.add_neighbor(TEH, BAG)
        self.add_neighbor(TEH, KAR)

        self.add_neighbor(BAG, CAI)
        self.add_neighbor(BAG, RIY)
        self.add_neighbor(BAG, KAR)

        self.add_neighbor(CAI, RIY)

        self.add_neighbor(RIY, KAR)

        self.add_neighbor(KAR, DEL)
        self.add_neighbor(KAR, MUM)

        self.add_neighbor(DEL, MUM)
        self.add_neighbor(DEL, CHE)
        self.add_neighbor(DEL, KOL)

        self.add_neighbor(MUM, CHE)

        self.add_neighbor(CHE, KOL)
        self.add_neighbor(CHE, BAN)
        self.add_neighbor(CHE, JAK)

        self.add_neighbor(KOL, BAN)
        self.add_neighbor(KOL, HK)

        # RED
        self.add_neighbor(BEI, SHA)
        self.add_neighbor(BEI, SEO)

        self.add_neighbor(SEO, TOK)
        self.add_neighbor(SEO, SHA)

        self.add_neighbor(TOK, SHA)
        self.add_neighbor(TOK, OSA)

        self.add_neighbor(SHA, TAI)
        self.add_neighbor(SHA, HK)

        self.add_neighbor(HK, TAI)
        self.add_neighbor(HK, MAN)
        self.add_neighbor(HK, HCM)
        self.add_neighbor(HK, BAN)

        self.add_neighbor(TAI, OSA)
        self.add_neighbor(TAI, MAN)

        self.add_neighbor(BAN, JAK)
        self.add_neighbor(BAN, HCM)

        self.add_neighbor(HCM, MAN)
        self.add_neighbor(HCM, JAK)

        self.add_neighbor(MAN, SYD)
        self.add_neighbor(JAK, SYD)

    def get_neighbors(self, city):
        return self.neighbors[city]

    def get_board(self):
        return self.neighbors

    def get_distance(self, start, end):
        queue = []
        queue.append(start)
        if start == end:
            return self.distance
        else:
            self.distance += 1
            for neighbor in self.neighbors[start]:
                self.getDistance(neighbor, end)

    def set_row(self, city, color):
        for row in range(3):
            if row not in self.rows[city]:
                self.rows[city][color] = row
                break

    def get_all_rows(self, city):
        return self.rows[city]

    def get_row(self, city, color):
        if self.rows[city][color] != -1:
            return self.rows[city][color]
        else:
            self.set_row(city, color)
            return self.rows[city][color]

    def delete_row(self, city, color):
        self.rows[city][color] = -1
        for c in COLORS:
            if self.rows[city][c] > 0:
                self.rows[city][c] -= 1
