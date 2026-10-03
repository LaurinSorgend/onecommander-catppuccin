"""Catppuccin palettes and per-flavor derived values for the OneCommander theme generator."""

NAMES = ["rosewater", "flamingo", "pink", "mauve", "red", "maroon", "peach", "yellow",
         "green", "teal", "sky", "sapphire", "blue", "lavender", "text", "subtext1",
         "subtext0", "overlay2", "overlay1", "overlay0", "surface2", "surface1",
         "surface0", "base", "mantle", "crust"]

RAW = {
    "Latte": "dc8a78 dd7878 ea76cb 8839ef d20f39 e64553 fe640b df8e1d 40a02b 179299 04a5e5 "
             "209fb5 1e66f5 7287fd 4c4f69 5c5f77 6c6f85 7c7f93 8c8fa1 9ca0b0 acb0be bcc0cc "
             "ccd0da eff1f5 e6e9ef dce0e8",
    "Frappe": "f2d5cf eebebe f4b8e4 ca9ee6 e78284 ea999c ef9f76 e5c890 a6d189 81c8be 99d1db "
              "85c1dc 8caaee babbf1 c6d0f5 b5bfe2 a5adce 949cbb 838ba7 737994 626880 51576d "
              "414559 303446 292c3c 232634",
    "Macchiato": "f4dbd6 f0c6c6 f5bde6 c6a0f6 ed8796 ee99a0 f5a97f eed49f a6da95 8bd5ca 91d7e3 "
                 "7dc4e4 8aadf4 b7bdf8 cad3f5 b8c0e0 a5adcb 939ab7 8087a2 6e738d 5b6078 494d64 "
                 "363a4f 24273a 1e2030 181926",
    "Mocha": "f5e0dc f2cdcd f5c2e7 cba6f7 f38ba8 eba0ac fab387 f9e2af a6e3a1 94e2d5 89dceb "
             "74c7ec 89b4fa b4befe cdd6f4 bac2de a6adc8 9399b2 7f849c 6c7086 585b70 45475a "
             "313244 1e1e2e 181825 11111b",
}

PALETTES = {flavor: dict(zip(NAMES, ("#" + h for h in hexes.split())))
            for flavor, hexes in RAW.items()}

DISPLAY_NAMES = {"Latte": "Latte", "Frappe": "Frappé", "Macchiato": "Macchiato", "Mocha": "Mocha"}

# Alpha (hex byte) used when tinting fills with an accent over the panel background.
# Latte needs lighter tints so that Text stays above 4.5:1 on top of them.
TINTS = {
    "Latte":     {"select": "33", "select_hover": "4D", "message": "33", "todo": "73", "todo_done": "59"},
    "Frappe":    {"select": "40", "select_hover": "4D", "message": "40", "todo": "CC", "todo_done": "CC"},
    "Macchiato": {"select": "40", "select_hover": "59", "message": "4D", "todo": "CC", "todo_done": "CC"},
    "Mocha":     {"select": "40", "select_hover": "59", "message": "4D", "todo": "CC", "todo_done": "CC"},
}


def derived(flavor):
    """Return the role-to-color mapping for one flavor (on top of the raw palette)."""
    p = PALETTES[flavor]
    t = TINTS[flavor]
    light = flavor == "Latte"
    return {
        **p,
        "mode": "Light" if light else "Dark",
        "display": DISPLAY_NAMES[flavor],
        "acrylic": "#D6" + p["crust"][1:],
        "text_overlay": "#BE" + p["base"][1:],
        "folder_selected_bg": "#B0" + p["base"][1:],
        "zebra": "#80" + p["mantle"][1:],
        "select": f"#{t['select']}{p['blue'][1:]}",
        "select_hover": f"#{t['select_hover']}{p['blue'][1:]}",
        "msg_success": f"#{t['message']}{p['green'][1:]}",
        "msg_error": f"#{t['message']}{p['red'][1:]}",
        "todo": f"#{t['todo']}{p['yellow'][1:]}",
        "todo_done": f"#{t['todo_done']}{p['green'][1:]}",
        "todo_fg": p["text"] if light else p["base"],
        "scroll_track": "#80" + p["mantle"][1:],
        "shadow_edge": "#44" + (p["overlay2"] if light else p["crust"])[1:],
        "shadow_clear": "#00" + (p["overlay2"] if light else p["crust"])[1:],
        "text_secondary": p["subtext1"] if light else p["subtext0"],
        "tooltip": p["surface0"] if light else p["surface1"],
        "scroll_thumb": p["overlay2"] if light else p["overlay1"],
        "scroll_thumb_hover": p["subtext0"] if light else p["overlay2"],
        "scroll_thumb_pressed": p["subtext1"] if light else p["subtext0"],
        "button_hover": p["crust"] if light else p["surface0"],
        "button_pressed": p["surface0"] if light else p["surface1"],
        "caret": p["text"] if light else p["rosewater"],
    }
