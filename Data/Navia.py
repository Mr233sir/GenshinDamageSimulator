if __name__ == '__main__':
    from PublicData import *
else:
    exec('from Data.PublicData import attack_type, calc_buff, heal')
    exec('import copy')

info = {'Navia_state': {'ATK': 2281, 'HP': 20852, 'DEF': 1012, 'EM': 16, 'ER': 1.181, 'CR': 0.757, 'CD': 1.358,
                        'UP_Geo': 0.466, 'Healer': 0.0, 'Healee': 0.0, 'SS': 0.25},
        'Navia_base': {'ATK': 960, 'HP': 12650, 'DEF': 793, 'Element': 'Geo'},
        'Navia_charge_max': 60,
        'Navia_skill': {'a1': ('ATK', 1.7181, 30, 4), 'a2': ('ATK', 1.5893, 28, 4), 'a3': ('ATK', 0.6409, 46, 4),
                        'a4': ('ATK', 2.4514, 50, 10), 'A1': ('ATK', 1.7181, 30, 4), 'A2': ('ATK', 1.5893, 28, 4),
                        'A3': ('ATK', 0.6409, 46, 4), 'A4': ('ATK', 2.4514, 50, 10), 's': ('', 0.0, 20),
                        'e': ('ATK', 6.61, 16, 24), 'q': ('ATK', 1.292, 110, 10), 'q0': ('', 0.0, 100)},
        'Navia_ele': {'a1': ('', 1, 3, 150, 'Navia_a'), 'a2': ('', 1, 3, 150, 'Navia_a'),
                      'a3': ('', 1, 3, 150, 'Navia_a'), 'a4': ('', 1, 3, 150, 'Navia_a'),
                      'A1': ('Geo', 1, 3, 150, 'Navia_a'), 'A2': ('Geo', 1, 3, 150, 'Navia_a'),
                      'A3': ('Geo', 1, 3, 150, 'Navia_a'), 'A4': ('Geo', 1, 3, 150, 'Navia_a'),
                      'e': ('Geo', 1, False, False, ''), 'q': ('Geo', 1, False, False, ''),
                      'q0': ('', 0, False, False, ''), 'Navia_q0': ('Geo', 1, 3, False, 'Navia_q0'),
                      's': ('', 0, False, False, '')},
        'Navia_back': {'Navia_q0': ('ATK', 0.8228, 45, 45)},
        'Navia_heal': {}, 'Navia_energy': {'e': (3.5, False, '')}, 'Navia_tough': (100, 5)}

name = {'Navia': '娜维娅'}


