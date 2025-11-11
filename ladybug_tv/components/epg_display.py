"""EPG display components"""
import reflex as rx

def epg_current_program(program: dict) -> rx.Component:
    """Display current program info"""
    return rx.box(
        rx.vstack(
            rx.text(program.get("title", ""), font_weight="bold", font_size="1.2em"),
            rx.text(program.get("description", ""), color="gray"),
            rx.text(
                f"{program.get('start_time', '')} - {program.get('end_time', '')}",
                font_size="0.9em",
            ),
            align_items="start",
        ),
        padding="20px",
    )
