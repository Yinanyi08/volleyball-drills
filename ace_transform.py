"""
ACE Fitness 数据翻译器
将爬取的英文数据翻译成中英双语格式
"""

import json
import re
import os

# ========== 翻译词典 ==========

# 训练动作名称翻译
EXERCISE_NAMES = {
    # 基础动作
    "Push-up": "俯卧撑",
    "Push-ups": "俯卧撑",
    "Bent Knee Push-up": "跪姿俯卧撑",
    "Push-up with Single-leg Raise": "单腿抬起俯卧撑",
    "Medicine Ball Push-ups": "药球俯卧撑",
    "Single-arm Medicine Ball Push-up": "单臂药球俯卧撑",
    "Stability Ball Push-up": "瑞士球俯卧撑",
    
    # 蹲类
    "Bodyweight Squat": "徒手深蹲",
    "Back Squat": "杠铃深蹲",
    "Front Squat": "前蹲",
    "Single-leg Squat": "单腿深蹲",
    "Stability Ball Wall Squats": "瑞士球靠墙深蹲",
    
    # 弓步
    "Forward Lunge": "前弓步",
    "Side Lunge": "侧弓步",
    "Walking Lunges with Twists": "行走弓步转体",
    "Lunge with Overhead Press": "弓步推举",
    "Lunge with Elbow Instep": "弓步肘触脚背",
    
    # 硬拉和臀部
    "Deadlift": "硬拉",
    "Glute Bridge": "臀桥",
    "Hip Hinge": "髋关节铰链",
    
    # 上肢推
    "Chest Press": "卧推",
    "Incline Chest Press": "上斜卧推",
    "Lying Chest Fly": "仰卧飞鸟",
    "Standing Shoulder Press": "站姿推举",
    "Seated Shoulder Press": "坐姿推举",
    "Push Press": "借力推举",
    "Push Jerk": "推挺",
    "Double Push Press": "双壶铃借力推举",
    
    # 上肢拉
    "Bent-over Row": "俯身划船",
    "Seated Row": "坐姿划船",
    "Seated High-Back Row": "坐姿高位划船",
    "Kneeling Lat Pulldowns": "跪姿高位下拉",
    "Bicep Curl": "二头肌弯举",
    "Hammer Curl": "锤式弯举",
    
    # 手臂
    "Triceps Pressdown": "三头肌下压",
    "Lying Barbell Triceps Extensions": "仰卧杠铃臂屈伸",
    "Lateral Raise": "侧平举",
    "Wrist Curl - Flexion": "腕屈",
    "Wrist Curl - Extension": "腕伸",
    "Wrist Supination and Pronation": "腕旋转",
    
    # 核心
    "Front Plank": "平板支撑",
    "Crunch": "卷腹",
    "Russian Twist": "俄罗斯转体",
    "Bird-dog": "鸟狗式",
    "Supermans": "超人式",
    "Cat-Cow": "猫牛式",
    "Supine Pelvic Tilts": "仰卧骨盆倾斜",
    "Standing Trunk Rotation": "站姿躯干旋转",
    "Standing Wood Chop": "站姿砍木",
    "Standing Hay Baler": "站姿斜向推举",
    "Half Kneeling Hay Baler": "半跪姿斜向推举",
    "Pull-over Crunch": "仰卧拉起卷腹",
    
    # 瑞士球
    "Stability Ball Knee Tucks": "瑞士球收膝",
    "Stability Ball Pikes": "瑞士球屈体",
    "Stability Ball Reverse Extensions": "瑞士球反向伸展",
    "Stability Ball Sit-ups - Crunches": "瑞士球仰卧起坐",
    "Stability Ball Prone Walkout": "瑞士球俯卧行走",
    "Stability Ball Hamstring Curl": "瑞士球腿弯举",
    "Stability Ball Shoulder Stabilization": "瑞士球肩稳定训练",
    
    # TRX
    "TRX ® Chest Press": "TRX胸推",
    "TRX ® Back Row": "TRX划船",
    "TRX ® Biceps Curl": "TRX二头弯举",
    "TRX ® Overhead Triceps Extension": "TRX三头伸展",
    "TRX ® Hamstrings Curl": "TRX腿弯举",
    "TRX ® Atomic Push-up": "TRX原子俯卧撑",
    "TRX ® Front Rollout": "TRX前滚",
    "TRX ® Suspended Knee Tucks": "TRX悬挂收膝",
    "TRX ® Suspended Pikes": "TRX悬挂屈体",
    "TRX ® Side Straddle Golf Swings": "TRX侧向高尔夫摆动",
    "TRX ® Assisted Side Lunge with Arm Raise": "TRX辅助侧弓步抬臂",
    "TRX ® Assisted Cross-over Lunge with Arm Raise": "TRX辅助交叉弓步抬臂",
    
    # 壶铃
    "Turkish Get-up": "土耳其起立",
    "Half Turkish Get-up": "半土耳其起立",
    "Low Windmill": "低位风车",
    "High Windmill": "高位风车",
    "Clean and Press": "翻铃推举",
    "Swing": "壶铃摆动",
    "Figure Eight": "8字传递",
    "Power Clean": "高翻",
    "Waiter's Carry": "侍者行走",
    "Suitcase Carry": "行李箱行走",
    
    # 药球
    "Seated Medicine Ball Trunk Rotations": "坐姿药球躯干旋转",
    "Overhead Slams": "药球砸地",
    "Overhead Medicine Ball Throws": "过头药球抛掷",
    
    # 腿部
    "Step-up": "箱式登阶",
    "Box Jumps": "跳箱",
    "Lateral Cone Jumps": "侧向跳锥",
    "Calf Raises": "提踵",
    "Standing Calf Raises - Wall": "靠墙站姿提踵",
    "Standing Dorsi Flexion - Calf Stretch": "站姿踝背屈小腿拉伸",
    "Standing Hamstrings Curl": "站姿腿弯举",
    "Prone-lying Hamstrings Curl": "俯卧腿弯举",
    "Standing Leg Extensions": "站姿腿屈伸",
    "Standing Hip Abduction": "站姿髋外展",
    "Standing Hip Adduction": "站姿髋内收",
    "Side-lying Hip Abduction": "侧卧髋外展",
    "Side-lying Hip Adduction": "侧卧髋内收",
    
    # 灵活性
    "Ankle Flexion": "踝关节屈伸",
    "Cobra Exercise": "眼镜蛇式",
    "Downward-facing Dog": "下犬式",
    "Neck Flexion and Extension": "颈部屈伸",
    "Lateral Neck Flexion": "颈部侧屈",
    "Supine Shoulder Roll": "仰卧肩环绕",
    
    # 功能性
    "Bear Crawl": "熊爬",
    "Inverted Flyers": "倒V飞鸟",
    "Incline Reverse Fly": "上斜反向飞鸟",
    "Kneeling Reverse Fly": "跪姿反向飞鸟",
    "Standing Single-leg Cable Rotation": "单腿站姿缆绳旋转",
    "Agility Ladder Lateral Shuffle": "敏捷梯侧向移动",
    "Single-Leg Stand with Reaches": "单腿站立触及",
    "Lying Pullovers": "仰卧拉举"
}

