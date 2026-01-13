This code in this repo has been generated using Google's Gemini CLI (plain Gemini 2.5). The first commit is the result of invoking two prompts to Gemini
> write a python program which reads mp3 files from a specified directory and analyzes their metadata for bad music tags
...lots of CLI output on the way to a result

> ok, now extend the script to include FLAC files as well as MP3 files
...lots more CLI output

# Music Tag Analyzer

This Python script recursively scans a specified directory for MP3 and FLAC files and analyzes their metadata to find common problems like missing tags, generic placeholders, or formatting issues.

## Features

-   Recursively scans a directory for `.mp3` and `.flac` files.
-   Checks for missing essential tags (`artist`, `title`, `album`).
-   Identifies generic and placeholder tags (e.g., "Unknown Artist", "Track 01").
-   Detects tags with unnecessary leading or trailing whitespace.
-   Reports a clear list of files with issues and what those issues are.
-   Provides a final summary of the scan.

## Setup

1.  **Install Dependencies:** Before running the script, you need to install the necessary Python library. A `requirements.txt` file is provided. The `mutagen` library handles both MP3 and FLAC formats.

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the script** from your terminal, providing the path to the directory you want to analyze as an argument.

    ```bash
    python analyze_music.py /path/to/your/music
    ```

    Replace `/path/to/your/music` with the actual path to your music folder.

### Example

```bash
$ python analyze_music.py ./my_music_collection

Scanning for MP3 and FLAC files in './my_music_collection'...

--- ISSUES FOUND in: collection/some_band/track01.mp3 ---
  - Missing tag: 'album'
  - Generic title found: 'Track 01'

--- ISSUES FOUND in: collection/another_band/song.flac ---
  - Missing tag: 'artist'

--- ISSUES FOUND in: downloads/new_song.mp3 ---
  - Tag 'artist' has leading or trailing whitespace.

--- Analysis Complete ---
Total files scanned: 92
Files with issues:   3
-------------------------
```
