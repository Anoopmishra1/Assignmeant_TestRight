# PROMPT_LOG.md — AI Interaction Documentation

## Section 3: AI-Assisted Charting

### Initial Prompt to the AI

> "Write a Python script that loads a JSON file (`output.json`) containing device telemetry
> summaries (device_id as keys, each with `avg_temperature`, `total_records`, and
> `error_count`) and generates a bar chart comparing the average temperature per device
> using matplotlib. Save the chart as `chart.png`."

### Bug / Formatting Issue in First Attempt

The AI's initial output had **overlapping value labels** on top of the bars. It placed the
temperature text directly at the bar height using `bar.get_height()` without adding any
vertical offset, causing the label to sit **on the edge** of the bar rather than above it.
Additionally, the y-axis limit was not adjusted, so the topmost label was **clipped
outside the visible chart area**.

```python
# Bug: label sits on the bar edge and gets clipped
ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
        f"{temp}°C", ha="center", va="bottom")
```

### Follow-up Prompt to Fix

> "The temperature labels on top of the bars are overlapping with the bar edges and the
> top label is getting clipped. Add a vertical offset of +1.0 to the label position, and
> increase the y-axis upper limit by 15 units above the max temperature so labels have
> breathing room. Also add `bbox_inches='tight'` to `savefig()` to prevent clipping."

### Result After Fix

The labels now float cleanly above each bar with proper spacing, and the chart renders
without any clipping. The final version also includes:
- Color-coded bars (green < 50°C, orange < 70°C, red ≥ 70°C)
- Error count labels inside each bar
- Grid lines and clean spine styling