# buff
def navia_psv_2(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp,
                party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Navia_psv_2' in buff_type and char in buff_type.get('Navia_psv_2', []):
        buff_['ATK_per'] = min(len([i for i in party_element if i in ['Pyro', 'Hydro', 'Electro', 'Cyro']]), 2) * 0.2
    return buff_, buff_type_, debuff_


def navia_psv_1(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp,
                party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Navia_psv_1' in buff_type and char in buff_type.get('Navia_psv_1', []) and now[0] in ['A', 'Z', 'X']:
        buff_['UP'] = 0.4
    return buff_, buff_type_, debuff_


def navia_e_(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp,
             party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if len(act) == 4:
        rea_type = act[3]
    else:
        rea_type = 1.0
    if 'Navia_e_' in buff_type and now in buff_type.get('Navia_e_', []) and rea_type == 0.0:
        buff_type_['Crystal'] = min(buff_type.get('Crystal', 0) + 1, 6)
    if 'Crystal' in buff_type and char == 'Navia' and attack_type(now) == 'e':
        if buff_type['Crystal'] == 0:
            buff_['extra'] = 0.4 * info['Navia_skill'][now][1] * state_act['ATK']
        elif buff_type['Crystal'] == 1:
            buff_['extra'] = 0.8 * info['Navia_skill'][now][1] * state_act['ATK']
        elif buff_type['Crystal'] == 2:
            buff_['extra'] = 4 / 3 * info['Navia_skill'][now][1] * state_act['ATK']
        else:
            buff_['extra'] = 2 * info['Navia_skill'][now][1] * state_act['ATK']
            buff_['UP'] = (buff_type['Crystal'] - 3) * 0.15
        buff_type['Crystal'] = 0
    return buff_, buff_type_, debuff_


def unforged(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp,
             party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Unforged' in buff_type and char in buff_type.get('Unforged', []):
        buff_['SS'] = 0.25
        if char == forward:
            buff_type_['Unforged_'] = [min(buff_type.get('Unforged_', [0])[0]+1, 5), frame, frame + 480]
    if 'Unforged_' in buff_type and char in buff_type.get('Unforged', []):
        if int(buff_type['Unforged_'][1]) <= frame < int(buff_type['Unforged_'][2]):
            buff_['ATK_per'] = buff_type['Unforged_'][0] * 0.05
            shield = 0
            for key in buff_type:
                if key.endswith('_shield'):
                    shield = max(buff_type[key][0], shield)
            if shield and char == forward:
                buff_['ATK_per'] *= 2
    return buff_, buff_type_, debuff_


def whispers(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp,
             party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Whispers' in buff_type and char in buff_type.get('Whispers', []) and attack_type(now) == 'e':
        buff_type_['Whispers_'] = [frame, frame + 600]
    if 'Crystal_shield' in buff_type and char == forward:
        if buff_type['Crystal_shield'][0]:
            buff_type_['Whispers__'] = [frame, frame + 60]
    if 'Whispers_' in buff_type and char in buff_type.get('Whispers', []):
        if int(buff_type['Whispers_'][0]) <= frame < int(buff_type['Whispers_'][1]):
            buff_['UP'] = 0.2
            if 'Whispers__' in buff_type and char in buff_type.get('Whispers', []):
                if int(buff_type['Whispers__'][0]) <= frame < int(buff_type['Whispers__'][1]):
                    buff_['UP'] *= 2.5
    return buff_, buff_type_, debuff_


# 行动
def navia_a1(frame, now, forward):
    if now == 'a1' and forward == 'Navia':
        frame += info['Navia_skill']['a1'][2]
        sequence_act_ = [frame, forward, 'a1']
        frame += info['Navia_skill']['a1'][3]
        return frame, sequence_act_, []


def navia_a2(frame, now, forward):
    if now == 'a2' and forward == 'Navia':
        frame += info['Navia_skill']['a2'][2]
        sequence_act_ = [frame, forward, 'a2']
        frame += info['Navia_skill']['a2'][3]
        return frame, sequence_act_, []


def navia_a3(frame, now, forward):
    sequence_act_ = []
    if now == 'a3' and forward == 'Navia':
        frame += info['Navia_skill']['a3'][2]
        sequence_act_.append([frame, forward, 'a3'])
        sequence_act_.append([frame + 3, forward, 'a3'])
        sequence_act_.append([frame + 6, forward, 'a3'])
        frame += info['Navia_skill']['a3'][3]
        return frame, sequence_act_, []


def navia_a4(frame, now, forward):
    if now == 'a4' and forward == 'Navia':
        frame += info['Navia_skill']['a4'][2]
        sequence_act_ = [frame, forward, 'a4']
        frame += info['Navia_skill']['a4'][3]
        return frame, sequence_act_, []


def navia_e(frame, now, forward):
    if now == 'e' and forward == 'Navia':
        frame += info['Navia_skill']['e'][2]
        sequence_act_ = [frame, forward, 'e']
        frame += info['Navia_skill']['e'][3]
        return frame, sequence_act_, []


def navia_q(frame, now, forward):
    if now == 'q' and forward == 'Navia':
        sequence_act_ = [[frame, forward, 'q0']]
        frame += info['Navia_skill']['q'][2]
        sequence_act_.append([frame, forward, 'q'])
        for i in range(int(info['Navia_back']['Navia_q0'][2]), 721, int(info['Navia_back']['Navia_q0'][3])):
            sequence_act_.append([frame + i, 'back', 'Navia_q0'])
        frame += info['Navia_skill']['q'][3]
        return frame, sequence_act_, []


buff_type = {'Whispers': ['Navia'], 'Unforged': ['Navia'], 'Navia_e_': ['Navia'], 'Navia_psv_1': ['Navia']}
buff_1 = [whispers, unforged, navia_e_, navia_psv_1]
buff_2 = []
buff_sp = []
act_lst = [navia_a1, navia_a2, navia_a3, navia_a4, navia_e, navia_q]
heal_lst = []
with_lst = []
