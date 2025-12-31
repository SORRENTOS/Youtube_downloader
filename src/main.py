import flet as ft
import yt_dlp
import time
from yt_dlp import YoutubeDL


def main(page: ft.Page):
    
    
    
    lista_videos = []
    destino_descarga = ""
    #anim de descarga
    def anim_descarga(logo): 
        while(True):
            logo.rotate.angle += 0.1
            page.update()
            time.sleep(0.1)

            
    #! AQUI DESCARGO EL VIDEO
    def descargar_video(lista,logo,columna_videos):
        global destino_descarga
        ydl_opts = {
        "paths": {"home": destino_descarga},  # <-- disco externo
        }
        logo.visible = True
        for x in lista:
            print(x)
            try:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download(x)
                    columna_videos.controls[0].offset = ft.Offset(-2,0)
                    time.sleep(0.5)
                    columna_videos.controls.pop(0)
            except:
                print("hola")
        lista.clear()

        logo.visible = False
        
        page.update()
        #! BUSCAR VIDEO
    def agregar_a_la_cola(columna,url_video,lista,contro_busqueda):
        contro_busqueda.offset = ft.Offset(0,0)
        
        lista.append(url_video)

        ydl_opts = {}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url_video, download=False)
            contro_busqueda.offset = ft.Offset(0,2)

        # ℹ️ ydl.sanitize_info makes the info json-serializable
            print(ydl.sanitize_info(info)["title"])
            Titulo_video = ft.Text(value=str(ydl.sanitize_info(info)["title"]),size=15,color="#74c69d")
            miniatura = ft.Image(src=ydl.sanitize_info(info)["thumbnail"],height=50,width=50 )
            fila_video = ft.Row([miniatura,Titulo_video])
            control = ft.Container(content= fila_video
                                ,padding=10,
                                bgcolor="#b7e4c7"
                                ,border_radius=10
                                    ,offset= ft.Offset(-2,0)
                                    ,animate_offset= ft.Animation(1000)
                                )
            columna.controls.insert(0,control)
            page.update()
            time.sleep(0.1)
            control.offset = ft.Offset(0,0)
            page.update()
        except:
            contro_busqueda.offset = ft.Offset(0,2)   
        
    
    
    page.bgcolor = "#d8f3dc"
    Url = ft.TextField(label="url del video",label_style=ft.TextStyle(color="#74c69d"),color="#74c69d",expand=True,border_radius= 10, bgcolor="#b7e4c7",border_width=0)
    btn_url = ft.IconButton(icon= ft.Icons.ADD,bgcolor="#b7e4c7",icon_color="#74c69d",padding= 10,alignment=ft.alignment.top_right,on_click= lambda x: agregar_a_la_cola(columna_videos,Url.value,lista_videos,container_busqueda_logo) )
    fila= ft.Row([Url,btn_url],expand= True,vertical_alignment= ft.CrossAxisAlignment.START)
    btn_descarga = ft.IconButton(icon=ft.Icons.DOWNLOAD,icon_color="#74c69d",bgcolor="#b7e4c7",padding= 10,on_click= lambda x : descargar_video(lista_videos,logo_de_descarga,columna_videos))
    columna_videos = ft.Column([],animate_size=ft.Animation(200) )
    logo_de_descarga = ft.Container(content= ft.IconButton(icon=ft.Icons.SWAP_VERT_CIRCLE,icon_color="#95d5b2"),animate_rotation=ft.Animation(1000,ft.AnimationCurve.BOUNCE_OUT),rotate=ft.Rotate(0, alignment=ft.alignment.center),visible=False)
    
    container_busqueda_logo = ft.Container(content= ft.Text("Buscando...", color="#74c69d"),
                                           bgcolor="#b7e4c7"
                                           ,padding=8
                                           , border_radius=10
                                           ,offset= ft.Offset(0,2)
                                           ,animate_offset= ft.Animation(800)
                                           )



    #SETTINGS PARA DESCARGAR VIDEO 
    def guardar_ruta_descarga(e):
        global destino_descarga
        

        destino_descarga = InputRutaDescarga.value
        settings_final_container.offset = (-2,0)
        page.update()


    InputRutaDescarga = ft.TextField(label="destino de descarga",label_style=ft.TextStyle(color="#74c69d"),color="#74c69d",expand=False,border_radius= 10, bgcolor="#d8f3dc",border_width=0)
    btnRuta = ft.ElevatedButton(text="Guardar",bgcolor="#74c69d",color="#b7e4c7",on_click=guardar_ruta_descarga)


    columnaSettings = ft.Column([InputRutaDescarga,btnRuta],horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    settings= ft.Container(content=columnaSettings, width=200,height=  150,bgcolor="#b7e4c7",border_radius=10,padding=30)
    settings_final_container = ft.Container(content=settings,alignment=ft.alignment.center,offset=(0,0),animate_offset=ft.Animation(1000))

    page.add(
        ft.SafeArea(
            ft.Container(
                ft.Stack([

                    ft.ResponsiveRow([

                    fila,
                    columna_videos,


                    ]),settings_final_container

                ,ft.Row([container_busqueda_logo,logo_de_descarga,btn_descarga],right=10,bottom=20),
                ])
                
               
                
            ),
            expand=True,
        )
    )
    
    anim_descarga(logo_de_descarga)
ft.app(main) 