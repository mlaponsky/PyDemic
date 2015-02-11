# -*- coding: utf-8 -*-

import constants
import city

class Board:
    neighbors = {}
    numCities = 0
    numNeighbors = 0
    distance = 0

    def __init__(self):
        for num in range(constants.NUM_CITIES):
            self.neighbors[num] = []

    def add_neighbor(self, n1, n2):
        self.neighbors[n1].append(n2)
        self.neighbors[n2].append(n1)

    def fill_neighbors(self):
        # BLUE
        self.add_neighbor(constants.SF, constants.TOK)
        self.add_neighbor(constants.SF, constants.MAN)
        self.add_neighbor(constants.SF, constants.LA)
        self.add_neighbor(constants.SF, constants.CHI)

        self.add_neighbor(constants.CHI, constants.ATL)
        self.add_neighbor(constants.CHI, constants.MON)
        self.add_neighbor(constants.CHI, constants.LA)
        self.add_neighbor(constants.CHI, constants.MC)

        self.add_neighbor(constants.MON, constants.WAS)
        self.add_neighbor(constants.MON, constants.NY)

        self.add_neighbor(constants.NY, constants.WAS)
        self.add_neighbor(constants.NY, constants.MAD)
        self.add_neighbor(constants.NY, constants.LON)

        self.add_neighbor(constants.ATL, constants.WAS)
        self.add_neighbor(constants.ATL, constants.MIA)

        self.add_neighbor(constants.LON, constants.PAR)
        self.add_neighbor(constants.LON, constants.ESS)
        self.add_neighbor(constants.LON, constants.MAD)

        self.add_neighbor(constants.MAD, constants.PAR)
        self.add_neighbor(constants.MAD, constants.ALG)
        self.add_neighbor(constants.MAD, constants.SP)

        self.add_neighbor(constants.PAR, constants.ESS)
        self.add_neighbor(constants.PAR, constants.MIL)
        self.add_neighbor(constants.PAR, constants.ALG)

        self.add_neighbor(constants.ESS, constants.MIL)
        self.add_neighbor(constants.ESS, constants.STP)

        self.add_neighbor(constants.MIL, constants.IST)

        self.add_neighbor(constants.WAS, constants.MIA)

        self.add_neighbor(constants.STP, constants.MOS)
        self.add_neighbor(constants.STP, constants.IST)

        # YELLOW
        self.add_neighbor(constants.LA, constants.SYD)
        self.add_neighbor(constants.LA, constants.MC)

        self.add_neighbor(constants.MC, constants.MIA)
        self.add_neighbor(constants.MC, constants.BOG)
        self.add_neighbor(constants.MC, constants.LIM)

        self.add_neighbor(constants.MIA, constants.BOG)

        self.add_neighbor(constants.BOG, constants.BA)
        self.add_neighbor(constants.BOG, constants.LIM)
        self.add_neighbor(constants.BOG, constants.SP)

        self.add_neighbor(constants.SP, constants.BA)
        self.add_neighbor(constants.SP, constants.LAG)

        self.add_neighbor(constants.LIM, constants.SAN)

        self.add_neighbor(constants.LAG, constants.KIN)
        self.add_neighbor(constants.LAG, constants.KHA)

        self.add_neighbor(constants.KIN, constants.KHA)
        self.add_neighbor(constants.KIN, constants.JOH)

        self.add_neighbor(constants.KHA, constants.JOH)
        self.add_neighbor(constants.KHA, constants.CAI)

        # BLACK
        self.add_neighbor(constants.ALG, constants.IST)
        self.add_neighbor(constants.ALG, constants.CAI)

        self.add_neighbor(constants.MOS, constants.TEH)
        self.add_neighbor(constants.MOS, constants.IST)

        self.add_neighbor(constants.IST, constants.CAI)
        self.add_neighbor(constants.IST, constants.BAG)

        self.add_neighbor(constants.TEH, constants.DEL)
        self.add_neighbor(constants.TEH, constants.BAG)
        self.add_neighbor(constants.TEH, constants.KAR)

        self.add_neighbor(constants.BAG, constants.CAI)
        self.add_neighbor(constants.BAG, constants.RIY)
        self.add_neighbor(constants.BAG, constants.KAR)

        self.add_neighbor(constants.CAI, constants.RIY)

        self.add_neighbor(constants.RIY, constants.KAR)

        self.add_neighbor(constants.KAR, constants.DEL)
        self.add_neighbor(constants.KAR, constants.MUM)

        self.add_neighbor(constants.DEL, constants.MUM)
        self.add_neighbor(constants.DEL, constants.CHE)
        self.add_neighbor(constants.DEL, constants.KOL)

        self.add_neighbor(constants.MUM, constants.CHE)

        self.add_neighbor(constants.CHE, constants.KOL)
        self.add_neighbor(constants.CHE, constants.BAN)
        self.add_neighbor(constants.CHE, constants.JAK)

        self.add_neighbor(constants.KOL, constants.BAN)
        self.add_neighbor(constants.KOL, constants.HK)

        # RED
        self.add_neighbor(constants.BEI, constants.SHA)
        self.add_neighbor(constants.BEI, constants.SEO)

        self.add_neighbor(constants.SEO, constants.TOK)
        self.add_neighbor(constants.SEO, constants.SHA)

        self.add_neighbor(constants.TOK, constants.SHA)
        self.add_neighbor(constants.TOK, constants.OSA)

        self.add_neighbor(constants.SHA, constants.TAI)
        self.add_neighbor(constants.SHA, constants.HK)

        self.add_neighbor(constants.HK, constants.TAI)
        self.add_neighbor(constants.HK, constants.MAN)
        self.add_neighbor(constants.HK, constants.HCM)
        self.add_neighbor(constants.HK, constants.BAN)

        self.add_neighbor(constants.TAI, constants.OSA)
        self.add_neighbor(constants.TAI, constants.MAN)

        self.add_neighbor(constants.BAN, constants.JAK)
        self.add_neighbor(constants.BAN, constants.HCM)

        self.add_neighbor(constants.HCM, constants.MAN)
        self.add_neighbor(constants.HCM, constants.JAK)

        self.add_neighbor(constants.MAN, constants.SYD)
        self.add_neighbor(constants.JAK, constants.SYD)

    def get_neighbors(self, city):
        return self.neighbors[city]

    def get_distance(self, start, end):
        queue = []
        queue.append(start)
        if start == end:
            return self.distance
        else:
            self.distance += 1
            for neighbor in self.neighbors[start]:
                self.getDistance(neighbor, end)
