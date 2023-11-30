from fractions import Fraction
import copy

now = ''
forward = ''
char = ''
base_act = {}
state_act = {}
act = []
sequence_gen = []
sequence_act = []
sequence_rea = []
sequence_dmg = []
sequence_heal = []
sequence_hp = []
sequence_enemy = []
sequence_energy = []
seed_bank = []
rea_type = 0.0
total = 0.0
order_dmg = 0
order_heal = 0
order_enemy = 0
order_energy = 0
order_gen = 0
info = {}
party_element = []
buff_1 = []
buff_2 = []
buff_sp = []
act_lst = []
heal_lst = []
with_lst = []
toughness = {}
element = {'Pyro': Fraction(0), 'Hydro': Fraction(0), 'Anemo': Fraction(0), 'Electro': Fraction(0),
           'Dendro': Fraction(), 'Cyro': Fraction(0), 'Geo': Fraction(0), 'Frozen': Fraction(0), 'Aggr': Fraction(0),
           'Burn': Fraction(0), 'EC_last': 0, 'EC_char': '', 'B_last': 0, 'B_char': '', 'Frozen_decay': Fraction(2, 5),
           'seed_burst': []}
elements = {'EnemyMain': copy.deepcopy(element)}
seed_lst = []
decay_1 = Fraction(1, 12)
decay_2 = Fraction(2, 15)
decay_3 = Fraction(1, 5)
buff_type = {'Armor': [], 'Favonius': [], 'Crystal': 3}
buff0 = {'ATK_num': 0, 'ATK_per': 0, 'HP_num': 0, 'HP_per': 0, 'DEF_num': 0, 'DEF_per': 0, 'EM': 0, 'ER': 0,
         'CR': 0, 'CD': 0, 'UP': 0, 'def_ig': 0, 'rea_ex': 0, 'extra': 0, 'Healer': 0, 'Healee': 0, 'speed': 0,
         'SS': 0}
debuff0 = {'resi': {'Pyro': 0.1, 'Hydro': 0.1, 'Anemo': 0.1, 'Electro': 0.1, 'Dendro': 0.1, 'Cyro': 0.1, 'Geo': 0.1,
                    'Physic': 0.1}, 'def_de': 0}
stand = {}
results = {}


# 伤害计算
def res(i):
    if i > 0.75:
        f = 1 / (4 * i + 1)
    elif i < 0:
        f = 1 - i / 2
    else:
        f = 1 - i
    return f


def aggravate(em, element_, extra=0.0):
    base = 1446.85 * element_ * (1 + em * 5 / (em + 1200) + extra)
    return base


def react_dmg(em, rea_type_, element_, debuff_, extra=0.0):
    resi_ = debuff_['resi'][element_]
    if rea_type_ in [0.0, 0.25, 0.5, 0.6, 1.6, 2.0, 3.0]:
        dmg = 1446.85 * rea_type_ * (1 + em * 16 / (em + 2000) + extra) * res(resi_)
    else:
        dmg = rea_type_ * res(resi_)
    return dmg


def seed_dmg(seed_, debuff_):
    em = seed_[2]
    extra = seed_[3]
    if seed_[-1] in ['Hyper', 'Burst']:
        rea_type_ = 3
    else:
        rea_type_ = 2
    resi_ = debuff_['resi']['Dendro']
    dmg = 1446.85 * rea_type_ * (1 + em * 16 / (em + 2000) + extra) * res(resi_)
    return dmg


