# 🔖 Readeck Backup to HTML

This script generates Netscape HTML bookmarks files from [Readeck](https://readeck.org) backups, for easy sharing with browsers or other bookmarking/read-it-later applications. Supports multiple users and retains link titles, tags, and (optionally) descriptions.

## Dependencies

- [Python 3.x](https://www.python.org)

## Installation

Simply clone the repository:

```bash
git clone https://github.com/lilacpixel/readeck-backup-to-html.git
cd ./readeck-backup-to-html
```

## Usage

[Back up your Readeck installation](https://readeck.org/en/docs/backups) from the command line:

```bash
readeck export -config /path/to/config.toml export.zip
```

Run the script with the path to your export file, plus any additional arguments (see [Optional arguments](#optional-arguments)):

```bash
./readeck-backup-to-html.py /path/to/export.zip
```

Bookmarks files will be saved to the current working directory. If a bookmarks file exists with the filename to be written, you'll be prompted to confirm before overwriting.

### Optional arguments

- **-d** or **--descriptions** - Retain descriptions from Readeck in your HTML bookmarks files. Can be omitted if your destination application generates its own descriptions.

## Licensing

This tool is licensed under GNU GPLv3. Full licensing information can be found in [LICENSE](LICENSE).
