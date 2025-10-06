import os
import yt_dlp
import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")

def download_youtube(url: str, output_dir: str = "outputs", output_format: str = "mp4"):
    """
    Download YouTube video as audio-only.
    Supported output formats: mp3, wav, mp4 (audio-only)
    Returns the full path to the downloaded file.
    """
    os.makedirs(output_dir, exist_ok=True)

    # yt-dlp options
    ydl_opts = {
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "format": "bestaudio[ext=m4a]/bestaudio/best",  # audio-only
        "keepvideo": True,  # keep the downloaded file after audio extraction
        "postprocessors": []
    }

    # Set postprocessor based on desired output
    if output_format in ["mp3", "wav"]:
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": output_format,
            "preferredquality": "192" if output_format == "mp3" else None
        }]
    elif output_format == "mp4":
        # mp4 as audio-only (AAC inside MP4 container)
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "aac",
            "preferredquality": "192"
        }]
    else:
        raise ValueError(f"Unsupported output format: {output_format}")

    logging.info(f"Downloading YouTube URL: {url} as {output_format}")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        # filename returned by yt-dlp
        filename = ydl.prepare_filename(info)

        # Determine actual extracted file
        if output_format == "mp4":
            # rename .m4a or .aac to .mp4
            base, ext = os.path.splitext(filename)
            if ext.lower() not in [".mp4"]:
                new_filename = base + ".mp4"
                if os.path.exists(filename):
                    os.rename(filename, new_filename)
                filename = new_filename
        else:
            # mp3 or wav
            base, _ = os.path.splitext(filename)
            filename = base + f".{output_format}"

    logging.info(f"Download complete: {filename}")
    return filename
