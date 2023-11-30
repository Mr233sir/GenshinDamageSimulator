"""
TODO:
已完成:行动条生成 全元素反应 元素附着cd/衰减 实时buff计算 生存压力/削韧测试 充能模拟 角色参数分离 护盾 元素增伤分离 草种子 风系染色 海染泡
暂时放弃:碎冰
"""
import os
from wcwidth import wcswidth
from Data.PublicData import *
import importlib
from datetime import datetime
import time


# 特殊机制
def special_gen(lst, lst2):
    global frame_gen
    for fun in buff_sp:
        buff_type.update(fun(frame_gen, lst[-1][1], lst[-1][2]))
    if lst[-1][2][0].lower() == 'a' and buff_type.get('speed', False) and len(lst) >= 2:
        if buff_type['speed'][1] < frame_gen < buff_type['speed'][2]:
            frame_gen -= int((lst[-1][0] - lst[-2][0]) * buff_type['speed'][0])
    # 神子q
    if now == 'q' and forward == 'Miko':
        lst = miko_remove(frame_gen, lst)
    # 雷神q
    if now == 'q' and forward == 'Raiden':
        lst = kokomi_fresh(frame_gen, lst)
        buff_type['Armor'].append(['Raiden', 0.0, frame_gen, frame_gen + 420])
    for x in reversed(lst):
        if x[1] == 'Raiden' and x[2] == 'q':
            enhance_ini = x[0]
            for y in lst:
                if enhance_ini < y[0] < enhance_ini + 420 and y[1] == 'Raiden' and y[2][0] in ['a', 'z']:
                    y[2] = y[2].title()
    # 心海q
    if now == 'q' and forward == 'Kokomi':
        lst = kokomi_fresh(frame_gen, lst)
        buff_type['Armor'].append(['Kokomi', 0.25, frame_gen, frame_gen + 600])
    for x in reversed(lst):
        if x[2] == 'q' and x[1] == 'Kokomi':
            enhance_ini = x[0]
            for y in lst:
                if enhance_ini < y[0] < enhance_ini + 600 and y[1] == 'Kokomi' and y[2][0] == 'a':
                    y[2] = y[2].title()
                    lst2.append([y[0], 'Kokomi_' + y[2]])
    # 金珀
    if forward_gen in buff_type.get('Prototype', []) and now_gen == 'q':
        lst2 = prototype_gen(frame_gen, lst2, forward_gen)
    # 娜维娅e
    for x in reversed(lst):
        if x[1] == 'Navia' and attack_type(x[2]) == 'e':
            enhance_ini = x[0]
            for y in lst:
                if enhance_ini < y[0] < enhance_ini + 240 and y[1] == 'Navia' and y[2][0] in ['a', 'z']:
                    y[2] = y[2].title()
    return lst, lst2


def special_calc(act__, heal__):
    global change_hp_per
    if len(act__) >= 3:
        if act__[1] == 'Furina' and act__[2] == 'q':
            change_hp_per = 0.0
        if act__[1] == 'Zhongli' and act__[2] == 'E':
            now_ = act__[2]
            frame__ = act__[0]
            char_ = now.split('_')[0] if '_' in now else act__[1]
            state_act_ = copy.deepcopy(info[char + '_state'])
            base_act_ = copy.deepcopy(info[char + '_base'])
            state_act_ = calc_buff(frame__, now_, char_, forward, info, act,
                                   copy.deepcopy(buff_type), stand, change_hp_per,
                                   copy.deepcopy(base_act_), copy.deepcopy(state_act_), buff_1,
                                   buff_2, copy.deepcopy(moment_hp), party_element)[0]
            buff_type['Jade_shield'] = [(state_act_['HP'] * 0.218 + 2506) * 1.5, frame__, frame__ + 1200]
        if act__[1] in buff_type['Favonius'] and '_' not in act__[2]:
            if not buff_type.get('Favonius_cd_' + act__[1], False):
                sequence_energy.append([act__[0] + 60, 3, 'null'])
                buff_type['Favonius_cd_' + act__[1]] = 360
    else:
        if act__[1].split('_')[0] != 'Furina' and 'Furina' in stand.values() and moment_hp[forward] == 1.0:
            for item_ in reversed(sequence_heal):
                if item_[1] == 'Furina_psv_1':
                    last_ = item_[0]
                    break
            else:
                last_ = 0
            for k in range(max(last_, act__[0]) + 120, frame + 240, 120):
                sequence_heal.append([k, 'Furina_psv_1'])
        if act__[1].split('_')[0] in buff_type.get('Ocean', []) and heal__ > 0:
            if 'Ocean_' not in buff_type and buff_type.get('Ocean_last', -210) <= act__[0] - 210:
                buff_type['Ocean_'] = [act__[0], min(heal__, 30000)]
                buff_type['Ocean_last'] = act__[0]
            elif 'Ocean_' in buff_type:
                buff_type['Ocean_'][1] = min(buff_type['Ocean_'][1] + heal__, 30000)


