"""FFmpeg transcoding wrapper"""
import subprocess

class Transcoder:
    """FFmpeg wrapper for stream transcoding"""
    
    def __init__(self, ffmpeg_path: str = "/usr/bin/ffmpeg"):
        self.ffmpeg_path = ffmpeg_path
    
    def transcode_to_hls(self, input_url: str, output_path: str):
        """Transcode stream to HLS format"""
        # TODO: Implement FFmpeg transcoding
        pass
