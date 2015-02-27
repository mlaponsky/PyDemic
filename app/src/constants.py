# -*- coding: utf-8 -*-
BLUE = 0
YELLOW = 1
BLACK = 2
RED = 3
EVENT = 4

COLORS = [ BLUE, YELLOW, BLACK, RED, EVENT ]
COLOR_STRINGS = ['blue', 'yellow', 'black', 'red', 'event']

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

CARDS = [
    {'name': 'San Francisco', 'population': 5864, 'player_card': 'static/img/player_cards/sf.svg' },
    {'name': 'Chicago', 'population': 9121, 'player_card': 'static/img/player_cards/chi.svg' },
    {'name': 'Montreal', 'population': 3429, 'player_card': 'static/img/player_cards/mon.svg' },
    {'name': 'New York', 'population': 20464, 'player_card': 'static/img/player_cards/ny.svg' },
    {'name': 'Washington', 'population': 4679, 'player_card': 'static/img/player_cards/was.svg' },
    {'name': 'Atlanta', 'population': 4715, 'player_card': 'static/img/player_cards/atl.svg' },
    {'name': 'Madrid', 'population': 5427, 'player_card': 'static/img/player_cards/mad.svg' },
    {'name': 'London', 'population': 8586, 'player_card': 'static/img/player_cards/lon.svg' },
    {'name': 'Paris', 'population': 10755, 'player_card': 'static/img/player_cards/par.svg' },
    {'name': 'Milan', 'population': 5232, 'player_card': 'static/img/player_cards/mil.svg' },
    {'name': 'Essen', 'population': 575, 'player_card': 'static/img/player_cards/ess.svg' },
    {'name': 'St. Petersburg', 'population': 4879, 'player_card': 'static/img/player_cards/stp.svg' },

    {'name': 'Los Angeles', 'population': 14900, 'player_card': 'static/img/player_cards/la.svg' },
    {'name': 'Mexico City', 'population': 19463, 'player_card': 'static/img/player_cards/mc.svg' },
    {'name': 'Miami', 'population': 5582, 'player_card': 'static/img/player_cards/mia.svg' },
    {'name': 'Bogotá', 'population': 8702, 'player_card': 'static/img/player_cards/bog.svg' },
    {'name': 'Lima', 'population': 9121, 'player_card': 'static/img/player_cards/lim.svg' },
    {'name': 'Santiago', 'population': 6015, 'player_card': 'static/img/player_cards/san.svg' },
    {'name': 'Buenos Aires', 'population': 13639, 'player_card': 'static/img/player_cards/ba.svg' },
    {'name': 'São Paulo', 'population': 20186, 'player_card': 'static/img/player_cards/sp.svg' },
    {'name': 'Lagos', 'population': 11547, 'player_card': 'static/img/player_cards/lag.svg' },
    {'name': 'Kinshasa', 'population': 9046, 'player_card': 'static/img/player_cards/kin.svg' },
    {'name': 'Khartoum', 'population': 4887, 'player_card': 'static/img/player_cards/kha.svg' },
    {'name': 'Johannesburg', 'population': 3888, 'player_card': 'static/img/player_cards/joh.svg' },

    {'name': 'Cairo', 'population': 14718, 'player_card': 'static/img/player_cards/cai.svg' },
    {'name': 'Algiers', 'population': 2946, 'player_card': 'static/img/player_cards/alg.svg' },
    {'name': 'Istanbul', 'population': 13576, 'player_card': 'static/img/player_cards/ist.svg' },
    {'name': 'Moscow', 'population': 15512, 'player_card': 'static/img/player_cards/mos.svg' },
    {'name': 'Tehran', 'population': 7419, 'player_card': 'static/img/player_cards/teh.svg' },
    {'name': 'Baghdad', 'population': 6204, 'player_card': 'static/img/player_cards/bag.svg' },
    {'name': 'Riyadh', 'population': 5037, 'player_card': 'static/img/player_cards/riy.svg' },
    {'name': 'Karachi', 'population': 20711, 'player_card': 'static/img/player_cards/kar.svg' },
    {'name': 'Delhi', 'population': 22242, 'player_card': 'static/img/player_cards/del.svg' },
    {'name': 'Mumbai', 'population': 16910, 'player_card': 'static/img/player_cards/mum.svg' },
    {'name': 'Chennai', 'population': 8865, 'player_card': 'static/img/player_cards/che.svg' },
    {'name': 'Kolkata', 'population': 14374, 'player_card': 'static/img/player_cards/kol.svg' },

    {'name': 'Bangkok', 'population': 7151, 'player_card': 'static/img/player_cards/ban.svg' },
    {'name': 'Hong Kong', 'population': 7106, 'player_card': 'static/img/player_cards/hk.svg' },
    {'name': 'Shanghai', 'population': 13482, 'player_card': 'static/img/player_cards/sha.svg' },
    {'name': 'Beijing', 'population': 17311, 'player_card': 'static/img/player_cards/bei.svg' },
    {'name': 'Seoul', 'population': 22547, 'player_card': 'static/img/player_cards/seo.svg' },
    {'name': 'Tokyo', 'population': 13189, 'player_card': 'static/img/player_cards/tok.svg' },
    {'name': 'Osaka', 'population': 2871, 'player_card': 'static/img/player_cards/osa.svg' },
    {'name': 'Taipei', 'population': 8338, 'player_card': 'static/img/player_cards/tai.svg' },
    {'name': 'Manila', 'population': 20767, 'player_card': 'static/img/player_cards/man.svg' },
    {'name': 'Ho Chi Minh City', 'population': 8314, 'player_card': 'static/img/player_cards/hcm.svg' },
    {'name': 'Jakarta', 'population': 26063, 'player_card': 'static/img/player_cards/jak.svg' },
    {'name': 'Sydney', 'population': 3785, 'player_card': 'static/img/player_cards/syd.svg' },

    {'name': 'Government Grant', 'population': 0, 'player_card': 'static/img/player_cards/gg.svg'},
    {'name': 'Forecast', 'population': 0, 'player_card': 'static/img/player_cards/forecast.svg'},
    {'name': 'Airlift', 'population': 0, 'player_card': 'static/img/player_cards/airlift.svg'},
    {'name': 'One Quiet Night', 'population': 0, 'player_card': 'static/img/player_cards/oqn.svg'},
    {'name': 'Resilient Population', 'population': 0, 'player_card': 'static/img/player_cards/rp.svg'}
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

ROLES = { CP:         {'color': '#29a3a3',
                       'title_img': 'static/img/roles/cp_txt.svg',
                       'piece_img': 'static/img/roles/cp.svg'},
          DISPATCHER: {'color': '#6b008f',
                       'title_img': 'static/img/roles/dispatcher_txt.svg',
                       'piece_img': 'static/img/roles/dispatcher.svg'},
          MEDIC:      {'color': '#ff9900',
                       'title_img': 'static/img/roles/medic_txt.svg',
                       'piece_img': 'static/img/roles/medic.svg'},
          OE:         {'color': '#248f24',
                       'title_img': 'static/img/roles/oe_txt.svg',
                       'piece_img': 'static/img/roles/oe.svg'},
          QS:         {'color': '#194719',
                       'title_img': 'static/img/roles/qs_txt.svg',
                       'piece_img': 'static/img/roles/qs.svg'},
          RESEARCHER: {'color': '#663300',
                       'title_img': 'static/img/roles/researcher_txt.svg',
                       'piece_img': 'static/img/roles/researcher.svg'},
          SCIENTIST:  {'color': '#888888',
                       'title_img': 'static/img/roles/scientist_txt.svg',
                       'piece_img': 'static/img/roles/scientist.svg'}}

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
