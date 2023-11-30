if __name__ == '__main__':
    from PublicData import *
else:
    exec('from Data.PublicData import attack_type, calc_buff, heal')
    exec('import copy')

info = {'Kokomi_state': {'ATK': 1390, 'HP': 37013, 'DEF': 786, 'EM': 82, 'ER': 1.909, 'CR': -0.95, 'CD': 0.554,
                         'UP_Hydro': 0.754, 'Healer': 0.759, 'Healee': 0.0, 'SS': 0.0},
        'Kokomi_base': {'ATK': 744, 'HP': 13471, 'DEF': 657, 'Element': 'Hydro'},
        'Kokomi_charge_max': 70,
        'Kokomi_skill': {'a1': ('ATK', 1.094, 4, 10), 'a2': ('ATK', 0.985, 12, 18), 'a3': ('ATK', 1.509, 48, 13),
                         'A1': (('ATK', 'HP'), (1.094, 0.19585), 4, 5), 's': ('', 0.0, 20),
                         'A2': (('ATK', 'HP'), (0.985, 0.19585), 17, 5), 'q0': ('', 0.0, 50),
                         'A3': (('ATK', 'HP'), (1.509, 0.19585), 61, 13), 'e': ('ATK', 0, 24, 36),
                         'q': ('HP', 0.177, 49, 28)},
        'Kokomi_ele': {'a1': ('Hydro', 1, 3, 150, 'Kokomi_a'), 'a2': ('Hydro', 1, 3, 150, 'Kokomi_a'),
                       'a3': ('Hydro', 1, 3, 150, 'Kokomi_a'), 'A1': ('Hydro', 1, 3, 150, 'Kokomi_a'),
                       'A2': ('Hydro', 1, 3, 150, 'Kokomi_a'), 'A3': ('Hydro', 1, 3, 150, 'Kokomi_a'),
                       'e': ('Hydro', 0, False, False, ''), 'Kokomi_e0': ('Hydro', 1, False, False, ''),
                       'Kokomi_e1': ('Hydro', 1, False, False, ''), 'q': ('Hydro', 2, False, False, ''),
                       's': ('', 0, False, False, ''), 'q0': ('', 0, False, False, '')},
        'Kokomi_back': {'Kokomi_e0': ('ATK', 1.856, 0, 120), 'Kokomi_e1': (('ATK', 'HP'), (1.856, 0.121), 120, 120)},
        'Kokomi_heal': {'A': ('HP', 0.0137, 157, True), 'e': ('HP', 0.075, 862, False)}, 'Kokomi_tough': (50, 3),
        'Kokomi_energy': {'Kokomi_e0': (2 / 3, False, ''), 'Kokomi_e1': (2 / 3, False, '')}}

name = {'Kokomi': '珊瑚宫心海'}


