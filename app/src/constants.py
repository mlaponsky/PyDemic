# -*- coding: utf-8 -*-
BLUE = 0
YELLOW = 1
BLACK = 2
RED = 3
EVENT = 4

COLORS = [ BLUE, YELLOW, BLACK, RED ]
COLOR_IMG = [ '../static/img/cubes/blue_cube.svg',
              '../static/img/cubes/yellow_cube.svg',
              '../static/img/cubes/black_cube.svg',
              '../static/img/cubes/red_cube.svg' ]
COLOR_STRINGS = ['blue', 'yellow', 'black', 'red', 'event']

# BLUE
ATL = 0
CHI = 1
ESS = 2
LON = 3
MAD = 4
MIL = 5
MON =6
NY = 7
PAR = 8
STP = 9
SF = 10
WAS = 11

# YELLOW
BOG = 12
BA = 13
JOH = 14
KHA = 15
KIN = 16
LAG = 17
LIM = 18
LA = 19
MC = 20
MIA = 21
SAN = 22
SP = 23

# BLACK
ALG = 24
BAG = 25
CAI = 26
CHE = 37
DEL = 28
IST = 29
KAR = 30
KOL = 31
MOS = 32
MUM = 33
RIY = 34
TEH = 35

# RED
BAN = 36
BEI = 37
HCM = 38
HK = 39
JAK = 40
MAN = 41
OSA = 42
SEO = 43
SHA = 44
SYD = 45
TAI = 46
TOK = 47

# EVENT CARDS
AIRLIFT = 48
FORECAST = 49
GG = 50
OQN = 51
RP = 52

# EPIDEMIC
EPIDEMIC = 53

