import os
import sys
import subprocess
from pydub import AudioSegment


def remove_drums(input_mp3):
    # Get the absolute path to the input file
    input_path = os.path.abspath(input_mp3)
    print(f"Using input file: {input_path}")

    # Create the output folder
    output_dir = "output"

    # Run Spleeter
    command = [
        "spleeter", "separate",  # No '-i' needed anymore
        input_path,  # Just give the file name directly
        "-p", "spleeter:5stems",
        "-o", output_dir
    ]
    subprocess.run(command)

    # Create the folder path where stems are saved
    song_name = os.path.splitext(os.path.basename(input_mp3))[0]
    stems_path = os.path.join(output_dir, song_name)

    print(f"Looking for stems in: {stems_path}")

    # Ensure the folder exists
    if not os.path.exists(stems_path):
        print(f"Error: Folder '{stems_path}' not found!")
        return

    # Load stems (ensure these files exist)
    try:
        vocals = AudioSegment.from_wav(os.path.join(stems_path, "vocals.wav"))
        bass = AudioSegment.from_wav(os.path.join(stems_path, "bass.wav"))
        piano = AudioSegment.from_wav(os.path.join(stems_path, "piano.wav"))
        other = AudioSegment.from_wav(os.path.join(stems_path, "other.wav"))
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        return

    # Mix the stems (without drums)
    print("Mixing stems...")
    no_drums = vocals.overlay(bass).overlay(piano).overlay(other)

    # Export the new song (without drums)
    output_file = f"{song_name}_no_drums.mp3"
    print(f"Exporting to {output_file}...")
    no_drums.export(output_file, format="mp3")
    print("✅ Done!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python remove_drums.py your_song.mp3")
    else:
        remove_drums(sys.argv[1])

    # print("Enter song")
    # song = input()
    #
    # remove_drums(song)
