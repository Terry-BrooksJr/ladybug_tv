import reflex as rx
import httpx
from typing import Any, Dict, List


class LadybugTVState(rx.State):
    """Main application state"""

    # Current stream
    current_stream_url: str = ""
    current_channel: dict = {}

    # Channel list
    channels: list[dict] = []
    filtered_channels: list[dict] = []

    # EPG data
    current_program: dict = {}
    upcoming_programs: list[dict] = []

    # User state
    is_authenticated: bool = False
    favorites: list[str] = []

    # UI state
    is_loading: bool = False
    sidebar_open: bool = True

    # Computed vars for safe dictionary access
    @rx.var
    def current_channel_name(self) -> str:
        return self.current_channel.get("name", "No channel selected")

    @rx.var
    def current_program_title(self) -> str:
        return self.current_program.get("title", "No program info")

    @rx.var
    def current_program_description(self) -> str:
        return self.current_program.get("description", "")

    @rx.var
    def current_program_time(self) -> str:
        start = self.current_program.get("start_time", "")
        end = self.current_program.get("end_time", "")
        if start and end:
            return f"{start} - {end}"
        return ""

    @rx.var
    def has_stream(self) -> bool:
        """Return True when a stream URL is ready"""
        return bool(self.current_stream_url)
    
    def toggle_sidebar(self):
        """Toggle sidebar visibility"""
        self.sidebar_open = not self.sidebar_open

    def load_channels(self):
        """Fetch available channels from API"""
        self.is_loading = True
        # Call your FastAPI backend
        response = httpx.get("http://api:8000/channels")
        self.channels = response.json()
        self.filtered_channels = self.channels
        self.is_loading = False
    
    def play_channel(self, channel_id: str):
        """Switch to a different channel"""
        # Get stream URL from backend
        response = httpx.get(f"http://api:8000/stream/{channel_id}")
        self.current_stream_url = response.json()["stream_url"]
        self.current_channel = next(
            (ch for ch in self.channels if ch["id"] == channel_id), 
            {}
        )
        self.load_epg(channel_id)
    
    def load_epg(self, channel_id: str):
        """Load EPG data for current channel"""
        response = httpx.get(f"http://api:8000/epg/{channel_id}")
        epg_data = response.json()
        self.current_program = epg_data["current"]
        self.upcoming_programs = epg_data["upcoming"]
    
    def toggle_favorite(self, channel_id: str):
        """Add/remove channel from favorites"""
        if channel_id in self.favorites:
            self.favorites.remove(channel_id)
        else:
            self.favorites.append(channel_id)
    
    def search_channels(self, query: str):
        """Filter channels by search query"""
        if not query:
            self.filtered_channels = self.channels
        else:
            self.filtered_channels = [
                ch for ch in self.channels 
                if query.lower() in ch["name"].lower()
            ]

def channel_list_item(channel: dict) -> rx.Component:
    """Individual channel in the list"""
    return rx.hstack(
        rx.image(
            src=channel["logo"],
            width="40px",
            height="40px",
            border_radius="4px",
        ),
        rx.vstack(
            rx.text(channel["name"], font_weight="bold"),
            rx.text(channel["category"], font_size="0.8em", color="gray"),
            align_items="start",
            spacing="0",
        ),
        rx.spacer(),
        rx.icon(
            tag="star",
            color=rx.cond(
                LadybugTVState.favorites.contains(channel["id"]),
                "yellow",
                "gray"
            ),
            cursor="pointer",
            on_click=LadybugTVState.toggle_favorite(channel["id"]),
        ),
        padding="10px",
        border_bottom="1px solid #e0e0e0",
        cursor="pointer",
        on_click=LadybugTVState.play_channel(channel["id"]),
        _hover={"background": "#f5f5f5"},
    )

def sidebar() -> rx.Component:
    """Channel list sidebar"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading("Channels", size="7"),
                rx.spacer(),
                rx.icon(
                    tag="menu",
                    on_click=LadybugTVState.toggle_sidebar,
                    cursor="pointer",
                ),
                width="100%",
            ),
            rx.input(
                placeholder="Search channels...",
                on_change=LadybugTVState.search_channels,
                width="100%",
            ),
            rx.box(
                rx.foreach(
                    LadybugTVState.filtered_channels,
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
        display=rx.cond(LadybugTVState.sidebar_open, "block", "none"),
    )

def video_player() -> rx.Component:
    """Render the HTML5 video element or a placeholder when no channel is selected."""
    return rx.cond(
        LadybugTVState.has_stream,
        rx.video(
            src=LadybugTVState.current_stream_url,
            controls=True,
            auto_play=True,
            muted=True,
            plays_inline=True,
            style={
                "width": "100%",
                "height": "100%",
                "objectFit": "contain",
                "background": "black",
            },
        ),
        rx.center(
            rx.vstack(
                rx.icon(tag="tv", size=32, color="gray"),
                rx.text(
                    "Select a channel to begin watching",
                    color="gray",
                    font_size="1.1em",
                ),
                spacing="2",
            ),
            width="100%",
            height="100%",
            background="black",
        ),
    )

def video_area() -> rx.Component:
    """Main video player area"""
    return rx.vstack(
        # Video player
        rx.box(
            video_player(),
            width="100%",
            height="60vh",
            background="black",
        ),
        # Current program info
        rx.box(
            rx.hstack(
                rx.vstack(
                    rx.heading(
                        LadybugTVState.current_channel_name,
                        size="9",
                    ),
                    rx.text(
                        LadybugTVState.current_program_title,
                        font_size="1.2em",
                        font_weight="bold",
                    ),
                    rx.text(
                        LadybugTVState.current_program_description,
                        color="gray",
                    ),
                    align_items="start",
                ),
                rx.spacer(),
                rx.badge(
                    LadybugTVState.current_program_time,
                    color_scheme="blue",
                ),
                width="100%",
            ),
            padding="20px",
            border_bottom="1px solid #e0e0e0",
        ),
        # Upcoming programs
        rx.box(
            rx.heading("Up Next", size="3", margin_bottom="10px"),
            rx.foreach(
                LadybugTVState.upcoming_programs,
                lambda prog: rx.hstack(
                    rx.text(prog["start_time"], font_weight="bold", width="80px"),
                    rx.text(prog["title"]),
                    padding="10px",
                    border_bottom="1px solid #f0f0f0",
                ),
            ),
            padding="20px",
            overflow_y="auto",
        ),
        width="100%",
        spacing="0",
    )

def index() -> rx.Component:
    """Main app layout"""
    return rx.box(
        rx.hstack(
            sidebar(),
            video_area(),
            spacing="0",
            width="100%",
        ),
        width="100%",
        height="100vh",
    )

# Create app
app = rx.App()
app.add_page(index)