NUM_CITIES = 48
CARDS = [
    {'name': 'Atlanta', 'population': 4715, 'description': 'Population: 4,715,000', 'player_card': 'static/img/player_cards/atl.svg' },
    {'name': 'Chicago', 'population': 9121, 'description': 'Population: 9,121,000', 'player_card': 'static/img/player_cards/chi.svg' },
    {'name': 'Essen', 'population': 575, 'description': 'Population: 575,000', 'player_card': 'static/img/player_cards/ess.svg' },
    {'name': 'London', 'population': 8586, 'description': 'Population: 8,586,000', 'player_card': 'static/img/player_cards/lon.svg' },
    {'name': 'Madrid', 'population': 5427, 'description': 'Population: 5,427,000', 'player_card': 'static/img/player_cards/mad.svg' },
    {'name': 'Milan', 'population': 5232, 'description': 'Population: 5,232,000', 'player_card': 'static/img/player_cards/mil.svg' },
    {'name': 'Montreal', 'population': 3429, 'description': 'Population: 3,429,000', 'player_card': 'static/img/player_cards/mon.svg' },
    {'name': 'New York', 'population': 20464, 'description': 'Population: 20,464,000', 'player_card': 'static/img/player_cards/ny.svg' },
    {'name': 'Paris', 'population': 10755, 'description': 'Population: 10,755,000', 'player_card': 'static/img/player_cards/par.svg' },
    {'name': 'St. Petersburg', 'population': 4879, 'description': 'Population: 4,879,000', 'player_card': 'static/img/player_cards/stp.svg' },
    {'name': 'San Francisco', 'population': 5864, 'description': 'Population: 5,864,000', 'player_card': 'static/img/player_cards/sf.svg' },
    {'name': 'Washington', 'population': 4679, 'description': 'Population: 4,679,000', 'player_card': 'static/img/player_cards/was.svg' },

    {'name': 'Bogotá', 'population': 8702, 'description': 'Population: 8,702,000', 'player_card': 'static/img/player_cards/bog.svg' },
    {'name': 'Buenos Aires', 'population': 13639, 'description': 'Population: 13,639,000', 'player_card': 'static/img/player_cards/ba.svg' },
    {'name': 'Johannesburg', 'population': 3888, 'description': 'Population: 3,888,000', 'player_card': 'static/img/player_cards/joh.svg' },
    {'name': 'Khartoum', 'population': 4887, 'description': 'Population: 4,887,000', 'player_card': 'static/img/player_cards/kha.svg' },
    {'name': 'Kinshasa', 'population': 9046, 'description': 'Population: 9,046,000', 'player_card': 'static/img/player_cards/kin.svg' },
    {'name': 'Lagos', 'population': 11547, 'description': 'Population: 11,547,000', 'player_card': 'static/img/player_cards/lag.svg' },
    {'name': 'Lima', 'population': 9121, 'description': 'Population: 9,121,000', 'player_card': 'static/img/player_cards/lim.svg' },
    {'name': 'Los Angeles', 'population': 14900, 'description': 'Population: 14,900,000', 'player_card': 'static/img/player_cards/la.svg' },
    {'name': 'Mexico City', 'population': 19463, 'description': 'Population: 19,463,000', 'player_card': 'static/img/player_cards/mc.svg' },
    {'name': 'Miami', 'population': 5582, 'description': 'Population: 5,582,000', 'player_card': 'static/img/player_cards/mia.svg' },
    {'name': 'Santiago', 'population': 6015, 'description': 'Population: 6,015,000', 'player_card': 'static/img/player_cards/san.svg' },
    {'name': 'São Paulo', 'population': 20186, 'description': 'Population: 20,186,000', 'player_card': 'static/img/player_cards/sp.svg' },

    {'name': 'Algiers', 'population': 2946, 'description': 'Population: 2,946,000', 'player_card': 'static/img/player_cards/alg.svg' },
    {'name': 'Baghdad', 'population': 6204, 'description': 'Population: 6,204,000', 'player_card': 'static/img/player_cards/bag.svg' },
    {'name': 'Cairo', 'population': 14718, 'description': 'Population: 14,718,000', 'player_card': 'static/img/player_cards/cai.svg' },
    {'name': 'Chennai', 'population': 8865, 'description': 'Population: 8,865,000', 'player_card': 'static/img/player_cards/che.svg' },
    {'name': 'Delhi', 'population': 22242, 'description': 'Population: 22,242,000', 'player_card': 'static/img/player_cards/del.svg' },
    {'name': 'Istanbul', 'population': 13576, 'description': 'Population: 13,576,000', 'player_card': 'static/img/player_cards/ist.svg' },
    {'name': 'Karachi', 'population': 20711, 'description': 'Population: 20,711,000', 'player_card': 'static/img/player_cards/kar.svg' },
    {'name': 'Kolkata', 'population': 14374, 'description': 'Population: 14,374,000', 'player_card': 'static/img/player_cards/kol.svg' },
    {'name': 'Moscow', 'population': 15512, 'description': 'Population: 15,512,000', 'player_card': 'static/img/player_cards/mos.svg' },
    {'name': 'Mumbai', 'population': 16910, 'description': 'Population: 16,910,000', 'player_card': 'static/img/player_cards/mum.svg' },
    {'name': 'Riyadh', 'population': 5037, 'description': 'Population: 5,037,000', 'player_card': 'static/img/player_cards/riy.svg' },
    {'name': 'Tehran', 'population': 7419, 'description': 'Population: 7,419,000', 'player_card': 'static/img/player_cards/teh.svg' },

    {'name': 'Bangkok', 'population': 7151, 'description': 'Population: 7,151,000', 'player_card': 'static/img/player_cards/ban.svg' },
    {'name': 'Beijing', 'population': 17311, 'description': 'Population: 17,311,000', 'player_card': 'static/img/player_cards/bei.svg' },
    {'name': 'Ho Chi Minh City', 'population': 8314, 'description': 'Population: 8,314,000', 'player_card': 'static/img/player_cards/hcm.svg' },
    {'name': 'Hong Kong', 'population': 7106, 'description': 'Population: 7,106,000', 'player_card': 'static/img/player_cards/hk.svg' },
    {'name': 'Jakarta', 'population': 26063, 'description': 'Population: 26,063,000', 'player_card': 'static/img/player_cards/jak.svg' },
    {'name': 'Manila', 'population': 20767, 'description': 'Population: 20,767,000', 'player_card': 'static/img/player_cards/man.svg' },
    {'name': 'Osaka', 'population': 2871, 'description': 'Population: 2,871,000', 'player_card': 'static/img/player_cards/osa.svg' },
    {'name': 'Seoul', 'population': 22547, 'description': 'Population: 22,547,000', 'player_card': 'static/img/player_cards/seo.svg' },
    {'name': 'Shanghai', 'population': 13482, 'description': 'Population: 13,482,000', 'player_card': 'static/img/player_cards/sha.svg' },
    {'name': 'Sydney', 'population': 3785, 'description': 'Population: 3,785,000', 'player_card': 'static/img/player_cards/syd.svg' },
    {'name': 'Taipei', 'population': 8338, 'description': 'Population: 8,338,000', 'player_card': 'static/img/player_cards/tai.svg' },
    {'name': 'Tokyo', 'population': 13189, 'description': 'Population: 13,189,000', 'player_card': 'static/img/player_cards/tok.svg' },

    {'name': 'Airlift', 'population': 0, 'description': 'Move any pawn to any city.', 'player_card': 'static/img/player_cards/airlift.svg'},
    {'name': 'Forecast', 'population': 0, 'description': '(Not an action) Draw, look at, and rearrange the top 6 cards of the Infection Deck.', 'player_card': 'static/img/player_cards/forecast.svg'},
    {'name': 'Government Grant', 'population': 0, 'description': 'Add 1 research station to any city.', 'player_card': 'static/img/player_cards/gg.svg'},
    {'name': 'One Quiet Night', 'population': 0, 'description': 'Skip the next INFECT CITIES stage.', 'player_card': 'static/img/player_cards/oqn.svg'},
    {'name': 'Resilient Population', 'population': 0, 'description': 'Remove any card in the Infection Discard Pile from the game. You may play this between the INFECT and INTENSIFY steps of an epidemic.', 'player_card': 'static/img/player_cards/rp.svg'}
]

