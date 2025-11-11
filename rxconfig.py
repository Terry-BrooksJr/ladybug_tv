import reflex as rx

config = rx.Config(
    app_name="ladybug_tv",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)