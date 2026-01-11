import json
import re
import os

# Helper to extract Chinese part from bilingual strings
def extract_chinese(text):
    if not text: return ""
    match = re.search(r'[\(\[\（\【]([^\(\)\[\]\（\）\【\】]+)[\)\]\）\】]\s*$', text)
    if match:
        return match.group(1).strip()
    if any('\u4e00' <= c <= '\u9fff' for c in text):
        chn = "".join(re.findall(r'[\u4e00-\u9fff，。！？、：；（）“”‘’《》【】0-9\u2190-\u21ff\s\-\.]+', text))
        if ':' in chn and not any('\u4e00' <= c <= '\u9fff' for c in chn.split(':')[0]):
            chn = chn.split(':')[1]
        return chn.strip()
    return text.strip()

def clean_text(text):
    if not text: return ""
    return extract_chinese(text)

TERM_MAP = {
    "No Equipment": "无器械",
    "Volleyballs": "排球",
    "Net": "球网",
    "Cones": "标志桩",
    "Half-court": "半场",
    "Full court": "全场",
    "Individual": "个人",
    "Strength": "力量",
    "Power": "爆发力",
    "Agility": "灵敏度",
    "Balance": "平衡",
    "Core": "核心稳定",
    "Flexibility": "柔韧性",
    "Low": "低",
    "Medium": "中",
    "High": "高",
    "Technical": "技术",
    "Conditioning": "体能",
}

