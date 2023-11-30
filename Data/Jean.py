if __name__ == '__main__':
    from PublicData import *
else:
    exec('from Data.PublicData import attack_type, calc_buff, heal')
    exec('import copy')

info = {
    'Jean_state': {'ATK': 1948, 'HP': 24678, 'DEF': 801, 'EM': 40, 'ER': 2.241, 'CR': 0.505, 'CD': 0.694, 'UP': 0.15,
                   'Healer': 0.2215, 'Healee': 0.0, 'SS': 0.0},
    'Jean_base': {'ATK': 694, 'HP': 14695, 'DEF': 769, 'Element': 'Anemo'},
    'Jean_charge_max': 80,
    'Jean_skill': {'e': ('ATK', 4.38, 21, 39), 'q': ('ATK', 6.8, 40, 0)},
    'Jean_ele': {'e': ('Anemo', 2, False, False, ''), 'q': ('Anemo', 2, False, False, '')},
    'Jean_heal': {'q': ('ATK', 4.02, 2888, True), 'q0': ('ATK', 0.4019, 289, False)}}

name = {'Jean': '琴'}


# buff
def viridescent(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp,
                party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {'resi': {}}
    if len(act) == 4:
        rea_type = act[3]
    else:
        rea_type = 1.0
    if 'Viridescent' in buff_type and now in buff_type.get('Viridescent', []) and now == forward and rea_type == 0.6:
        buff_type_['Viridescent_' + char] = [frame, frame + 600]
        buff_['rea_ex'] = 0.6
    if 'Viridescent_Pyro' in buff_type and int(buff_type['Viridescent_Pyro'][0]) <= frame < int(
            buff_type['Viridescent_Pyro'][1]):
        debuff_['resi']['Pyro'] = -0.4
    if 'Viridescent_Hydro' in buff_type and int(buff_type['Viridescent_Hydro'][0]) <= frame < int(
            buff_type['Viridescent_Hydro'][1]):
        debuff_['resi']['Hydro'] = -0.4
    if 'Viridescent_Electro' in buff_type and int(buff_type['Viridescent_Electro'][0]) <= frame < int(
            buff_type['Viridescent_Electro'][1]):
        debuff_['resi']['Electro'] = -0.4
    if 'Viridescent_Cyro' in buff_type and int(buff_type['Viridescent_Cyro'][0]) <= frame < int(
            buff_type['Viridescent_Cyro'][1]):
        debuff_['resi']['Cyro'] = -0.4
    return buff_, buff_type_, debuff_


# 行动
def jean_e(frame, now, forward):
    if now == 'e' and forward == 'Jean':
        frame += info['Jean_skill']['e'][2]
        sequence_act_ = [frame, forward, 'e']
        frame += info['Jean_skill']['e'][3]
        return frame, sequence_act_, []


def jean_q(frame, now, forward):
    sequence_heal_ = []
    if now == 'q' and forward == 'Jean':
        frame += info['Jean_skill']['q'][2]
        sequence_act_ = [frame, forward, 'q']
        sequence_heal_.append([frame, 'Jean_q'])
        for i in range(60, 601, 60):
            sequence_heal_.append([frame + i, 'Jean_q0'])
        frame += info['Jean_skill']['q'][3]
        return frame, sequence_act_, sequence_heal_


# 血条
def jean_q_heal(frame, now, char, forward, info, act, buff_type_, stand, change_hp_per, base_, state_, buff_1, buff_2,
                moment_hp, party_element):
    char = 'Jean'
    now = 'q'
    state_act, debuff, buff_type_ = calc_buff(frame, now, char, forward, info, act, buff_type_, stand, change_hp_per,
                                              base_, state_, buff_1, buff_2,
                                              moment_hp, party_element)
    heal_ = 0.0
    heal__ = heal(state_act, info['Jean_heal']['q'][2], info['Jean_heal']['q'][1], info['Jean_heal']['q'][0])
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


def jean_q0_heal(frame, now, char, forward, info, act, buff_type_, stand, change_hp_per, base_, state_, buff_1, buff_2,
                 moment_hp, party_element):
    char = 'Jean'
    state_act, debuff, buff_type_ = calc_buff(frame, now, char, forward, info, act, buff_type_, stand, change_hp_per,
                                              base_, state_, buff_1, buff_2,
                                              moment_hp, party_element)

    heal_ = heal(state_act, info['Jean_heal']['q0'][2], info['Jean_heal']['q0'][1], info['Jean_heal']['q0'][0])
    state_act, debuff, buff_type_ = calc_buff(frame, now, char, forward, info, act, buff_type_, stand,
                                              change_hp_per, base_, state_, buff_1, buff_2, moment_hp, party_element)
    moment_hp[forward] = min(moment_hp[forward] + heal_ / state_act['HP'], info[forward + '_state']['HP'], 1.0)
    return moment_hp, heal_


# 加速
def jean_c2(frame, forward, now):
    buff_type_ = {}
    if now == 'e' and forward == 'Jean':
        buff_type_['speed'] = [0.15, frame, frame + 750]
    return buff_type_


buff_type = {'Viridescent': ['Jean']}
buff_1 = [viridescent]
buff_2 = []
buff_sp = [jean_c2]
act_lst = [jean_e, jean_q]
heal_lst = [jean_q_heal, jean_q0_heal]
with_lst = []
