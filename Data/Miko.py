if __name__ == '__main__':
    from PublicData import *
else:
    exec('from Data.PublicData import attack_type, calc_buff, heal')
    exec('import copy')

info = {'Miko_state': {'ATK': 1811, 'HP': 15690, 'DEF': 650, 'EM': 373, 'ER': 1.11, 'CR': 0.685, 'CD': 2.25, 'UP': 0,
                       'Healer': 0.0, 'Healee': 0.0, 'SS':0.0},
        'Miko_base': {'ATK': 948, 'HP': 10372, 'DEF': 569, 'Element': 'Electro'},
        'Miko_charge_max': 90,
        'Miko_skill': {'e': ('ATK', 0.0, 10, 30), 'q': ('ATK', 5.53, 99, 0)},
        'Miko_ele': {'Miko_e0': ('Electro', 1, 3, 150, 'Miko_e0'), 'q': ('Electro', 1, False, False, ''),
                     'Miko_q0': ('Electro', 1, False, False, ''), 'e': ('Electro', 0, False, False, '')},
        'Miko_back': {'Miko_e0': ('ATK', 2.518, 112, 180), 'Miko_q0': ('ATK', 7.09, 55, 24)},
        'Miko_e_counter': 0}

name = {'Miko': '八重神子'}


# buff
def miko_psv_2(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp, party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Miko_psv_2' in buff_type and char in buff_type.get('Miko_psv_2', []) and attack_type(now) == 'e':
        buff_['UP'] = info[char + '_state']['EM'] * 0.0015
    return buff_, buff_type_, debuff_


def miko_c4(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp, party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Miko_c4' in buff_type and char in buff_type.get('Miko_c4', []) and attack_type(now) == 'e':
        buff_type['Miko_c4_'] = [frame, frame + 300]
        buff_['UP'] = 0.2
    if 'Miko_c4_' in buff_type and char in stand.values():
        if int(buff_type['Miko_c4_'][0]) <= frame < int(buff_type['Miko_c4_'][1]) \
                and info[char + '_base']['Element'] == 'Electro':
            buff_['UP'] = 0.2
    return buff_, buff_type_, debuff_


def miko_c6(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp, party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Miko_c6' in buff_type and char in buff_type.get('Miko_c6', []) and attack_type(now) == 'e':
        buff_['def_ig'] = 0.6
    return buff_, buff_type_, debuff_


def kagura(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp, party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Kagura' in buff_type and char in buff_type.get('Kagura', []) and now == 'e':
        buff_type_['Kagura_'] = [frame, frame + 960, min(int(buff_type.get('Kagura_', [0])[-1]) + 1, 3)]
    if 'Kagura_' in buff_type and char in buff_type.get('Kagura', []) and attack_type(now) == 'e':
        if int(buff_type['Kagura_'][0]) <= frame < int(buff_type['Kagura_'][1]):
            buff_['UP'] = 0.12 * int(buff_type['Kagura_'][-1])
    if 'Kagura_' in buff_type and char in buff_type.get('Kagura', []) and int(buff_type['Kagura_'][-1]) == 3:
        if 'UP' in buff_type:
            buff_['UP'] += 0.12
        else:
            buff_['UP'] = 0.12
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


# 行动
def miko_e(frame, now, forward):
    sequence_act_ = []
    if now == 'e' and forward == 'Miko':
        frame += info['Miko_skill']['e'][2]
        sequence_act_.append([frame, forward, 'e'])
        for i in range(info['Miko_back']['Miko_e0'][2], 840, info['Miko_back']['Miko_e0'][3]):
            sequence_act_.append([frame + i, 'back', 'Miko_e0'])
        info['Miko_e_counter'] += 1
        frame += info['Miko_skill']['e'][3]
        return frame, sequence_act_, []


def miko_q(frame, now, forward):
    sequence_act_ = []
    if now == 'q' and forward == 'Miko':
        sequence_act_.append([frame, forward, 'q'])
        for i in range(info['Miko_back']['Miko_q0'][2],
                       info['Miko_back']['Miko_q0'][2] + info['Miko_back']['Miko_q0'][3] * info['Miko_e_counter'] + 1,
                       info['Miko_back']['Miko_q0'][3]):
            sequence_act_.append([frame + i, forward, 'Miko_q0'])
        info['Miko_e_counter'] = 0
        frame += info['Miko_skill']['q'][3]
        return frame, sequence_act_, []


buff_type = {'Miko_psv_2': ['Miko'], 'Miko_c4': ['Miko'], 'Miko_c6': ['Miko'], 'Kagura': ['Miko'], 'Golden': ['Miko']}
buff_1 = [miko_psv_2, miko_c4, miko_c6, kagura, golden]
buff_2 = []
buff_sp = []
act_lst = [miko_e, miko_q]
heal_lst = []
with_lst = []