TITLE_REPLACEMENTS = {
    "Standing": "站姿",
    "Seated": "坐姿",
    "Lying": "仰卧",
    "Prone": "俯卧",
    "Supine": "仰卧",
    "Single-leg": "单腿",
    "Single Leg": "单腿",
    "Single-arm": "单臂",
    "Single Arm": "单臂",
    "Reverse": "反向",
    "Lateral": "侧向",
    "Forward": "前向",
    "Hurdle": "跨栏",
    "Run": "跑",
    "Bench": "卧推凳",
    "Chest": "胸部",
    "Shoulder": "肩部",
    "Back": "背部",
    "Arm": "手臂",
    "Leg": "腿部",
    "Hip": "髋部",
    "Glute": "臀部",
    "Core": "核心",
    "Stability": "稳定性",
    "Balance": "平衡",
    "Stretch": "拉伸",
    "Rotation": "旋转",
    "Raise": "提升",
    "Press": "推举",
    "Row": "划船",
    "Curl": "弯举",
    "Extension": "伸展",
    "Flexion": "屈曲",
    "Workout": "训练",
    "Squat": "深蹲",
    "Plank": "平板",
    "Lunge": "弓步",
    "Push-up": "俯卧撑",
    "Deadlift": "硬拉",
    "Crunch": "卷腹",
    "Dorsi": "足背",
    "Flexion": "屈",
    "Calf": "腓肠肌",
    "Ankle": "踝关节",
    "Bodyweight": "自重",
    "Weighted": "负重",
    "Jump": "跳跃",
    "Slam": "砸地",
    "Tuck": "收腹",
    "Power": "爆发",
    "Clean": "高翻",
    "Snatch": "抓举",
    "Swing": "摆动",
    "Turkish": "土耳其",
    "Farmer": "农夫",
    "Carry": "行走",
    "Wait": "侍者",
    "Suitcase": "行李箱",
    "Inchworm": "寸步移",
    "Mountain": "登山",
    "Climber": "跑",
    "Agility": "敏捷",
    "Ladder": "梯",
    "Shuffle": "侧向滑步",
    "Hurdle Run": "跨栏跑",
    "Dorsi": "背屈",
    "Rotator Cuff": "肩袖",
    "Cuff": "袖",
    "Internal": "内旋",
    "External": "外旋",
    "Decline": "下斜",
    "Cable": "拉力器",
    "Kneeling": "跪姿",
    "Triceps": "三头肌",
    "Biceps": "二头肌",
    "Pepper": "垫传对练",
    "Sideout": "一传转攻",
    "Linear": "直线",
    "Cone Jumps": "标志桩跳跃",
    "ABC's": "动作基础",
    "Formation": "阵型",
    "Stabilization": "稳定",
    "Parascapular": "肩胛旁",
    "Scapular": "肩胛",
    "Mobilization": "松动",
    "Cycled": "循环",
    "Split": "分腿",
    "Waves": "战绳波浪",
    "Simultaneous": "同步",
    "Asynchronous": "异步",
    "Wood Chop": "伐木式",
    "Suitcase": "行李箱",
    "Thomas": "托马斯",
    "Romanian": "罗马尼亚",
    "Hammer": "锤式",
    "Chin-ups": "引体向上",
    "Rotational": "旋转",
    "Uppercut": "上勾拳",
    "Alternate": "交替",
    "Push-off": "蹬起",
    "Overhead": "过顶",
    "Zig Zags": "之字形移动",
    "Spinal Twist": "脊柱扭转",
    "Rib Grab": "抓肋",
    "Progressions": "进阶方案",
    "Activation": "激活",
    "Modified": "改良版",
    "Bridge": "桥",
    "Fly": "飞鸟",
    "Swing": "摆动",
    "Clean": "高翻",
    "High-low": "高低位",
    "Partner": "伙伴",
    "See-saw": "锯式",
    "Contralateral": "对侧",
    "Limb": "肢体",
    "Raises": "抬升",
    "Hexagon": "六角形",
    "Spider": "蜘蛛",
    "Walks": "行走",
    "V-ups": "V字起",
    "Suitcase": "行李箱",
    "Carry": "行走",
    "Pass": "传递",
    "Turkish": "土耳其",
    "Get-up": "起立",
    "Renegade": "叛逆者",
    "Farmer's": "农夫",
    "Monkey": "猴式",
    "Zatsiorsky": "扎齐奥尔斯基",
    "Plank": "平板支撑",
    "Lunge": "弓步",
    "Squat": "深蹲",
    "Press": "推举",
    "Row": "划船",
    "Curl": "弯举",
    "Stretch": "拉伸",
    "Wood Chop": "伐木式",
    "Shoulder": "肩部",
    "Chest": "胸部",
    "Back": "背部",
    "Leg": "腿部",
    "Arm": "手臂",
    "Hand": "手部",
    "Wrist": "手腕",
    "Ankle": "足踝",
    "Hip": "髋部",
    "Glute": "臀部",
    "Abdominal": "腹部",
    "Core": "核心",
    "Stability": "稳定性",
    "Jump": "跳跃",
    "Lateral": "侧向",
    "Linear": "线性",
    "Forward": "前向",
    "Backward": "后向",
    "Reverse": "反向",
    "Side": "侧向",
    "Prone": "俯卧",
    "Supine": "仰卧",
    "Seated": "坐姿",
    "Standing": "站姿",
    "Kneeling": "跪姿",
    "Single-arm": "单臂",
    "Single-leg": "单腿",
    "Bent-knee": "屈膝",
    "Cable": "缆绳",
    "Band": "弹力带",
    "Dumbbell": "哑铃",
    "Barbell": "杠铃",
    "Medicine Ball": "药球",
    "Swiss Ball": "瑞士球",
    "Stability Ball": "平衡球",
    "Kettlebell": "壶铃",
    "TRX": "悬挂带",
    "Battling Ropes": "战绳",
    "Cone": "标志桩",
    "Hurdle": "跨栏",
    "Step": "踏板",
    "Bench": "卧推凳",
    "Decline": "下斜",
    "Incline": "上斜",
    "Close-grip": "窄握",
    "Rotation": "旋转",
    "Twist": "扭转",
    "Flexion": "屈曲",
    "Extension": "伸展",
    "Tuck": "抱膝",
    "Pike": "屈体",
    "Plantar": "跖屈",
    "Dorsi": "背屈",
    "Roll Out": "滚筒滚动",
    "Childs Pose": "婴儿式",
    "Walking": "行走",
    "Abduction": "外展",
    "Adduction": "内收",
    "Shrug": "耸肩",
    "Box": "跳箱",
    "Run": "跑",
    "Sprints": "冲刺",
    "Agility": "灵敏",
    "Ladder": "绳梯",
    "Shuffles": "碎步滑跑",
    "Linear": "线性",
    "Linear Jumps": "线性跳跃",
    "Linear Run": "线性跑",
    "Linear Sprints": "线性冲刺",
    "Waves": "波浪",
    "Waves with": "波浪配合",
}

