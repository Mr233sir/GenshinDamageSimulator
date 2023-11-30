if __name__ == '__main__':
    from PublicData import *
else:
    exec('from Data.PublicData import attack_type, calc_buff, heal')
    exec('import copy')

info = {
    'Furina_state': {'ATK': 1006, 'HP': 36347, 'DEF': 769, 'EM': 54, 'ER': 2.05, 'CR': 0.549, 'CD': 1.972,
                     'UP_Hydro': 0.0, 'Healer': 0.0, 'Healee': 0.0, 'SS': 0.0},
    'Furina_base': {'ATK': 645, 'HP': 15307, 'DEF': 696, 'Element': 'Hydro'},
    'Furina_charge_max': 60,
    'Furina_skill': {'e': ('HP', 0.1337, 18, 39), 'q': ('HP', 0.1939, 94, 0), 'q0': ('', 0.0, 15)},
    'Furina_ele': {'Furina_e1': ('Hydro', 1, 2, False, 'Furina_e1'),
                   'Furina_e2': ('Hydro', 1, 2, False, 'Furina_e2'),
                   'Furina_e3': ('Hydro', 1, False, False, ''), 'q': ('Hydro', 1, False, False, ''),
                   'e': ('Hydro', 1, False, False, ''), 'q0': ('', 0, False, False, '')},
    'Furina_back': {'Furina_e1': ('HP', 0.0549, 72, 72), 'Furina_e2': ('HP', 0.1013, 174, 174),
                    'Furina_e3': ('HP', 0.1409, 144, 288)},
    'Furina_heal': {'Furina_e1': ('minus', 0.016, 0, False), 'Furina_e2': ('minus', 0.024, 0, False),
                    'Furina_e3': ('minus', 0.036, 0, False)}, 'Furina_tough': (100, 5),
    'Furina_energy': {'Furina_e1': (1, 150, 'Furina_e'), 'Furina_e2': (1, 150, 'Furina_e'),
                      'Furina_e3': (1, 150, 'Furina_e')}}

name = {'Furina': '芙宁娜'}


