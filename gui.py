import flet as ft
import probe

def main(page: ft.Page):
    prober = probe.Prober()

    def start_probe(e):
        global url
        url = prober.checkin(fingerprint.value, model.value)
        if url is not None:
            update_info.value = "An update is available!"
            downloadBtn.disabled = False
            update_dlg_btn.disabled = False
            update_dlg.content = ft.Text(prober.get_update_desc())
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

    page.on_resized = page_resized

    update_dlg = ft.AlertDialog(
        title=ft.Text("Update changelog"),
        on_dismiss=lambda e: print("Dialog dismissed."),
    )

    page.title = "Google OTA Prober"
    fingerprint = ft.TextField(label="Enter fingerprint here")
    model = ft.TextField(label="Enter model here")
    downloadBtn = ft.ElevatedButton("Download", on_click=download, disabled=True)
    update_info = ft.Text("Update info will be displayed here")
    update_dlg_btn = ft.ElevatedButton("Changelog", on_click=lambda e: page.open(update_dlg), disabled=True)

    content = ft.Column([
        ft.Container(content=fingerprint, alignment=ft.alignment.center),
        ft.Container(content=model, alignment=ft.alignment.center),
        ft.Container(content=ft.ElevatedButton("Start probe", bgcolor="#FF8F8F", on_click=start_probe), alignment=ft.alignment.center),
        ft.Container(content=downloadBtn, alignment=ft.alignment.center),
        ft.Container(content=update_info, alignment=ft.alignment.center),
        ft.Container(content=update_dlg_btn, alignment=ft.alignment.center)
    ], alignment=ft.MainAxisAlignment.CENTER, height=page.window.height)

    page.add(content)
    page.update()

ft.app(target=main)