def translate_english_title(title):
    res = title
    # Sort replacements by length descending to catch longer phrases first
    sorted_keys = sorted(TITLE_REPLACEMENTS.keys(), key=len, reverse=True)
    for eng in sorted_keys:
        chn = TITLE_REPLACEMENTS[eng]
        res = re.sub(rf'\b{eng}\b', chn, res, flags=re.IGNORECASE)
    
    # Clean up multiple spaces or lingering English chars
    res = re.sub(r'[a-zA-Z\s\-]+', ' ', res).strip()
    if not res: return title # Fallback
    return res

def translate_ace_content(title_chn, category, equipment):
    # Professional, data-driven templates
    if "拉伸" in title_chn or "柔韧" in title_chn or category == "柔韧性":
        desc = f"针对{title_chn}的专业拉伸练习，通过延展目标肌群筋膜，有效提升关节灵活性。"
        steps = [
            f"采取稳定的{title_chn}起始姿势，确保身体中线对齐。",
            "缓慢延伸肢体至有明显拉伸感的位置，保持呼吸深长。",
            "维持静止状态15-30秒，感受肌肉逐渐放松和拉长。",
            "吸气并缓慢还原，换侧或循环练习。"
        ]
        tips = ["严禁弹动式拉伸，应保持静力性延展", "感受目标区域的酸胀感，逐渐增加深度", "配合深长呼气，有助于肌肉进一步松弛"]
    elif "深蹲" in title_chn or "弓步" in title_chn or "腿" in title_chn:
        desc = f"下肢力量进阶练习，通过{title_chn}强化臀腿肌群集群稳定性与爆发力。"
        steps = [
            "双脚站立与肩同宽，脚尖微外展，脊柱保持中立支撑。",
            "吸气控制重心下降，膝盖与脚尖方向一致，核心收紧。",
            f"下蹲至大腿平齐或略低于膝盖，感受{equipment}带来的负荷。",
            "呼气并由足底发力蹬起，回到起始位置。"
        ]
        tips = ["核心全程收紧，保护腰椎稳定性", "膝盖不要内扣，与脚尖保持一致线", "保证动作全程受控，不要快速下坠"]
    elif "俯卧撑" in title_chn or "推举" in title_chn or "卧推" in title_chn:
        desc = f"上肢推力系统训练，重点强化胸部、肩部及三头肌的肌肉耐力与力量储备。"
        steps = [
            "双手略宽于肩，稳定支撑于地面或器材上，核心收紧。",
            "吸气并缓慢下沉身体，手肘成45-90度夹角，感受胸部拉伸。",
            "利用胸大肌与手臂力量爆发性推起肢体。",
            "在动作顶点避免肘关节锁死，保持肌肉持续张力。"
        ]
        tips = ["保持肩胛骨下沉收紧，避免斜方肌过度代偿", "腰腹部不要塌陷，身体呈一直线", "呼气推起，吸气还原"]
    elif "核心" in title_chn or "平板" in title_chn or "卷腹" in title_chn or category == "核心稳定":
        desc = f"核心功能性训练，旨在建立强有力的躯干支柱，优化力量传导效率并预防伤病。"
        steps = [
            "进入起始体位，建立腹内压，确保骨盆处于中立位。",
            f"保持{title_chn}姿态，对抗身体被重力或阻力扭转的趋势。",
            "感受深层腹横肌的紧绷感，维持稳定的呼吸节奏。",
            "保持高质量支撑直至力竭或达到目标时间。"
        ]
        tips = ["想象肋骨与骨盆之间相互拉近，锁死核心", "避免憋气，采用浅长呼吸维持压力", "若动作变形应立即停止，求精不求多"]
    elif category == "爆发力" or "跳" in title_chn or "砸" in title_chn:
        desc = f"高强度爆发力训练，通过{title_chn}激发神经肌肉召集效率，提升单位时间功率输出。"
        steps = [
            "迅速进入预拉伸姿态，完成能量蓄力。",
            "利用全身联动爆发性完成向心收缩部分，速度至上。",
            "落地时重心后移，通过三关节联动（髋膝踝）完成静音缓冲。",
            "短暂调整，确保每一次重复都是最高功率输出。"
        ]
        tips = ["动作必须“脆”，能量转换速度是第一核心指标", "落地缓冲是安全的根本，严防膝盖冲击", "组间休息要充足，保证神经系统恢复"]
    else:
        desc = f"这是一项针对{category}的{title_chn}专业训练，结合排球运动特质优化发力逻辑。"
        steps = [
            f"准备好{equipment}并调整到正确的起始姿势，核心预收缩。",
            f"在解剖学中立位基础上执行{title_chn}动作轨迹。",
            "感受目标肌群的主动收缩，保持动作全程平稳受控。",
            "完成预定组数后，进行针对性放松。 "
        ]
        tips = ["注意动作的标准性，严控代偿行为", "根据自身水平选择合适的强度等级", "由于小程序显示限制，建议配合专业指导进行"]
    
    return desc, steps, tips