# 器材翻译
EQUIPMENT_MAP = {
    "No Equipment": "无器械",
    "Dumbbells": "哑铃",
    "Barbell": "杠铃",
    "Bench": "卧推凳",
    "Resistance Bands/Cables": "弹力带/缆绳",
    "Stability Ball": "瑞士球",
    "Medicine Ball": "药球",
    "TRX": "TRX悬挂带",
    "Raised Platform/Box": "跳箱/平台",
    "Kettlebells": "壶铃",
    "Cones": "标志桩",
    "Ladder": "敏捷梯",
    "Pull up bar": "单杠",
    "BOSU Trainer": "BOSU平衡球",
    "Weight Machines / Selectorized": "健身器械",
    "Heavy Ropes": "战绳",
    "Hurdles": "跨栏"
}

# 身体部位翻译
BODY_PART_MAP = {
    "Abs": "腹部",
    "Arms": "手臂",
    "Back": "背部",
    "Butt/Hips": "臀髋",
    "Chest": "胸部",
    "Full Body/Integrated": "全身",
    "Legs - Calves and Shins": "小腿",
    "Legs - Thighs": "大腿",
    "Shoulders": "肩部",
    "Neck": "颈部"
}

# 难度翻译
DIFFICULTY_MAP = {
    "Beginner": "初级",
    "Intermediate": "中级",
    "Advanced": "高级"
}

def translate_title(title):
    """翻译动作名称为双语格式"""
    # 清理标题
    title = title.strip()
    title = re.sub(r'\s+', ' ', title)
    
    # 查找翻译
    for en, cn in EXERCISE_NAMES.items():
        if en.lower() == title.lower() or en.lower() in title.lower():
            return f"{cn} ({title})"
    
    # 没找到翻译，使用原标题
    return title

def translate_equipment(equipment):
    """翻译器材名称"""
    if not equipment:
        return "无器械", "No Equipment"
    
    cn_parts = []
    en_parts = equipment.split(", ")
    
    for eq in en_parts:
        eq = eq.strip()
        cn = EQUIPMENT_MAP.get(eq, eq)
        cn_parts.append(cn)
    
    return "、".join(cn_parts), equipment

