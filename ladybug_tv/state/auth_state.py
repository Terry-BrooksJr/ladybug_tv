"""Authentication state"""
import reflex as rx

class AuthState(rx.State):
    """Handle user authentication"""
    
    is_authenticated: bool = False
    user_email: str = ""
    access_token: str = ""
    
    def login(self, email: str, password: str):
        """Login user"""
        # TODO: Implement login
        pass
    
    def logout(self):
        """Logout user"""
        self.is_authenticated = False
        self.user_email = ""
        self.access_token = ""
