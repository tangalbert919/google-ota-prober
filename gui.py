import flet as ft
import probe

def main(page: ft.Page):
    prober = probe.Prober()
    url = ""

    def start_probe(e):
        print("Button clicked")
        print(fingerprint.value)
        global url
        url = prober.checkin(fingerprint.value, model.value)
        if url is not None:
            print("Download button enabled")
            downloadBtn.disabled = False
        else:
            print("Download button disabled")
            downloadBtn.disabled = True
        page.update()
    
    def download(e):
        print("Download button clicked")
        global url
        prober.download(url)

    page.title = "Google OTA Prober"
    fingerprint = ft.TextField(label="Enter fingerprint here")
    model = ft.TextField(label="Enter model here")
    downloadBtn = ft.ElevatedButton("Download", on_click=download, disabled=True)
    page.add(ft.Column([
        ft.Container(content=fingerprint, alignment=ft.alignment.center),
        ft.Container(content=model, alignment=ft.alignment.center),
        ft.Container(content=ft.ElevatedButton("Start probe", bgcolor="#FF8F8F", on_click=start_probe), alignment=ft.alignment.center),
        ft.Container(content=downloadBtn, alignment=ft.alignment.center)
    ], alignment=ft.MainAxisAlignment.CENTER))
    page.update()

ft.app(target=main)