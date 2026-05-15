import re

filepath = "app/src/main/java/com/brouken/player/PlayerActivity.kt"

with open(filepath, "r") as f:
    content = f.read()

# Define the custom feature
custom_code = """
    // --- CUSTOM CHAPTER MARKERS ---
    private fun injectChapters() {
        val timeBar = findViewById<androidx.media3.ui.DefaultTimeBar>(androidx.media3.ui.R.id.exo_progress)
        player?.addListener(object : androidx.media3.common.Player.Listener {
            override fun onTimelineChanged(timeline: androidx.media3.common.Timeline, reason: Int) {
                if (timeline.isEmpty) return
                val window = androidx.media3.common.Timeline.Window()
                player?.let { activePlayer ->
                    timeline.getWindow(activePlayer.currentMediaItemIndex, window)
                    val chapterTimesList = mutableListOf<Long>()
                    for (i in 0 until timeline.periodCount) {
                        val period = androidx.media3.common.Timeline.Period()
                        timeline.getPeriod(i, period)
                        if (period.positionInWindowMs > 0) {
                            chapterTimesList.add(period.positionInWindowMs)
                        }
                    }
                    if (chapterTimesList.isNotEmpty()) {
                        val adGroupTimesMs = chapterTimesList.toLongArray()
                        val playedAdGroups = BooleanArray(adGroupTimesMs.size) { false } 
                        timeBar?.setAdGroupTimesMs(adGroupTimesMs, playedAdGroups, adGroupTimesMs.size)
                    }
                }
            }
        })
    }
"""

# Inject the function exactly before the last closing bracket of the class
content = re.sub(r'}(?=\s*$)', custom_code + '\n}', content)

# Inject the function call right into onStart() so it actually runs
content = content.replace("override fun onStart() {", "override fun onStart() {\n        injectChapters()")

with open(filepath, "w") as f:
    f.write(content)

print("✅ Code injected perfectly inside the class!")