# 配置
stand = {1: 'Kokomi', 2: 'Yelan', 3: 'Kazuha', 4: 'Furina'}
moment_hp = {stand[1]: 1.0, stand[2]: 1.0, stand[3]: 1.0, stand[4]: 1.0}
cycle_length = 1200
enemy_lv = 90
enemy_start = 120
enemy_damage = 15000
tough_de = enemy_tough_de = 75
unbalance_time = 60
enemy_damage_interval = 60
unbalance_counter = 0
enemy_energy = 1
enemy_energy_dmg = 200000
buff = copy.deepcopy(buff0)
debuff = copy.deepcopy(debuff0)
sequence_input = '4 e q 3 E 1 e 2 q a1 0.1s e a1 e 3 a1 q 1 q a1 a2 s a1 a2 s a1 a2 s a1 a2 s a1 a2 s a1 a2 s a1 ' \
                     'a2 s a1 a2'

# 防warning
start_time = time.time()
name = {}
forward_gen = forward = stand[1]
char1 = char = stand[1]
buff_1 = buff_1
buff_2 = buff_2
frame_gen = frame = 0
sequence_act = sequence_act
sequence_heal = sequence_heal
now1 = now = now
base_act = base_act
state_act = state_act
change_hp_per = 0.0
app = None
act = act
shield = 0
heal_value = 0
enemy_energy_exist = 0

# 导入数据
for value in stand.values():
    try:
        module = importlib.import_module('Data.' + value)
    except ModuleNotFoundError:
        raise Exception('角色不存在')
    else:
        try:
            buff_1.extend(getattr(module, 'buff_1'))
            buff_2.extend(getattr(module, 'buff_2'))
            buff_sp.extend(getattr(module, 'buff_sp'))
            act_lst.extend(getattr(module, 'act_lst'))
            heal_lst.extend(getattr(module, 'heal_lst'))
            with_lst.extend(getattr(module, 'with_lst'))
        except AttributeError:
            raise Exception('列表不存在')
        try:
            info.update(getattr(module, 'info'))
            name.update(getattr(module, 'name'))
            buff_type_ = getattr(module, 'buff_type')
            for key in buff_type_:
                if key in buff_type:
                    buff_type[key].extend(buff_type_[key])
                else:
                    buff_type[key] = buff_type_[key]
        except AttributeError:
            raise Exception('字典不存在')
        except Exception:
            raise Exception('字典格式错误')
    finally:
        buff_1 = del_rep(buff_1)
        buff_2 = del_rep(buff_2)
toughness = {stand[1]: info[stand[1] + '_tough'][0], stand[2]: info[stand[2] + '_tough'][0],
             stand[3]: info[stand[3] + '_tough'][0], stand[4]: info[stand[4] + '_tough'][0]}
moment_charge = {stand[1]: info[stand[1] + '_charge_max'], stand[2]: info[stand[2] + '_charge_max'],
                 stand[3]: info[stand[3] + '_charge_max'], stand[4]: info[stand[4] + '_charge_max']}
total_charge = {stand[1]: 0.0, stand[2]: 0.0, stand[3]: 0.0, stand[4]: 0.0}
party_element = [info[stand[1] + '_base']['Element'], info[stand[2] + '_base']['Element'],
                 info[stand[3] + '_base']['Element'], info[stand[4] + '_base']['Element']]
for t in range(enemy_start, cycle_length, enemy_damage_interval):
    sequence_enemy.append([t, enemy_damage])

results['生存情况'] = ['0.0s,', f'{name[stand[1]]} {round(moment_hp[stand[1]] * 100, 1)}%,',
                       f'{name[stand[2]]} {round(moment_hp[stand[2]] * 100, 1)}%,',
                       f'{name[stand[3]]} {round(moment_hp[stand[3]] * 100, 1)}%,',
                       f'{name[stand[4]]} {round(moment_hp[stand[4]] * 100, 1)}%\n']
