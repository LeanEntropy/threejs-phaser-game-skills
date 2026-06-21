# Playtest QA Checklist

- Start from a clean load.
- Play through the main loop for at least 2 minutes.
- Verify controls, camera (follow/zoom/bounds), objective feedback, failure/retry, and progression.
- Try rapid input changes and edge movement against world bounds (`setCollideWorldBounds`).
- Trigger collisions/overlaps from multiple angles.
- Pause, restart, resize, and refocus the tab if supported.
- Check audio unlock and volume behavior after the first gesture (web audio unlock on first input).
- Watch for unreadable moments, camera framing issues, jitter, and missed feedback.
- Capture screenshots for desktop and mobile.
- Record bugs as reproduction steps with expected and actual behavior.
