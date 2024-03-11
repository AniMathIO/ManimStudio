from ffmpeg import FFmpeg
import os

from src.utils.logger_utility import logger


@logger.catch
def create_low_quality_version(input_path, output_dir):
    if not os.path.isfile(input_path):
        logger.error(f"Input file '{input_path}' does not exist.")
        return None

    output_path = os.path.join(output_dir, ".cache", os.path.basename(input_path))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    ffmpeg = FFmpeg().option("y")  # Overwrite output files without asking

    # Get the file extension to determine the file type
    _, file_extension = os.path.splitext(input_path)
    file_extension = file_extension.lower()

    # Set compression options based on the file type
    if file_extension in [".mp4", ".mov", ".avi", ".mkv"]:  # Video files
        ffmpeg = ffmpeg.input(input_path).output(
            output_path, vcodec="libx264", crf=28, acodec="aac", vf="scale=640:-1"
        )
    elif file_extension in [".mp3", ".wav", ".flac"]:  # Audio files
        ffmpeg = ffmpeg.input(input_path).output(output_path, acodec="aac", ab="128k")
    elif file_extension in [".jpg", ".png", ".bmp", ".gif"]:  # Image files
        ffmpeg = ffmpeg.input(input_path).output(
            output_path, vframes=1, filter_complex="scale=640:-1"
        )
    else:
        logger.error(f"Unsupported file type: {file_extension}")
        return None

    try:
        ffmpeg.execute()
        logger.info(f"Created low-quality version: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Error creating low-quality version: {e}")
        return None