# buff
def dawn(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp, party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Dawn' in buff_type and char in buff_type.get('Ferryman', []) and moment_hp[char] >= 0.9:
        buff_['CR'] = 0.28
    return buff_, buff_type_, debuff_


def ferryman(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp,
             party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Ferryman' in buff_type and char in buff_type.get('Ferryman', []) and now == 'e':
        buff_type['Ferryman_'] = [frame, frame + 300]
    if 'Ferryman' in buff_type and char in buff_type.get('Ferryman', []) and attack_type(now) == 'e':
        buff_['CR'] = 0.16
    if 'Ferryman_' in buff_type and char in buff_type.get('Ferryman', []):
        if int(buff_type['Ferryman_'][0]) <= frame < int(buff_type['Ferryman_'][1]):
            buff_['ER'] = 0.32
    return buff_, buff_type_, debuff_


def furina_e_(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp,
              party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    add = 0.0
    if 'Furina_e' in buff_type and char in buff_type.get('Furina_e', []) and now in ['Furina_e1', 'Furina_e2',
                                                                                     'Furina_e3']:
        for k in moment_hp:
            if moment_hp[k] > 0.5:
                add += 0.1
        buff_['extra'] = add * info['Furina_back'][now][1] * state_act['HP']
    return buff_, buff_type_, debuff_


def furina_q_(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp,
              party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Furina_q' in buff_type and char in buff_type.get('Furina_q', []) and now == 'q':
        buff_type['Furina_q_'] = [frame, frame + 1080]
    if 'Furina_q_' in buff_type and char in stand.values():
        if int(buff_type['Furina_q_'][0]) <= frame < int(buff_type['Furina_q_'][1]):
            buff_['UP'] = min(change_hp_per * 0.23, 0.69)
            buff_['Healee'] = min(change_hp_per * 0.09, 0.23)
        if 'Furina_c2' in buff_type and char in buff_type.get('Furina_c2', []) and change_hp_per * 3.5 > 4:
            buff_['HP_per'] = min((change_hp_per * 3.5 - 4) * 0.35, 1.4)

    return buff_, buff_type_, debuff_


def golden(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp, party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Golden' in buff_type and char in buff_type.get('Golden', []) and attack_type(now) == 'e':
        buff_['UP'] = 0.45
        if char != forward:
            buff_['UP'] = 0.7
    return buff_, buff_type_, debuff_


def furina_psv_2(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp,
                 party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Furina_psv_2' in buff_type and char in buff_type.get('Furina_psv_2', []) and now in ['Furina_e1', 'Furina_e2',
                                                                                             'Furina_e3']:
        buff_['UP'] = min(info[char + '_state']['HP'] * 0.000007, 0.28)
    return buff_, buff_type_, debuff_


# 行动
def furina_e(frame, now, forward):
    sequence_act_ = []
    sequence_heal_ = []
    if now == 'e' and forward == 'Furina':
        frame += info['Furina_skill']['e'][2]
        sequence_act_.append([frame, forward, 'e'])
        for i in range(int(info['Furina_back']['Furina_e1'][2]), 1800, int(info['Furina_back']['Furina_e1'][3])):
            sequence_act_.append([frame + i, 'back', 'Furina_e1'])
            sequence_heal_.append([frame + i, 'Furina_e1'])
        for i in range(int(info['Furina_back']['Furina_e2'][2]), 1800, int(info['Furina_back']['Furina_e2'][3])):
            sequence_act_.append([frame + i, 'back', 'Furina_e2'])
            sequence_heal_.append([frame + i, 'Furina_e2'])
        for i in range(int(info['Furina_back']['Furina_e3'][2]), 1800, int(info['Furina_back']['Furina_e3'][3])):
            sequence_act_.append([frame + i, 'back', 'Furina_e3'])
            sequence_heal_.append([frame + i, 'Furina_e3'])
        frame += info['Furina_skill']['e'][3]
        return frame, sequence_act_, sequence_heal_


def furina_q(frame, now, forward):
    if now == 'q' and forward == 'Furina':
        sequence_act_ = [[frame, forward, 'q0']]
        frame += info['Furina_skill']['q'][2]
        sequence_act_.append([frame, forward, 'q'])
        frame += info['Furina_skill']['q'][3]
        return frame, sequence_act_, []


# 血条
def furina_e1_heal(frame, now, char, forward, info, act, buff_type_, stand, change_hp_per, base_, state_, buff_1,
                   buff_2, moment_hp, party_element):
    for k in moment_hp:
        if moment_hp[k] > 0.5:
            moment_hp[k] -= 0.016
    return moment_hp, 0


def furina_e2_heal(frame, now, char, forward, info, act, buff_type_, stand, change_hp_per, base_, state_, buff_1,
                   buff_2, moment_hp, party_element):
    for k in moment_hp:
        if moment_hp[k] > 0.5:
            moment_hp[k] -= 0.024
    return moment_hp, 0


def furina_e3_heal(frame, now, char, forward, info, act, buff_type_, stand, change_hp_per, base_, state_, buff_1,
                   buff_2, moment_hp, party_element):
    for k in moment_hp:
        if moment_hp[k] > 0.5:
            moment_hp[k] -= 0.036
    return moment_hp, 0


def furina_psv_1_heal(frame, now, char, forward, info, act, buff_type_, stand, change_hp_per, base_, state_, buff_1,
                      buff_2, moment_hp, party_element):
    char = 'Furina'
    state_act, debuff, buff_type_ = calc_buff(frame, now, char, forward, info, act, buff_type_, stand, change_hp_per,
                                              base_, state_, buff_1, buff_2, moment_hp, party_element)

    fix_ = heal(state_act, 1.0, 0.0, 'HP')
    heal_ = 0.0
    for k in moment_hp:
        char = k
        state_ = copy.deepcopy(info[k + '_state'])
        base_ = copy.deepcopy(info[k + '_state'])
        state_act, debuff, buff_type_ = calc_buff(frame, now, char, forward, info, act, buff_type_, stand,
                                                  change_hp_per, base_, state_, buff_1, buff_2, moment_hp,
                                                  party_element)
        moment_hp[k] = min(moment_hp[k] + fix_ * 0.02 * (1 + state_act['Healee']), 1.0)
        heal_ += state_act['HP'] * fix_ * 0.02 * (1 + state_act['Healee'])
    return moment_hp, heal_


buff_type = {'Ferryman': [], 'Furina_e': ['Furina'], 'Furina_q': ['Furina'], 'Furina_psv_2': ['Furina'],
             'Golden': ['Furina'], 'Furina_c2': [], 'Dawn': ['Furina']}
buff_1 = [ferryman, furina_q_, furina_psv_2, golden, dawn]
buff_2 = [furina_e_]
buff_sp = []
act_lst = [furina_e, furina_q]
heal_lst = [furina_e1_heal, furina_e2_heal, furina_e3_heal, furina_psv_1_heal]
with_lst = []
