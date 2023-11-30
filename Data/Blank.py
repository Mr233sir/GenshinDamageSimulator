if __name__ == '__main__':
    from PublicData import *
else:
    exec('from Data.PublicData import attack_type, calc_buff, heal')
    exec('import copy')

info = {'Name_state': {'ATK': 0, 'HP': 0, 'DEF': 0, 'EM': 0, 'ER': 1.0, 'CR': 0.05, 'CD': 0.5, 'UP': 0.0,
                       'Healer': 0.0, 'Healee': 0.0, 'SS': 0.0},
        'Name_base': {'ATK': 0, 'HP': 0, 'DEF': 0, 'Element': ''},
        'Name_charge_max': 0,
        'Name_skill': {},
        'Name_ele': {},
        'Name_back': {},
        'Name_heal': {},
        'Name_energy': {},
        'Name_tough': ()}

name = {'Name': '中文名'}

# buff

# 行动

# 血条

# 协同

# 加速

buff_type = {}
buff_1 = []
buff_2 = []
buff_sp = []
act_lst = []
heal_lst = []
with_lst = []
