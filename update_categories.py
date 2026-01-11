import json
import re

# Precise mapping from site categories to my internal IDs
ID_MAP = {
    "warm-up": "phase:热身",
    "ball-control": "key:ball control",
    "blocking": "Blocking",
    "defense": "Defense",
    "down-balls": "key:down ball",
    "hitting": "Hitting",
    "middle-hitter": "key:middle",
    "offense": "key:attack",
    "outside-hitter": "key:hitter",
    "passing": "Passing",
    "pass-set-hit": "key:trans",
    "pepper": "key:pepper",
    "serve-defense": "key:receive",
    "serving": "key:serve",
    "setting": "Setting",
    "fitness": "phase:体能"
}

# The mapping data from browser subagent
CATEGORY_DATA = {
  "warm-up": ["perfect-passes", "passing-technique-warm-up", "passing-pass-and-move", "pass-and-weave", "two-way-pepper", "cross-court-pepper", "ball-control-25-contact-drill", "ball-control-with-back-row-attacks", "tag-team-warm-up", "back-row-running-warmup", "volleyball-partner-pass-and-down-balls", "free-ball-transition-and-catch", "volleyball-24-touches-ball-control", "volleyball-footwork-drill", "4-x-2-pepper-drill", "3-skill-pepper-with-partner", "warm-up-with-wall", "middle-back-defensive-positioning-and-movement", "partner-forearm-passing-drill", "volleyball-corner-serving-drill", "individual-setting-drill", "individual-forearm-passing-drill", "line-setting-drill", "volleyball-passing-run-through-and-short-pass", "serving-with-partner", "circle-passing-drill", "3-player-down-ball-with-movement", "volleyball-ball-control-with-movement", "long-distance-back-setting-drill", "volleyball-2-player-pepper-drill-multiple-hits", "volleyball-set-and-switch-drill", "volleyball-pass-and-move-with-simulated-blocks", "volleyball-serving-drill-ten-zones", "cross-court-setting-drill", "over-the-net-pepper-drill", "setting-and-overhead-passing-warm-up"],
  "ball-control": ["passing-middle-or-lateral", "perfect-passes", "serving-bombs-away", "lateral-passing-3-touch", "serve-receive-with-2-servers", "passing-out-of-the-net", "defense-4-corner-pit", "defense-touch-ten", "passing-pass-and-move", "pass-and-weave", "run-the-middle", "no-easy-points-serve-receive", "serve-receive-lines", "two-way-pepper", "cross-court-pepper", "ball-control-25-contact-drill", "ball-control-with-back-row-attacks", "blocking-net-decision", "tag-team-warm-up", "back-row-running-warmup", "sideout-or-lose", "endurance-hitting-drill", "-volleyball-hitting-bucket-ball", "short-serve-competition", "vollebyball-jump-serve-updown", "individual-serving-relay", "down-ball-challenge", "volleyball-partner-pass-and-down-balls", "volleyball-serving-around-the-world", "volleyball-passing-free-balls-to-setter", "free-ball-transition-and-catch", "volleyball-24-touches-ball-control", "ball-control-pass-set-downball", "volleyball-ball-control-two-person-four-square", "volleyball-ball-control-elimination", "volleyball-back-row-attack-ping-pong", "quick-setter-transitioning-drill", "serve-receive-transition-to-hitting-drill", "rapid-pass-set-drill", "net-save-drill", "12-ball-wash-drill", "4-x-2-pepper-drill", "set-and-switch", "set-and-spin", "3-skill-pepper-with-partner", "setters-vs-passers-game", "double-the-number", "warm-up-with-wall", "setting-game", "3-and-over", "partner-setting-and-overhead-passing-drill", "partner-forearm-passing-drill", "individual-setting-drill", "individual-forearm-passing-drill", "line-setting-drill", "volleyball-passing-run-through-and-short-pass", "serving-to-21", "circle-passing-drill", "2-player-down-volleyball-passing-drill", "3-player-down-ball-with-movement", "volleyball-ball-control-with-movement", "long-distance-back-setting-drill", "volleyball-2-player-pepper-drill-multiple-hits", "volleyball-set-and-switch-drill", "volleyball-pass-and-move-with-simulated-blocks", "w-passing-drill", "triangle-pepper-drill-over-the-net", "setting-drill-setting-after-a-bad-pass", "cross-court-setting-drill", "line-hitting-drill", "setting-drill-triangle", "over-the-net-pepper-drill", "setting-and-overhead-passing-warm-up"],
  "blocking": ["hitting-drill-turn-go-hit", "run-the-middle", "no-easy-points-serve-receive", "blocking-net-decision", "back-row-running-warmup", "offense-vs-blockers", "endurance-hitting-drill", "double-block-attacking-drill", "volleyball-footwork-drill", "coverage-drill", "blocking-form-drill", "volleyball-3v3-drill-reading-the-block", "volleyball-pass-and-move-with-simulated-blocks"],
  "defense": ["perfect-passes", "hitting-drill-turn-go-hit", "lateral-passing-3-touch", "serve-receive-with-2-servers", "defense-4-corner-pit", "defense-touch-ten", "no-easy-points-serve-receive", "serve-receive-lines", "two-way-pepper", "ball-control-25-contact-drill", "blocking-net-decision", "tag-team-warm-up", "back-row-running-warmup", "sideout-or-lose", "reverse-sideout-game", "offense-vs-blockers", "offense-kill-drill", "double-block-attacking-drill", "volleyball-defense-touch-ten", "volleyball-passing-free-balls-to-setter", "free-ball-pass-set-cover-and-catch", "free-ball-transition-and-catch", "volleyball-24-touches-ball-control", "volleyball-ball-control-two-person-four-square", "volleyball-ball-control-elimination", "volleyball-back-row-attack-ping-pong", "back-row-attacking-drill", "net-save-drill", "volleyball-double-serving-game", "coverage-drill", "12-ball-wash-drill", "middle-back-defensive-positioning-and-movement", "volleyball-3v3-drill-reading-the-block"],
  "down-balls": ["two-way-pepper", "cross-court-pepper", "ball-control-25-contact-drill", "ball-control-with-back-row-attacks", "tag-team-warm-up", "back-row-running-warmup", "down-ball-challenge", "volleyball-partner-pass-and-down-balls", "volleyball-24-touches-ball-control", "ball-control-pass-set-downball", "volleyball-ball-control-two-person-four-square", "volleyball-ball-control-elimination", "12-ball-wash-drill", "4-x-2-pepper-drill", "3-skill-pepper-with-partner", "warm-up-with-wall", "3-player-down-ball-with-movement", "volleyball-2-player-pepper-drill-multiple-hits"],
  "hitting": ["hitting-drill-turn-go-hit", "defense-touch-ten", "run-the-middle", "no-easy-points-serve-receive", "ball-control-25-contact-drill", "ball-control-with-back-row-attacks", "back-row-running-warmup", "sideout-or-lose", "reverse-sideout-game", "offense-vs-blockers", "offense-kill-drill", "endurance-hitting-drill", "-volleyball-hitting-bucket-ball", "vollebyball-jump-serve-updown", "down-ball-challenge", "double-block-attacking-drill", "volleyball-defense-touch-ten", "volleyball-passing-free-balls-to-setter", "free-ball-pass-set-cover-and-catch", "volleyball-24-touches-ball-control", "ball-control-pass-set-downball", "volleyball-ball-control-two-person-four-square", "volleyball-ball-control-elimination", "volleyball-back-row-attack-ping-pong", "back-row-attacking-drill", "quick-setter-transitioning-drill", "serve-receive-transition-to-hitting-drill", "volleyball-double-serving-game", "coverage-drill", "12-ball-wash-drill", "volleyball-3v3-drill-reading-the-block", "3-player-down-ball-with-movement", "volleyball-ball-control-with-movement", "volleyball-2-player-pepper-drill-multiple-hits", "triangle-pepper-drill-over-the-net", "line-hitting-drill", "over-the-net-pepper-drill"],
  "middle-hitter": ["defense-touch-ten", "run-the-middle", "no-easy-points-serve-receive", "offense-vs-blockers", "offense-kill-drill", "volleyball-defense-touch-ten", "volleyball-footwork-drill", "serve-receive-transition-to-hitting-drill"],
  "offense": ["hitting-drill-turn-go-hit", "defense-touch-ten", "serve-receive-lines", "ball-control-25-contact-drill", "tag-team-warm-up", "back-row-running-warmup", "sideout-or-lose", "reverse-sideout-game", "offense-vs-blockers", "offense-kill-drill", "-volleyball-hitting-bucket-ball", "double-block-attacking-drill", "volleyball-passing-free-balls-to-setter", "free-ball-pass-set-cover-and-catch", "volleyball-24-touches-ball-control", "ball-control-pass-set-downball", "volleyball-ball-control-two-person-four-square", "volleyball-ball-control-elimination", "volleyball-back-row-attack-ping-pong", "back-row-attacking-drill", "volleyball-double-serving-game", "12-ball-wash-drill", "volleyball-3v3-drill-reading-the-block", "volleyball-corner-serving-drill", "triangle-pepper-drill-over-the-net", "setting-drill-setting-after-a-bad-pass", "line-hitting-drill"],
  "outside-hitter": ["hitting-drill-turn-go-hit", "defense-touch-ten", "no-easy-points-serve-receive", "ball-control-25-contact-drill", "offense-vs-blockers", "offense-kill-drill", "endurance-hitting-drill", "-volleyball-hitting-bucket-ball", "volleyball-defense-touch-ten", "volleyball-passing-free-balls-to-setter", "volleyball-24-touches-ball-control", "quick-setter-transitioning-drill", "serve-receive-transition-to-hitting-drill", "volleyball-3v3-drill-reading-the-block", "3-player-down-ball-with-movement", "line-hitting-drill"],
  "passing": ["passing-middle-or-lateral", "perfect-passes", "hitting-drill-turn-go-hit", "lateral-passing-3-touch", "serve-receive-with-2-servers", "passing-technique-warm-up", "passing-out-of-the-net", "defense-4-corner-pit", "defense-touch-ten", "passing-pass-and-move", "pass-and-weave", "run-the-middle", "no-easy-points-serve-receive", "serve-receive-lines", "two-way-pepper", "cross-court-pepper", "ball-control-25-contact-drill", "ball-control-with-back-row-attacks", "tag-team-warm-up", "back-row-running-warmup", "sideout-or-lose", "reverse-sideout-game", "offense-vs-blockers", "offense-kill-drill", "endurance-hitting-drill", "-volleyball-hitting-bucket-ball", "down-ball-challenge", "volleyball-partner-pass-and-down-balls", "double-block-attacking-drill", "volleyball-defense-touch-ten", "volleyball-passing-free-balls-to-setter", "free-ball-pass-set-cover-and-catch", "free-ball-transition-and-catch", "volleyball-24-touches-ball-control", "ball-control-pass-set-downball", "volleyball-ball-control-two-person-four-square", "volleyball-ball-control-elimination", "volleyball-back-row-attack-ping-pong", "back-row-attacking-drill", "quick-setter-transitioning-drill", "serve-receive-transition-to-hitting-drill", "rapid-pass-set-drill", "net-save-drill", "volleyball-double-serving-game", "12-ball-wash-drill", "4-x-2-pepper-drill", "setters-vs-passers-game", "double-the-number", "warm-up-with-wall", "3-and-over", "middle-back-defensive-positioning-and-movement", "volleyball-3v3-drill-reading-the-block", "partner-forearm-passing-drill", "individual-setting-drill", "individual-forearm-passing-drill", "volleyball-passing-run-through-and-short-pass", "circle-passing-drill", "2-player-down-volleyball-passing-drill", "3-player-down-ball-with-movement", "volleyball-ball-control-with-movement", "volleyball-2-player-pepper-drill-multiple-hits", "volleyball-pass-and-move-with-simulated-blocks", "w-passing-drill", "triangle-pepper-drill-over-the-net", "setting-drill-setting-after-a-bad-pass", "line-hitting-drill", "setting-drill-triangle", "over-the-net-pepper-drill", "setting-and-overhead-passing-warm-up"],
  "pass-set-hit": ["run-the-middle", "no-easy-points-serve-receive", "two-way-pepper", "ball-control-25-contact-drill", "ball-control-with-back-row-attacks", "tag-team-warm-up", "back-row-running-warmup", "sideout-or-lose", "reverse-sideout-game", "volleyball-24-touches-ball-control", "ball-control-pass-set-downball", "volleyball-ball-control-two-person-four-square", "volleyball-ball-control-elimination", "volleyball-back-row-attack-ping-pong", "back-row-attacking-drill", "12-ball-wash-drill", "3-skill-pepper-with-partner", "volleyball-3v3-drill-reading-the-block", "3-player-down-ball-with-movement", "triangle-pepper-drill-over-the-net", "line-hitting-drill"],
  "pepper": ["two-way-pepper", "4-x-2-pepper-drill", "volleyball-2-player-pepper-drill-multiple-hits", "triangle-pepper-drill-over-the-net", "over-the-net-pepper-drill"],
  "serve-defense": ["passing-middle-or-lateral", "serving-bombs-away", "serve-receive-with-2-servers", "run-the-middle", "no-easy-points-serve-receive", "serve-receive-lines", "sideout-or-lose", "reverse-sideout-game", "-volleyball-hitting-bucket-ball", "double-block-attacking-drill", "volleyball-back-row-attack-ping-pong", "serve-receive-transition-to-hitting-drill", "volleyball-double-serving-game", "12-ball-wash-drill"],
  "serving": ["passing-middle-or-lateral", "serving-bombs-away", "serve-receive-with-2-servers", "run-the-middle", "no-easy-points-serve-receive", "serve-receive-lines", "sideout-or-lose", "reverse-sideout-game", "-volleyball-hitting-bucket-ball", "short-serve-competition", "vollebyball-jump-serve-updown", "individual-serving-relay", "double-block-attacking-drill", "volleyball-serving-around-the-world", "volleyball-serving-relay", "volleyball-ball-control-two-person-four-square", "volleyball-back-row-attack-ping-pong", "quick-setter-transitioning-drill", "serve-receive-transition-to-hitting-drill", "volleyball-double-serving-game", "serving-corner-killer-drill", "12-ball-wash-drill", "warm-up-with-wall", "volleyball-corner-serving-drill", "serving-with-partner", "serving-to-21", "volleyball-serving-drill-ten-zones"],
  "setting": ["defense-touch-ten", "run-the-middle", "no-easy-points-serve-receive", "two-way-pepper", "cross-court-pepper", "ball-control-25-contact-drill", "ball-control-with-back-row-attacks", "tag-team-warm-up", "back-row-running-warmup", "sideout-or-lose", "reverse-sideout-game", "offense-vs-blockers", "offense-kill-drill", "down-ball-challenge", "double-block-attacking-drill", "volleyball-defense-touch-ten", "volleyball-passing-free-balls-to-setter", "free-ball-pass-set-cover-and-catch", "volleyball-24-touches-ball-control", "ball-control-pass-set-downball", "volleyball-ball-control-two-person-four-square", "volleyball-ball-control-elimination", "volleyball-back-row-attack-ping-pong", "back-row-attacking-drill", "quick-setter-transitioning-drill", "serve-receive-transition-to-hitting-drill", "rapid-pass-set-drill", "net-save-drill", "volleyball-double-serving-game", "12-ball-wash-drill", "4-x-2-pepper-drill", "set-and-switch", "set-and-spin", "setters-vs-passers-game", "double-the-number", "warm-up-with-wall", "setting-game", "3-and-over", "partner-setting-and-overhead-passing-drill", "volleyball-3v3-drill-reading-the-block", "individual-setting-drill", "line-setting-drill", "circle-passing-drill", "2-player-down-volleyball-passing-drill", "3-player-down-ball-with-movement", "volleyball-ball-control-with-movement", "long-distance-back-setting-drill", "volleyball-2-player-pepper-drill-multiple-hits", "volleyball-set-and-switch-drill", "w-passing-drill", "triangle-pepper-drill-over-the-net", "cross-court-setting-drill", "line-hitting-drill", "setting-drill-triangle", "setting-and-overhead-passing-warm-up"],
  "fitness": ["pass-and-weave", "tag-team-warm-up", "back-row-running-warmup", "endurance-hitting-drill", "individual-serving-relay", "middle-back-defensive-positioning-and-movement", "volleyball-ball-control-with-movement", "volleyball-pass-and-move-with-simulated-blocks", "setting-and-overhead-passing-warm-up"]
}

