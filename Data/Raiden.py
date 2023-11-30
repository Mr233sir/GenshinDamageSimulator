if __name__ == '__main__':
    from PublicData import *
else:
    exec('from Data.PublicData import attack_type, calc_buff, heal')
    exec('import copy')

info = {'Raiden_state': {'ATK': 2188, 'HP': 17687, 'DEF': 992, 'EM': 0, 'ER': 2.356, 'CR': 0.703, 'CD': 1.728, 'UP': 0,
                         'Healer': 0.0, 'Healee': 0.0, 'SS':0.0},
        'Raiden_base': {'ATK': 943, 'HP': 12907, 'DEF': 789, 'Element': 'Electro'},
        'Raiden_charge_max': 90,
        'Raiden_skill': {'a1': ('ATK', 0.461, 12, 9), 'a2': ('ATK', 0.462, 13, 5), 'a3': ('ATK', 0.58, 11, 7),
                         'z1': ('ATK', 1.158, 24, 0), 'z2': ('ATK', 0, 8, 28), 'A1': ('ATK', 0.798 + 0.786, 12, 9),
                         'A2': ('ATK', 0.784 + 0.786, 13, 5), 'A3': ('ATK', 0.96 + 0.786, 11, 7),
                         'Z1': ('ATK', 1.099 + 0.786, 24, 0), 'Z2': ('ATK', 1.099 + 0.786, 8, 28),
                         'e': ('ATK', 1.992, 51, -15), 'q': ('ATK', 7.21 + 4.2, 98, 12)},
        'Raiden_ele': {'a1': ('', 1, 3, 150, 'Raiden_a'), 'a2': ('', 1, 3, 150, 'Raiden_a'),
                       'a3': ('', 1, 3, 150, 'Raiden_a'), 'z1': ('', 1, 3, 150, 'Raiden_z'),
                       'z2': ('', 1, 3, 150, 'Raiden_z'), 'A1': ('Electro', 1, 3, 150, 'Raiden_a'),
                       'A2': ('Electro', 1, 3, 150, 'Raiden_a'), 'A3': ('Electro', 1, 3, 150, 'Raiden_a'),
                       'Z1': ('Electro', 1, 3, 150, 'Raiden_z'), 'Z2': ('Electro', 1, 3, 150, 'Raiden_z'),
                       'e': ('Electro', 1, False, False, ''), 'Raiden_e0': ('Electro', 1, False, False, ''),
                       'q': ('Electro', 2, False, False, '')},
        'Raiden_back': {'Raiden_e0': ('ATK', 0.714)}, 'Raiden_e0_last': 0}

name = {'Raiden': '雷电将军'}


