# Custom themes

`classic-wata.json` is the "Classic v1 (WATA)" layout running on an unmodified
upstream build (checked against v2.20.0):

- thin elapsed-time bars under the 5-hour and weekly usage bars
- a 7-segment weekly bar with the Fable weekly limit underneath
  (`claude.model.fable.*`)
- usage lines with the percent padded to two digits and the reset countdown
  rounded up (`61m` reads `1.1h`, so the real time left is never longer than shown)

## Install

1. Copy `classic-wata.json` to `%APPDATA%\ClaudeCodeUsageMonitor\themes`.
2. Pick **Classic v1 (WATA)** under **Settings > Appearance > Active theme**.

## Regenerate

`convert_theme.py` rebuilds it from the fork's original theme on the `v2`
branch; see the docstring for the commands.
