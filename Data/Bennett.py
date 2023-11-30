if __name__ == '__main__':
    from PublicData import *
else:
    exec('from Data.PublicData import attack_type, calc_buff, heal')
    exec('import copy')

info = {'Bennett_state': {'ATK': 1080, 'HP': 29727, 'DEF': 850, 'EM': 0, 'ER': 2.941, 'CR': 0.05, 'CD': 0.5,
                          'UP_Pyro': 0.0, 'Healer': 0.0, 'Healee': 0.0, 'SS': 0.0},
        'Bennett_base': {'ATK': 646, 'HP': 12397, 'DEF': 771, 'Element': 'Pyro'},
        'Bennett_charge_max': 60,
        'Bennett_skill': {'e': ('ATK', 1.82, 16, 24), 'q': ('ATK', 4.66, 37, 15), 'q0': ('', 0.0, 36)},
        'Bennett_ele': {'e': ('Pyro', 2, False, False, ''), 'q': ('Pyro', 2, False, False, ''),
                        'q0': ('', False, False, '')},
        'Bennett_back': {}, 'Bennett_tough': (100, 5),
        'Bennett_heal': {'Bennett_q0': ('HP', 0.12, 1477, False)},
        'Bennett_energy': {'e': (2.25, 0.3, 'Bennett_e')}}

name = {'Bennett': '班尼特'}


# buff
def bennett_q_(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp,
               party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Bennett_q_' in buff_type and char in buff_type.get('Bennett_q_', []) and now == 'q':
        buff_type_['Bennett_q__'] = [frame, frame + 720]
    if 'Bennett_q__' in buff_type and char in stand.values() and char == forward:
        buff_['ATK_num'] = info['Bennett_base']['ATK'] * 1.32
    return buff_, buff_type_, debuff_


def bennett_c2(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp,
               party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Bennett_c2' in buff_type and char in buff_type.get('Bennett_c2', []) and moment_hp[char] < 0.7:
        buff_['ER'] = 0.3
    return buff_, buff_type_, debuff_


def noblesse(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp,
             party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {}
    if 'Noblesse' in buff_type and char in buff_type.get('Noblesse', []) and now == 'q':
        buff_['UP'] = 0.2
        buff_type_['Noblesse_'] = [frame, frame + 720]
    if 'Bennett_q__' in buff_type and char in stand.values():
        buff_['ATK_per'] = 0.2
    return buff_, buff_type_, debuff_


# 行动
def bennett_q(frame, now, forward):
    sequence_heal_ = []
    if now == 'q' and forward == 'Bennett':
        sequence_act_ = [[frame, forward, 'q0']]
        frame += info['Bennett_skill']['q'][2]
        sequence_act_.append([frame, forward, 'q'])
        for i in range(60, 721, 60):
            sequence_heal_.append([frame + i, 'Bennett_q0'])
        frame += info['Bennett_skill']['q'][3]
        return frame, sequence_act_, sequence_heal_


def bennett_e(frame, now, forward):
    if now == 'e' and forward == 'Bennett':
        frame += info['Bennett_skill']['e'][2]
        sequence_act_ = [[frame, forward, 'e']]
        frame += info['Bennett_skill']['e'][3]
        return frame, sequence_act_, []


# 血条
def bennett_q0_heal(frame, now, char, forward, info, act, buff_type_, stand, change_hp_per, base_, state_, buff_1,
                    buff_2, moment_hp, party_element):
    char = 'Bennett'
    state_act, debuff, buff_type_ = calc_buff(frame, now, char, forward, info, act, buff_type_, stand, change_hp_per,
                                              base_, state_, buff_1, buff_2, moment_hp, party_element)
    heal_ = 0.0
    heal__ = heal(state_act, info['Bennett_heal']['Bennett_q0'][2], info['Bennett_heal']['Bennett_q0'][1],
                  info['Bennett_heal']['Bennett_q0'][0])
    state_act, debuff, buff_type_ = calc_buff(frame, now, char, forward, info, act, buff_type_, stand,
                                              change_hp_per, base_, state_, buff_1, buff_2, moment_hp, party_element)
    if moment_hp[forward] < 0.7:
        moment_hp[forward] = min(moment_hp[forward] + heal__ / state_act['HP'] * (1 + state_act['Healee']), 1.0)
        heal_ += heal__ * (1 + state_act['Healee'])
    return moment_hp, heal_


buff_type = {'Bennett_q_': ['Bennett'], 'Bennett_c2': ['Bennett'], 'Noblesse': ['Bennett'], 'Favonius': ['Bennett']}
buff_1 = [bennett_q_, bennett_c2, noblesse]
buff_2 = []
buff_sp = []
act_lst = [bennett_q, bennett_e]
heal_lst = [bennett_q0_heal]
with_lst = []