def load_antigravity_translations():
    trans_map = {}
    try:
        with open('apply_translations.py', 'r', encoding='utf-8') as f:
            content = f.read()
            entries = re.findall(r'"([^"]+)":\s*\{(.*?)\n    \}', content, re.DOTALL)
            for eid, body in entries:
                d = {}
                tm = re.search(r'"title":\s*"([^"]+)"', body)
                if tm: d['title'] = extract_chinese(tm.group(1))
                dm = re.search(r'"description":\s*"([^"]+)"', body)
                if dm: d['description'] = extract_chinese(dm.group(1))
                sm = re.search(r'"setup":\s*\{([^}]+)\}', body, re.DOTALL)
                if sm:
                    sb = sm.group(1)
                    sd = {}
                    for fld in ['players', 'court', 'equipment', 'roles']:
                        fm = re.search(f'"{fld}":\s*"([^"]*)"', sb)
                        if fm: sd[fld] = extract_chinese(fm.group(1))
                    d['setup'] = sd
                for fld in ['steps', 'variations', 'coaching_tips']:
                    am = re.search(f'"{fld}":\s*\[(.*?)\]', body, re.DOTALL)
                    if am:
                        its = re.findall(r'"([^"]+)"', am.group(1))
                        d[fld] = [extract_chinese(it) for it in its]
                trans_map[eid] = d
    except: pass
    return trans_map

def process_file(filepath, trans_map):
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        json_str = content[content.find('['):content.rfind(']')+1]
        data = json.loads(json_str)

    new_data = []
    for item in data:
        eid = item.get('i')
        is_conditioning = 'conditioning' in item.get('m', '')
        
        if eid in trans_map:
            t_data = trans_map[eid]
            item['t'] = t_data.get('title', item['t'])
            item['d'] = t_data.get('description', item['d'])
            if 'setup' in t_data:
                s = item.get('s', {})
                ts = t_data['setup']
                if 'p' in s: s['p'] = ts.get('players', s['p'])
                if 'u' in s: s['u'] = ts.get('court', s['u'])
                if 'e' in s: s['e'] = ts.get('equipment', s['e'])
                item['s'] = s
            if 'steps' in t_data: item['st'] = t_data['steps']
            if 'v' in item and 'variations' in t_data: item['v'] = t_data['variations']
            if 'ct' in item and 'coaching_tips' in t_data: item['ct'] = t_data['coaching_tips']
        else:
            item['t'] = translate_english_title(item['t'])
            item['c'] = translate_term(item.get('c', ''))
            
            if is_conditioning:
                equip = item.get('s', {}).get('e', '无器械')
                if equip == 'No Equipment' or not equip: equip = '无器械'
                item['d'], item['st'], item['ct'] = translate_ace_content(item['t'], item['c'], equip)
            else:
                 item['d'] = clean_text(item.get('d', ''))
                 item['st'] = [clean_text(s) for s in item.get('st', [])]
                 item['v'] = [clean_text(v) for v in item.get('v', [])]
                 item['ct'] = [clean_text(ct) for ct in item.get('ct', [])]
            
            if 's' in item and isinstance(item['s'], dict):
                for k in item['s']:
                    if isinstance(item['s'][k], str):
                        item['s'][k] = translate_term(item['s'][k])
        
        if 'p' in item: item['p'] = translate_term(item['p'])
        if 'n' in item: item['n'] = translate_term(item['n'])
        if 'g' in item: item['g'] = [translate_term(g) for g in item['g']]
        
        item['t'] = translate_english_title(item['t'])
        new_data.append(item)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"module.exports = {json.dumps(new_data, separators=(',', ':'), ensure_ascii=False)};")

def translate_term(term):
    if term in TERM_MAP: return TERM_MAP[term]
    if isinstance(term, list): return [translate_term(t) for t in term]
    if not term: return term
    return term

if __name__ == "__main__":
    trans_map = load_antigravity_translations()
    process_file('data/drills.js', trans_map)
    process_file('data/conditioning.js', trans_map)