def damage(state_, property_, debuff_, atk_m=0.0, hp_m=0.0, def_m=0.0, em_m=0.0, enemy_lv=90):
    # 解包
    atk_v = state_['ATK']
    hp_v = state_['HP']
    def_v = state_['DEF']
    em_v = state_['EM']
    up = state_['UP']
    crit_rate = state_['CR']
    crit_dmg = state_['CD']
    extra = state_.get('extra', 0.0)
    rea_ex_ = state_.get('rea_ex', 0.0)
    def_ig_ = state_.get('def_ig', 0.0)
    if type(property_[0]) is str and type(property_[1]) is float:
        if property_[0] == 'ATK':
            atk_m = property_[1]
        elif property_[0] == 'HP':
            hp_m = property_[1]
        elif property_[0] == 'DEF':
            def_m = property_[1]
        elif property_[0] == 'EM':
            em_m = property_[1]
    elif type(property_[0]) is tuple and type(property_[1]) is tuple:
        for k in range(len(property_[0])):
            if property_[0][k] == 'ATK':
                atk_m = property_[1][k]
            elif property_[0][k] == 'HP':
                hp_m = property_[1][k]
            elif property_[0][k] == 'DEF':
                def_m = property_[1][k]
            elif property_[0][k] == 'EM':
                em_m = property_[1][k]
    for key_ in state_:
        if key_.endswith('_' + property_[2]):
            up += state_[key_]
    resi_ = debuff_['resi'][property_[2]]
    def_de_ = debuff_['def_de']
    rea_ = property_[3]
    # 计算
    if rea_ == 1.15 or rea_ == 1.25:
        extra += aggravate(em_m, rea_, rea_ex_)
        rea_ = 1
    elif rea_ == 1.5 or rea_ == 2:
        rea_ *= 1 + 2.78 * em_v / (em_v + 1400) + rea_ex_

    base = atk_v * atk_m + hp_v * hp_m + def_v * def_m + extra
    dmg = base * rea_ * (1 + up) * (1 + min(max(crit_rate, 0), 1) * crit_dmg) * res(resi_) * 950 / (
            max((5 * enemy_lv + 500) * (1 - def_de_) * (1 - def_ig_), 0) + 950)
    return dmg


# 治疗计算
def heal(state_, stable_, muti_, type_):
    source = state_[type_]
    heal_ = (source * muti_ * (1 + state_['Healer']) + stable_) * (1 + state_['Healee'])
    return heal_


# 攻击类型判断
def attack_type(now_):
    now_ = now_.lower()
    if '_' not in now_:
        type_ = now_[0]
    else:
        type_ = now_.split('_')[-1][0]
    if type_ not in ['a', 'e', 'q', 'z', 'x', 's']:
        type_ = '?'
    return type_


# 其他机制
def del_rep(lst):
    seen = set()
    result = [x for x in lst if not (x in seen or seen.add(x))]
    return result


def calc_skill(frame, now, forward):
    for func in act_lst:
        result = func(frame, now, forward)
        if result:
            return result


def calc_buff(frame, now, char, forward, info, act, buff_type_, stand, change_hp_per, base_, state_, buff_1, buff_2,
              moment_hp, party_element, buff0_=None, debuff0_=None):
    if buff0_ is None:
        buff0_ = buff0
    if debuff0_ is None:
        debuff0_ = debuff0
    buff_ = copy.deepcopy(buff0_)
    debuff_ = copy.deepcopy(debuff0_)
    for func in buff_1:
        a, b, c = func(frame, now, char, forward, info, act, buff_type_, stand, change_hp_per, copy.deepcopy(state_),
                       moment_hp, party_element)
        for key in a:
            buff_[key] = buff_.get(key, 0) + a[key]
        buff_type_.update(b)
        for key in c:
            if key == 'resi':
                for key_ in c[key]:
                    debuff_[key][key_] += c[key][key_]
            else:
                debuff_[key] += c[key]
    state_ = state(state_, base_, buff_)

    buff_ = copy.deepcopy(buff0_)
    for func in buff_2:
        a, b, c = func(frame, now, char, forward, info, act, buff_type_, stand, change_hp_per, copy.deepcopy(state_),
                       moment_hp, party_element)
        for key in a:
            buff_[key] = buff_.get(key, 0) + a[key]
        buff_type_.update(b)
        for key in c:
            if key == 'resi':
                for key_ in c[key]:
                    debuff_[key][key_] += c[key][key_]
            else:
                debuff_[key] += c[key]
    state_ = state(state_, base_, buff_)
    return state_, debuff_, buff_type_


