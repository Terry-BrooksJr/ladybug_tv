"""Channel management state"""
import reflex as rx

class ChannelState(rx.State):
    """Manage channel operations"""
    
    selected_category: str = "All"
    categories: list[str] = ["All", "News", "Sports", "Entertainment", "Movies"]
    
    def filter_by_category(self, category: str):
        """Filter channels by category"""
        self.selected_category = category
        # TODO: Implement filtering logic
