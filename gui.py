import flet as ft
import probe
from markdownify import markdownify as md

def main(page: ft.Page):
    prober = probe.Prober()

    # Needed methods for buttons
    def start_probe(e):
        global url
        url = prober.checkin(fingerprint.value, model.value)
        if url is not None:
            update_info.value = "An update is available!"
            downloadBtn.disabled = False
            update_dlg_btn.disabled = False
            update_dlg.content = ft.Markdown(md(prober.get_update_desc()))
        else:
            update_info.value = "No update is available."
            downloadBtn.disabled = True
            update_dlg_btn.disabled = True
        page.update()

    def download(e):
        print("Download button clicked")
        global url
        prober.download(url)

    def page_resized(e):
        content.height = page.window.height
        page.update()

    def validate_fingerprint(e):
        if fingerprint.value == "":
            probeBtn.disabled = True
        else:
            probeBtn.disabled = False
        page.update()

    page.on_resized = page_resized

    # Theme
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE_GREY_900)
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.WHITE24)
    page.title = "Google OTA Prober"

    # GUI Components
    update_dlg = ft.AlertDialog(
        title=ft.Text("Update changelog", text_align=ft.TextAlign.CENTER),
        on_dismiss=lambda e: print("Dialog dismissed."),
    )

    fingerprint = ft.TextField(label="Enter fingerprint here", on_change=validate_fingerprint)
    model = ft.TextField(label="Enter model here (optional)")
    probeBtn = ft.ElevatedButton("Start probe", bgcolor="#057A2C", color="#FFFFFF", on_click=start_probe, disabled=True)
    downloadBtn = ft.ElevatedButton("Download", on_click=download, disabled=True)
    update_info = ft.Text("Update info will be displayed here")
    update_dlg_btn = ft.ElevatedButton("Changelog", on_click=lambda e: page.open(update_dlg), disabled=True)

    # Generate the page
    content = ft.Column([
        ft.Container(content=fingerprint, alignment=ft.alignment.center),
        ft.Container(content=model, alignment=ft.alignment.center),
        ft.Container(content=probeBtn, alignment=ft.alignment.center),
        ft.Container(content=downloadBtn, alignment=ft.alignment.center),
        ft.Container(content=update_info, alignment=ft.alignment.center),
        ft.Container(content=update_dlg_btn, alignment=ft.alignment.center)
    ], alignment=ft.MainAxisAlignment.CENTER, height=page.window.height)

    page.add(content)
    page.update()

ft.app(target=main)