def state(state_, base_, buff_):
    # 总面板
    ATK = state_['ATK'] + base_['ATK'] * buff_['ATK_per'] + buff_.get('ATK_num', 0.0)
    HP = state_['HP'] + base_['HP'] * buff_['HP_per'] + buff_.get('HP_num', 0.0)
    DEF = state_['DEF'] + base_['DEF'] * buff_['DEF_per'] + buff_.get('DEF_num', 0.0)
    EM = state_['EM'] + buff_.get('EM', 0.0)
    ER = state_['ER'] + buff_.get('ER', 0.0)
    CR = state_['CR'] + buff_.get('CR', 0.0)
    CD = state_['CD'] + buff_.get('CD', 0.0)
    UP = state_.get('UP', 0.0) + buff_.get('UP', 0.0)
    def_ig = state_.get('def_ig', 0.0) + buff_.get('def_ig', 0.0)
    rea_ex = state_.get('rea_ex', 0.0) + buff_.get('rea_ex', 0.0)
    extra = state_.get('extra', 0.0) + buff_.get('extra', 0.0)
    Healer = state_.get('Healer', 0.0) + buff_.get('Healer', 0.0)
    Healee = state_.get('Healee', 0.0) + buff_.get('Healee', 0.0)
    SS = state_.get('SS', 0.0) + buff_.get('SS', 0.0)
    UP_Pyro = state_.get('UP_Pyro', 0.0) + buff_.get('UP_Pyro', 0.0)
    UP_Hydro = state_.get('UP_Hydro', 0.0) + buff_.get('UP_Hydro', 0.0)
    UP_Anemo = state_.get('UP_Anemo', 0.0) + buff_.get('UP_Anemo', 0.0)
    UP_Electro = state_.get('UP_Electro', 0.0) + buff_.get('UP_Electro', 0.0)
    UP_Dendro = state_.get('UP_Dendro', 0.0) + buff_.get('UP_Dendro', 0.0)
    UP_Cyro = state_.get('UP_Cyro', 0.0) + buff_.get('UP_Cyro', 0.0)
    UP_Geo = state_.get('UP_Geo', 0.0) + buff_.get('UP_Geo', 0.0)
    UP_Physic = state_.get('UP_Physic', 0.0) + buff_.get('UP_Physic', 0.0)

    dic_ = {'ATK': ATK, 'HP': HP, 'DEF': DEF, 'EM': EM, 'ER': ER, 'CR': CR, 'CD': CD, 'UP': UP, 'def_ig': def_ig,
            'rea_ex': rea_ex, 'extra': extra, 'Healer': Healer, 'Healee': Healee, 'SS': SS, 'UP_Pyro': UP_Pyro,
            'UP_Hydro': UP_Hydro, 'UP_Anemo': UP_Anemo, 'UP_Electro': UP_Electro, 'UP_Dendro': UP_Dendro,
            'UP_Cyro': UP_Cyro, 'UP_Geo': UP_Geo, 'UP_Physic': UP_Physic}
    return dic_