CITIES = CARDS[:NUM_CITIES]

EVENT_C = ['Government Grant', 'Forecast', 'Airlift', 'One Quiet Night', 'Resilient Population']

# ROLES
CP = 'Contingency Planner'
DISPATCHER = 'Dispatcher'
MEDIC = 'Medic'
OE = 'Operations Expert'
QS = 'Quarantine Specialist'
RESEARCHER = 'Researcher'
SCIENTIST = 'Scientist'

ROLES = { CP:         { 'id': 'cp',
                        'color': '#29a3a3',
                        'title_img': 'static/img/roles/cp_txt.svg',
                        'piece_img': 'static/img/roles/cp.svg'},
          DISPATCHER: { 'id': 'dispatcher',
                        'color': '#6b008f',
                        'title_img': 'static/img/roles/dispatcher_txt.svg',
                        'piece_img': 'static/img/roles/dispatcher.svg'},
          MEDIC:      { 'id': 'medic',
                        'color': '#ff9900',
                        'title_img': 'static/img/roles/medic_txt.svg',
                        'piece_img': 'static/img/roles/medic.svg'},
          OE:         { 'id': 'oe',
                        'color': '#248f24',
                        'title_img': 'static/img/roles/oe_txt.svg',
                        'piece_img': 'static/img/roles/oe.svg'},
          QS:         { 'id': 'qs',
                        'color': '#194719',
                        'title_img': 'static/img/roles/qs_txt.svg',
                        'piece_img': 'static/img/roles/qs.svg'},
          RESEARCHER: { 'id': 'researcher',
                        'color': '#663300',
                        'title_img': 'static/img/roles/researcher_txt.svg',
                        'piece_img': 'static/img/roles/researcher.svg'},
          SCIENTIST:  { 'id': 'scientist',
                        'color': '#888888',
                        'title_img': 'static/img/roles/scientist_txt.svg',
                        'piece_img': 'static/img/roles/scientist.svg'}}

MAX_CUBES = 3
MAX_INFECT = 4
MAX_OUTBREAKS = 8
MAX_CARDS = 7
NUM_CUBES = 24
MAX_ACTIONS = 4
MAX_STATIONS = 6
NUM_PLAYER_CARDS = 53
CITIES_PER_COLOR = 12
ERADICATED = 2

## Phases
INFECT_1 = 0
INFECT_2 = 1
INFECT_3 = 2
INFECT_4 = 3

DRAW = 4

ACTION_0 = 5
ACTION_1 = 6
ACTION_2 = 7
ACTION_3 = 8

INACTIVE = 20

EP_INCREASE = 9
EP_INFECT = 10
EP_INSTENSIFY = 11
