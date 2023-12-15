import flet as ft
import speech_recognition as sr
from googletrans import Translator

def main(page: ft.Page):
    page.title = "Universal Translator"
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    def join_trans(e):
        if not join_language.value:
            join_language.error_text = "Name cannot be blank!"
            join_language.update()
        else:
            page.dialog.open = False

            page.update()
    def take_command():
        command = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening")
            command.pause_threshold = 1
            audio = command.listen(source, 0, 20)
            try:
                print("Recognizing........")
                query = command.recognize_google(audio, language=join_language.value)
                print(f"you said : {query}")
            except Exception as Error:
                return "None"

            return query.lower();

    def translatorhtoe(text):
        line = str(text)
        trans = Translator()
        chat.controls.append(ft.Text(f"You said : {line}"))
        page.update()
        result = trans.translate(line)
        data = result.text
        print(data)
        return data
    def mtrans(e):

        data = take_command()
        a = translatorhtoe(data)
        chat.controls.append(ft.Text(f"English : {a}"))
        page.update()


    join_language = ft.RadioGroup(content=ft.Column([
    ft.Radio(value="hi", label="Hindi"),
    ft.Radio(value="ja", label="Japanese"),
    ft.Radio(value="de", label="German")]))


    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome!"),
        content=ft.Column([join_language], width=300, height=170, tight=True),
        actions=[ft.ElevatedButton(text="Select Language", on_click=join_trans)],
        actions_alignment="end",
    )
    page.add(ft.Container(content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,),
             ft.ElevatedButton("Push to speak",on_click=mtrans))
    page.update()

ft.app(target=main)