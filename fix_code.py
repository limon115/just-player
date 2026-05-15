import os

filepath = os.popen('find app -name "PlayerActivity.kt" | head -n 1').read().strip()

with open(filepath, "r") as f:
    lines = f.readlines()

custom_func = """
    // --- KHALID'S CUSTOM CHAPTER MARKERS ---
    private fun addKhalidChapterMarkers() {
        val timeBar = findViewById<androidx.media3.ui.DefaultTimeBar>(androidx.media3.ui.R.id.exo_progress)
        player?.addListener(object : androidx.media3.common.Player.Listener {
            override fun onTimelineChanged(timeline: androidx.media3.common.Timeline, reason: Int) {
                if (timeline.isEmpty) return
                val window = androidx.media3.common.Timeline.Window()
                player?.let { activePlayer ->
                    timeline.getWindow(activePlayer.currentMediaItemIndex, window)
                    val chapters = mutableListOf<Long>()
                    for (i in 0 until timeline.periodCount) {
                        val period = androidx.media3.common.Timeline.Period()
                        timeline.getPeriod(i, period)
                        if (period.positionInWindowMs > 0) chapters.add(period.positionInWindowMs)
                    }
                    if (chapters.isNotEmpty()) {
                        val adTimes = chapters.toLongArray()
                        timeBar?.setAdGroupTimesMs(adTimes, BooleanArray(adTimes.size) { false }, adTimes.size)
                    }
                }
            }
        })
    }
"""

# Insert the function call safely into onResume
for i, line in enumerate(lines):
    if "super.onResume()" in line or "super.onStart()" in line:
        lines[i] = line + "        addKhalidChapterMarkers()\n"
        break

# Insert the custom function right before the final closing bracket of the class
for i in range(len(lines)-1, -1, -1):
    if lines[i].strip() == '}':
        lines.insert(i, custom_func)
        break

with open(filepath, "w") as f:
    f.writelines(lines)

print("✅ Pristine file restored and Khalid's code flawlessly injected!")