def reaction(later_, char_, frame__, tar):
    global elements
    lst_dmg = []
    lst_up = []
    lst_seed = []
    stay = True
    if later_:
        if not later_[0]:
            return lst_dmg, lst_up, lst_seed
        if later_[0] == 'Pyro' and later_[1]:
            if elements[tar]['Electro']:
                minus = min(later_[1], elements[tar]['Electro'])
                lst_dmg.append([frame__, 'Pyro', char_, 2.0])
                later_[1] -= minus
                elements[tar]['Electro'] -= minus
                stay = False
            if elements[tar]['Cyro']:
                minus = min(later_[1], elements[tar]['Cyro'] / 2)
                lst_up.append(2.0)
                later_[1] -= minus
                elements[tar]['Cyro'] -= minus * 2
                stay = False
            if elements[tar]['Frozen']:
                minus = min(later_[1], elements[tar]['Frozen'] / 2)
                lst_up.append(2.0)
                later_[1] = 0
                elements[tar]['Frozen'] -= minus * 2
                stay = False
            if elements[tar]['Hydro']:
                minus = min(later_[1] / 2, elements[tar]['Hydro'])
                lst_up.append(1.5)
                later_[1] -= minus * 2
                elements[tar]['Hydro'] -= minus
                stay = False
            if elements[tar]['Dendro'] or elements[tar]['Aggr']:
                elements[tar]['Burn'] = Fraction(2)
                elements[tar]['B_char'] = char_
                stay = True

        elif later_[0] == 'Hydro' and later_[1]:
            if elements[tar]['Cyro']:
                minus = min(later_[1], elements[tar]['Cyro'])
                elements[tar]['Frozen'] += minus * 2
                later_[1] -= minus
                elements[tar]['Cyro'] -= minus
                stay = False
            if elements[tar]['Pyro'] or elements[tar]['Burn']:
                minus = min(later_[1], max(elements[tar]['Pyro'], elements[tar]['Burn']) / 2)
                lst_up.append(2.0)
                later_[1] -= minus
                elements[tar]['Pyro'] = max(elements[tar]['Pyro'] - minus * 2, Fraction(0))
                elements[tar]['Burn'] = max(elements[tar]['Burn'] - minus * 2, Fraction(0))
                stay = False
            if elements[tar]['Dendro'] or elements[tar]['Aggr']:
                minus = min(later_[1] / 2, max(elements[tar]['Dendro'], elements[tar]['Aggr']))
                lst_seed.append([frame__, 'Proto', char_])
                later_[1] -= minus * 2
                elements[tar]['Aggr'] = max(elements[tar]['Aggr'] - minus, Fraction(0))
                elements[tar]['Dendro'] = max(elements[tar]['Dendro'] - minus, Fraction(0))
                stay = False

        elif later_[0] == 'Anemo' and later_[1]:
            stay = False
            if elements[tar]['Cyro']:
                minus = min(later_[1] / 2, elements[tar]['Cyro'])
                lst_dmg.append([frame__, 'Cyro', char_, 0.6])
                later_[1] -= minus * 2
                elements[tar]['Cyro'] -= minus
            if elements[tar]['Electro']:
                minus = min(later_[1] / 2, elements[tar]['Electro'])
                lst_dmg.append([frame__, 'Electro', char_, 0.6])
                later_[1] -= minus * 2
                elements[tar]['Electro'] -= minus
            if elements[tar]['Hydro']:
                minus = min(later_[1] / 2, elements[tar]['Hydro'])
                lst_dmg.append([frame__, 'Hydro', char_, 0.6])
                later_[1] -= minus * 2
                elements[tar]['Hydro'] -= minus
            if elements[tar]['Frozen']:
                minus = min(later_[1] / 2, elements[tar]['Frozen'])
                lst_dmg.append([frame__, 'Cyro', char_, 0.6])
                later_[1] -= minus * 2
                elements[tar]['Frozen'] -= minus
            if elements[tar]['Pyro'] or elements[tar]['Burn']:
                minus = min(later_[1] / 2, max(elements[tar]['Pyro'], elements[tar]['Burn']))
                lst_dmg.append([frame__, 'Pyro', char_, 0.6, ])
                later_[1] -= minus * 2
                elements[tar]['Pyro'] = max(elements[tar]['Pyro'] - minus, Fraction(0))
                elements[tar]['Burn'] = max(elements[tar]['Burn'] - minus, Fraction(0))

        elif later_[0] == 'Electro' and later_[1]:
            if elements[tar]['Pyro']:
                minus = min(later_[1], elements[tar]['Pyro'])
                lst_dmg.append([frame__, 'Pyro', char_, 2.0])
                later_[1] -= minus
                elements[tar]['Pyro'] -= minus
                stay = False
            if elements[tar]['Cyro']:
                minus = min(later_[1], elements[tar]['Cyro'])
                lst_dmg.append([frame__, 'Cyro', char_, 0.5])
                later_[1] -= minus
                elements[tar]['Cyro'] -= minus
                stay = False
            if elements[tar]['Dendro']:
                minus = min(later_[1], elements[tar]['Dendro'])
                elements[tar]['Aggr'] = minus
                if minus < 2:
                    elements[tar]['Aggr_decay'] = decay_1
                elif minus == 2:
                    elements[tar]['Aggr_decay'] = decay_2
                elif minus == 4:
                    elements[tar]['Aggr_decay'] = decay_3
                elements[tar]['Dendro'] -= minus
                stay = False

        elif later_[0] == 'Dendro' and later_[1]:
            if elements[tar]['Pyro']:
                elements[tar]['Burn'] = Fraction(2)
                elements[tar]['B_char'] = char_
                stay = True
            if elements[tar]['Electro']:
                minus = min(later_[1], elements[tar]['Dendro'])
                elements[tar]['Aggr'] = minus
                if minus < 2:
                    elements[tar]['Aggr_decay'] = decay_1
                elif minus == 2:
                    elements[tar]['Aggr_decay'] = decay_2
                elif minus == 4:
                    elements[tar]['Aggr_decay'] = decay_3
                elements[tar]['Dendro'] -= minus
                if elements[tar]['Hydro'] and elements[tar]['Aggr']:
                    minus = min(elements[tar]['Aggr'], elements[tar]['Hydro'])
                    elements[tar]['Aggr'] = max(minus, Fraction(2))
                    lst_seed.append('')
                    elements[tar]['Hydro'] -= minus
                    elements[tar]['Aggr'] -= minus
                stay = False

        elif later_[0] == 'Cyro' and later_[1]:
            if elements[tar]['Pyro']:
                minus = min(later_[1], elements[tar]['Pyro'] / 2)
                lst_up.append(1.5)
                later_[1] -= minus
                elements[tar]['Pyro'] -= minus * 2
                stay = False
            if elements[tar]['Electro']:
                minus = min(later_[1], elements[tar]['Electro'])
                lst_dmg.append([frame__, 'Cyro', char_, 0.5])
                later_[1] -= minus
                elements[tar]['Electro'] -= minus
                stay = False
            if elements[tar]['Hydro']:
                minus = min(later_[1], elements[tar]['Hydro'])
                elements[tar]['Frozen'] += minus * 2
                later_[1] -= minus
                elements[tar]['Hydro'] -= minus
                stay = False

        elif later_[0] == 'Geo' and later_[1]:
            stay = False
            if elements[tar]['Cyro']:
                minus = min(later_[1] / 2, elements[tar]['Cyro'])
                lst_dmg.append([frame__, 'Cyro', char_, 0.0])
                later_[1] -= minus * 2
                elements[tar]['Cyro'] -= minus
            if elements[tar]['Electro']:
                minus = min(later_[1] / 2, elements[tar]['Electro'])
                lst_dmg.append([frame__, 'Electro', char_, 0.0])
                later_[1] -= minus * 2
                elements[tar]['Electro'] -= minus
            if elements[tar]['Hydro']:
                minus = min(later_[1] / 2, elements[tar]['Hydro'])
                lst_dmg.append([frame__, 'Hydro', char_, 0.0])
                later_[1] -= minus * 2
                elements[tar]['Hydro'] -= minus
            if elements[tar]['Frozen']:
                minus = min(later_[1] / 2, elements[tar]['Frozen'])
                lst_dmg.append([frame__, 'Cyro', char_, 0.0])
                later_[1] -= minus * 2
                elements[tar]['Frozen'] -= minus
            if elements[tar]['Pyro'] or elements[tar]['Burn']:
                minus = min(later_[1] / 2, max(elements[tar]['Pyro'], elements[tar]['Burn']))
                lst_dmg.append([frame__, 'Pyro', char_, 0.0])
                later_[1] -= minus * 2
                elements[tar]['Pyro'] = max(elements[tar]['Pyro'] - minus, Fraction(0))
                elements[tar]['Burn'] = max(elements[tar]['Burn'] - minus, Fraction(0))

        if stay:
            if elements[tar][later_[0]] == 0:
                if later_[1] >= 4:
                    elements[tar][later_[0] + '_decay'] = decay_3
                elif later_[1] >= 2:
                    elements[tar][later_[0] + '_decay'] = decay_2
                else:
                    elements[tar][later_[0] + '_decay'] = decay_1
            elements[tar][later_[0]] = later_[1] * Fraction(4, 5)
            if later_[0] == 'Electro' or later_[0] == 'Hydro':
                elements[tar]['EC_char'] = char_

    if elements[tar]['Aggr'] and later_[0] == 'Electro':
        lst_up.append(1.15)
    if elements[tar]['Aggr'] and later_[0] == 'Dendro':
        lst_up.append(1.25)
    if elements[tar]['Electro'] and elements[tar]['Hydro'] and elements[tar]['EC_last'] < frame__ - 30:
        lst_dmg.append([frame__, 'Electro', elements[tar]['EC_char'], 1.2])
        elements[tar]['Electro'] = max(elements[tar]['Electro'] - Fraction(2, 5), Fraction(0))
        elements[tar]['Hydro'] = max(elements[tar]['Hydro'] - Fraction(2, 5), Fraction(0))
        elements[tar]['EC_last'] = frame__
    if elements[tar]['Burn'] and elements[tar]['B_last'] < frame__ - 15:
        lst_dmg.append([frame__, 'Electro', elements[tar]['B_char'], 0.25])
        elements[tar]['B_last'] = frame__
        elements[tar]['Pyro'] = max(elements[tar]['Pyro'], Fraction(4, 5))

    lst_dmg_1 = []
    found = False
    for i in lst_dmg:
        if i[-1] == 0.0:
            if not found:
                lst_dmg_1.append(i)
                found = True
        else:
            lst_dmg_1.append(i)
    return lst_dmg, lst_up, lst_seed


