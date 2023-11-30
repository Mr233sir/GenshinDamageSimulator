if __name__ == '__main__':
    from PublicData import *
else:
    exec('from Data.PublicData import attack_type, calc_buff, heal')
    exec('import copy')

info = {'Zhongli_state': {'ATK': 1226, 'HP': 48668, 'DEF': 1002, 'EM': 23, 'ER': 1.533, 'CR': 0.466, 'CD': 1.114,
                          'UP_Geo': 0.288, 'Healer': 0.0, 'Healee': 0.0, 'SS': 0.0},
        'Zhongli_base': {'ATK': 816, 'HP': 14695, 'DEF': 738, 'Element': 'Geo'},
        'Zhongli_charge_max': 40,
        'Zhongli_skill': {'E': (('ATK', 'HP'), (1.632, 0.019), 47, 28), 'q': (('ATK', 'HP'), (7.05, 0.33), 101, 37),
                          'q0': ('', 0.0, 7)},
        'Zhongli_ele': {'E': ('Geo', 2, 3, 150, 'Zhongli_e'), 'Zhongli_e0': ('Geo', 1, 3, 150, 'Zhongli_e'),
                        'q': ('Geo', 4, False, False, ''), 'q0': ('', False, False, '')},
        'Zhongli_back': {'Zhongli_e0': (('ATK', 'HP'), (0.544, 0.019), 120, 120)},
        'Zhongli_heal': {}, 'Zhongli_energy': {'Zhongli_e0': (0.5, 2, 'Zhongli_e0')}, 'Zhongli_tough': (100, 5)}

name = {'Zhongli': '钟离'}


# buff
def zhongli_e_(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp,
               party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {'resi': {}}
    if 'Zhongli_e_' in buff_type:
        if 'Jade_shield' in buff_type:
            if buff_type['Jade_shield'][0]:
                debuff_['resi'] = {'Pyro': -0.2, 'Hydro': -0.2, 'Anemo': -0.2, 'Electro': -0.2, 'Dendro': -0.2,
                                   'Cyro': -0.2, 'Geo': -0.2, 'Physic': -0.2}
    return buff_, buff_type_, debuff_


# 行动
def zhongli_e(frame, now, forward):
    if now == 'E' and forward == 'Zhongli':
        sequence_act_ = []
        frame += info['Zhongli_skill']['E'][2]
        sequence_act_.append([frame, forward, 'E'])
        for i in range(int(info['Zhongli_back']['Zhongli_e0'][2]), 1801, int(info['Zhongli_back']['Zhongli_e0'][3])):
            sequence_act_.append([frame + i, 'back', 'Zhongli_e0'])
        frame += info['Zhongli_skill']['E'][3]
        return frame, sequence_act_, []


def zhongli_q(frame, now, forward):
    if now == 'q' and forward == 'Zhongli':
        sequence_act_ = [[frame, forward, 'q0']]
        frame += info['Zhongli_skill']['q'][2]
        sequence_act_.append([frame, forward, 'q'])
        frame += info['Zhongli_skill']['q'][3]
        return frame, sequence_act_, []


buff_type = {'Zhongli_e_': ['Zhongli'], 'Favonius': ['Zhongli']}
buff_1 = [zhongli_e_]
buff_2 = []
buff_sp = []
act_lst = [zhongli_e, zhongli_q]
heal_lst = []
with_lst = []