def translate_difficulty(difficulty):
    """翻译难度"""
    if not difficulty:
        return "中", "Intermediate"
    
    cn = DIFFICULTY_MAP.get(difficulty, "中")
    return cn, difficulty

def infer_category(title, equipment, body_part):
    """推断训练分类"""
    title_lower = title.lower()
    
    # 核心
    if any(kw in title_lower for kw in ['plank', 'crunch', 'twist', 'superman', 'bird', 'cat', 'cow', 'pelvic', 'rotation', 'hay baler', 'wood chop']):
        return "核心稳定"
    
    # 柔韧
    if any(kw in title_lower for kw in ['stretch', 'cobra', 'downward', 'flexion', 'extension', 'roll']):
        return "柔韧性"
    
    # 爆发力
    if any(kw in title_lower for kw in ['jump', 'throw', 'slam', 'power', 'clean', 'jerk', 'swing']):
        return "爆发力"
    
    # 力量
    return "力量"

def infer_intensity(difficulty, title):
    """推断训练强度"""
    if difficulty == "Beginner":
        return "低"
    elif difficulty == "Advanced":
        return "高"
    
    title_lower = title.lower()
    if any(kw in title_lower for kw in ['stretch', 'mobility', 'cat', 'cow', 'neck']):
        return "低"
    if any(kw in title_lower for kw in ['jump', 'power', 'atomic', 'clean']):
        return "高"
    
    return "中"

def transform_data(input_file, output_file):
    """转换数据为双语格式"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    print(f"读取原始数据: {len(raw_data)} 条")
    
    transformed = []
    
    for item in raw_data:
        if not item.get('title') or not item.get('steps'):
            continue
        
        # 翻译标题
        title = translate_title(item['title'])
        
        # 翻译器材
        equipment_cn, equipment_en = translate_equipment(item.get('equipment', ''))
        
        # 翻译难度
        difficulty_cn, difficulty_en = translate_difficulty(item.get('difficulty', ''))
        
        # 推断分类和强度
        category = infer_category(item['title'], item.get('equipment', ''), item.get('targetBodyPart', ''))
        intensity = infer_intensity(item.get('difficulty', ''), item['title'])
        
        # 清理步骤
        steps = []
        for step in item.get('steps', [])[:5]:
            # 过滤无关内容
            if any(skip in step.lower() for skip in [
                'create fitness', 'practicing equity', 'special olympics',
                'learn more', 'copyright', 'privacy'
            ]):
                continue
            steps.append(step)
        
        if not steps:
            continue
        
        # 生成描述（截取首个步骤的前100个字符）
        description = steps[0][:100] + "..." if len(steps[0]) > 100 else steps[0]
        
        exercise = {
            "id": item['id'],
            "title": title,
            "description": description,
            "category": category,
            "intensity": intensity,
            "ageGroup": ["intermediate", "high_school", "advanced"],
            "image": "/public/images/conditioning/default.png",
            "setup": {
                "equipment": f"{equipment_cn} ({equipment_en})" if equipment_cn != equipment_en else equipment_cn,
                "players": "个人 (Individual)",
                "court": "健身房或室内 (Gym or Indoor)"
            },
            "steps": steps,
            "coachingTips": [
                "保持正确姿势，避免代偿。(Maintain proper form, avoid compensation.)",
                "控制动作节奏，注意呼吸。(Control the tempo, focus on breathing.)"
            ],
            "variations": []
        }
        
        transformed.append(exercise)
    
    # 保存转换后的数据
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(transformed, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 转换完成!")
    print(f"   有效数据: {len(transformed)} 条")
    print(f"   输出文件: {output_file}")
    
    # 统计分类
    categories = {}
    for item in transformed:
        cat = item['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\n分类统计:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"   {cat}: {count}")
    
    return transformed

def generate_conditioning_js(data, output_file):
    """生成小程序用的 conditioning.js 文件"""
    
    js_content = "module.exports = [\n"
    
    for i, item in enumerate(data):
        js_content += "  " + json.dumps(item, ensure_ascii=False, indent=4).replace('\n', '\n  ')
        if i < len(data) - 1:
            js_content += ","
        js_content += "\n"
    
    js_content += "];\n"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"✅ 生成 conditioning.js 完成: {output_file}")

if __name__ == "__main__":
    INPUT_FILE = "output/ace_fitness/exercises_full.json"
    OUTPUT_JSON = "output/ace_fitness/exercises_bilingual.json"
    OUTPUT_JS = "data/conditioning.js"
    
    # 转换数据
    transformed = transform_data(INPUT_FILE, OUTPUT_JSON)
    
    # 生成 JS 文件
    generate_conditioning_js(transformed, OUTPUT_JS)
