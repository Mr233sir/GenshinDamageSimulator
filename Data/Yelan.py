if __name__ == '__main__':
    from PublicData import *
else:
    exec('from Data.PublicData import attack_type, calc_buff, heal')
    exec('import copy')

info = {
    'Yelan_state': {'ATK': 1114, 'HP': 33049, 'DEF': 625, 'EM': 0, 'ER': 1.757, 'CR': 0.697, 'CD': 2.346,
                    'UP_Hydro': 0.466, 'Healer': 0.0, 'Healee': 0.0, 'SS':0.0},
    'Yelan_base': {'ATK': 786, 'HP': 14450, 'DEF': 548, 'Element': 'Hydro'},
    'Yelan_charge_max': 70,
    'Yelan_skill': {'e': ('HP', 0.362, 35, 6), 'q': ('HP', 0.1242, 76, 16), 'a1': ('ATK', 0.44, 13, 2),
                    'q0': ('', 0.0, 5)},
    'Yelan_ele': {'e': ('Hydro', 1, False, False, ''), 'q': ('Hydro', 2, False, False, ''),
                  'Yelan_q0': ('Hydro', 1, 3, 120, 'Yelan_q0'), 'Yelan_q1': ('Hydro', 1, False, False, ''),
                  'a1': ('', 1, False, False, ''), 'q0': ('', 0, False, False, '')},
    'Yelan_back': {'Yelan_q0': ('HP', 0.0828), 'Yelan_q1': ('HP', 0.14)},
    'Yelan_heal': {}, 'Yelan_q0_last': 0, 'Yelan_q1_last': 0, 'Yelan_tough': (50, 3),
    'Yelan_energy': {'e': (4, False, '')}}

name = {'Yelan': '夜兰'}


# buff
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


def yelan_psv_1(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp, party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Yelan_psv_1' in buff_type and char in buff_type.get('Yelan_psv_1', []):
        buff_['HP_per'] = 0.12
    return buff_, buff_type_, debuff_


def yelan_psv_2(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp, party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Yelan_psv_2' in buff_type and char in buff_type.get('Yelan_psv_2', []) and now == 'q':
        buff_type_['Yelan_psv_2_'] = [frame, frame + 900]
    if 'Yelan_psv_2_' in buff_type and char in stand.values() and char == forward:
        if int(buff_type['Yelan_psv_2_'][0]) <= frame < int(buff_type['Yelan_psv_2_'][1]):
            buff_['UP'] = 0.01 + int((frame - buff_type['Yelan_psv_2_'][0]) / 60) * 0.035
    return buff_, buff_type_, debuff_


def aqua(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp, party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Aqua' in buff_type and char in buff_type.get('Aqua', []):
        buff_['UP'] = 0.2
    return buff_, buff_type_, debuff_


# 行动
def yelan_a1(frame, now, forward):
    if now == 'a1' and forward == 'Yelan':
        frame += info['Yelan_skill']['a1'][2]
        sequence_act_ = [frame, forward, 'a1']
        frame += info['Yelan_skill']['a1'][3]
        return frame, sequence_act_, []


def yelan_e(frame, now, forward):
    if now == 'e' and forward == 'Yelan':
        frame += info['Yelan_skill']['e'][2]
        sequence_act_ = [frame, forward, 'e']
        frame += info['Yelan_skill']['e'][3]
        return frame, sequence_act_, []


def yelan_q(frame, now, forward):
    if now == 'q' and forward == 'Yelan':
        sequence_act_ = [[frame, forward, 'q0']]
        frame += info['Yelan_skill']['q'][2]
        sequence_act_.append([frame, forward, 'q'])
        frame += info['Yelan_skill']['q'][3]
        return frame, sequence_act_, []


# 协同
def yelan_q0(frame_, char, forward, info, act_, buff_type_, stand_):
    app = None
    last = info['Yelan_q0_last']
    if 'Yelan_psv_2_' in buff_type_ and char in stand_.values() and last <= frame_ - 60:
        if int(buff_type_['Yelan_psv_2_'][0]) <= frame_ < int(buff_type_['Yelan_psv_2_'][1]) and attack_type(
                act_[2]) == 'a':
            app = [[frame_ + 23, forward, 'Yelan_q0'], [frame_ + 30, forward, 'Yelan_q0'],
                   [frame_ + 35, forward, 'Yelan_q0']]
            last = frame_
    if 'Yelan_psv_2_' in buff_type_ and char in stand_.values() and int(buff_type_['Yelan_psv_2_'][0]) <= frame_ < int(
            buff_type_['Yelan_psv_2_'][1]) and char == 'Yelan' and attack_type(act_[2]) == 'e':
        app = [[frame_ + 25, forward, 'Yelan_q0'], [frame_ + 30, forward, 'Yelan_q0'],
               [frame_ + 35, forward, 'Yelan_q0']]
    return app, last


def yelan_q1(frame_, char, forward, info, act_, buff_type_, stand_):
    app = None
    last = info['Yelan_q1_last']
    if act_[2] == 'Yelan_q0' and last <= frame_ - 108:
        app = [frame_, forward, 'Yelan_q1']
        last = frame_
    return app, last


buff_type = {'Emblem': ['Yelan'], 'Yelan_psv_1': ['Yelan'], 'Yelan_psv_2': ['Yelan'], 'Aqua': ['Yelan']}
buff_1 = [yelan_psv_1, yelan_psv_2, aqua]
buff_2 = [emblem]
buff_sp = []
act_lst = [yelan_q, yelan_e, yelan_a1]
heal_lst = []
with_lst = [yelan_q0, yelan_q1]
