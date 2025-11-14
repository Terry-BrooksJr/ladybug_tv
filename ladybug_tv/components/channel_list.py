"""Channel list component"""

import reflex as rx


def channel_list_item(channel: dict) -> rx.Component:
    """Individual channel in the list"""
    return rx.hstack(
        rx.image(
            src=channel.get("logo", ""),
            width="40px",
            height="40px",
            border_radius="4px",
        ),
        rx.vstack(
            rx.text(channel.get("name", ""), font_weight="bold"),
            rx.text(channel.get("category", ""), font_size="0.8em", color="gray"),
            align_items="start",
            spacing="0",
        ),
        padding="10px",
        border_bottom="1px solid #e0e0e0",
        cursor="pointer",
        _hover={"background": "#f5f5f5"},
    )
