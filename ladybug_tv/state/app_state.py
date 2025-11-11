"""Main application state"""
import reflex as rx

class IPTVState(rx.State):
    """Main IPTV application state"""
    
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
    
    def toggle_sidebar(self):
        """Toggle sidebar visibility"""
        self.sidebar_open = not self.sidebar_open
    
    def load_channels(self):
        """Fetch available channels from API"""
        self.is_loading = True
        # TODO: Implement API call
        self.is_loading = False
    
    def play_channel(self, channel_id: str):
        """Switch to a different channel"""
        # TODO: Implement channel switching
        pass
    
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
