import os
from pydub import AudioSegment

SUPPORTED_AUDIO = {"mp3", "wav", "mp4"}  # mp4 is audio-only

def convert_audio(input_file: str, output_file: str):
    """
    Convert input_file to output_file (mp3, wav, mp4 audio-only)
    """
    out_ext = os.path.splitext(output_file)[1][1:].lower()

    if out_ext not in SUPPORTED_AUDIO:
        raise ValueError(f"Unsupported output format: {out_ext}")

    # force mp4 as audio-only (AAC inside MP4 container)
    export_format = "mp4" if out_ext == "mp4" else out_ext

    try:
        audio = AudioSegment.from_file(input_file)
        audio.export(output_file, format=export_format)
        print(f"✅ Converted: {input_file} -> {output_file}")
        return output_file
    except Exception as e:
        print(f"❌ Error converting file: {e}")
        return None
