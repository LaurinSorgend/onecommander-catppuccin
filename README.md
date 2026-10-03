# Catppuccin for One Commander

[Catppuccin](https://github.com/catppuccin/catppuccin) themes for the One Commander file manager, in all four flavors: Latte (light), Frappé, Macchiato and Mocha.

## Install

Copy the folders in `themes/` into One Commander's theme folder (About > Settings location, usually `%LOCALAPPDATA%\OneCommander\Themes`) and pick the theme in settings.

### Icons

`icons/` has file and folder icon packs converted from [catppuccin/vscode-icons](https://github.com/catppuccin/vscode-icons). Copy `icons/FileIcons/*` and `icons/FolderIcons/*` into the matching folders under `%LOCALAPPDATA%\OneCommander\Resources`, then pick them in Settings > Theme. Restart One Commander from the tray icon if they don't show up.

One Commander matches file icons by extension only. VS Code rules for exact filenames like `package.json` or `Dockerfile` are dropped. Dotfiles such as `.gitignore` still work.


## Regenerating

The XAML files are generated. Don't edit them by hand.

- `generator/palettes.py` has the four palettes and the role mapping (which color goes where).
- `generator/template.xaml` is the theme with `@role@` placeholders.
- `python generator/contrast.py` checks contrast for every flavor.
- `python generator/generate.py` writes `themes/`, including the thumbnails. It needs Pillow and compares keys against the bundled `Dark` theme in your One Commander install.

- `python generator/icons.py` clones catppuccin/vscode-icons into `generator/.cache/` and writes `icons/`. It needs PyMuPDF.

The thumbnails are schematic drawings, not screenshots.
