// Custom visual chapter markers via ExoPlayer AdGroup API
val timeBar = findViewById<androidx.media3.ui.DefaultTimeBar>(androidx.media3.ui.R.id.exo_progress)

mPlayer?.addListener(object : androidx.media3.common.Player.Listener {
    override fun onTimelineChanged(timeline: androidx.media3.common.Timeline, reason: Int) {
        if (timeline.isEmpty) return
        
        val window = androidx.media3.common.Timeline.Window()
        timeline.getWindow(mPlayer!!.currentMediaItemIndex, window)
        
        val chapterTimesList = mutableListOf<Long>()
        
        // Extract chapter positions
        for (i in 0 until timeline.periodCount) {
            val period = androidx.media3.common.Timeline.Period()
            timeline.getPeriod(i, period)
            if (period.positionInWindowMs > 0) {
                chapterTimesList.add(period.positionInWindowMs)
            }
        }

        // Push chapter markers to the TimeBar
        if (chapterTimesList.isNotEmpty()) {
            val adGroupTimesMs = chapterTimesList.toLongArray()
            val playedAdGroups = BooleanArray(adGroupTimesMs.size) { false } 
            timeBar?.setAdGroupTimesMs(adGroupTimesMs, playedAdGroups, adGroupTimesMs.size)
        }
    }
})

