# -*- coding: utf-8 -*-
BLUE = 0
YELLOW = 1
BLACK = 2
RED = 3

COLORS = [ BLUE, YELLOW, BLACK, RED ]

# BLUE
SF = 0
CHI = 1
MON =2
NY = 3
WAS = 4
ATL = 5
MAD = 6
LON = 7
PAR = 8
MIL = 9
ESS = 10
STP = 11

# YELLOW
LA = 12
MC = 13
MIA = 14
BOG = 15
LIM = 16
SAN = 17
BA = 18
SP = 19
LAG = 20
KIN = 21
KHA = 22
JOH = 23

# BLACK
CAI = 24
ALG = 25
IST = 26
MOS = 27
TEH = 28
BAG = 29
RIY = 30
KAR = 31
DEL = 32
MUM = 33
CHE = 34
KOL = 35

# RED
BAN = 36
HK = 37
SHA = 38
BEI = 39
SEO = 40
TOK = 41
OSA = 42
TAI = 43
MAN = 44
HCM = 45
JAK = 46
SYD = 47

# EVENT CARDS
GG = 48
FORECAST = 49
AIRLIFT = 50
OQN = 51
RP = 52

# EPIDEMIC
EPIDEMIC = 53

CITIES = [
    {'name': 'San Francisco', 'population': 5864 },
    {'name': 'Chicago', 'population': 9121 },
    {'name': 'Atlanta', 'population': 4715 },
    {'name': 'Montreal', 'population': 3429 },
    {'name': 'Washington', 'population': 4679 },
    {'name': 'New York', 'population': 20464 },
    {'name': 'London', 'population': 8586 },
    {'name': 'Madrid', 'population': 5427 },
    {'name': 'Paris', 'population': 10755 },
    {'name': 'Essen', 'population': 575 },
    {'name': 'Milan', 'population': 5232 },
    {'name': 'St. Petersburg', 'population': 4879 },

    {'name': 'Los Angeles', 'population': 14900 },
    {'name': 'Mexico City', 'population': 19463 },
    {'name': 'Miami', 'population': 5582 },
    {'name': 'Bogotá', 'population': 8702 },
    {'name': 'São Paulo', 'population': 20186 },
    {'name': 'Lima', 'population': 9121 },
    {'name': 'Santiago', 'population': 6015 },
    {'name': 'Buenos Aires', 'population': 13639 },
    {'name': 'Lagos', 'population': 11547 },
    {'name': 'Kinshasa', 'population': 9046 },
    {'name': 'Khartoum', 'population': 4887 },
    {'name': 'Johannesburg', 'population': 3888 },

    {'name': 'Algiers', 'population': 2946 },
    {'name': 'Istanbul', 'population': 13576 },
    {'name': 'Moscow', 'population': 15512 },
    {'name': 'Tehran', 'population': 7419 },
    {'name': 'Baghdad', 'population': 6204 },
    {'name': 'Cairo', 'population': 14718 },
    {'name': 'Riyadh', 'population': 5037 },
    {'name': 'Karachi', 'population': 20711 },
    {'name': 'Delhi', 'population': 22242 },
    {'name': 'Mumbai', 'population': 16910 },
    {'name': 'Chennai', 'population': 8865 },
    {'name': 'Kolkata', 'population': 14374 },

    {'name': 'Beijing', 'population': 17311 },
    {'name': 'Seoul', 'population': 22547 },
    {'name': 'Tokyo', 'population': 13189 },
    {'name': 'Shanghai', 'population': 13482 },
    {'name': 'Hong Kong', 'population': 7106 },
    {'name': 'Taipei', 'population': 8338 },
    {'name': 'Osaka', 'population': 2871 },
    {'name': 'Bangkok', 'population': 7151 },
    {'name': 'Ho Chi Minh City', 'population': 8314 },
    {'name': 'Manila', 'population': 20767 },
    {'name': 'Jakarta', 'population': 26063 },
    {'name': 'Sydney', 'population': 3785 },
]

EVENT_C = ['Government Grant', 'Forecast', 'Airlift', 'One Quiet Night', 'Resilient Population']

# ROLES
CP = 'Contingency Planner'
DISPATCHER = 'Dispatcher'
MEDIC = 'Medic'
OE = 'Operations Expert'
QS = 'Quarantine Specialist'
RESEARCHER = 'Researcher'
SCIENTIST = 'Scientist'

ROLES = [CP, DISPATCHER, MEDIC, OE, QS, RESEARCHER, SCIENTIST]

NUM_CITIES = 48
MAX_CUBES = 3
MAX_INFECT = 4
MAX_OUTBREAKS = 8
MAX_CARDS = 7
NUM_CUBES = 24
MAX_ACTIONS = 4
MAX_STATIONS = 6
NUM_PLAYER_CARDS = 53
CITIES_PER_COLOR = 12

## Phases
DRAW = 0

EPIDEMIC_T = 1

INFECT_1 = 2
INFECT_2 = 3
INFECT_3 = 4
INFECT_4 = 5

OUTBREAK = 6

ACTIONS = 7

INACTIVE = 8