# buff
def engulfing_(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp, party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if char in buff_type.get('Engulfing', []) and attack_type(now) == 'q':
        buff_type_['Engulfing_'] = [frame, frame + 720]
        buff_['ER'] = 0.3
    if 'Engulfing_' in buff_type and char in buff_type.get('Engulfing', []):
        if int(buff_type['Engulfing_'][0]) <= frame < int(buff_type['Engulfing_'][1]):
            buff_['ER'] = 0.3
    return buff_, buff_type_, debuff_


def engulfing(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp, party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Engulfing' in buff_type and char in buff_type.get('Engulfing', []):
        buff_['ATK_per'] = min((state_act['ER'] - 1) * 0.28, 0.8)
    return buff_, buff_type_, debuff_


def raiden_psv_2(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp, party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Raiden_psv_2' in buff_type and char in buff_type.get('Raiden_psv_2', []):
        buff_['UP'] = (info[char + '_state']['ER'] - 1) * 0.4
    return buff_, buff_type_, debuff_


def emblem(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp, party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Emblem' in buff_type and char in buff_type.get('Emblem', []):
        if attack_type(now) == 'q':
            buff_['UP'] = min(state_act['ER'] * 0.25, 3.0)
        elif char in ['Raiden'] and attack_type(now) in ['a', 'z']:
            buff_['UP'] = min(state_act['ER'] * 0.25, 3.0)
    return buff_, buff_type_, debuff_


def raiden_c2(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp, party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Raiden_c2' in buff_type and char in buff_type.get('Raiden_c2', []) and attack_type(now) in ['a', 'z', 'q']:
        buff_['def_ig'] = 0.6
    return buff_, buff_type_, debuff_


def raiden_e_(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp, party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Raiden_e' in buff_type and char in buff_type.get('Raiden_e', []) and now == 'e':
        buff_type['Raiden_e_'] = [frame, frame + 1500]
    if 'Raiden_e_' in buff_type and char in stand.values() and attack_type(now) == 'q':
        if int(buff_type['Raiden_e_'][0]) <= frame < int(buff_type['Raiden_e_'][1]):
            buff_['UP'] = info[char + '_charge_max'] * 0.003
    elif 'Raiden_e_' in buff_type and char in ['Raiden'] and attack_type(now) in ['a', 'z']:
        if int(buff_type['Raiden_e_'][0]) <= frame < int(buff_type['Raiden_e_'][1]):
            buff_['UP'] = min(info[char + '_state']['ER'] * 0.25, 3.0)
    return buff_, buff_type_, debuff_


# 行动
def raiden_e(frame, now, forward):
    if now == 'e' and forward == 'Raiden':
        frame += info['Raiden_skill']['e'][2]
        sequence_act_ = [frame, forward, 'e']
        frame += info['Raiden_skill']['e'][3]
        return frame, sequence_act_, []


def raiden_q(frame, now, forward):
    if now == 'q' and forward == 'Raiden':
        frame += info['Raiden_skill']['q'][2]
        sequence_act_ = [frame, forward, 'q']
        frame += info['Raiden_skill']['q'][3]
        return frame, sequence_act_, []


def raiden_a1(frame, now, forward):
    if now == 'a1' and forward == 'Raiden':
        frame += info['Raiden_skill']['a1'][2]
        sequence_act_ = [frame, forward, 'a1']
        frame += info['Raiden_skill']['a1'][3]
        return frame, sequence_act_, []


def raiden_a2(frame, now, forward):
    if now == 'a2' and forward == 'Raiden':
        frame += info['Raiden_skill']['a2'][2]
        sequence_act_ = [frame, forward, 'a2']
        frame += info['Raiden_skill']['a2'][3]
        return frame, sequence_act_, []


def raiden_a3(frame, now, forward):
    if now == 'a3' and forward == 'Raiden':
        frame += info['Raiden_skill']['a3'][2]
        sequence_act_ = [frame, forward, 'a3']
        frame += info['Raiden_skill']['a3'][3]
        return frame, sequence_act_, []


def raiden_z(frame, now, forward):
    if now == 'z' and forward == 'Raiden':
        frame += info['Raiden_skill']['z1'][2]
        sequence_act_1 = [frame, forward, 'z1']
        frame += info['Raiden_skill']['z1'][3]
        frame += info['Raiden_skill']['z2'][2]
        sequence_act_2 = [frame, forward, 'z2']
        frame += info['Raiden_skill']['z2'][3]
        return frame, [sequence_act_1, sequence_act_2], []


# 协同
def raiden_e0(frame_, char, forward, info, act_, buff_type_, stand_):
    app = None
    last = info['Raiden_e0_last']
    if 'Raiden_e_' in buff_type_ and char in stand_.values() and last <= frame_ - 54:
        if int(buff_type_['Raiden_e_'][0]) <= frame_ < int(buff_type_['Raiden_e_'][1]) and (act_[1], act_[2]) not in [
            ('Miko', 'e')]:
            app = [frame_, forward, 'Raiden_e0']
            last = frame_
    return app, last


buff_type = {'Engulfing': ['Raiden'], 'Raiden_psv_2': ['Raiden'], 'Emblem': ['Raiden'], 'Raiden_c2': ['Raiden'],
             'Raiden_e': ['Raiden']}
buff_1 = [engulfing_, raiden_psv_2, raiden_c2, raiden_e_]
buff_2 = [engulfing, emblem]
buff_sp = []
act_lst = [raiden_e, raiden_q, raiden_a1, raiden_a2, raiden_a3, raiden_z]
heal_lst = []
with_lst = [raiden_e0]
