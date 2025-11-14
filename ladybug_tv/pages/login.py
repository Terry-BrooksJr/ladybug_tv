"""Login page"""

import reflex as rx


def login() -> rx.Component:
    """Login page"""
    return rx.center(
        rx.vstack(
            rx.heading("Login to Ladybug TV", size="lg"),
            rx.input(placeholder="Email"),
            rx.input(placeholder="Password", type="password"),
            rx.button("Login"),
            spacing="4",
        ),
        height="100vh",
    )