def update():
    # Read the current data/drills.js
    with open('data/drills.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # Extract the array part
    match = re.search(r'=\s*(\[.*\]);', js_content, re.DOTALL)
    if not match:
        print("Could not find array in drills.js")
        return
    
    drills = json.loads(match.group(1))
    
    # Update each drill
    for drill in drills:
        slug = drill['id']
        new_cats = []
        for site_cat, slugs in CATEGORY_DATA.items():
            if slug in slugs:
                new_cats.append(ID_MAP[site_cat])
        
        # Merge or replace. Since ground truth from site is better, we replace.
        # But we also keep existing automated categorization as fallback if empty
        if not new_cats:
            # Fallback keyword logic
            t = (drill['title'] + drill['id']).lower()
            if 'pass' in t: new_cats.append('Passing')
            if 'serve' in t: new_cats.append('key:serve')
            if 'hit' in t: new_cats.append('Hitting')
        
        drill['categories'] = sorted(list(set(new_cats)))
        
        # Primary category/phase update if needed
        if 'phase:热身' in drill['categories']: drill['phase'] = '热身'
        elif 'phase:体能' in drill['categories']: drill['phase'] = '体能'
    
    # Re-write the file
    new_json = json.dumps(drills, ensure_ascii=False, indent=2)
    new_content = re.sub(r'=\s*\[.*\];', f'= {new_json};', js_content, flags=re.DOTALL)
    
    with open('data/drills.js', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Updated {len(drills)} drills with precise site categories.")

if __name__ == "__main__":
    update()
