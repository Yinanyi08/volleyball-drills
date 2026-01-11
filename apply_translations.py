#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
排球训练内容双语集成脚本
由 Antigravity 亲自翻译并生成
"""

import json
from pathlib import Path

# 原始数据
INPUT_FILE = Path("output/drills_data.json")
OUTPUT_FILE = Path("constants.ts")

# 翻译映射表 (由 Antigravity 提供)
TRANSLATIONS = {
    "perfect-passes": {
        "title": "Volleyball Passing Drill: Perfect Passes Repetition (排球垫球训练：完美垫球重复练习)",
        "description": "This volleyball passing drill builds consistency, ball control, and defensive posture by focusing on perfect passes through high-repetition training. (此训练专注于通过高强度重复练习建立稳定性、控球力及防守姿态。)",
        "setup": {
            "players": "2 passers, 2 tossers, 2 targets (2名垫球手，2名抛球手，2名目标手)",
            "court": "Half-court or designated passing zone (半场或指定的垫球区域)",
            "equipment": "Volleyballs (排球)",
            "roles": "Tossers initiate play, passers receive and direct the ball (抛球手发起球，垫球手接收并导向球)"
        },
        "steps": [
            "Tosser tosses toward the passer. (抛球手将球抛向垫球手。)",
            "Passer performs a controlled forearm pass to the target. (垫球手执行受控的下手垫球送往目标。)",
            "Rotate roles: tosser → passer → target. (轮换角色：抛球手 → 垫球手 → 目标手。)",
            "Continue until a set number of perfect passes is achieved. (持续练习直到达到预设的完美垫球数。)"
        ],
        "variations": [
            "Use overhead pass only. (仅使用上手传球。)",
            "Time challenge: 50 perfect passes in 3 minutes. (时间挑战：3分钟内完成50个。)"
        ],
        "coaching_tips": [
            "Maintain a ready position with knees bent. (保持膝盖弯曲的准备姿势。)",
            "Lock arms for a stable platform. (锁紧双臂以保持稳定的平面。)"
        ]
    },
    "serving-bombs-away": {
        "title": "Volleyball Serving Drill: Bombs Away! Short Serve Challenge (排球发球训练：地毯式发球！短球挑战)",
        "description": "Improves short serve accuracy while challenging defenders' reactions. (提高短球发球准确性，同时挑战防守者的反应。)",
        "setup": {
            "players": "3 servers, 3 passers (3名发球手，3名接球手)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs (排球)",
            "roles": "Servers aim for short zones. (发球手瞄准短球区。)"
        },
        "steps": [
            "Servers attempt to serve as short as possible. (发球手尝试发出尽可能短的球。)",
            "Passers sprint forward to catch or pass. (接球手向前冲刺接球。)",
            "Scoring: Point if ball lands untouched. (计分：如果球落地未触碰则得分。)"
        ],
        "variations": [
            "Instead of catching, passers must pass to a target. (不抓球，而是通过垫球送向目标。)"
        ],
        "coaching_tips": [
            "Focus on a consistent toss. (专注于稳定的抛球。)"
        ]
    },
    "passing-out-of-the-net": {
        "title": "Volleyball Passing Drill: Passing Out of the Net (排球垫球训练：球网起球练习)",
        "description": "Teaches players to read and control balls rebounding off the net. (教会球员阅读并控制从球网反弹的球。)",
        "setup": {
             "players": "3 passers, 3 tossers (3名垫球手，3名抛球手)",
             "court": "Full court, net (全场，球网)",
             "equipment": "Volleyballs (排球)",
             "roles": "Tossers throw into net. (抛球手将球抛向网中。)"
        },
        "steps": [
            "Tosser throws a ball into the net. (抛球手将球抛入网中。)",
            "Passer reads the rebound and makes a controlled pass. (垫球手阅读反弹并进行受控垫球。)"
        ],
        "variations": [
            "Hit down balls into the net instead of tossing. (用下击球代替抛球击向球网。)"
        ],
        "coaching_tips": [
            "Stay low and balanced. (保持低位和重心平衡。)"
        ]
    },
    "defense-touch-ten": {
        "title": "Volleyball Defense Drill: Touch Ten! (排球防守训练：防守触球十次！)",
        "description": "Builds aggressiveness as defenders work to touch ten attacked balls. (通过触碰十次进攻球来建立防守积极性。)",
        "setup": {
            "players": "3 hitters, 1 defender (3名扣球手，1名防守手)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs (排球)",
            "roles": "Defender stays in until 10 touches. (防守者直到触球10次才轮换。)"
        },
        "steps": [
            "Hitters take turns attacking the ball. (扣球手轮流进行进攻进攻。)",
            "Defender pursues every ball. (防守者追逐每一个球。)"
        ],
        "variations": [
            "Add a second defender for teamwork. (增加第二名防守者练配合。)"
        ],
        "coaching_tips": [
            "Keep eyes on the hitter's shoulders. (紧盯着扣球手的肩膀。)"
        ]
    },
    "passing-technique-warm-up": {
        "title": "Volleyball Passing Warm-Up: Technique Path (排球垫球热身：垫球技术路径练习)",
        "description": "Develops a solid platform and low movement base. (建立稳固的手臂平面和低位移动基础。)",
        "setup": {
            "players": "Entire team (全队)",
            "court": "W sequence (W型路径)",
            "equipment": "Cones (标志桩)",
            "roles": ""
        },
        "steps": [
            "Shuffle between cones in a passing stance. (以垫球姿态在标志桩间滑步。)",
            "Mimic a pass at each cone. (在每个标志桩处模拟垫球。)"
        ],
        "variations": [
            "Add a coach's toss at each station. (在每个站点增加教练抛球。)"
        ],
        "coaching_tips": [
            "Don't cross your feet while shuffling. (滑步时不要交叉双脚。)"
        ]
    },
    "defense-4-corner-pit": {
        "title": "Volleyball Defense Drill: 4-Corner Pit (排球防守训练：四角防守深坑训练)",
        "description": "Improves quick reaction and movement to court corners. (提高对场地四个角落球路的快速反应和移动能力。)",
        "setup": {
            "players": "1 defender, 1 coach (1名防守者，1名教练)",
            "court": "Four corners marked (标出四个角)",
             "equipment": "Volleyballs (排球)",
             "roles": "Coach hits to corners. (教练将球击向角落。)"
        },
        "steps": [
            "Coach hits or tosses to the marked corners. (教练将球击向或抛向标记的角落。)",
            "Defender must touch every ball before it lands. (防守者必须在球落地前触碰球。)"
        ],
        "variations": [
            "Randomize the order to increase difficulty. (随机化顺序以增加难度。)"
        ],
        "coaching_tips": [
            "Explode from the first step. (第一步一定要有爆发力。)"
        ]
    },
    "serve-receive-with-2-servers": {
        "title": "Volleyball Serve Receive Drill with Two Servers (排球接发球训练：双人发球强化训练)",
        "description": "Challenges players to pass short serves consistently. (挑战球员稳定接好短发球的能力。)",
        "setup": {
            "players": "3 passers, 2 servers (3名接球手，2名发球手)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs, net (排球，球网)",
            "roles": "Servers only serve short. (发球手仅发短球。)"
        },
        "steps": [
            "Servers alternate short serves. (发球手交替发出短球。)",
            "Passers must target the ball to the net. (接球手必须将球垫向网前。)"
        ],
        "variations": [
            "Servers can mix in one deep serve. (发球手可以夹杂一个长球。)"
        ],
        "coaching_tips": [
            "Call the ball early and loud. (大声且尽早地呼应接球。)"
        ]
    },
    "lateral-passing-3-touch": {
        "title": "Volleyball Passing Drill: 3-Touch Lateral Passing (排球垫球训练：三触点横向垫球)",
        "description": "Develops movement and passing from midline and lateral positions. (训练从中线和侧向位置进行移动垫球。)",
        "setup": {
            "players": "1 passer, 1 tosser (1名垫球手，1名抛球手)",
            "court": "Half court (半场)",
            "equipment": "Volleyballs (排球)",
            "roles": "Tosser feeds Right-Mid-Left. (抛球手按 右-中-左 顺序抛球。)"
        },
        "steps": [
            "Tosser throws to the right, then center, then left. (抛球手向右、中、左依次抛球。)",
            "Passer moves to be behind each ball. (垫球手移动到每个球的后方。)"
        ],
        "variations": [
            "Tosser moves to vary the distance. (抛球手移动以改变抛球距离。)"
        ],
        "coaching_tips": [
            "Keep the platform tilted toward the target. (保持手臂平面倾向目标。)"
        ]
    },
    "passing-pass-and-move": {
        "title": "Volleyball Passing Drill: Pass and Move (排球垫球训练：垫球与移动练习)",
        "description": "Trains lateral movement and squaring to the target under pressure. (训练在压力下的横向移动及正对目标垫球。)",
        "setup": {
            "players": "1 passer, 2 tossers (1名垫球手，2名抛球手)",
            "court": "Half court (半场)",
             "equipment": "Volleyballs (排球)",
             "roles": "Passer touches coach's foot after each pass. (垫球手每次垫球后触摸教练的脚。)"
        },
        "steps": [
            "Pass the ball, then sprint to touch the coach's foot. (垫球，然后冲刺触摸教练的脚。)",
            "Backpedal quickly to the next position. (快速退回到下一个位置。)"
        ],
        "variations": [
            "Use a cone instead of the foot for safety. (为了安全，用标志桩代替脚。)"
        ],
        "coaching_tips": [
            "Focus on a fast transition. (专注于快速的转换过程。)"
        ]
    },
    "pass-and-weave": {
        "title": "Volleyball Passing Drill: Pass and Weave (排球垫球训练：垫球与穿梭移动)",
        "description": "Develops ball control and lateral footwork through markers. (在穿梭标记物的同时提高控球力和横向步法。)",
        "setup": {
            "players": "1 passer, 3 tossers (1名垫球手，3名抛球手)",
            "court": "3 markers in a line (3个标记排成一线)",
            "equipment": "Volleyballs, markers (排球，标记物)",
            "roles": "Passer weaves between markers. (垫球手在标记物间穿梭。)"
        },
        "steps": [
            "Pass the ball from the first station. (在第一个站点垫球。)",
            "Weave around the marker to the next station. (绕过标记物跑向下一个站点进行垫球。)"
        ],
        "variations": [
            "Add a jumping element over the markers. (在标记物间增加跳跃元素。)"
        ],
        "coaching_tips": [
            "Maintain balance throughout the weave. (在穿梭过程中始终保持重心平衡。)"
        ]
    },
    "no-easy-points-serve-receive": {
        "title": "Volleyball Serve Receive Drill: No Easy Points! (排球接发球训练：别想轻易得分！)",
        "description": "Emphasizes passing accuracy and earning rotations through consistent swings. (强调接发球精准度，并通过稳定的扣球攻击来赢得轮转。)",
        "setup": {
            "players": "1 server, 6-player team, 3 blockers (1名发球手，6名接球方，3名拦网手)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs, net (排球，球网)",
            "roles": "Receivers must earn rotations. (接球方必须通过进攻赢得轮转。)"
        },
        "steps": [
            "Team must achieve 3 consecutive successful swings in-bounds. (全队必须连续完成3次界内有力进攻。)",
            "Rotation only occurs after the goal is met. (只有达到目标后才能进行轮转。)"
        ],
        "variations": [
            "Increase to 5 consecutive swings for elite teams. (精英团队可增加到连续5次。)"
        ],
        "coaching_tips": [
            "Focus on the 'first ball' contact. (专注于“一传”触球力求到位。)"
        ]
    },
    "serve-receive-lines": {
        "title": "Volleyball Serve Receive Drill: Serve Receive Lines (排球接发球训练：接发球排队练习)",
        "description": "High-repetition drill focusing on individual consistency and target accuracy. (高重复性练习，专注于个人稳定性及送球精准度。)",
        "setup": {
            "players": "Servers on one side, passers in lines (一侧发球手，另一侧接球手排队)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs (排球)",
            "roles": "Passers shag their own ball. (垫球后自己捡球。)"
        },
        "steps": [
            "Passers enter the court, pass one serve, and rotate out. (进入场地，接发一个球后轮换出场。)",
            "Aim to get the ball into a target basket. (目标是将球垫入指定的篮筐或区域。)"
        ],
        "variations": [
            "Add a point system for accuracy. (增加精准度积分系统。)"
        ],
        "coaching_tips": [
            "Feet should be still at the moment of contact. (触球瞬间双脚应保持不动。)"
        ]
    },
    "cross-court-pepper": {
        "title": "Volleyball Warm-Up: Cross-Court Pepper (排球热身：跨场对练)",
        "description": "A dynamic warm-up that improves control, communication, and movement. (一种动态热身，旨在提高控球、沟通和移动能力。)",
        "setup": {
            "players": "Partners (1对1)",
            "court": "Diagonal placement (对角站位)",
            "equipment": "Volleyballs (排球)",
             "roles": ""
        },
        "steps": [
            "Partners hit back and forth across a diagonal space. (伴侣间在对角空间内进行往返击球。)",
            "Sequence: Pass - Set - Hit. (序列：垫、传、扣。)"
        ],
        "variations": [
            "One hand only for advanced control. (仅用单手以练习高阶控制。)"
        ],
        "coaching_tips": [
            "Keep the ball active as long as possible. (保持球尽可能长时间在空中运行。)"
        ]
    },
    "ball-control-25-contact-drill": {
        "title": "Volleyball Ball Control Drill: 25-Contact Challenge (排球控球训练：25次触球挑战)",
        "description": "Builds team consistency and focus on keeping the ball in play. (建立团队稳定性，专注于保持球不落地。)",
        "setup": {
            "players": "Groups of 6 (6人一组)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Keep the ball up for 25 consecutive touches using any legal contact. (使用任何合法触球动作保持球连续25次不落地。)"
        ],
        "variations": [
            "Requirement: 10 passes, 10 sets, 5 hits. (要求：10个垫球，10个传球，5个扣球。)"
        ],
        "coaching_tips": [
            "Call 'Mine' loudly for every touch. (每次触球都大声喊“我的”。)"
        ]
    },
    "hitting-drill-turn-go-hit": {
        "title": "Volleyball Hitting Drill: Turn, Go, Hit (排球扣球训练：转身、启动与扣球转换)",
        "description": "Improves hitter transitions and approach timing from off-net positions. (提高扣球手离网后的转换速度和助跑时机。)",
        "setup": {
            "players": "Hitters, setter (扣球手，二传手)",
            "court": "Net (网口)",
            "equipment": "Volleyballs (排球)",
            "roles": "Hitter starts at the net. (扣球手从网口开始。)"
        },
        "steps": [
            "Hitter touches net, turns, and transitions to approach. (触网、转身、后撤转换并开始助跑。)",
            "Execute a full approach and attack. (执行完整的助跑并完成进攻。)"
        ],
        "variations": [
            "Add a block to transition around. (增加拦网动作后再进行转换。)"
        ],
        "coaching_tips": [
            "Stay low during the transition step. (转换步中保持低重心。)"
        ]
    },
    "tag-team-warm-up": {
        "title": "Volleyball Warm-Up: Tag Team Rotation (排球热身：团队协作轮转热身)",
        "description": "Creates a fun, high-energy environment for pre-practice movement. (为训练前移动创造有趣、高能量的环境。)",
        "setup": {
            "players": "Entire team (全队)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs (排球)",
             "roles": "Partner work. (搭档配合。)"
        },
        "steps": [
            "Partners alternate touching the ball and rotating. (搭档间交替触球并轮换位置。)"
        ],
        "variations": [
            "Increase speed with multiple balls. (多球同时运行以加快速度。)"
        ],
        "coaching_tips": [
            "Keep your feet moving constantly. (双脚保持持续移动。)"
        ]
    },
    "down-ball-challenge": {
        "title": "Volleyball Ball Control: Down Ball Challenge (排球控球：下击球挑战赛)",
        "description": "Focuses on purposeful hitting and defensive coverage in a game scenario. (在比赛情境中专注于有目的的击球和防守覆盖。)",
        "setup": {
            "players": "6v6 (6对6)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs (排球)",
             "roles": ""
        },
        "steps": [
            "Rally starts with a down ball. (通过下击球发起回合。)",
            "Play out the point. (完成该回合。)"
        ],
        "variations": [
            "Points only count if hit to specified zones. (点击中指定区域才算得分。)"
        ],
        "coaching_tips": [
            "Cover your hitters deeply. (深层保护你的扣球手。)"
        ]
    },
    "free-ball-transition-and-catch": {
        "title": "Volleyball Free Ball Drill: Transition and Catch (排球送球训练：送球转换与接球练习)",
        "description": "Teaches teams to transition efficiently from base defense to free ball positions. (教会团队高效地从基本防守转换为送球防守位。)",
        "setup": {
             "players": "6 players (6名球员)",
             "court": "Full court (全场)",
             "equipment": "Volleyballs (排球)",
             "roles": ""
        },
        "steps": [
            "Team starts in defensive base. (团队从防守位开始。)",
            "Coach calls 'Free Ball' and tosses. (教练喊“送球”并投球。)",
            "Team transitions and catches at the target. (团队转换并在目标点接住球。)"
        ],
        "variations": [
            "Switch to passing and attacking once mastered. (熟练后切换为传扣进攻。)"
        ],
        "coaching_tips": [
            "Communicate 'Free' early. (尽早呼喊“送球”。)"
        ]
    },
    "volleyball-24-touches-ball-control": {
        "title": "Volleyball Ball Control Drill: 24-Touches! (排球控球训练：24项触球控球练习)",
        "description": "A comprehensive individual or pair drill covering all contact types. (涵盖所有触球类型的全面个人或双人练习。)",
        "setup": {
            "players": "Individual or pairs (个人或双人)",
            "court": "Any (任意位置)",
            "equipment": "1 ball (1个球)",
            "roles": ""
        },
        "steps": [
            "Perform a series of specific touches (e.g., 6 passes, 6 sets, 6 one-hand). (执行一系列特定的触球动作，如6个传球、6个垫球、6个单手等。)"
        ],
        "variations": [
            "Increase to 48 touches for advanced players. (高阶球员增加到48次触球。)"
        ],
        "coaching_tips": [
            "Focus on clean contact every time. (专注于每次触球的动作干净利索。)"
        ]
    },
    "blocking-form-drill": {
        "title": "Volleyball Blocking Drill: Blocking Form (排球拦网训练：拦网姿态强化训练)",
        "description": "Focuses on hand positioning, timing, and efficient net movement. (专注于手型、时机和高效的网口移动。)",
        "setup": {
             "players": "Blockers (拦网手)",
             "court": "Net (网口)",
             "equipment": "Net (球网)",
             "roles": ""
        },
        "steps": [
            "Practice hand position and penetration over the net. (练习过网的手型和穿透力。)",
            "Work on lateral footwork without crossing. (练习不交叉的侧向步法。)"
        ],
        "variations": [
            "Add a hitter to mimic timing. (增加一名扣球手以配合练习时机。)"
        ],
        "coaching_tips": [
            "Keep hands firm and high. (手部保持稳固且高举。)"
        ]
    },
    "blocking-middle-shuffles": {
        "title": "Middle Blocker Shuffles (副攻/中路拦网滑步强化)",
        "description": "Trains middle blockers to move laterally with speed and balance. (训练中路拦网手快速且平衡地进行侧向移动。)",
        "setup": {
            "players": "Middle blockers (副攻/中路拦网手)",
            "court": "At the net (网口)",
            "equipment": "Net (球网)",
            "roles": ""
        },
        "steps": [
            "Perform lateral shuffle steps along the net. (沿网口执行侧向滑步。)",
            "Finish with a controlled block jump. (以受控的拦网跳跃结束。)"
        ],
        "variations": [
            "Add a mirror drill with another player. (与另一名球员进行镜像同步练习。)"
        ],
        "coaching_tips": [
            "Do not cross your feet. (不要交叉双脚。)"
        ]
    },
    "defense-2-man-pit": {
        "title": "2-Man Defense Pit (两人防守深坑训练)",
        "description": "High-intensity defense for pairs. (针对双人的高强度防守训练。)",
        "setup": {
            "players": "2 defenders (2名防守者)",
            "court": "Half court (半场)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Defenders must stay in until a set number of digs. (防守者必须留在场内直到达到预设的起球数。)",
            "Balls are hit rapidly to various spots. (球被快速击向不同的位置。)"
        ],
        "variations": [
            "Require perfect passes to the setter spot. (要求必须完美起到二传位。)"
        ],
        "coaching_tips": [
            "Stay on the balls of your feet. (保持前脚掌着地。)"
        ]
    },
    "defense-3-man-pit": {
        "title": "3-Man Defense Pit (三人防守深坑训练)",
        "description": "Covers more court area with three defenders. (三名防守者覆盖更大的场地面积。)",
        "setup": {
            "players": "3 defenders (3名防守者)",
            "court": "Full court back-row (后排全场)",
            "equipment": "Volleyballs (排球)",
             "roles": ""
        },
        "steps": [
            "Similar to 2-man pit but with 3 players covers the 'short' and 'deep' zones. (类似于两人深坑训练，但由三名球员覆盖“浅区”和“深区”。)"
        ],
        "variations": [
            "Hitter moves around the court to change angles. (扣球手在场内走动以改变攻击角度。)"
        ],
        "coaching_tips": [
            "Communicate the 'seams' (gaps between players). (对“接缝区”，即球员间的空隙，进行有效沟通。)"
        ]
    },
    "passing-lateral-movement-drill": {
        "title": "Lateral Movement Passing (侧向移动垫球训练)",
        "description": "Focuses on footwork and platform stability while moving. (专注于移动中的步法和手臂平面稳定性。)",
        "setup": {
            "players": "1 passer, 1 tosser (1名垫球手，1名抛球手)",
            "court": "Half court (半场)",
             "equipment": "Volleyballs (排球)",
             "roles": ""
        },
        "steps": [
            "Passer starts at center. (垫球手从中线开始。)",
            "Tosser throws to the side. (抛球手向侧面抛球。)",
            "Passer shuffles and passes back. (垫球手滑步并垫球回传。)"
        ],
        "variations": [
            "Alternate sides rapidly. (快速交替左右两侧。)"
        ],
        "coaching_tips": [
            "Square your shoulders to the target before contact. (触球前双肩正对目标。)"
        ]
    },
    "defense-sprawl-and-dig": {
        "title": "Sprawl and Dig (鱼跃控球防守训练)",
        "description": "Teaches emergency defensive techniques for low balls. (教授针对低球的紧急防守技术。)",
        "setup": {
            "players": "Defenders (防守者)",
            "court": "Back row (后排)",
            "equipment": "Volleyballs (排球)",
            "roles": "Focus on floor safety. (专注于地板动作安全性。)"
        },
        "steps": [
            "Defenders start in low ready position. (防守者低位准备。)",
            "Coach tosses a low ball in front. (教练向前抛出一个低球。)",
            "Defender sprawls and digs the ball up. (防守者鱼跃扑地并起球。)"
        ],
        "variations": [
            "Add a second ball immediately after recovery. (恢复位后立即接第二个球。)"
        ],
        "coaching_tips": [
            "Slide through the contact, don't just dive down. (滑过触球点，而不仅仅是向下俯冲。)"
        ]
    },
    "serve-receive-3-pass-and-rotate": {
        "title": "3 Pass and Rotate (3次接发球与轮转训练)",
        "description": "Simulates game rotations and serve receive pressure. (模拟比赛轮转和接发球压力。)",
        "setup": {
            "players": "6-player team (6人团队)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs, net (排球，球网)",
            "roles": ""
        },
        "steps": [
            "Pass 3 consecutive serves perfectly to rotate. (连续完美接好3个发球方可轮转。)"
        ],
        "variations": [
            "Allow offensive swings after the pass. (允许接发球后进行进攻。)"
        ],
        "coaching_tips": [
            "Movement before the ball is served is key. (发球前的移动是关键。)"
        ]
    },
    "passing-middle-or-lateral": {
        "title": "Middle or Lateral Passing (中路或侧向垫球判定)",
        "description": "Teaches hitters to adjust their platform based on ball location. (教会击球手根据来球位置调整手臂平面。)",
        "setup": {
            "players": "Passers, coach (接球手，教练)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs (排球)",
            "roles": "Coach serves/tosses randomly. (教练随机发球/抛球。)"
        },
        "steps": [
            "Identify if the ball is coming to the midline or lateral side. (判断球是看向中路还是侧向。)",
            "Adjust platform angle accordingly. (相应地调整手臂平面角度。)"
        ],
        "variations": [
            "Add a setter to finish the play. (增加二传手以完成该回合。)"
        ],
        "coaching_tips": [
            "Early identification is essential. (及早判断至关重要。)"
        ]
    },
    "setters-vs-passers-game": {
        "title": "Setters vs. Passers Game (二传 vs 垫球手对抗赛)",
        "description": "A fun competitive game focusing on specific contact types. (专注于特定触球类型的有趣对抗赛。)",
        "setup": {
            "players": "2 hitters, 2 passers (2名击球手，2名垫球手)",
            "court": "Small court (小场地)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Play a small-sided game. (进行小场地比赛。)",
            "One side can only set, the other only pass. (一侧只能用传球，另一侧只能用垫球。)"
        ],
        "variations": [
            "Switch roles after 5 points. (每5分交换角色。)"
        ],
        "coaching_tips": [
            "Focus on the unique challenges of each technique. (专注于每种技术的独特挑战。)"
        ]
    },
    "double-the-number": {
        "title": "Double the Number (数量翻倍控球赛)",
        "description": "Team-building ball control game. (团队建设类的控球游戏。)",
        "setup": {
            "players": "Entire team (全队)",
            "court": "Full court (全场)",
             "equipment": "Volleyballs (排球)",
             "roles": ""
        },
        "steps": [
            "Start with 1 touch, then 2, then 4, doubling each round. (从1次触球开始，然后2次、4次，每一轮翻倍。)"
        ],
        "variations": [
            "Use different types of contacts for each round. (每一轮使用不同类型的触球方法。)"
        ],
        "coaching_tips": [
            "Maintain focus as the number increases. (随着数量增加保持专注。)"
        ]
    },
    "volleyball-footwork-drill": {
        "title": "Middle Hitter Footwork (副攻步法训练)",
        "description": "Specific movements for middle attackers. (针对中路进攻者的专项移动练习。)",
        "setup": {
            "players": "Middle hitters (副攻)",
            "court": "At the net (网口)",
            "equipment": "Net (球网)",
            "roles": ""
        },
        "steps": [
            "Practice 'X' and 'Open' steps for transitions. (练习转换中的“X”型步和“开口”步。)",
            "Simulate approach from different points. (模拟从不同点发起的助跑。)"
        ],
        "variations": [
            "Add a setter for realistic timing. (增加二传手以获得真实的配合时机。)"
        ],
        "coaching_tips": [
            "Stay balanced and ready to jump. (保持平衡，随时准备起跳。)"
        ]
    },
    "volleyball-serving-relay": {
        "title": "Serving Relay (发球接力赛)",
        "description": "Competitive serving under pressure. (压力下的发球竞赛。)",
        "setup": {
            "players": "Two teams (两支队伍)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Teams relay to serve the ball into specific zones. (两队轮流发球，争取击中特定区域。)",
            "Wait for teammate's success before next serve. (在下一个人发球前，等待前一名队友成功击中目标。)"
        ],
        "variations": [
            "Add a sprint element between serves. (在发球间隙增加冲刺元素。)"
        ],
        "coaching_tips": [
            "Keep composed under pressure. (在压力下保持冷静。)"
        ]
    },
    "free-ball-pass-set-cover-and-catch": {
        "title": "Pass, Set, Cover, and Catch (垫、传、保护与接球)",
        "description": "Full sequence training for free ball situations. (针对送球情境的全流程训练。)",
        "setup": {
            "players": "6-player team (6人团队)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Pass the free ball, set it, then simulate a cover scenario. (垫送球，进行传球，然后模拟保护情境。)"
        ],
        "variations": [
            "Add a hitter to make it a full play. (增加一名扣球手以完成整个回合。)"
        ],
        "coaching_tips": [
            "Know your coverage responsibilities. (明确你的保护区域责任。)"
        ]
    },
    "volleyball-partner-pass-and-down-balls": {
        "title": "Partner Pass and Down Balls (双人垫球与下击球)",
        "description": "Small group control and hitting. (小组成组的控球与击球练习。)",
        "setup": {
             "players": "Partners (1对1)",
             "court": "Half court (半场)",
             "equipment": "Volleyballs (排球)",
             "roles": ""
        },
        "steps": [
            "Partners alternate between passing and hitting down balls. (伴侣间在垫球和下击球之间交替练习。)"
        ],
        "variations": [
            "Increase speed and power over time. (随着时间推移增加速度和力量。)"
        ],
        "coaching_tips": [
            "Focus on the rhythm of the drill. (专注于练习的节奏感。)"
        ]
    },
    "3-and-over": {
        "title": "3 and Over (三次过网训练)",
        "description": "Introduction to the three-touch rule for beginners. (初学者对三次触球规则的入门。)",
        "setup": {
            "players": "Groups of 3 (3人一组)",
            "court": "Mini court (小场地)",
            "equipment": "Volleyballs (排球)",
             "roles": ""
        },
        "steps": [
            "Must use 3 touches to send the ball over. (必须使用3次触球将球过网。)"
        ],
        "variations": [
            "Requirement: Pass, Set, Hit in order. (要求：按垫、传、扣的顺序。)"
        ],
        "coaching_tips": [
            "Celebrate every 3-touch success. (为每一次成功的三次触球喝彩。)"
        ]
    },
    "volleyball-passing-free-balls-to-setter": {
        "title": "Free Balls to Setter (送球至二传练习)",
        "description": "Focuses on transition and passing accuracy to the target. (专注于转换和向目标垫送球的精准度。)",
        "setup": {
            "players": "Passers, setter (接球手，二传手)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Coach tosses free ball. (教练抛送球。)",
            "Passer delivers a perfect pass to the setter station. (接球手将球完美垫向二传位。)"
        ],
        "variations": [
            "Increase the distance of the toss. (增加抛球的距离。)"
        ],
        "coaching_tips": [
            "High, easy-to-handle passes are best. (高且易于处理的垫球是最好的。)"
        ]
    },
    "setting-game": {
        "title": "Volleyball Setting Game (传球竞赛)",
        "description": "Only overhead passes allowed in this competitive game. (在这项竞赛中仅限使用上手传球。)",
        "setup": {
            "players": "2v2 or 3v3 (2对2或3对3)",
            "court": "Small side (小场地)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Play a standard game but use only overhead sets. (进行标准比赛，但只能用上手传球。)"
        ],
        "variations": [
            "Allowed 1 bounce for beginners. (初学者允许落地一次。)"
        ],
        "coaching_tips": [
            "Get into position early with hands high. (尽早到位并保持手部高举。)"
        ]
    },
    "partner-setting-and-overhead-passing-drill": {
        "title": "Partner Setting (双人传球练习)",
        "description": "Fundamental overhead passing consistency for training. (基础上手传球稳定性的专项训练。)",
        "setup": {
            "players": "Partners (1对1)",
            "court": "Half court (半场)",
            "equipment": "Volleyballs (排球)",
             "roles": ""
        },
        "steps": [
            "Set back and forth at a close distance. (近距离进行往返传球。)"
        ],
        "variations": [
            "One partner kneels to focus on hand movement. (一个搭档跪地练习以专注于手部动作。)"
        ],
        "coaching_tips": [
            "Use your legs to power the set. (利用双腿的力量为传球发力。)"
        ]
    },
    "rapid-pass-set-drill": {
        "title": "Rapid Pass and Set (快速垫传训练)",
        "description": "Improving tempo and accuracy in ball transitions. (在球路转换中提高节奏和精准度。)",
        "setup": {
            "players": "Groups of 4 (4人一组)",
            "court": "Full court (全场)",
            "equipment": "Multiple volleyballs (多个排球)",
            "roles": ""
        },
        "steps": [
            "Quickly pass and set one ball after another. (连续不断地进行下一个球的垫传练习。)"
        ],
        "variations": [
            "Limit the time between contacts. (限制触球间的时间间隔。)"
        ],
        "coaching_tips": [
            "Focus on fast footwork. (专注于快捷的步法。)"
        ]
    },
    "volleyball-passing-run-through-and-short-pass": {
        "title": "Run Through and Short Pass (冲前垫球与短球练习)",
        "description": "Movement-based passing warm-up to improve reaction. (基于移动的垫球热身以提高反应速度。)",
        "setup": {
            "players": "Passers, coach (接球手，教练)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Coach tosses a short ball. (教练抛短球。)",
            "Passer runs through to pass the ball while moving. (接球手冲上前并在移动中将球垫起。)"
        ],
        "variations": [
            "Vary the angle of the toss. (改变抛球的角度。)"
        ],
        "coaching_tips": [
            "Keep your platform steady even while running. (即使在跑动中也要保持手臂平面稳定。)"
        ]
    },
    "blocking-net-decision": {
        "title": "Net Decision Blocking (网口拦网决策训练)",
        "description": "Reading the ball and making blocking decisions at the net. (在网口阅读球路并作出拦网决策。)",
        "setup": {
             "players": "Blockers, hitters (拦网手，扣球手)",
             "court": "Net (网口)",
             "equipment": "Volleyballs, net (排球，球网)",
             "roles": ""
        },
        "steps": [
            "Hitter simulates different attacks. (扣球手模拟不同的进攻。)",
            "Blocker decides whether to commit or close the seam. (拦网手决定是进行定人拦网还是补位。)"
        ],
        "variations": [
            "Add a second blocker for tandem decisions. (增加第二名拦网手练习双人配合决策。)"
        ],
        "coaching_tips": [
            "Watch the hitter's approach and shoulders. (观察扣球手的助跑和肩膀动作。)"
        ]
    },
    "warm-up-with-wall": {
        "title": "Warm-up with Wall (墙面控球热身)",
        "description": "Individual ball control against a wall. (针对墙面的个人控球热身。)",
        "setup": {
            "players": "Individual (个人)",
            "court": "Near a wall (墙边)",
            "equipment": "1 volleyball (1个排球)",
            "roles": ""
        },
        "steps": [
            "Hit the ball against the wall repeatedly using passes and sets. (利用垫球和传球连续对着墙击球。)",
            "Keep the ball at a consistent height. (保持球在稳定的高度。)"
        ],
        "variations": [
            "Use only one hand for added difficulty. (增加难度：仅用单手。)"
        ],
        "coaching_tips": [
            "Stay on your toes. (保持脚尖着地。)"
        ]
    },
    "serving-with-partner": {
        "title": "Serving with Partner (双人对发球训练)",
        "description": "Focuses on serving accuracy to a specific target partner. (专注于向特定目标搭档发球的精准度训练。)",
        "setup": {
            "players": "Partners (1对1)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs (排球)",
            "roles": "Partners stand opposite each other. (搭档相对而立。)"
        },
        "steps": [
            "Server aims for the partner's chest. (发球手瞄准搭档的胸部位置。)",
            "Partner catches or passes back. (搭档接球或垫球回传。)"
        ],
        "variations": [
             "Aim for specific spots on the floor around the partner. (瞄准搭档周围地面上的特定点。)"
        ],
        "coaching_tips": [
            "Focus on a consistent follow-through. (专注于稳定的随挥动作。)"
        ]
    },
    "line-setting-drill": {
        "title": "Line Setting Drill (排队传球训练)",
        "description": "Focuses on squaring up to the target in a fast-paced line. (专注于在快节奏的排队中正对目标进行传球。)",
        "setup": {
            "players": "Line of setters (排队的传球手)",
            "court": "Half court (半场)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Run into position, square up, and set to target. (跑入位置，正对目标，并将球传出。)",
            "Rotate to the back of the line. (轮换到队尾。)"
        ],
        "variations": [
            "Add a movement obstacle like a cone. (增加移动障碍，如标志桩。)"
        ],
        "coaching_tips": [
            "Hurry to get under the ball. (尽快跑到球的下方。)"
        ]
    },
    "volleyball-ball-control-with-movement": {
        "title": "Ball Control with Movement (移动中控球训练)",
        "description": "Improving dynamic ball control while moving across the court. (在穿越场地移动时提高动态控球能力。)",
        "setup": {
            "players": "Partners (1对1)",
            "court": "Side to side (横贯全场)",
            "equipment": "Volleyballs (排球)",
             "roles": ""
        },
        "steps": [
            "Partners move across the court while keeping the ball in the air. (搭档在球不落地的情况下横穿场地。)",
            "Use only controlled touches. (仅使用受控的触球动作。)"
        ],
        "variations": [
            "Include a 360-degree turn between touches. (在触球之间增加360度转身动作。)"
        ],
        "coaching_tips": [
            "Keep your eyes on the ball, not your feet. (盯着球看，而不是盯着脚。)"
        ]
    },
    "2-player-down-volleyball-passing-drill": {
        "title": "2 Player Down Passing (二人倒地起球垫球训练)",
        "description": "Quick reaction and recovery defense drill for pairs. (针对双人的快速反应与恢复位防守练习。)",
        "setup": {
            "players": "2 defenders (2名防守者)",
            "court": "Half court (半场)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Defender starts on the floor, pops up, and passes a ball. (防守者从地面起步，弹起并垫球。)"
        ],
        "variations": [
            "Alternate who is 'down' each touch. (每次触球交替进行倒地动作。)"
        ],
        "coaching_tips": [
            "Focus on a fast first step after recovery. (专注于恢复位后的第一快步。)"
        ]
    },
    "circle-passing-drill": {
        "title": "Circle Passing Drill (圆圈垫球热身)",
        "description": "Basic ball control in a group circle formation. (小组内以圆圈阵型进行基础控球热身。)",
        "setup": {
            "players": "Groups of 5-6 (5-6人一组)",
            "court": "Open area (空旷区域)",
            "equipment": "1 ball (1个球)",
             "roles": ""
        },
        "steps": [
            "Group forms a circle and keeps the ball up using only passes. (小组围成一圈，仅用垫球保持球不落地。)"
        ],
        "variations": [
            "One person in the middle must pass every other touch. (中间站一人，必须隔一次触球就接一次球。)"
        ],
        "coaching_tips": [
            "Work as a team to keep the rhythm. (团队协作以保持节奏。)"
        ]
    },
    "ball-control-with-back-row-attacks": {
        "title": "Back Row Attacks Ball Control (后场进攻控球训练)",
        "description": "Improving back row attacking accuracy and depth. (提高后排进攻的控球精准度和深度。)",
        "setup": {
            "players": "Back row hitters (后排扣球手)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Hitter attacks from behind the 3-meter line. (击球手在三米线后发起进攻。)",
            "Aim for specific target zones in the deep court. (瞄准场地深处的特定目标区域。)"
        ],
        "variations": [
             "Vary the set height and location. (改变传球的高度和位置。)"
        ],
        "coaching_tips": [
             "Coordinate your approach and jump. (协调你的助跑和起跳动作。)"
        ]
    },
    "volleyball-set-and-switch-drill": {
        "title": "Set and Switch Drill (传球与换位训练)",
        "description": "Focuses on overhead passing and quick movement after the set. (专注于上手传球以及在传球后的快速移动与换位。)",
        "setup": {
            "players": "Groups of 3 (3人一组)",
            "court": "Half court (半场)",
            "equipment": "Volleyballs (排球)",
             "roles": ""
        },
        "steps": [
            "Set the ball, then sprint to the next station. (传球，然后冲刺到下一个站点。)",
            "Follow your pass. (跟着你传出的球移动。)"
        ],
        "variations": [
            "Switch positions after every 5 successful sets. (每成功传球5次后交换位置。)"
        ],
        "coaching_tips": [
            "Focus on a clean release of the ball. (专注于干净利索的出手。)"
        ]
    },
    "individual-setting-drill": {
        "title": "Individual Setting Drill (个人传球专项练习)",
        "description": "Self-touches to improve hand contact and finger strength. (通过自传练习提高触球感和手指力量。)",
        "setup": {
            "players": "Individual (个人)",
            "court": "Any (任意位置)",
            "equipment": "1 volleyball (1个排球)",
            "roles": ""
        },
        "steps": [
            "Set the ball to yourself repeatedly. (对着自己重复进行传球练习。)",
            "Maintain a consistent height above the head. (保持在头顶上方稳定的高度。)"
        ],
        "variations": [
            "Vary the height from low to high. (高度从低到高不断变换。)"
        ],
        "coaching_tips": [
            "Use soft but firm finger contact. (手指触球要轻柔但有力。)"
        ]
    },
    "down-ball-hitting-drill": {
        "title": "Down Ball Hitting (下击球扣球训练)",
        "description": "Purposeful hitting technique from the floor. (针对地面发起的有目的性击球技术。)",
        "setup": {
            "players": "Hitters (扣球手)",
            "court": "Back row (后排)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Execute a controlled down ball attack over the net. (执行一次受控的下击球进攻将球送过网。)"
        ],
        "variations": [
            "Target lines or cross-court specifically. (专门练习针对直线或斜线的进攻点。)"
        ],
        "coaching_tips": [
            "Snap your wrist for better control. (压手腕以获得更好的控制。)"
        ]
    },
    "short-serve-competition": {
        "title": "Serving for Accuracy (精准发球训练)",
        "description": "Targeting specific zones on the court to improve serve precision. (练习瞄准场地特定区域发球，以提高发球精准度。)",
        "setup": {
            "players": "Servers (发球手)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs, hoops or cones as targets (排球，圆圈或标志桩作为目标)",
            "roles": ""
        },
        "steps": [
            "Attempt to serve into specified target zones. (尝试向指定的发球目标区域发球。)",
            "Vary the serve type (standing, jump float). (变换发球类型，如上手或跳飘。)"
        ],
        "variations": [
            "Competitive game: First to hit all zones wins. (竞赛：首个击中所有区域者获胜。)"
        ],
        "coaching_tips": [
            "Pick a small target to stay focused. (选一个小一点的目标来保持专注。)"
        ]
    },
    "volleyball-serving-around-the-world": {
        "title": "Serving Around the World (环游世界发球挑战)",
        "description": "A fun challenge to hit every court zone in sequence. (按顺序击中场地每一个区域的有趣挑战练习。)",
        "setup": {
            "players": "Individual or teams (个人或团队)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs, cones for zones (排球，标志桩划分区域)",
            "roles": ""
        },
        "steps": [
            "Serve into zones 1 through 6 in numeric order. (按数字顺序向1号位到6号位依次发球。)",
            "Must hit the zone before moving to the next. (必须击中当前区域才能进入下一个。)"
        ],
        "variations": [
            "Timed challenge: Fastest to finish 'the world' wins. (计时挑战：最快完成“环游世界”者获胜。)"
        ],
        "coaching_tips": [
            "Keep a consistent serving routine for every rep. (每次发球都要保持一致的准备动作。)"
        ]
    },
    "volleyball-ball-control-two-person-four-square": {
        "title": "Partner Digging (双人防守起球练习)",
        "description": "Refining individual digging skills through high-repetition pair work. (通过高重复性的双人练习来精炼个人防守起球技术。)",
        "setup": {
            "players": "Partners (1对1)",
            "court": "Half court (半场)",
            "equipment": "Volleyballs (排球)",
            "roles": "One hits, one digs. (一人击球，一人防守。)"
        },
        "steps": [
            "Hitters deliver various balls (tips, drives) to the digger. (击球手向防守者送出各种球，如吊球、重扣等。)",
            "Digger tries to return every ball to a target spot. (防守者尝试将每个球都防起到目标位。)"
        ],
        "variations": [
            "Switch roles every 10 successful digs. (每10个成功起球后交换角色。)"
        ],
        "coaching_tips": [
            "Stay low and keep your platform away from your body. (保持低重心，手臂平面远离身体。)"
        ]
    },
    "quick-setter-transitioning-drill": {
        "title": "Setter Movement & Accuracy (二传移动与精准度)",
        "description": "Getting to the ball quickly and delivering a hitable set. (快速向球移动并送出高质量的可攻击传球。)",
        "setup": {
            "players": "Setters (二传手)",
            "court": "Near net (靠近网口)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Coach tosses balls randomly across the court. (教练向全场随机投球。)",
            "Setter moves to set each one to a target. (二传手移动并将每个球传至目标位。)"
        ],
        "variations": [
            "Include 'out-of-system' balls from the back court. (加入从后场传回的“不到位”球。)"
        ],
        "coaching_tips": [
            "Be efficient in your movement path. (移动路径要尽可能高效。)"
        ]
    },
    "individual-serving-relay": {
        "title": "Serving Zones Challenge (发球区域得分挑战)",
        "description": "Strategic serving drill where points are awarded for hitting difficult zones. (战略性发球训练，通过击中困难区域来赢得分数。)",
        "setup": {
            "players": "Servers (发球手)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs, target mats (排球，目标垫)",
            "roles": ""
        },
        "steps": [
            "Hitters serve to zones 1, 5, or the 'short' zones for dynamic points. (向1号位、5号位或“浅区”发球以获得动态积分。)",
            "Track individual or team progress. (跟踪个人或团队的积分进度。)"
        ],
        "variations": [
            "Deduct points for serves that go out or into the net. (发球出界或下网扣分。)"
        ],
        "coaching_tips": [
            "Toss is the most important part of the serve. (抛球是发球中最重要的部分。)"
        ]
    },
    "serve-receive-transition-to-hitting-drill": {
        "title": "Serve Receive to Attack (接发球转攻专项训练)",
        "description": "Training the full sequence from serve receive to side-out attack. (训练从接发球到侧应战转攻的完整流程。)",
        "setup": {
            "players": "Passers, hitters, setter (接球手，扣球手，二传手)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs, net (排球，球网)",
            "roles": ""
        },
        "steps": [
            "Pass a serve, then perform a transition to attack. (接一个发球，然后立即执行进攻转换。)",
            "Finish with a controlled attack into a target zone. (以一次针对目标区域的受控进攻结束。)"
        ],
        "variations": [
            "Rotate positions after 5 successful points. (每得5分后换一次位。)"
        ],
        "coaching_tips": [
            "Focus on the rhythm between the pass and the attack. (专注于垫球和进攻之间的节奏感。)"
        ]
    },
    "net-save-drill": {
        "title": "Passing Out of the Net (球网起球练习)",
        "description": "Teaches players to read and control balls rebounding off the net. (教导球员如何应对并起起从网上弹回的球。)",
        "setup": {
            "players": "Groups of 3 (3人一组)",
            "court": "Net area (网区)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Toss ball into the net at various heights. (将球以不同高度抛向网上。)",
            "Passer must react and pop the ball up for a setter. (接球手必须做出反应并将球垫起给二传。)"
        ],
        "variations": [
            "Add a second ball immediately after the first. (第一个球后立即抛出第二个球。)"
        ],
        "coaching_tips": [
            "Stay low and watch the ball's angle off the mesh. (保持低重心，观察球在网面上的反弹角度。)"
        ]
    },
    "volleyball-double-serving-game": {
        "title": "Team Communication (团队沟通专项训练)",
        "description": "Building loud and efficient court talk to avoid collisions and missed balls. (建立高效、响亮的球场沟通，以避免碰撞和漏球。)",
        "setup": {
            "players": "Full 6-player team (完整的6人队)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Play out rallies where every touch must be accompanied by a loud call. (进行回合练习，规定每次触球必须伴随着响亮的呼喊。)",
            "Failure to call results in a point for the other side. (未呼喊则判定对方得分。)"
        ],
        "variations": [
            "Silent warm-up followed by hyper-vocal play to emphasize the difference. (先进行无声热身，再进行高强度发声练习，以强调沟通的差异。)"
        ],
        "coaching_tips": [
            "Talk early and talk often! (早沟通，勤沟通！)"
        ]
    },
    "volleyball-defense-touch-ten": {
        "title": "Defense: Touch Ten (防守：触球10次挑战)",
        "description": "Improving quick movement and recovery from flooring a ball. (提高倒地起球后的快速移动与恢复动态。)",
        "setup": {
            "players": "Defenders (防守者)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Coach hits a ball; defender must touch the ball and immediately touch a line before the next ball. (教练击球；防守者触球后必须立即在下一个球到来前触碰场线。)",
            "Perform 10 consecutive touches without error. (连续完成10次触球且无失误。)"
        ],
        "variations": [
            "Increase speed of delivery. (增加供球速度。)"
        ],
        "coaching_tips": [
            "Stay on your toes and move with purpose. (保持脚尖着地，有目的地移动。)"
        ]
    },
    "12-ball-wash-drill": {
        "title": "12-Ball Wash (12球洗刷对抗赛)",
        "description": "Intense side-out game to simulate match pressure and consistency. (高强度侧重对抗赛，模拟比赛压力下的稳定性。)",
        "setup": {
            "players": "Two 6-player teams (两支6人队)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Teams compete in mini-sets of 12 balls initiated by the coach. (球队在教练启动的12球小组赛中竞争。)",
            "A point is only awarded to the side that wins the 'wash' (e.g., scoring twice in a row). (只有连续赢得“洗刷”（如连续得两分）的一方才能得分。)"
        ],
        "variations": [
             "Vary the starting ball (free ball, down ball, serve). (变换初始球位，如接发、下击球、发球。)"
        ],
        "coaching_tips": [
             "Maintain focus throughout the entire wash. (在整个洗刷过程中保持高度专注。)"
        ]
    },
    "volleyball-ball-control-elimination": {
        "title": "Ball Control Elimination (控球淘汰赛)",
        "description": "Last-player-standing drill focusing on precise touches under pressure. (最后一人留存练习，侧重于压力下的精准触球。)",
        "setup": {
            "players": "Varies (不限制人数)",
            "court": "Half court (半场)",
            "equipment": "1 volleyball (1个球)",
            "roles": ""
        },
        "steps": [
            "Players must execute a specific touch (e.g., set to self) while moving. (球员在移动中必须执行特定的触球动作，如自传。)",
            "The player with the least controlled touch is eliminated. (触球质量最差的球员被淘汰。)"
        ],
        "variations": [
            "Vary the required touch type. (变换要求的触球类型。)"
        ],
        "coaching_tips": [
            "Don't lose focus as the group gets smaller. (不要随着人数减少而失去专注。)"
        ]
    },
    "set-and-spin": {
        "title": "Set and Spin (传球后转身练习)",
        "description": "Improving dynamic balance and quick reset for setters. (提高二传手的动态平衡感和快速重置能力。)",
        "setup": {
            "players": "Setters (二传手)",
            "court": "Near net (网口附近)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Execute a set, perform a 360-degree spin, and immediately square up for the next ball. (完成一次传球，原地360度转身，随后立即正对下一个来球。)"
        ],
        "variations": [
            "Add hurdles or cones to spin around. (增加障碍物或标志桩围绕旋转。)"
        ],
        "coaching_tips": [
            "Find your target quickly after the spin. (转身后快速锁定目标。)"
        ]
    },
    "coverage-drill": {
        "title": "Back Row Defense & Rotation (后排防守与重心移动)",
        "description": "Improve positioning and reading from the backcourt during active rallies. (在回合中提高后场的位移、站位与阅读能力。)",
        "setup": {
            "players": "Back row defenders (后排防守球员)",
            "court": "Back row (后排区域)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Defenders rotate through positions based on the simulated attack origin. (防守者根据模拟进攻的来源点进行防守位移。)",
            "Focus on maintaining a low, ready stance while moving. (专注于在移动中保持低位的准备姿态。)"
        ],
        "variations": [
            "Add a 'sinker' ball to force a forward move. (增加一个“下沉球”以强迫防守者前冲。)"
        ],
        "coaching_tips": [
            "Beat the ball to the spot! (先于球到达防守位！)"
        ]
    },
    "vollebyball-jump-serve-updown": {
        "title": "Jump Serve Speed & Power (跳发球速度与力量强化)",
        "description": "Improving jump serve velocity and difficulty. (提高跳发球的球速和破坏力。)",
        "setup": {
            "players": "Servers (发球手)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Execute powerful jump serves to target zones. (向目标区域执行强力跳发球。)",
            "Focus on high contact and explosive approach. (专注于高点触球和爆发性助跑。)"
        ],
        "variations": [
            "Competitive speed tracking. (竞争性的速度追踪练习。)"
        ],
        "coaching_tips": [
            "Snap that wrist over the top. (扣动手腕越过球的上方。)"
        ]
    },
    "3-skill-pepper-with-partner": {
        "title": "3-Skill Pepper (三项控球对练)",
        "description": "Integrating pass, set, and attack in a high-control sequence. (在受控序列中集成垫、传、打三项技术。)",
        "setup": {
            "players": "Partners (1对1)",
            "court": "Open space (空旷空地)",
            "equipment": "1 volleyball (1个球)",
            "roles": ""
        },
        "steps": [
            "Perform a controlled Pass-Set-Attack sequence with a partner. (与搭档进行受控的“垫-传-打”循环练习。)",
            "Goal is to maintain the sequence for 50 reps. (目标是连续维持循环50次。)"
        ],
        "variations": [
            "Switch attack heights mid-sequence. (练习中途变换攻击高度。)"
        ],
        "coaching_tips": [
            "Focus on consistency over power. (相对于力量，更应专注于稳定性。)"
        ]
    },
    "middle-back-defensive-positioning-and-movement": {
        "title": "Middle-Back Defense (中后排防守定位)",
        "description": "Specifically training the 6-position defender for line and angle balls. (专门针对6号位防守者的直线和对角球防守训练。)",
        "setup": {
            "players": "6-position defenders (6号位防守球员)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Defender reads the hitter and moves to cover line or angle based on coach's signal. (防守者阅读扣球手动作，并根据教练信号移动封堵直线或斜线。)"
        ],
        "variations": [
            "Add a block to simulate screen situations. (增加拦网以模拟视觉遮挡情况。)"
        ],
        "coaching_tips": [
            "Read the ball from the hitter's hand. (从扣球手的手部动作判断球路。)"
        ]
    },
    "ball-control-pass-set-downball": {
        "title": "Pass-Set-Downball Sequence (垫传下击球序列练习)",
        "description": "Improving the connection between the first three touches. (提高前三次触球之间的衔接质量。)",
        "setup": {
            "players": "Groups of 3 (3人一组)",
            "court": "Net-side (网侧)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Pass a toss, set to an attacker, who executes a downball. (接抛球并传给进攻手，进攻手执行下击球过网。)",
            "Repeat for rhythm. (重复练习以建立节奏感。)"
        ],
        "variations": [
             "Change directions after every 5 reps. (每5次后更换方位。)"
        ],
        "coaching_tips": [
             "Keep the ball high enough for the next player to adjust. (保持球的高度足以让下一名球员进行调整。)"
        ]
    },
    "set-and-switch": {
        "title": "Set and Switch Drill (传球与换位训练)",
        "description": "Focuses on overhead passing and quick movement after the set. (专注于上手传球以及在传球后的快速移动与换位。)",
        "setup": {
            "players": "Groups of 3 (3人一组)",
            "court": "Half court (半场)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Set the ball, then sprint to the next station. (传球，然后冲刺到下一个站点。)",
            "Follow your pass. (跟着你传出的球移动。)"
        ],
        "variations": [
            "Switch positions after every 5 successful sets. (每成功传球5次后交换位置。)"
        ],
        "coaching_tips": [
            "Focus on a clean release of the ball. (专注于干净利索的出手。)"
        ]
    },
    "triangle-pepper-drill-over-the-net": {
        "title": "Triangle Pepper Over the Net (隔网三角对练)",
        "description": "Multi-player control sequence across the net to build awareness. (跨网的多人控球序列，旨在建立场地意识。)",
        "setup": {
            "players": "Groups of 3 per side (每侧3人一组)",
            "court": "Net (网口)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Maintain a Pass-Set-Attack loop between both sides forming a triangle flow. (在两组间建立“垫-传-打”循环，形成三角流动感。)"
        ],
        "variations": [
            "No jumping allowed. (禁止起跳。)"
        ],
        "coaching_tips": [
            "Communicate the next touch early. (尽早呼喊下一次触球。)"
        ]
    },
    "3-player-down-ball-with-movement": {
        "title": "3 Player Down Ball with Movement (三人移动下击球练习)",
        "description": "Targeting high-reward zones from the back from 3 attackers. (通过三名进攻者瞄准后场高回报区域的进攻练习。)",
        "setup": {
            "players": "3 attackers (3名进攻者)",
            "court": "Back row (后排)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Attackers rotate through hitting spots, executing down balls to target zones. (进攻者轮换击球位，向目标区域执行下击球进攻。)",
            "Emphasize ball depth and transition speed. (强调球的落点深度和转换速度。)"
        ],
        "variations": [
            "Competitive scoring based on target accuracy. (根据目标精准度进行竞争性计分。)"
        ],
        "coaching_tips": [
            "Arm swing should be consistent regardless of target. (无论目标在哪，挥臂动作应保持一致。)"
        ]
    },
    "setter-dump-and-attack": {
        "title": "Setter Dump & Attack (二传手吊球与进攻)",
        "description": "Adding offensive threat to the setter position to keep blockers guessing. (增加二传位置的进攻威胁，使对方拦网手难以预判。)",
        "setup": {
            "players": "Setters (二传手)",
            "court": "Net (网口)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Simulate a standard set, but tip the ball over to an empty spot. (模拟标准传球，但将球轻吊至对方空位。)",
            "Practice the 'no-look' dump. (练习“不看球”吊球技术。)"
        ],
        "variations": [
             "Add a defensive player to pick up the dump. (增加一名防守球员练习救吊球。)"
        ],
        "coaching_tips": [
             "Make it look like a real set until the very last millisecond. (在最后一毫秒前都要做得像真的传球。)"
        ]
    },
    "diving-defense-and-recovery": {
        "title": "Diving Defense & Recovery (鱼跃防守与快速恢复)",
        "description": "Mastering safe floor movement and quick reset to return to the play. (掌握安全的地板移动和快速重置，以便重回比赛回合。)",
        "setup": {
            "players": "Defenders (防守者)",
            "court": "Back row (后排)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Dive for a low ball, then immediately roll or push up to base position. (鱼跃接一个低球，然后立即滚翻或撑起回到基础位。)",
            "Check for second ball readiness. (检查对第二个球的准备情况。)"
        ],
        "variations": [
             "High-repetition 'suicide' drills for endurance. (高强度“自杀式”耐力训练。)"
        ],
        "coaching_tips": [
             "Leading hand should be flat. (领头手手心应保持平整。)"
        ]
    },
    "outside-hitter-off-speed-shots": {
        "title": "OH Off-Speed Shots (主攻手变线与轻吊练习)",
        "description": "Developing variety in scoring tools beyond just power hitting. (在强力进攻之外，开发更多样化的得分手段。)",
        "setup": {
            "players": "Outside hitters (主攻手)",
            "court": "Left side (左侧)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Approach like a hard spike, but use a roll shot or tip last second. (助跑像重扣一样，但在最后一秒改为抹球或吊球。)",
            "Target the deep corners or short 'donut' area. (瞄准深底角或浅区的“甜甜圈”空白地带。)"
        ],
        "variations": [
            "Coach calls the shot type mid-air. (教练在空中指令进攻类型。)"
        ],
        "coaching_tips": [
            "Maintain approach speed; don't slow down for a tip. (保持助跑速度，不要因为要吊球就减速。)"
        ]
    },
    "over-the-net-pepper-drill": {
        "title": "Over the Net Pepper (隔网对练)",
        "description": "Small side control across the net to improve ball awareness. (隔着球网的小组控球训练，以提高球感意识。)",
        "setup": {
            "players": "2-3 players on each side (每侧2-3名球员)",
            "court": "Net (网口)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Keep the ball active across the net using only pass, set, and down hits. (仅用垫、传、下击球动作保持球隔网连续运行。)"
        ],
        "variations": [
             "No jumping allowed to focus on control. (不允许起跳，以专注于控球。)"
        ],
        "coaching_tips": [
             "Keep the ball high to allow partner time. (垫高球给搭档留出反应时间。)"
        ]
    },
    "4-x-2-pepper-drill": {
        "title": "4x2 Pepper (4x2 对练挑战)",
        "description": "Advanced pepper involving more movement and specific transition roles. (涉及更多位移和特定转换角色的高级对练。)",
        "setup": {
            "players": "Groups of 6 (6人一组)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Setters and hitters work in a 4-on-2 setup to maintain a continuous loop. (二传和扣球手在4对2的阵型中配合，保持连续循环。)"
        ],
        "variations": [
            "Switch the '2' side positions every 2 minutes. (每2分钟更换“2人侧”的站位。)"
        ],
        "coaching_tips": [
            "Communication is key for the 4-person side. (4人侧的沟通是成功的关键。)"
        ]
    },
    "back-row-attacking-drill": {
        "title": "Back Row Attack Control (后排进攻控球强化)",
        "description": "Refining deep attacks and consistency from behind the 3-meter line. (精炼三米线后发起的深区进攻及其稳定性。)",
        "setup": {
            "players": "Back row hitters (后排扣球手)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Repeated attacks from back positions to deep diagonal corners. (在后排对深对角位进行重复进攻练习。)"
        ],
        "variations": [
            "Target 'seams' between hypothetical defenders. (瞄准假设防守者间的“接缝区”。)"
        ],
        "coaching_tips": [
            "Maintain a high elbow throughout the swing. (挥臂过程中始终保持高肘位。)"
        ]
    },
    "volleyball-back-row-attack-ping-pong": {
        "title": "Back Row Attack Ping Pong (后排进攻乒乓赛)",
        "description": "Competitive drill focusing on back row offense and transition. (侧重于后排进攻与转换的竞赛练习。)",
        "setup": {
            "players": "Teams of 3-6 (3-6人组队)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Play out points where only attacks from behind the 3-meter line are allowed. (进行比赛，规定仅允许三米线后的进攻。)",
            "The ball must stay in system to allow for the back row jump. (保持一传到位，为后排进攻创造条件。)"
        ],
        "variations": [
            "No tips allowed; power hits only. (不允许吊球，仅限重扣。)"
        ],
        "coaching_tips": [
            "Setters must push the ball deep enough for the back row approach. (二传必须将球传出足够的深度以配合后排助跑。)"
        ]
    },
    "serving-corner-killer-drill": {
        "title": "Serving Corner Killer (发球角隅杀手练习)",
        "description": "Precision serving targeting the difficult diagonal deep corners. (针对困难的对角深区角隅位置进行精准发球训练。)",
        "setup": {
            "players": "Servers (发球手)",
            "court": "Full court (全场)",
            "equipment": "Volleyballs, target mats (排球，目标垫)",
            "roles": ""
        },
        "steps": [
            "Attempt to land serves in the far corners of zones 1 and 5. (尝试将球发在1号位和5号位的远端角上。)",
            "Track hits vs. misses. (统计命中与失误次数。)"
        ],
        "variations": [
            "Timed pressure: 5 hits in 2 minutes. (限时压力：2分钟内击中5次。)"
        ],
        "coaching_tips": [
            "Aim for the corner shadow. (瞄准角落的阴影处发。)"
        ]
    },
    "offense-kill-drill": {
        "title": "Offense Kill Drill (进攻制胜抽球练习)",
        "description": "High-intensity hitting drill to finish points decisively. (旨在果断终结回合的高强度进攻训练。)",
        "setup": {
            "players": "Hitters, setters (扣球手，二传手)",
            "court": "Net (网口)",
            "equipment": "Ball cart (球筐)",
            "roles": ""
        },
        "steps": [
            "Attacker must 'kill' the ball into a specific zone to earn a point. (进攻者必须将球扣入特定区域“打死”得分。)",
            "Focus on aggressive swings and finding gaps. (专注于积极的挥臂并寻找防守空隙。)"
        ],
        "variations": [
            "Add a defender to block or dig. (增加一名防守者进行拦网或防起。)"
        ],
        "coaching_tips": [
            "Go for the line if the block is late. (若拦网未到位，果断打直线。)"
        ]
    },
    "setting-drill-triangle": {
        "title": "Triangle Setting (三角传球基础练习)",
        "description": "Fundamental passing drill in a triangle formation for better footwork. (在三角阵型中进行的基础传球练习，旨在改进步法。)",
        "setup": {
            "players": "Groups of 3 (3人一组)",
            "court": "Half court (半场)",
            "equipment": "1 ball per group (每组1球)",
            "roles": ""
        },
        "steps": [
            "Pass the ball in a continuous triangle pattern using only sets. (仅用传球方式，使球在三人间呈三角轨迹持续运行。)",
            "Emphasize squaring up to each target. (强调每一次传球都要正对目标。)"
        ],
        "variations": [
            "Change triangle direction. (变换三角流动方向。)"
        ],
        "coaching_tips": [
            "Feet should be set before the ball arrives. (来球前脚下应先站稳。)"
        ]
    },
    "line-hitting-drill": {
        "title": "Line Hitting (直线扣球专项训练)",
        "description": "Improving accuracy for the 'down the line' attack. (提高“打直线”进攻的精准度。)",
        "setup": {
            "players": "Hitters (扣球手)",
            "court": "Net (网口)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Attackers focus on hitting the sideline within the back 3 meters. (进攻者专注于击中底线往回3米内的边线范围。)"
        ],
        "variations": [
            "Include a blocker taking away the angle. (增加一名封锁斜线线路的拦网手。)"
        ],
        "coaching_tips": [
            "Keep your shoulders square until the last moment. (肩膀始终保持平正，直到最后一刻再转体。)"
        ]
    },
    "setting-and-overhead-passing-warm-up": {
        "title": "Overhead Passing Warm-up (上手传球热身)",
        "description": "General warm-up for hand contact and movement. (针对触球手感和移动的综合性热身练习。)",
        "setup": {
            "players": "Pairs or small groups (对练或小组)",
            "court": "Any (任意位置)",
            "equipment": "Volleyballs (排球)",
            "roles": ""
        },
        "steps": [
            "Continuous overhead passing with various heights. (利用不同高度进行连续上手传球。)"
        ],
        "variations": [
            "Sit on the floor to focus on hands only. (坐在地板上练习，以专注于手部技术。)"
        ],
        "coaching_tips": [
            "Keep hands in a 'window' shape. (手部保持“窗口”形状。)"
        ]
    },
    "volleyball-3v3-drill-reading-the-block": {
        "title": "3v3 Reading the Block (3对3：阅读拦网挑战)",
        "description": "Small-sided game where attackers must find holes in the block. (小场比赛，进攻者必须在拦网中寻找破绽。)",
        "setup": {
            "players": "Groups of 3 (3人一组)",
            "court": "Small court (小场)",
            "equipment": "Volleyballs, net (排球，球网)",
            "roles": ""
        },
        "steps": [
            "Players compete 3-on-3; emphasis is on offensive decision making against a blocker. (进行3对3比赛；重心在于面对拦网手时的进攻决策。)"
        ],
        "variations": [
            "Limit touches to 2. (限定为两次触球。)"
        ],
        "coaching_tips": [
            "See the block with your peripheral vision. (用余光观察拦网位置。)"
        ]
    },
    "double-block-attacking-drill": {
        "title": "Double Block Attacking (面对双人拦网扣球练习)",
        "description": "Training hitters to score against a solid two-person wall. (训练扣球手在稳固的双人拦网墙面前得分。)",
        "setup": {
            "players": "Hitter, setter, 2 blockers (扣球手，二传手，2名拦网手)",
            "court": "Net (网口)",
            "equipment": "Ball cart (球筐)",
            "roles": ""
        },
        "steps": [
            "Blockers close the seam; hitter must wipe off the hands or find the gap. (拦网手并网封闭接缝；扣球手必须通过打手出界或寻找缝隙得分。)"
        ],
        "variations": [
            "Add a defender behind the block. (在拦网后增加一名防守者。)"
        ],
        "coaching_tips": [
            "High hands are better for wiping. (高手更利于制作打手出界。)"
        ]
    }
}

def clean_content(content):
    if isinstance(content, list):
        cleaned = []
        for s in content:
            # Remove breadcrumbs and meta-info from the site
            if any(x in s for x in ["Drills by Age", "Drills by Skill", "Roles:", "Court:", "Equipment:"]): 
                continue
            # Filter out very short strings unless they look like translations
            if len(s.strip()) < 10 and not any(zh in s for zh in ["(", ")"]): 
                continue
            cleaned.append(s.strip())
        return cleaned
    return content

# Category ID mapping based on volleyballxpert.com
CATEGORY_ID_MAP = {
    'Warm-Up': 'phase:热身',
    'Ball Control': 'key:ball control',
    'Blocking': 'Blocking',
    'Defense': 'Defense',
    'Down Balls': 'key:down ball',
    'Hitting': 'Hitting',
    'Middle Hitter': 'key:middle',
    'Offense': 'key:attack',
    'Outside Hitter': 'key:hitter',
    'Passing': 'Passing',
    'Pass-Set-Hit': 'key:trans',
    'Pepper': 'key:pepper',
    'Serve Defense': 'key:receive',
    'Serving': 'key:serve',
    'Setting': 'Setting',
    'Fitness': 'phase:体能'
}

def main():
    if not INPUT_FILE.exists(): return
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        drills = json.load(f)

    processed_drills = []
    for drill in drills:
        slug = drill.get("slug", "")
        trans = TRANSLATIONS.get(slug, {})
        
        trans_setup = trans.get("setup", {})
        raw_setup = drill.get("setup", {})
        
        d = {
            "id": slug,
            "title": trans.get("title", drill.get("title", "")),
            "description": trans.get("description", drill.get("description", "")),
            "categories": [], # Will be populated
            "phase": "技术", 
            "ageGroup": [],
            "image": f"/images/drills/{slug}.png",
            "setup": {
                "players": trans_setup.get("players", raw_setup.get("players", "")),
                "court": trans_setup.get("court", raw_setup.get("court", "")),
                "equipment": trans_setup.get("equipment", raw_setup.get("equipment", "")),
                "roles": trans_setup.get("roles", raw_setup.get("roles", ""))
            },
            "steps": clean_content(trans.get("steps", drill.get("steps", []))),
            "variations": clean_content(trans.get("variations", drill.get("variations", []))),
            "coachingTips": clean_content(trans.get("coaching_tips", drill.get("coaching_tips", [])))
        }
        
        # Extract Categories from raw steps (which contains breadcrumbs)
        raw_steps = drill.get("steps", [])
        raw_cat_str = next((s for s in raw_steps if "Drills by Skill" in s), "")
        
        drill_cats = []
        if raw_cat_str:
            for site_name, target_id in CATEGORY_ID_MAP.items():
                if site_name in raw_cat_str:
                    drill_cats.append(target_id)
        
        # Fallback to keyword matching if breadcrumb extraction failed
        if not drill_cats:
            t = (d["title"] + " " + slug).lower()
            if any(w in t for w in ["pass", "dig", "receive"]): drill_cats.append("Passing")
            if any(w in t for w in ["serve"]): drill_cats.append("key:serve")
            if any(w in t for w in ["set", "overhead"]): drill_cats.append("Setting")
            if any(w in t for w in ["hit", "attack", "kill", "spike"]): drill_cats.append("Hitting")
            if any(w in t for w in ["defen", "dig"]): drill_cats.append("Defense")
            if any(w in t for w in ["block"]): drill_cats.append("Blocking")
        
        d["categories"] = drill_cats
        
        # Set primary phase based on priority
        if "phase:热身" in drill_cats: d["phase"] = "热身"
        elif "phase:体能" in drill_cats: d["phase"] = "体能"
        elif any(w in (d["title"] + slug).lower() for w in ["game", "play", "match", "scrimmage", "wash"]): d["phase"] = "实战"

        d["ageGroup"] = drill.get("age_groups", ["All"])
        processed_drills.append(d)

    ts_header = """import { Drill, SkillCategory, AgeLevel } from './types';

export const SKILL_CATEGORIES: SkillCategory[] = [
  { id: 'all', name: '所有类别', icon: 'Layout' },
  { id: 'Passing', name: '垫球/接发', icon: 'MousePointer2' },
  { id: 'Setting', name: '传球', icon: 'Target' },
  { id: 'Hitting', name: '扣球/进攻', icon: 'Zap' },
  { id: 'Serving', name: '发球', icon: 'Wind' },
  { id: 'Blocking', name: '拦网', icon: 'Shield' },
  { id: 'Defense', name: '防守', icon: 'Sword' },
  { id: 'Other', name: '其他', icon: 'MoreHorizontal' }
];

export const AGE_LEVELS: AgeLevel[] = [
  { id: 'Under 8', name: '8岁以下' },
  { id: '8 to 11', name: '8-11岁' },
  { id: '12 to 14', name: '12-14岁' },
  { id: '15 to 18', name: '15-18岁' },
  { id: 'All', name: '所有年龄' }
];

export const DRILLS_DATA: Drill[] = """

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(ts_header + json.dumps(processed_drills, ensure_ascii=False, indent=2) + ";")
    print(f"Generated {OUTPUT_FILE} with {len(processed_drills)} drills.")

if __name__ == "__main__":
    main()
