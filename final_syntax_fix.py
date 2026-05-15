import os

# 1. Find the real Java file dynamically
filepath = os.popen('find app -name "PlayerActivity.java" | head -n 1').read().strip()

if not filepath:
    print("❌ Could not find PlayerActivity.java!")
    exit(1)

with open(filepath, "r") as f:
    content = f.read()

# 2. Fix the Variable Names (The log says symbol 'mPlayer' is missing)
# We replace our previous 'mPlayer' with the 'player' variable the app actually uses
content = content.replace("mPlayer != null", "player != null")
content = content.replace("mPlayer.addListener", "player.addListener")
content = content.replace("mPlayer.getCurrentMediaItemIndex()", "player.getCurrentMediaItemIndex()")

# 3. Fix Java Getters (Java needs .getPositionInWindowMs() not .positionInWindowMs)
content = content.replace("period.positionInWindowMs", "period.getPositionInWindowMs()")

with open(filepath, "w") as f:
    f.write(content)

print("✅ Syntax corrected: 'mPlayer' -> 'player' and property access -> method calls.")
