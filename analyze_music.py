import argparse
import os
import re
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from mutagen.flac import FLAC

def analyze_audio_file(file_path):
    """
    Analyzes a single audio file for common metadata issues.

    Args:
        file_path (str): The full path to the audio file.

    Returns:
        list: A list of strings, where each string is a description of an issue found.
              Returns an empty list if no issues are found.
    """
    issues = []
    file_lower = file_path.lower()
    
    try:
        if file_lower.endswith('.mp3'):
            audio = EasyID3(file_path)
        elif file_lower.endswith('.flac'):
            audio = FLAC(file_path)
        else:
            # This case should not be reached if called from find_audio_files
            return []
    except ID3NoHeaderError:
        issues.append("File does not contain any ID3 metadata tags.")
        return issues
    except Exception as e:
        issues.append(f"Could not process file. Error: {e}")
        return issues

    # --- Define checks for bad tags ---

    # 1. Check for missing essential tags
    essential_tags = ['artist', 'title', 'album']
    for tag in essential_tags:
        if tag not in audio or not audio[tag][0].strip():
            issues.append(f"Missing tag: '{tag}'")

    # 2. Check for generic placeholder content
    generic_patterns = {
        'artist': ['unknown artist'],
        'album': ['unknown album'],
        'title': ['untitled']
    }
    for tag, patterns in generic_patterns.items():
        if tag in audio:
            for pattern in patterns:
                if pattern in audio[tag][0].lower():
                    issues.append(f"Generic tag found: '{tag}: {audio[tag][0]}'")

    # 3. Check for titles like "Track 01", "Track 2", etc.
    if 'title' in audio:
        title = audio['title'][0].strip()
        if re.match(r'^track\s*\d+', title, re.IGNORECASE):
            issues.append(f"Generic title found: '{title}'")

    # 4. Check for tags with leading/trailing whitespace
    for tag in audio.keys():
        if isinstance(audio[tag][0], str) and audio[tag][0].strip() != audio[tag][0]:
            issues.append(f"Tag '{tag}' has leading or trailing whitespace.")
            
    # 5. Check for tracknumber and discnumber being 0
    for tag in ['tracknumber', 'discnumber']:
        if tag in audio and audio[tag][0] in ('0', '0/0'):
             issues.append(f"Tag '{tag}' is zero ('{audio[tag][0]}')")


    return issues

def find_audio_files(directory):
    """
    Recursively finds all MP3 and FLAC files in a given directory.

    Args:
        directory (str): The directory to search.

    Returns:
        list: A list of file paths for all found audio files.
    """
    audio_files = []
    supported_extensions = ('.mp3', '.flac')
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(supported_extensions):
                audio_files.append(os.path.join(root, file))
    return audio_files

def main():
    """
    Main function to parse arguments and drive the analysis.
    """
    parser = argparse.ArgumentParser(
        description="Analyze MP3 and FLAC files in a directory for bad or missing metadata tags.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "directory",
        help="The path to the directory containing your music files."
    )
    args = parser.parse_args()

    music_directory = args.directory
    if not os.path.isdir(music_directory):
        print(f"Error: Directory not found at '{music_directory}'")
        return

    print(f"Scanning for MP3 and FLAC files in '{music_directory}'...\n")
    audio_files = find_audio_files(music_directory)

    if not audio_files:
        print("No MP3 or FLAC files found.")
        return

    files_with_issues = 0
    total_files_scanned = len(audio_files)

    for file_path in audio_files:
        issues = analyze_audio_file(file_path)
        if issues:
            files_with_issues += 1
            # Use relative path for cleaner output
            relative_path = os.path.relpath(file_path, music_directory)
            print(f"--- ISSUES FOUND in: {relative_path} ---")
            for issue in issues:
                print(f"  - {issue}")
            print("") # Newline for readability

    # --- Print Summary ---
    print("--- Analysis Complete ---")
    print(f"Total files scanned: {total_files_scanned}")
    print(f"Files with issues:   {files_with_issues}")
    print("-------------------------")

if __name__ == "__main__":
    main()