def resonance(frame, now, char, forward, info, act, buff_type, stand, change_hp_per, state_act, moment_hp,
              party_element):
    buff_type_ = {}
    buff_ = {}
    debuff_ = {'resi': {}}
    if len([k for k in party_element if k == 'Hydro']):
        buff_['HP_per'] = 0.25
    if len([k for k in party_element if k == 'Pyro']):
        buff_['ATK_per'] = 0.25
    if len([k for k in party_element if k == 'Geo']):
        buff_['SS'] = 0.15
        buff_type_['Geo'] = True
    if buff_type.get('Geo', False):
        shield = 0
        for key in buff_type:
            if key.endswith('_shield'):
                shield = max(shield, buff_type[key][0])
        if shield and char in stand.values():
            buff_['UP'] = 0.15
            debuff_['resi']['Geo'] = -0.2

    return buff_, buff_type_, debuff_


buff_1.append(resonance)


def miko_remove(frame_, old):
    new = [i for i in old if not (i[0] > frame_ and i[2] == 'Miko_e0')]
    return new


def kokomi_fresh(frame_, old):
    new = [i for i in old if not (i[0] > frame_ and i[2] == 'Kokomi_e0')]
    for x in reversed(new):
        if x[2] == 'Kokomi_e0':
            last = x[0]
            break
    else:
        last = 0
    if last:
        for i in range(info['Kokomi_back']['Kokomi_e1'][2], 721, info['Kokomi_back']['Kokomi_e1'][3]):
            new.append([last + i, 'back', 'Kokomi_e1'])
    return new


def prototype_gen(frame_, old2,forward_):
    new2 = copy.deepcopy(old2)
    new2.append([frame_ + 120, forward_+'_Prototype'])
    new2.append([frame_ + 240, forward_+'_Prototype'])
    new2.append([frame_ + 360, forward_+'_Prototype'])
    return new2