# buff
def blue(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp, party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Blue' in buff_type and char in buff_type.get('Blue', []) and attack_type(now) in ['a', 'z']:
        buff_type['Blue_'] = [frame, frame + 360, min(int(buff_type.get('Blue_', [0])[-1]) + 1, 3)]
        if int(buff_type['Blue_'][0]) <= frame < int(buff_type['Blue_'][1]):
            buff_['UP'] = 0.16 * int(buff_type['Blue_'][-1])
    return buff_, buff_type_, debuff_


# 行动
def kokomi_e(frame, now, forward):
    sequence_act_ = []
    sequence_heal_ = []
    if now == 'e' and forward == 'Kokomi':
        frame += info['Kokomi_skill']['e'][2]
        sequence_act_.append([frame, forward, 'e'])
        for i in range(int(info['Kokomi_back']['Kokomi_e0'][2]), 721, int(info['Kokomi_back']['Kokomi_e0'][3])):
            sequence_act_.append([frame + i, 'back', 'Kokomi_e0'])
            sequence_heal_.append([frame + i, 'Kokomi_e'])
        frame += info['Kokomi_skill']['e'][3]
        return frame, sequence_act_, sequence_heal_


def kokomi_q(frame, now, forward):
    if now == 'q' and forward == 'Kokomi':
        sequence_act_ = [[frame, forward, 'q0']]
        frame += info['Kokomi_skill']['q'][2]
        sequence_act_.append([frame, forward, 'q'])
        frame += info['Kokomi_skill']['q'][3]
        return frame, sequence_act_, []


def kokomi_a1(frame, now, forward):
    if now == 'a1' and forward == 'Kokomi':
        frame += info['Kokomi_skill']['a1'][2]
        sequence_act_ = [frame, forward, 'a1']
        frame += info['Kokomi_skill']['a1'][3]
        return frame, sequence_act_, []


def kokomi_a2(frame, now, forward):
    if now == 'a2' and forward == 'Kokomi':
        frame += info['Kokomi_skill']['a2'][2]
        sequence_act_ = [frame, forward, 'a2']
        frame += info['Kokomi_skill']['a2'][3]
        return frame, sequence_act_, []


def kokomi_a3(frame, now, forward):
    if now == 'a3' and forward == 'Kokomi':
        frame += info['Kokomi_skill']['a3'][2]
        sequence_act_ = [frame, forward, 'a3']
        frame += info['Kokomi_skill']['a3'][3]
        return frame, sequence_act_, []


def kokomi_s(frame, now, forward):
    if now == 's' and forward == 'Kokomi':
        frame += info['Kokomi_skill']['s'][2]
        sequence_act_ = [frame, forward, 's']
        return frame, sequence_act_, []


# 血条
def kokomi_a1_heal(frame, now, char, forward, info, act, buff_type_, stand, change_hp_per, base_, state_, buff_1,
                   buff_2, moment_hp, party_element):
    char = 'Kokomi'
    now = 'A'
    state_act, debuff, buff_type_ = calc_buff(frame, now, char, forward, info, act, buff_type_, stand, change_hp_per,
                                              base_, state_, buff_1, buff_2, moment_hp, party_element)
    heal_ = 0.0
    heal__ = heal(state_act, info['Kokomi_heal']['A'][2], info['Kokomi_heal']['A'][1], info['Kokomi_heal']['A'][0])
    for k in moment_hp:
        char = k
        state_ = copy.deepcopy(info[k + '_state'])
        base_ = copy.deepcopy(info[k + '_state'])
        state_act, debuff, buff_type_ = calc_buff(frame, now, char, forward, info, act, buff_type_, stand,
                                                  change_hp_per, base_, state_, buff_1, buff_2, moment_hp,
                                                  party_element)
        moment_hp[k] = min(moment_hp[k] + heal__ / state_act['HP'] * (1 + state_act['Healee']), 1.0)
        heal_ += heal__ * (1 + state_act['Healee'])
    return moment_hp, heal_


def kokomi_a2_heal(frame, now, char, forward, info, act, buff_type_, stand, change_hp_per, base_, state_, buff_1,
                   buff_2, moment_hp, party_element):
    return kokomi_a1_heal(frame, now, char, forward, info, act, buff_type_, stand, change_hp_per, base_, state_, buff_1,
                          buff_2, moment_hp, party_element)


def kokomi_a3_heal(frame, now, char, forward, info, act, buff_type_, stand, change_hp_per, base_, state_, buff_1,
                   buff_2, moment_hp):
    return kokomi_a1_heal(frame, now, char, forward, info, act, buff_type_, stand, change_hp_per, base_, state_, buff_1,
                          buff_2, moment_hp, party_element)


def kokomi_e_heal(frame, now, char, forward, info, act, buff_type_, stand, change_hp_per, base_, state_, buff_1,
                  buff_2, moment_hp, party_element):
    char = 'Kokomi'
    state_act, debuff, buff_type_ = calc_buff(frame, now, char, forward, info, act, buff_type_, stand, change_hp_per,
                                              base_, state_, buff_1, buff_2, moment_hp, party_element)
    heal_ = heal(state_act, info['Kokomi_heal']['e'][2], info['Kokomi_heal']['e'][1], info['Kokomi_heal']['e'][0])
    state_ = copy.deepcopy(info[forward + '_state'])
    base_ = copy.deepcopy(info[forward + '_state'])
    state_act, debuff, buff_type_ = calc_buff(frame, now, char, forward, info, act, buff_type_, stand,
                                              change_hp_per, base_, state_, buff_1, buff_2, moment_hp, party_element)
    moment_hp[forward] = min(moment_hp[forward] + heal_ / state_act['HP'] * (1 + state_act['Healee']),
                             info[forward + '_state']['HP'], 1.0)
    heal_ *= (1 + state_act['Healee'])
    return moment_hp, heal_


def kokomi_prototype_heal(frame, now, char, forward, info, act, buff_type_, stand, change_hp_per, base_, state_, buff_1,
                          buff_2, moment_hp, party_element):
    char = 'Kokomi'
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
        moment_hp[k] = min(moment_hp[k] + fix_ * 0.06 * (1 + state_act['Healee']), 1.0)
        heal_ += state_act['HP'] * fix_ * 0.06 * (1 + state_act['Healee'])
    return moment_hp, heal_


buff_type = {'Blue': [], 'Prototype': ['Kokomi'], 'Ocean': ['Kokomi']}
buff_1 = [blue]
buff_2 = []
buff_sp = []
act_lst = [kokomi_e, kokomi_q, kokomi_a1, kokomi_a2, kokomi_a3, kokomi_s]
heal_lst = [kokomi_e_heal, kokomi_a1_heal, kokomi_a2_heal, kokomi_a3_heal, kokomi_prototype_heal]
with_lst = []
