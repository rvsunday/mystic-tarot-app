import flet as ft
import random
import asyncio

TAROT_DATA = [
    {"name": "The Fool", "meaning": "New beginnings and fresh opportunities.", "emoji": "🤹"},
    {"name": "The Magician", "meaning": "Manifestation and personal power.", "emoji": "🪄"},
    {"name": "The High Priestess", "meaning": "Intuition and hidden knowledge.", "emoji": "🌙"},
    {"name": "The Empress", "meaning": "Abundance and nurturing energy.", "emoji": "🌸"},
    {"name": "The Emperor", "meaning": "Authority and structure.", "emoji": "👑"},
    {"name": "The Lovers", "meaning": "Love and alignment.", "emoji": "❤️"},
    {"name": "The Chariot", "meaning": "Determination and victory.", "emoji": "🐎"},
    {"name": "Strength", "meaning": "Inner courage and patience.", "emoji": "🦁"},
    {"name": "The Hermit", "meaning": "Soul searching and wisdom.", "emoji": "🕯"},
    {"name": "Wheel of Fortune", "meaning": "Destiny and turning points.", "emoji": "🎡"},
    {"name": "Justice", "meaning": "Truth and fairness.", "emoji": "⚖️"},
    {"name": "Death", "meaning": "Transformation and rebirth.", "emoji": "💀"},
    {"name": "The Tower", "meaning": "Sudden change and awakening.", "emoji": "⚡"},
    {"name": "The Star", "meaning": "Hope and renewal.", "emoji": "⭐"},
    {"name": "The Moon", "meaning": "Illusion and intuition.", "emoji": "🌑"},
    {"name": "The Sun", "meaning": "Success and joy.", "emoji": "☀️"},
    {"name": "Judgement", "meaning": "Awakening and reflection.", "emoji": "📯"},
    {"name": "The World", "meaning": "Completion and achievement.", "emoji": "🌍"},
]


def main(page: ft.Page):

    page.title = "Celestial Arcana"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0b0616"
    page.window_width = 420
    page.window_height = 750
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    # ---------------- TEXT CONTROLS ----------------
    card_symbol = ft.Text("🃏", size=80)
    card_title = ft.Text("", size=26, weight=ft.FontWeight.BOLD, color="#FFD700")
    card_meaning = ft.Text("", size=16, text_align=ft.TextAlign.CENTER)

    # ---------------- DRAW FUNCTION ----------------
    async def draw_card(e):
        draw_button.disabled = True
        page.update()

        await asyncio.sleep(0.8)

        card = random.choice(TAROT_DATA)
        reversed_state = random.random() < 0.5

        card_symbol.value = card["emoji"]
        card_title.value = card["name"] + (" (Reversed)" if reversed_state else "")
        card_meaning.value = card["meaning"]

        reveal_card.rotation = 3.14 if reversed_state else 0

        dark_overlay.visible = True
        modal_stack.visible = True
        reveal_card.scale = 1
        reveal_card.opacity = 1

        page.update()
        draw_button.disabled = False

    # ---------------- CLOSE FUNCTION ----------------
    def close_modal(e):
        reveal_card.scale = 0
        reveal_card.opacity = 0
        page.update()

        async def hide():
            await asyncio.sleep(0.3)
            modal_stack.visible = False
            dark_overlay.visible = False
            page.update()

        page.run_task(hide)

    # ---------------- CARD UI ----------------
    reveal_card = ft.Container(
        width=300,
        height=450,
        bgcolor="#1a1033",
        border_radius=25,
        border=ft.border.all(2, "#FFD700"),
        alignment=ft.Alignment(0, 0),
        scale=0,
        opacity=0,
        animate_scale=300,
        animate_opacity=300,
        animate_rotation=300,
        shadow=[
            ft.BoxShadow(
                blur_radius=40,
                color="#FFD70055",
                spread_radius=3,
            )
        ],
    )

    card_column = ft.Column(
        [
            card_symbol,
            card_title,
            card_meaning,
            
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
    )

    reveal_card.content = card_column

    # ---------------- MODAL ----------------
    dark_overlay = ft.Container(
        bgcolor="#000000aa",
        expand=True,
        visible=False,
        on_click=close_modal,
    )

    modal_stack = ft.Stack(
    [
        dark_overlay,
        ft.Column(
            [
                reveal_card,
                ft.Container(height=20),

                ft.Row(
                    [
                        ft.TextButton("Draw Again 🔮", on_click=draw_card),
                        ft.TextButton("Close ✨", on_click=close_modal),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=40,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        ),
    ],
    expand=True,
    visible=False,
)

    # ---------------- MAIN UI ----------------
    title = ft.Text(
        "CELESTIAL ARCANA",
        size=32,
        weight=ft.FontWeight.BOLD,
        color="#FFD700",
    )

    crystal_ball = ft.Container(
        content=ft.Text("🔮", size=120),
        width=220,
        height=220,
        border_radius=110,
        bgcolor="#1e123a",
        alignment=ft.Alignment(0, 0),
        shadow=[
            ft.BoxShadow(
                blur_radius=50,
                color="#8a2be255",
                spread_radius=5,
            )
        ],
    )

    draw_button = ft.ElevatedButton(
        "DRAW A CARD",
        width=220,
        height=50,
        style=ft.ButtonStyle(
            bgcolor="#FFD700",
            color="#1a1033",
            shape=ft.RoundedRectangleBorder(radius=15),
        ),
        on_click=draw_card,
    )

    page.add(
        ft.Stack(
            [
                ft.Column(
                    [
                        ft.Container(height=60),
                        title,
                        ft.Container(height=50),
                        crystal_ball,
                        ft.Container(height=50),
                        draw_button,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                modal_stack,
            ],
            expand=True,
        )
    )


ft.app(target=main)