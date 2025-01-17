import flet as ft
import probe
import time
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
            saveBtn.disabled = False
            update_dlg.content = ft.Markdown(md(prober.get_update_desc()))
        else:
            update_info.value = "No update is available."
            downloadBtn.disabled = True
            update_dlg_btn.disabled = True
            saveBtn.disabled = True
        page.update()

    def download(e):
        print("Download button clicked")
        global url
        prober.download(url, progress_bar=progress_bar, page=page)

    def validate_fingerprint(e):
        if fingerprint.value == "":
            probeBtn.disabled = True
        else:
            probeBtn.disabled = False
        page.update()

    def save_fingerprint(e):
        # Check if fingerprints.txt exists.
        try:
            fingerprint_file = open("fingerprints.txt", "r+")
        except:
            print("Fingerprints.txt does not exist. Creating one.")
            fingerprint_file = open("fingerprints.txt", "w+")
        # Check if the fingerprint is already in the file
        temp = update_info.value
        duplicate = False
        for line in fingerprint_file:
            if line == fingerprint.value:
                update_info.value = "Fingerprint already exists in the file."
                duplicate = True
                break
        if not duplicate:
            fingerprint_file.write(fingerprint.value + '\n')
            update_info.value = "Fingerprint saved."
        page.update()
        fingerprint_file.close()
        time.sleep(3)
        update_info.value = temp
        page.update()

    # Theme
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE_GREY_900)
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.WHITE24)
    page.title = "Google OTA Prober"

    # GUI Components
    update_dlg = ft.AlertDialog(
        title=ft.Text("Update changelog", text_align=ft.TextAlign.CENTER),
        on_dismiss=lambda e: print("Dialog dismissed."),
    )
    about_dlg = ft.AlertDialog(
        title=ft.Text("About", text_align=ft.TextAlign.CENTER),
        content=ft.Text("Google OTA Prober v1.0", text_align=ft.TextAlign.CENTER),
        on_dismiss=lambda e: print("Dialog dismissed."),
    )

    fingerprint = ft.TextField(label="Enter fingerprint here", on_change=validate_fingerprint)
    model = ft.TextField(label="Enter model here (optional)")
    probeBtn = ft.ElevatedButton("Start probe", bgcolor="#057A2C", color="#FFFFFF", on_click=start_probe, disabled=True)
    downloadBtn = ft.ElevatedButton("Download", on_click=download, disabled=True)
    saveBtn = ft.ElevatedButton("Save", on_click=save_fingerprint, disabled=True)
    update_info = ft.Text("Update info will be displayed here")
    update_dlg_btn = ft.ElevatedButton("Changelog", on_click=lambda e: page.open(update_dlg), disabled=True)
    progress_bar = ft.ProgressBar(width=300, value=0)

    page.bottom_appbar = ft.BottomAppBar(
        bgcolor="#057A2C",
        content=ft.Row(
            controls=[
                ft.IconButton(ft.Icons.HOME, on_click=lambda e: page.go("/")),
                ft.IconButton(ft.Icons.SETTINGS, on_click=lambda e: page.go("/settings")),
                ft.Container(expand=True),
                ft.Column(
                    controls=[progress_bar, update_info], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True
                ),
                ft.Container(expand=True),
                ft.IconButton(ft.Icons.INFO, on_click=lambda e: page.open(about_dlg))
            ]
        )
    )

    # Generate the page
    content = ft.Column([
        ft.Container(content=fingerprint, alignment=ft.alignment.center),
        ft.Container(content=model, alignment=ft.alignment.center),
        ft.Container(content=probeBtn, alignment=ft.alignment.center),
        ft.Container(content=ft.Row([downloadBtn, saveBtn], alignment=ft.MainAxisAlignment.CENTER, expand=True), alignment=ft.alignment.center),
        ft.Container(content=update_dlg_btn, alignment=ft.alignment.center)
    ], alignment=ft.MainAxisAlignment.CENTER, expand=True)

    page.add(content)
    page.update()

ft.app(target=main)