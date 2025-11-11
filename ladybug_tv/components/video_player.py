"""Custom HLS video player component"""
import reflex as rx

class VideoPlayer(rx.Component):
    """Custom HLS video player component"""
    
    library = "video.js"
    tag = "VideoPlayer"
    
    # Props
    stream_url: rx.Var[str]
    autoplay: rx.Var[bool] = False
    controls: rx.Var[bool] = True


def video_player(**props) -> rx.Component:
    """Video player component"""
    return VideoPlayer.create(**props)
