import reflex as rx

config = rx.Config(
    app_name="reflex_charts_demo",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        # Explicit since Reflex 0.9: the demo uses Radix Themes components
        # (rx.card, rx.heading, ...), so enable the bundle deliberately.
        rx.plugins.RadixThemesPlugin(),
    ],
)
