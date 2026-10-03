# Catppuccin for One Commander

[Catppuccin](https://github.com/catppuccin/catppuccin) themes for the One Commander file manager, in all four flavors: Latte (light), Frappé, Macchiato and Mocha.

## Install

Copy the folders in `themes/` into One Commander's theme folder (About > Settings location, usually `%LOCALAPPDATA%\OneCommander\Themes`) and pick the theme in settings.


## Regenerating

The XAML files are generated. Don't edit them by hand.

- `generator/palettes.py` has the four palettes and the role mapping (which color goes where).
- `generator/template.xaml` is the theme with `@role@` placeholders.
- `python generator/contrast.py` checks contrast for every flavor.
- `python generator/generate.py` writes `themes/`, including the thumbnails. It needs Pillow and compares keys against the bundled `Dark` theme in your One Commander install.

The thumbnails are schematic drawings, not screenshots.
