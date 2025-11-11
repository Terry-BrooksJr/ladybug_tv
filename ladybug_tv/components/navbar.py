"""Navigation bar component"""
import reflex as rx

def navbar() -> rx.Component:
    """Top navigation bar"""
    return rx.hstack(
        rx.heading("🐞 Ladybug TV", size="lg"),
        rx.spacer(),
        rx.button("Settings"),
        padding="20px",
        border_bottom="1px solid #e0e0e0",
        width="100%",
    )
