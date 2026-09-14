from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from jnius import autoclass
from android.permissions import request_permissions, Permission, check_permission
from datetime import datetime

PythonActivity = autoclass('org.kivy.android.PythonActivity')
Uri = autoclass('android.net.Uri')

class SMSReader(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=8, padding=10, **kwargs)

        # Campo para el encabezado
        self.input_header = TextInput(
            hint_text='Escribe el encabezado (ej: PAGOXMOVIL)',
            multiline=False,
            size_hint_y=None,
            height=dp(45),
            font_size=18
        )
        self.add_widget(self.input_header)

        # Botón
        self.btn = Button(
            text='Buscar mensajes',
            size_hint_y=None,
            height=dp(50),
            font_size=18
        )
        self.btn.bind(on_press=self.buscar_sms)
        self.add_widget(self.btn)

        # Contenedor de resultados con scroll
        self.scroll = ScrollView()
        self.resultados_box = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=10,
            padding=5
        )
        self.resultados_box.bind(minimum_height=self.resultados_box.setter('height'))
        self.scroll.add_widget(self.resultados_box)
        self.add_widget(self.scroll)

        # Mensaje inicial
        self.mostrar_mensaje('Escribe un encabezado y pulsa Buscar...')

    def on_start(self):
        request_permissions([Permission.READ_SMS])

    def limpiar_resultados(self):
        self.resultados_box.clear_widgets()

    def mostrar_mensaje(self, texto):
        self.limpiar_resultados()
        lbl = Label(
            text=texto,
            size_hint_y=None,
            height=dp(60),
            halign='center',
            valign='middle'
        )
        self.resultados_box.add_widget(lbl)

    def crear_tarjeta_mensaje(self, address, fecha, body):
        """Crea una tarjeta limpia por cada mensaje"""
        tarjeta = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=10,
            spacing=4
        )
        tarjeta.bind(minimum_height=tarjeta.setter('height'))

        # Remitente + fecha
        encabezado = Label(
            text=f'[b]De:[/b] {address}   |   {fecha}',
            markup=True,
            size_hint_y=None,
            height=dp(25),
            halign='left',
            valign='middle',
            color=(0.2, 0.6, 1, 1)
        )
        encabezado.bind(size=encabezado.setter('text_size'))
        tarjeta.add_widget(encabezado)

        # Cuerpo del mensaje
        cuerpo = Label(
            text=body,
            size_hint_y=None,
            halign='left',
            valign='top',
            text_size=(self.width - dp(40), None),  # se ajusta al ancho
            color=(1, 1, 1, 1)
        )
        cuerpo.bind(texture_size=cuerpo.setter('size'))
        tarjeta.add_widget(cuerpo)

        # Separador
        separador = Label(
            text='─' * 40,
            size_hint_y=None,
            height=dp(20),
            color=(0.5, 0.5, 0.5, 1)
        )
        tarjeta.add_widget(separador)

        return tarjeta

    def buscar_sms(self, instance):
        header = self.input_header.text.strip()

        if not header:
            self.mostrar_mensaje('Escribe un encabezado primero.')
            return

        if not check_permission(Permission.READ_SMS):
            self.mostrar_mensaje('No tienes permiso READ_SMS.\nConcédelo en Ajustes.')
            return

        try:
            activity = PythonActivity.mActivity
            content_resolver = activity.getContentResolver()

            uri = Uri.parse('content://sms/inbox')
            projection = ['_id', 'address', 'body', 'date']

            cursor = content_resolver.query(uri, projection, None, None, 'date DESC')

            self.limpiar_resultados()
            contador = 0
            header_upper = header.upper()

            if cursor is not None:
                while cursor.moveToNext():
                    address = cursor.getString(cursor.getColumnIndex('address')) or 'Desconocido'
                    body = cursor.getString(cursor.getColumnIndex('body')) or ''
                    date_ms = cursor.getLong(cursor.getColumnIndex('date'))

                    if header_upper in body.upper():
                        # Convertir fecha a legible
                        fecha = datetime.fromtimestamp(date_ms / 1000).strftime('%d/%m/%Y %H:%M')
                        
                        tarjeta = self.crear_tarjeta_mensaje(address, fecha, body)
                        self.resultados_box.add_widget(tarjeta)
                        contador += 1

                cursor.close()

            if contador == 0:
                self.mostrar_mensaje(f'No se encontraron mensajes con:\n"{header}"')
            else:
                # Añadir contador arriba
                titulo = Label(
                    text=f'[b]Se encontraron {contador} mensaje(s)[/b]',
                    markup=True,
                    size_hint_y=None,
                    height=dp(35),
                    color=(0.3, 0.9, 0.3, 1)
                )
                self.resultados_box.add_widget(titulo, index=0)

        except Exception as e:
            self.mostrar_mensaje(f'Error:\n{str(e)}')

class SMSApp(App):
    def build(self):
        return SMSReader()

    def on_start(self):
        self.root.on_start()

if __name__ == '__main__':
    SMSApp().run()
