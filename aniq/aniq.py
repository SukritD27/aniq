"""Welcome to Reflex! This file outlines the steps to create a basic app."""

from rxconfig import config

import reflex as rx
from utilities.testing import getAnswer

docs_url = "https://reflex.dev/docs/getting-started/introduction/"
filename = f"{config.app_name}/{config.app_name}.py"


class State(rx.State):
    """The app state."""

class TextAreaControlled(rx.State):
    text: str = "Hello World!"
    answer: str = ""

    def handle_submission(self):
        self.answer = getAnswer(self.text)


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.form.root(
                rx.vstack(
                     rx.heading("CliQ", size="9"),
            #rx.text("Get started by editing ", rx.code(filename)),
            rx.text_area( width="100%", value=TextAreaControlled.text,
            on_change=TextAreaControlled.set_text),
            rx.button(
                "Get answer",
                on_click=TextAreaControlled.handle_submission,
                size="4",
            ),
            
            rx.text(TextAreaControlled.answer),
            align="center",
            
                )
            ),

            align="center",
            spacing="7",
            font_size="2em",
        ),
    
        height="100vh",
        background_color="#dcf4f7"
    )


app = rx.App()
app.add_page(index)
