import os

# Dynamically find the real Java file
filepath = os.popen('find app -name "PlayerActivity.java" | head -n 1').read().strip()

if not filepath:
    print("❌ Could not find PlayerActivity.java!")
    exit(1)

with open(filepath, "r") as f:
    lines = f.readlines()

custom_func = """
    // --- KHALID'S CUSTOM CHAPTER MARKERS ---
    private void addKhalidChapterMarkers() {
        try {
            final androidx.media3.ui.DefaultTimeBar timeBar = findViewById(androidx.media3.ui.R.id.exo_progress);
            if (mPlayer != null && timeBar != null) {
                mPlayer.addListener(new androidx.media3.common.Player.Listener() {
                    @Override
                    public void onTimelineChanged(androidx.media3.common.Timeline timeline, int reason) {
                        if (timeline.isEmpty()) return;
                        androidx.media3.common.Timeline.Window window = new androidx.media3.common.Timeline.Window();
                        timeline.getWindow(mPlayer.getCurrentMediaItemIndex(), window);
                        
                        java.util.ArrayList<Long> chapters = new java.util.ArrayList<>();
                        for (int i = 0; i < timeline.getPeriodCount(); i++) {
                            androidx.media3.common.Timeline.Period period = new androidx.media3.common.Timeline.Period();
                            timeline.getPeriod(i, period);
                            if (period.positionInWindowMs > 0L) chapters.add(period.positionInWindowMs);
                        }
                        if (!chapters.isEmpty()) {
                            long[] adTimes = new long[chapters.size()];
                            boolean[] playedAds = new boolean[chapters.size()];
                            for (int i = 0; i < chapters.size(); i++) {
                                adTimes[i] = chapters.get(i);
                                playedAds[i] = false;
                            }
                            timeBar.setAdGroupTimesMs(adTimes, playedAds, adTimes.length);
                        }
                    }
                });
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
"""

# Inject the function call into the Android onResume lifecycle
for i, line in enumerate(lines):
    if "super.onResume();" in line or "super.onStart();" in line:
        lines[i] = line + "        addKhalidChapterMarkers();\n"
        break

# Inject the actual function right before the final closing bracket of the class
for i in range(len(lines)-1, -1, -1):
    if lines[i].strip() == '}':
        lines.insert(i, custom_func)
        break

with open(filepath, "w") as f:
    f.writelines(lines)

print("✅ Found the real Java file and injected the code!")
