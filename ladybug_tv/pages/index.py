"""Main TV viewer page"""
import reflex as rx
from ladybug_tv.components.navbar import navbar
from ladybug_tv.components.video_player import video_player
from ladybug_tv.components.channel_list import channel_list_item
from ladybug_tv.state.app_state import IPTVState

def sidebar() -> rx.Component:
    """Channel list sidebar"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading("Channels", size="md"),
                rx.spacer(),
                rx.icon(
                    tag="menu",
                    on_click=IPTVState.toggle_sidebar,
                    cursor="pointer",
                ),
                width="100%",
            ),
            rx.input(
                placeholder="Search channels...",
                on_change=IPTVState.search_channels,
                width="100%",
            ),
            rx.box(
                rx.foreach(
                    IPTVState.filtered_channels,
                    channel_list_item,
                ),
                overflow_y="auto",
                height="calc(100vh - 150px)",
            ),
            spacing="4",
            padding="20px",
        ),
        width="300px",
        height="100vh",
        background="white",
        border_right="1px solid #e0e0e0",
        display=rx.cond(IPTVState.sidebar_open, "block", "none"),
    )

def video_area() -> rx.Component:
    """Main video player area"""
    return rx.vstack(
        rx.box(
            video_player(
                stream_url=IPTVState.current_stream_url,
                autoplay=True,
                controls=True,
            ),
            width="100%",
            height="60vh",
            background="black",
        ),
        rx.box(
            rx.text("Video Player Area"),
            padding="20px",
        ),
        width="100%",
    )

def index() -> rx.Component:
    """Main TV viewer page"""
    return rx.box(
        navbar(),
        rx.hstack(
            sidebar(),
            video_area(),
            spacing="0",
            width="100%",
        ),
        width="100%",
    )