results['伤害情况'] = ['0.0s  初始化完成  0.0\n']
results['充能情况'] = ['0.0s,', f'{name[stand[1]]} {round(moment_charge[stand[1]], 1)},  ',
                       f'{name[stand[2]]} {round(moment_charge[stand[2]], 1)},  ',
                       f'{name[stand[3]]} {round(moment_charge[stand[3]], 1)},  ',
                       f'{name[stand[4]]} {round(moment_charge[stand[4]], 1)}\n']

# 计算模拟
sequence_gen = sequence_input.split(' ')
for current_time in range(cycle_length + 1):
    damage_active = True
    # 行动生成
    if order_gen < len(sequence_gen):
        if current_time >= frame_gen:
            if sequence_gen[order_gen].isdigit():
                forward_gen = stand[int(sequence_gen[order_gen])]
            elif sequence_gen[order_gen][0].isdigit() and sequence_gen[order_gen].endswith('s'):
                frame_gen += round(float(sequence_gen[order_gen][:-1]) * 60)
            else:
                now_gen = sequence_gen[order_gen]
                frame_gen, act_gen, heal_gen = calc_skill(frame_gen, now_gen, forward_gen)
                sequence_heal.extend(heal_gen)
                if act_gen:
                    if type(act_gen[0]) is list:
                        sequence_act.extend(act_gen)
                    else:
                        sequence_act.append(act_gen)
                sequence_act, sequence_heal = special_gen(sequence_act, sequence_heal)
                sequence_act.sort(key=lambda x: x[0])
                sequence_heal.sort(key=lambda x: x[0])
                for item in sequence_act:
                    if item[1] == 'back':
                        item[1] = forward
                    else:
                        forward = item[1]
            order_gen += 1
    # 场上角色信息
    if order_dmg < len(sequence_act):
        if current_time >= sequence_act[order_dmg][0]:
            if sequence_act[order_dmg][1] in stand.values() and '_' not in sequence_act[order_dmg][2]:
                forward = sequence_act[order_dmg][1]
            if sequence_act[order_dmg][1] in stand.values() and '_' not in sequence_act[order_dmg][2]:
                now1 = sequence_act[order_dmg][2]
    # 原魔伤害/削韧
    if order_enemy < len(sequence_enemy):
        if current_time >= sequence_enemy[order_enemy][0]:
            state_act = copy.deepcopy(info[forward + '_state'])
            base_act = copy.deepcopy(info[forward + '_base'])
            previous_hp = copy.deepcopy(moment_hp)
            state_act, debuff, buff_type_ = calc_buff(current_time, now, char, forward, info, act,
                                                      copy.deepcopy(buff_type), stand, change_hp_per,
                                                      copy.deepcopy(base_act), copy.deepcopy(state_act), buff_1,
                                                      buff_2, copy.deepcopy(moment_hp), party_element)
            buff_type.update(buff_type_)
            moment_def = state_act['DEF']
            moment_ss = state_act['SS']
            moment_hp_max = state_act['HP']
            if now1 not in ['q0', 's']:
                if now1 in ['e', 'E']:
                    tough_de = enemy_tough_de * 0.6
                for item in buff_type['Armor']:
                    if item[0] == 'forward' and item[-1] >= current_time > item[-2]:
                        tough_de *= item[1]
                    elif item[0] == forward and item[-1] >= current_time > item[-2]:
                        tough_de *= item[1]
                Damage = sequence_enemy[order_enemy][1] * ((enemy_lv * 5 + 500) / (moment_def + enemy_lv * 5 + 1000))
                for key in buff_type:
                    if key.endswith('_shield'):
                        shield = max(buff_type[key][0], shield)
                shield *= (1 + moment_ss)
                if shield >= Damage:
                    for key in buff_type:
                        if key.endswith('_shield'):
                            buff_type[key][0] = max(buff_type[key][0] - Damage / (1 + moment_ss), 0.0)
                elif shield > 0.1:
                    moment_hp[forward] -= (Damage - shield) / moment_hp_max
                    for key in buff_type:
                        if key.endswith('_shield'):
                            buff_type[key][0] = 0.0
                else:
                    moment_hp[forward] -= (Damage - shield) / moment_hp_max
                    toughness[forward] -= tough_de
                    for key in buff_type:
                        if key.endswith('_shield'):
                            buff_type[key][0] = 0.0
                if toughness[forward] <= 0:
                    for item in sequence_act:
                        if item[0] >= current_time:
                            item[0] += unbalance_time
                    toughness[forward] = info[forward + '_tough'][0]
                    results['生存情况'].append(
                        f'{round(current_time / 60, 1)}s,被打断,行动延后{round(unbalance_time / 60, 1)}s\n')
                    unbalance_counter += 1
                for item in moment_hp:
                    change_hp_per += abs(moment_hp[item] - previous_hp[item])
                results['生存情况'].extend(
                    [f'{round(current_time / 60, 1)}s,', f'{name[stand[1]]} {round(moment_hp[stand[1]] * 100, 1)}%,',
                     f'{name[stand[2]]} {round(moment_hp[stand[2]] * 100, 1)}%,',
                     f'{name[stand[3]]} {round(moment_hp[stand[3]] * 100, 1)}%,',
                     f'{name[stand[4]]} {round(moment_hp[stand[4]] * 100, 1)}%\n'])
            if moment_hp[forward] <= 0:
                print(f'当前时间{round(current_time / 60, 1)}s,{name[forward]}暴毙')
                break
            order_enemy += 1
    # 元素反应
    later = []
    if 'Ocean_' in buff_type:
        if buff_type['Ocean_'][0] <= current_time - 180:
            sequence_act.insert(order_dmg + 1, [current_time, 'Physic', 'Ocean', buff_type['Ocean_'][1] * 0.9])
            sequence_act.sort(key=lambda x: x[0])
            del buff_type['Ocean_']
    if order_dmg < len(sequence_act):
        act = sequence_act[order_dmg]
        if current_time >= act[0] and act[1] in stand.values():
            now = act[2]
            frame = act[0]
            char = now.split('_')[0] if '_' in now else act[1]
            if now.endswith('Dye') and now not in buff_type:
                for ele in ['Pyro', 'Hydro', 'Electro', 'Cyro']:
                    dye = ''
                    for target in elements:
                        if elements[target][ele] > 0:
                            dye = ele
                    if dye:
                        buff_type[now] = dye
                        break
            if info[char + '_ele'][now][3] and not elements['EnemyMain'].get(info[char + '_ele'][now][-1] + '_timer',
                                                                             False):
                elements['EnemyMain'][info[char + '_ele'][now][-1] + '_timer'] = info[char + '_ele'][now][3]
            if elements['EnemyMain'].get(info[char + '_ele'][now][-1] + '_timer', cycle_length) == 0:
                elements['EnemyMain'][info[char + '_ele'][now][-1]] = 0
            if info[char + '_ele'][now][1] and not elements['EnemyMain'].get(info[char + '_ele'][now][-1], False):
                later.append(info[char + '_ele'][now][0])
                later.append(Fraction(info[char + '_ele'][now][1]))
                elements['EnemyMain'][info[char + '_ele'][now][-1]] = max(info[char + '_ele'][now][2] - 1, 0)
            elif info[char + '_ele'][now][1] and elements['EnemyMain'].get(info[char + '_ele'][now][-1], False):
                elements['EnemyMain'][info[char + '_ele'][now][-1]] -= 1
        rea_dmg, rea_up, rea_seed = reaction(later, char, current_time + 1, 'EnemyMain')
        if rea_up and len(sequence_act[order_dmg]) < 4:
            sequence_act[order_dmg].append(rea_up[0])
        elif len(sequence_act[order_dmg]) < 4:
            sequence_act[order_dmg].append(1.0)
        if rea_dmg:
            for i in range(len(rea_dmg)):
                sequence_act.insert(order_dmg + i + 1, rea_dmg[i])
        # 草种子
        for item in rea_seed:
            state_act = copy.deepcopy(info[char + '_state'])
            base_act = copy.deepcopy(info[char + '_base'])
            state_act, debuff, buff_type_ = calc_buff(frame, now, char, forward, info, act,
                                                      copy.deepcopy(buff_type), stand, change_hp_per,
                                                      copy.deepcopy(base_act), copy.deepcopy(state_act), buff_1,
                                                      buff_2, copy.deepcopy(moment_hp), party_element)
            buff_type.update(buff_type_)
            if 'Nilou_psv_1_' in buff_type and int(buff_type['Nilou_psv_1__'][1]) <= frame < int(
                    buff_type['Nilou_psv_1_'][2]):
                delay = 30
            else:
                delay = 360
            seed_bank.append([frame, frame + delay, state_act['EM'], state_act['rea_ex'], ''])
            seed_bank.sort(key=lambda x: x[1])
    # 草种子迸发
    if seed_bank:
        if seed_bank[0][1] <= current_time:
            frame = seed_bank[0][1]
            Damage = seed_dmg(seed_bank[0], debuff)
            seed_bank.pop(0)
            try:
                if elements['EnemyMain']['seed_burst'][-1] > frame - 30 and elements['EnemyMain']['seed_burst'][
                    -2] > frame - 30:
                    seed_active = False
                else:
                    seed_active = True
            except IndexError:
                seed_active = True
            if seed_active:
                if act[-1] == 'Hyper':
                    rea_word = '超绽放'
                elif act[-1] == 'Burst':
                    rea_word = '烈绽放'
                else:
                    rea_word = '原绽放'
                total += Damage
                sequence_dmg.append([frame, rea_word, Damage])
                elements['EnemyMain']['seed_burst'].append(frame)
        if len(seed_bank) > 5:
            frame = current_time
            Damage = seed_dmg(seed_bank[0], debuff)
            seed_bank.pop(0)
            try:
                if elements['EnemyMain']['seed_burst'][-1] > frame - 30 and elements['EnemyMain']['seed_burst'][
                    -2] > frame - 30:
                    seed_active = False
                else:
                    seed_active = True
            except IndexError:
                seed_active = True
            if seed_active:
                if act[-1] == 'Hyper':
                    rea_word = '超绽放'
                elif act[-1] == 'Burst':
                    rea_word = '烈绽放'
                else:
                    rea_word = '原绽放'
                total += Damage
                sequence_dmg.append([frame, rea_word, Damage])
                elements['EnemyMain']['seed_burst'].append(frame)
    # 角色伤害
    if order_dmg < len(sequence_act):
        if current_time >= sequence_act[order_dmg][0]:
            act = sequence_act[order_dmg]
            now = act[2]
            frame = act[0]
            char = now.split('_')[0] if '_' in now else act[1]
            special_calc(act, 0)
            # 直伤
            if char in stand.values():
                rea_type = act[3]
                if '_' in now:
                    property_act = [info[char + '_back'][now][0], info[char + '_back'][now][1],
                                    info[char + '_base']['Element'], rea_type]
                else:
                    property_act = [info[char + '_skill'][now][0], info[char + '_skill'][now][1],
                                    info[char + '_base']['Element'], rea_type]
                if info[char + '_base']['Element'] == 'Pyro':
                    for item in seed_bank:
                        if not item[-1]:
                            item[1] = frame
                            item[-1] = 'Burst'
                elif info[char + '_base']['Element'] == 'Electro':
                    for item in seed_bank:
                        if not item[-1]:
                            item[1] = frame + 30
                            item[-1] = 'Hyper'
                if now.endswith('Dye') and buff_type.get(now, False):
                    property_act[2] = buff_type[now]
                elif now.endswith('Dye'):
                    damage_active = False
                if damage_active:
                    state_act = copy.deepcopy(info[char + '_state'])
                    base_act = copy.deepcopy(info[char + '_base'])
                    state_act, debuff, buff_type_ = calc_buff(frame, now, char, forward, info, act,
                                                              copy.deepcopy(buff_type), stand, change_hp_per,
                                                              copy.deepcopy(base_act), copy.deepcopy(state_act), buff_1,
                                                              buff_2, copy.deepcopy(moment_hp), party_element)
                    buff_type.update(buff_type_)
                    Damage = damage(state_act, property_act, debuff, enemy_lv=enemy_lv)
                    total += Damage
                    sequence_dmg.append([frame, name.get(char, '???') + attack_type(now), Damage])
                # 充能行动条
                if now == 'q0':
                    results['充能情况'].extend([f'{round(current_time / 60, 1)}s,{name[char]}开大清空能量，',
                                                f'开大前能量{round(moment_charge[char])}\n'])
                    moment_charge[char] = 0
                else:
                    if info[char + '_energy'].get(now, False):
                        if not info[char + '_energy'][now][-1] and not buff_type.get(
                                info[char + '_energy'][now][-1] + '_timer', False):
                            sequence_energy.append(
                                [current_time + 60, info[char + '_energy'][now][0], info[char + '_base']['Element']])
                            if info[char + '_energy'][now][-1]:
                                buff_type[info[char + '_energy'][now][-1] + '_timer'] = \
                                    info[char + '_energy'][now][1]

            # 剧变
            else:
                act = sequence_act[order_dmg]
                rea_type = act[3]
                if now in stand.values():
                    state_act = copy.deepcopy(info[now + '_state'])
                    base_act = copy.deepcopy(info[now + '_state'])
                    state_act, debuff, buff_type_ = calc_buff(frame, now, char, forward, info, act,
                                                              copy.deepcopy(buff_type), stand, change_hp_per,
                                                              copy.deepcopy(base_act), copy.deepcopy(state_act), buff_1,
                                                              buff_2, copy.deepcopy(moment_hp), party_element)
                    buff_type.update(buff_type_)
                    Damage = react_dmg(state_act['EM'], rea_type, char, debuff, state_act['rea_ex'])
                else:
                    Damage = react_dmg(0, rea_type, char, debuff, 0)
                if rea_type == 0.0:
                    moment_EM = state_act['EM']
                    shield = 1851 * (1 + 5 * moment_EM / (moment_EM + 1400))
                    buff_type['Crystal_shield'] = [shield, frame, frame + 900]
                total += Damage
                rea_word = '?'
                if rea_type == 0.25:
                    rea_word = '扩散'
                elif rea_type == 0.5:
                    rea_word = '超导'
                elif rea_type == 0.6:
                    if char == 'Pyro':
                        rea_word = '火扩散'
                    elif char == 'Hydro':
                        rea_word = '水扩散'
                    elif char == 'Electro':
                        rea_word = '雷扩散'
                    elif char == 'Cyro':
                        rea_word = '冰扩散'
                elif rea_type == 1.2:
                    rea_word = '感电'
                elif rea_type == 2.0:
                    rea_word = '超载'
                elif rea_type == 0.0:
                    rea_word = '结晶'
                else:
                    rea_word = '特殊'
                sequence_dmg.append([frame, rea_word, Damage])
            # 协同
            for func in with_lst:
                app, last = func(current_time, char, forward, info, act, buff_type, stand)
                if app:
                    if type(app[0]) is list:
                        for index in range(len(app)):
                            sequence_act.insert(order_dmg + index + 1, app[index])
                        info[app[0][-1] + '_last'] = last
                        sequence_act.sort(key=lambda x: x[0])
                    else:
                        sequence_act.insert(order_dmg + 1, app)
                        info[app[-1] + '_last'] = last
                    app = None
            sequence_energy.sort(key=lambda x: x[0])
            order_dmg += 1
    # 血量变动
    if order_heal < len(sequence_heal):
        if current_time >= sequence_heal[order_heal][0]:
            heal_ = sequence_heal[order_heal]
            frame = heal_[0]
            previous_hp = copy.deepcopy(moment_hp)
            for func in heal_lst:
                if func.__name__ == heal_[1].lower() + '_heal':
                    moment_hp, heal_value = func(frame, now, char, forward, info, act, copy.deepcopy(buff_type), stand,
                                                 change_hp_per,
                                                 copy.deepcopy(base_act), copy.deepcopy(state_act), buff_1, buff_2,
                                                 copy.deepcopy(moment_hp), party_element)
            for key in moment_hp:
                if 1 - moment_hp[key] < 0.001:
                    moment_hp[key] = 1.0
            special_calc(heal_, heal_value)
            sequence_heal.sort(key=lambda x: x[0])
            for item in moment_hp:
                change_hp_per += abs(moment_hp[item] - previous_hp[item])
            order_heal += 1
            sequence_hp.append([frame, copy.deepcopy(moment_hp)])
            results['生存情况'].extend(
                [f'{str(round(frame / 60, 1))}s,', f'{name[stand[1]]} {round(moment_hp[stand[1]] * 100, 1)}%,',
                 f'{name[stand[2]]} {round(moment_hp[stand[2]] * 100, 1)}%,',
                 f'{name[stand[3]]} {round(moment_hp[stand[3]] * 100, 1)}%,',
                 f'{name[stand[4]]} {round(moment_hp[stand[4]] * 100, 1)}%\n'])
    # 充能计算
    if total > (1 + enemy_energy_exist) * enemy_energy_dmg:
        num = int(total / enemy_energy_dmg - enemy_energy_exist)
        sequence_energy.append([current_time + 60, enemy_energy * num, 'null'])
        enemy_energy_exist += num
    for key in buff_type:
        if key.endswith('_timer'):
            buff_type[key] = max(buff_type[key] - 1, 0)
    if order_energy < len(sequence_energy):
        if current_time >= sequence_energy[order_energy][0]:
            for key in moment_charge:
                char = key
                state_act = copy.deepcopy(info[char + '_state'])
                base_act = copy.deepcopy(info[char + '_base'])
                state_act, debuff, buff_type_ = calc_buff(current_time, attack_type(now), char, forward, info, act,
                                                          copy.deepcopy(buff_type), stand, change_hp_per,
                                                          copy.deepcopy(base_act), copy.deepcopy(state_act), buff_1,
                                                          buff_2, copy.deepcopy(moment_hp), party_element)
                charge = state_act['ER']
                if key == forward:
                    if info[key + '_base']['Element'] == sequence_energy[order_energy][-1]:
                        moment_charge[key] = min(moment_charge[key] + sequence_energy[order_energy][1] * 3 * charge,
                                                 info[key + '_charge_max'])
                        total_charge[key] += sequence_energy[order_energy][1] * 3 * charge
                    elif sequence_energy[order_energy][-1] == 'null':
                        moment_charge[key] = min(moment_charge[key] + sequence_energy[order_energy][1] * 2 * charge,
                                                 info[key + '_charge_max'])
                        total_charge[key] += sequence_energy[order_energy][1] * 2 * charge
                    else:
                        moment_charge[key] = min(moment_charge[key] + sequence_energy[order_energy][1] * 1 * charge,
                                                 info[key + '_charge_max'])
                        total_charge[key] += sequence_energy[order_energy][1] * 1 * charge
                else:
                    if info[key + '_base']['Element'] == sequence_energy[order_energy][-1]:
                        moment_charge[key] = min(moment_charge[key] + sequence_energy[order_energy][1] * 1.8 * charge,
                                                 info[key + '_charge_max'])
                        total_charge[key] += sequence_energy[order_energy][1] * 1.8 * charge
                    elif sequence_energy[order_energy][-1] == 'null':
                        moment_charge[key] = min(moment_charge[key] + sequence_energy[order_energy][1] * 1.2 * charge,
                                                 info[key + '_charge_max'])
                        total_charge[key] += sequence_energy[order_energy][1] * 1.2 * charge
                    else:
                        moment_charge[key] = min(moment_charge[key] + sequence_energy[order_energy][1] * 0.6 * charge,
                                                 info[key + '_charge_max'])
                        total_charge[key] += sequence_energy[order_energy][1] * 0.6 * charge
            results['充能情况'].extend(
                [f'{round(current_time / 60, 1)}s,', f'{name[stand[1]]} {round(moment_charge[stand[1]], 1)},  ',
                 f'{name[stand[2]]} {round(moment_charge[stand[2]], 1)},  ',
                 f'{name[stand[3]]} {round(moment_charge[stand[3]], 1)},  ',
                 f'{name[stand[4]]} {round(moment_charge[stand[4]], 1)}\n'])
            order_energy += 1
    # 元素衰减
    if elements['EnemyMain']['Pyro'] != 0:
        elements['EnemyMain']['Pyro'] = max(
            elements['EnemyMain']['Pyro'] - elements['EnemyMain'].get('Pyro_decay', decay_1) / 60, Fraction(0))
    if elements['EnemyMain']['Hydro'] != 0:
        elements['EnemyMain']['Hydro'] = max(
            elements['EnemyMain']['Hydro'] - elements['EnemyMain'].get('Hydro_decay', decay_1) / 60, Fraction(0))
    if elements['EnemyMain']['Electro'] != 0:
        elements['EnemyMain']['Electro'] = max(
            elements['EnemyMain']['Electro'] - elements['EnemyMain'].get('Electro_decay', decay_1) / 60, Fraction(0))
    if elements['EnemyMain']['Dendro'] != 0:
        if elements['EnemyMain']['Burn'] == 0:
            elements['EnemyMain']['Dendro'] = max(
                elements['EnemyMain']['Dendro'] - elements['EnemyMain'].get('Dendro_decay', decay_1) / 60, Fraction(0))
        else:
            elements['EnemyMain']['Dendro'] = max(elements['EnemyMain']['Dendro'] - Fraction(2, 5) / 60, Fraction(0))
    if elements['EnemyMain']['Aggr'] != 0:
        if elements['EnemyMain']['Burn'] == 0:
            elements['EnemyMain']['Aggr'] = max(
                elements['EnemyMain']['Aggr'] - elements['EnemyMain'].get('Aggr_decay', decay_1) / 60, Fraction(0))
        else:
            elements['EnemyMain']['Aggr'] = max(elements['EnemyMain']['Aggr'] - Fraction(2, 5) / 60, Fraction(0))
    if elements['EnemyMain']['Cyro'] != 0:
        elements['EnemyMain']['Cyro'] = max(
            elements['EnemyMain']['Cyro'] - elements['EnemyMain'].get('Cyro_decay', decay_1) / 60, Fraction(0))
    if elements['EnemyMain']['Frozen'] != 0:
        elements['EnemyMain']['Frozen'] = max(
            elements['EnemyMain']['Frozen'] - elements['EnemyMain']['Frozen_decay'] / 60, Fraction(0))
        elements['EnemyMain']['Frozen_decay'] = min(elements['EnemyMain']['Frozen_decay'] + Fraction(1, 600),
                                                    Fraction(2))
    if elements['EnemyMain']['Dendro'] == 0:
        elements['EnemyMain']['Burn'] = Fraction(0)
    # 附着计时器衰减
    for key in element:
        if key.endswith('_timer'):
            elements['EnemyMain'][key] = max(elements['EnemyMain'][key] - 1, 0)
    # 西风计时器
    for key in buff_type:
        if key.startswith('Favonius_cd_'):
            buff_type[key] = max(buff_type[key] - 1, 0)
    # 韧性恢复
    for key in toughness:
        if toughness[key] < info[key + '_tough'][0]:
            toughness[key] = min(info[key + '_tough'][1] / 60, info[key + '_tough'][0])

