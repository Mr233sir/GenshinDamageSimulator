if __name__ == '__main__':
    from PublicData import *
else:
    exec('from Data.PublicData import attack_type, calc_buff, heal')
    exec('import copy')

info = {'Kazuha_state': {'ATK': 1336, 'HP': 19337, 'DEF': 1198, 'EM': 945, 'ER': 1.544, 'CR': 0.182, 'CD': 0.554,
                         'UP_Anemo': 0.15, 'Healer': 0.0, 'Healee': 0.0, 'SS': 0.0},
        'Kazuha_base': {'ATK': 806, 'HP': 13348, 'DEF': 807, 'Element': 'Anemo'},
        'Kazuha_charge_max': 60,
        'Kazuha_skill': {'E': ('ATK', 3.91, 33, 0), 'x': ('ATK', 2.21, 33, 19), 'q': ('ATK', 3.94, 82, 10),
                         'a1': ('ATK', 0.486, 13, 3), 'q0': ('', 0.0, 4)},
        'Kazuha_ele': {'E': ('Anemo', 2, False, False, ''), 'q': ('Anemo', 2, False, False, ''),
                       'x': ('Anemo', 1, False, False, ''), 'Kazuha_q0': ('Anemo', 1, False, False, ''),
                       'a1': ('', 1, False, False, ''), 'Kazuha_xDye': ('', 1, False, False, ''),
                       'Kazuha_q0Dye': ('', 1, False, False, ''), 'q0': ('', 0, False, False, '')},
        'Kazuha_back': {'Kazuha_q0': ('ATK', 1.8, 120, 120), 'Kazuha_xDye': ('ATK', 2.0, -1, 0),
                        'Kazuha_q0Dye': ('ATK', 0.54, 119, 120)}, 'Kazuha_tough': (100, 5),
        'Kazuha_energy': {'E': (4, False, '')}}

name = {'Kazuha': '枫原万叶'}


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


def kazuha_psv_2(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp,
                 party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {'resi': {}}
    if len(act) == 4:
        rea_type = act[3]
    else:
        rea_type = 1.0
    if 'Kazuha_psv_2' in buff_type and now in buff_type.get('Kazuha_psv_2', []) and now == forward and rea_type == 0.6:
        buff_type_['Kazuha_psv_2_' + char] = [frame, frame + 480]
    if 'Kazuha_psv_2_Pyro' in buff_type and char in stand.values() and info.get(char + '_base', {'Element': ''})[
        'Element'] == 'Pyro':
        buff_['UP_Pyro'] = min(info['Kazuha_state']['EM'] * 0.0004, 0.4)
    if 'Kazuha_psv_2_Hydro' in buff_type and char in stand.values() and info.get(char + '_base', {'Element': ''})[
        'Element'] == 'Hydro':
        buff_['UP_Hydro'] = min(info['Kazuha_state']['EM'] * 0.0004, 0.4)
    if 'Kazuha_psv_2_Electro' in buff_type and char in stand.values() and info.get(char + '_base', {'Element': ''})[
        'Element'] == 'Electro':
        buff_['UP_Electro'] = min(info['Kazuha_state']['EM'] * 0.0004, 0.4)
    if 'Kazuha_psv_2_Cyro' in buff_type and char in stand.values() and info.get(char + '_base', {'Element': ''})[
        'Element'] == 'Cyro':
        buff_['UP_Cyro'] = min(info['Kazuha_state']['EM'] * 0.0004, 0.4)
    return buff_, buff_type_, debuff_


def xiphos(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp, party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {'resi': {}}
    if 'Xiphos' in buff_type and char in buff_type.get('Xiphos', []):
        buff_['ER'] = info['Kazuha_state']['EM'] * 0.00072
    elif 'Xiphos' in buff_type and char in stand.values():
        buff_['ER'] = info['Kazuha_state']['EM'] * 0.000216
    return buff_, buff_type_, debuff_


# 行动
def kazuha_a1(frame, now, forward):
    if now == 'a1' and forward == 'Kazuha':
        frame += info['Kazuha_skill']['a1'][2]
        sequence_act_ = [frame, forward, 'a1']
        frame += info['Kazuha_skill']['a1'][3]
        return frame, sequence_act_, []


def kazuha_E(frame, now, forward):
    sequence_act_ = []
    if now == 'E' and forward == 'Kazuha':
        frame += info['Kazuha_skill']['E'][2]
        sequence_act_.append([frame, forward, 'E'])
        frame += info['Kazuha_skill']['x'][2]
        sequence_act_.append([frame + int(info['Kazuha_back']['Kazuha_xDye'][2]), forward, 'Kazuha_xDye'])
        sequence_act_.append([frame, forward, 'x'])
        frame += info['Kazuha_skill']['x'][3]
        return frame, sequence_act_, []


def kazuha_q(frame, now, forward):
    if now == 'q' and forward == 'Kazuha':
        sequence_act_ = [[frame, forward, 'q0']]
        frame += info['Kazuha_skill']['q'][2]
        sequence_act_.append([frame, forward, 'q'])
        for i in range(int(info['Kazuha_back']['Kazuha_q0'][2]), 481, int(info['Kazuha_back']['Kazuha_q0'][3])):
            sequence_act_.append([frame + i, 'back', 'Kazuha_q0'])
        for i in range(int(info['Kazuha_back']['Kazuha_q0Dye'][2]), 481, int(info['Kazuha_back']['Kazuha_q0Dye'][3])):
            sequence_act_.append([frame + i, 'back', 'Kazuha_q0Dye'])
        frame += info['Kazuha_skill']['q'][3]
        return frame, sequence_act_, []


buff_type = {'Viridescent': ['Kazuha'], 'Kazuha_psv_2': ['Kazuha'], 'Xiphos': ['Kazuha']}
buff_1 = [viridescent, kazuha_psv_2, xiphos]
buff_2 = []
buff_sp = []
act_lst = [kazuha_E, kazuha_q, kazuha_a1]
heal_lst = []
with_lst = []
