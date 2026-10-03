"""WCAG contrast checks for the foreground/background pairs the theme actually uses."""
from palettes import PALETTES, derived


def rgb(color, under=None):
    """Parse #RRGGBB or #AARRGGBB, compositing alpha over `under` when given."""
    h = color.lstrip("#")
    if len(h) == 8:
        alpha = int(h[:2], 16) / 255
        top = [int(h[i:i + 2], 16) for i in (2, 4, 6)]
        bottom = rgb(under)
        return [round(a * alpha + b * (1 - alpha)) for a, b in zip(top, bottom)]
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def luminance(c):
    def channel(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(v) for v in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg, bg):
    a, b = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def pairs(d):
    """(label, fg, bg-or-tint, under, minimum) tuples."""
    return [
        ("Text on Base", d["text"], d["base"], None, 4.5),
        ("Text on Crust", d["text"], d["crust"], None, 4.5),
        ("Mauve (important) on Base", d["mauve"], d["base"], None, 4.5),
        ("Secondary text on Base", d["text_secondary"], d["base"], None, 4.5),
        ("Subtext1 (group title) on Mantle", d["subtext1"], d["mantle"], None, 4.5),
        ("Text on selection", d["text"], d["select"], d["base"], 4.5),
        ("Text on selection hover", d["text"], d["select_hover"], d["base"], 4.5),
        ("Text on hover Surface0", d["text"], d["surface0"], None, 4.5),
        ("Text on tooltip", d["text"], d["tooltip"], None, 4.5),
        ("Text on button hover", d["text"], d["button_hover"], None, 4.5),
        ("Text on button pressed", d["text"], d["button_pressed"], None, 4.5),
        ("Text on success msg", d["text"], d["msg_success"], d["mantle"], 4.5),
        ("Text on error msg", d["text"], d["msg_error"], d["mantle"], 4.5),
        ("ToDo fg on ToDo", d["todo_fg"], d["todo"], d["base"], 4.5),
        ("ToDo fg on ToDo done", d["todo_fg"], d["todo_done"], d["base"], 4.5),
        ("Blue accent edge vs Base", d["blue"], d["base"], None, 3.0),
        ("Scroll thumb vs Base", d["scroll_thumb"], d["base"], None, 3.0),
        ("Caret vs Surface0", d["caret"], d["surface0"], None, 3.0),
    ]


if __name__ == "__main__":
    failures = 0
    for flavor in PALETTES:
        d = derived(flavor)
        print(f"== {flavor}")
        for label, fg, bg, under, minimum in pairs(d):
            r = ratio(rgb(fg), rgb(bg, under))
            ok = r >= minimum
            failures += not ok
            print(f"  {'ok  ' if ok else 'FAIL'} {r:5.2f} (>= {minimum}) {label}")
    print("failures:", failures)
