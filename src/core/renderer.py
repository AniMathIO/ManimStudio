from ffmpeg import FFmpeg
import os

from src.utils.logger_utility import logger


@logger.catch
def create_low_quality_version(input_path, output_dir):
    if not input_path or not output_dir:
        logger.error("Invalid input or output directory.")
        return None  # Or handle the error as appropriate for your application

    output_path = os.path.join(output_dir, ".cache", os.path.basename(input_path))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    ffmpeg = (
        FFmpeg()
        .option("y")  # Overwrite output files without asking
        .input(input_path)
        .output(output_path, vcodec="libx264", crf=28, acodec="aac", vf="scale=640:-1")
    )

    ffmpeg.execute()

    return output_path