else:
    for item in sequence_dmg:
        output1 = (str(round(item[0] / 60, 1)) + 's').ljust(6)
        output2_l = wcswidth(item[1])
        output2 = str(item[1]) + ' ' * (10 - output2_l)
        results['伤害情况'].append(f'{output1}{output2}{round(item[2], 1)}\n')
    total = sum(i[2] for i in sequence_dmg)
    total_1 = sum(i[2] for i in sequence_dmg if name[stand[1]] in i[1])
    total_2 = sum(i[2] for i in sequence_dmg if name[stand[2]] in i[1])
    total_3 = sum(i[2] for i in sequence_dmg if name[stand[3]] in i[1])
    total_4 = sum(i[2] for i in sequence_dmg if name[stand[4]] in i[1])
    results['统计信息'] = [f'轴长{round(cycle_length / 60)}s\n', f'总伤害 {round(total)}\n',
                           f'每秒伤害 {round(total * 60 / cycle_length)}\n',
                           f'{name[stand[1]]}伤害{round(total_1, 1)}占比{round(total_1 / total * 100, 2)}%\n',
                           f'{name[stand[2]]}伤害{round(total_2, 1)}占比{round(total_2 / total * 100, 2)}%\n',
                           f'{name[stand[3]]}伤害{round(total_3, 1)}占比{round(total_3 / total * 100, 2)}%\n',
                           f'{name[stand[4]]}伤害{round(total_4, 1)}占比{round(total_4 / total * 100, 2)}%\n',
                           f'反应伤害{round(total - total_1 - total_2 - total_3 - total_4, 1)}占比'
                           f'{round(100 - (total_1 + total_2 + total_3 + total_4) / total * 100, 2)}%\n\n',
                           f'被打断{unbalance_counter}次，行动总计延后{round(unbalance_counter * unbalance_time / 60, 1)}s\n',
                           f'\n{name[stand[1]]}总计获得充能{round(total_charge[stand[1]], 1)}\n',
                           f'{name[stand[2]]}总计获得充能{round(total_charge[stand[2]], 1)}\n',
                           f'{name[stand[3]]}总计获得充能{round(total_charge[stand[3]], 1)}\n',
                           f'{name[stand[4]]}总计获得充能{round(total_charge[stand[4]], 1)}\n']
if len(results['伤害情况']) == 1:
    results['伤害情况'].append('模拟中断，停止输出，请查看其他文件')
    results['统计信息'] = ['模拟中断，无法统计，请查看其他文件']

results['统计信息'].insert(0, f'模拟耗时{time.time() - start_time:.3f}s\n\n')
folder = datetime.now().strftime('output-%Y%m%d-%H%M%S')
if not os.path.exists(folder):
    os.makedirs(folder)
for category, result_list in results.items():
    file_path = os.path.join(folder, f'{category}.txt')
    if os.path.isfile(file_path):
        os.remove(file_path)
    with open(file_path, 'w', encoding='utf-8') as file:
        for result in result_list:
            file.write(result)

print(f'模拟结束，结果已输出到{os.getcwd()}\\{folder}文件夹内')
