"""Convert the fork's "Classic v1 (WATA)" theme so it runs on upstream builds.

Upstream lacks the fork's `usage_line_precise` format (percent padded to two
digits, countdown rounded up) and the `weekly_scoped` bindings. Both are
re-expressed with upstream's own theme expressions and bindings.

The source theme lives on the `v2` branch at src/themes/classic-wata.json:

    git show v2:src/themes/classic-wata.json > classic-wata.v2.json
    python convert_theme.py classic-wata.v2.json classic-wata.json
"""
import json
import re
import sys

src, dst = sys.argv[1], sys.argv[2]


def precise_line(base: str) -> str:
    provider = base.split(".")[0]
    ok = f"(!data.loading && !data.has_error && (!data.poll_ok || {provider}.available))"
    has_reset = f"({ok} && {base}.reset.unix > 0)"
    c = f"ceil({base}.reset.seconds)"
    # Tenths of a day or an hour, rounded up.
    tenths = f"if({c} >= 86400, ceil({c} / 8640), ceil({c} / 360))"
    unit = (
        f"if({c} >= 86400, i18n.day_suffix, if({c} >= 3600, i18n.hour_suffix, "
        f"if({c} >= 60, i18n.minute_suffix, if({c} > 0, i18n.second_suffix, i18n.now))))"
    )
    tokens = [
        f'{{if(data.loading, "--", if({ok}, "", "!"))}}',
        f'{{if({ok} && round({base}.display) < 10, "0", "")}}',
        f'{{if({ok}, {base}.display, ""):0}}',
        f'{{if({ok}, "%", "")}}',
        f'{{if({has_reset}, " · ", "")}}',
        f'{{if({has_reset} && {c} > 0, if({c} >= 3600, floor({tenths} / 10), '
        f'if({c} >= 60, ceil({c} / 60), {c})), ""):0}}',
        f'{{if({has_reset} && {c} >= 3600, ".", "")}}',
        f'{{if({has_reset} && {c} >= 3600, {tenths} - floor({tenths} / 10) * 10, ""):0}}',
        f'{{if({has_reset}, {unit}, "")}}',
    ]
    return "".join(tokens)


text = open(src, encoding="utf-8").read()
theme = json.loads(text)
theme["id"] = "classic-wata-upstream"
theme["name"] = "Classic v1 (WATA)"

counts = {"precise": 0, "scoped": 0}


def walk(node):
    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(value, str):
                new, n = re.subn(
                    r"\{([a-z_]+\.[a-z_]+)\.display:usage_line_precise\}",
                    lambda m: precise_line(m.group(1)),
                    value,
                )
                counts["precise"] += n
                if "weekly_scoped." in new:
                    counts["scoped"] += new.count("weekly_scoped.")
                    new = new.replace("claude.weekly_scoped.", "claude.model.fable.")
                node[key] = new
            else:
                walk(value)
    elif isinstance(node, list):
        for item in node:
            walk(item)


walk(theme)
leftover = [s for s in ("usage_line_precise", "duration_ceil", "weekly_scoped") if s in json.dumps(theme)]
print(counts, "leftover:", leftover)
json.dump(theme, open(dst, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
