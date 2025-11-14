"""Settings page"""

import reflex as rx


def settings() -> rx.Component:
    """Settings page"""
    return rx.box(
        rx.heading("Settings"),
        rx.text("Settings page coming soon..."),
        padding="20px",
    )
