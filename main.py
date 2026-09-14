from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.metrics import dp
from jnius import autoclass
from android.permissions import request_permissions, Permission
from datetime import datetime

class SMSReader(App):
    def build(self):
        root = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        self.filtro_input = TextInput(
            text="PAGOXMOVIL",
            hint_text="Encabezado a buscar",
            multiline=False,
            size_hint_y=None,
            height=dp(50)
        )
        root.add_widget(self.filtro_input)

        self.btn = Button(text="Buscar SMS", size_hint_y=None, height=dp(50))
        self.btn.bind(on_press=self.pedir_permiso)
        root.add_widget(self.btn)

        self.scroll = ScrollView()

        self.label = Label(
            text="Escribe un encabezado y presiona 'Buscar SMS'...",
            size_hint_y=None,          # la altura la fijamos manualmente
            halign="left",
            valign="top",
            markup=False,
            color=(1, 1, 1, 1),        # blanco explícito
            padding=(dp(8), dp(8)),
        )

        # ✅ CLAVE: text_size sigue el ancho REAL del propio Label
        self.label.bind(
            width=lambda *a: self.label.setter('text_size')(self.label, (self.label.width, None))
        )
        # ✅ CLAVE: altura sigue el alto real del texto
        self.label.bind(
            texture_size=lambda *a: self.label.setter('height')(self.label, self.label.texture_size[1])
        )

        self.scroll.add_widget(self.label)
        root.add_widget(self.scroll)

        return root

    def pedir_permiso(self, instance):
        filtro = self.filtro_input.text.strip()
        if not filtro:
            self.label.text = "⚠️ Escribe un encabezado antes de buscar."
            return
        request_permissions([Permission.READ_SMS], self.callback_permiso)

    def callback_permiso(self, permissions, grants):
        if all(grants):
            self.label.text = f"Buscando '{self.filtro_input.text.strip()}'..."
            Clock.schedule_once(lambda dt: self.leer_sms(), 0.3)
        else:
            self.label.text = "Permiso denegado."

    def leer_sms(self):
        try:
            filtro = self.filtro_input.text.strip().upper()

            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Uri = autoclass('android.net.Uri')
            activity = PythonActivity.mActivity

            columnas = ["address", "body", "date"]
            uri = Uri.parse("content://sms/inbox")

            cursor = activity.getContentResolver().query(uri, columnas, None, None, "date DESC")

            mensajes = []
            if cursor:
                while cursor.moveToNext():
                    address = cursor.getString(cursor.getColumnIndex("address")) or ""
                    body = cursor.getString(cursor.getColumnIndex("body")) or ""
                    date_ms = cursor.getLong(cursor.getColumnIndex("date"))

                    if filtro in address.upper() or filtro in body.upper():
                        fecha = datetime.fromtimestamp(date_ms / 1000).strftime("%Y-%m-%d %H:%M:%S")
                        mensajes.append(
                            f"De: {address}\nFecha: {fecha}\nMensaje:\n{body}\n{'-'*40}"
                        )
                cursor.close()

            if mensajes:
                self.label.text = f"Se encontraron {len(mensajes)} mensaje(s):\n\n" + "\n\n".join(mensajes)
            else:
                self.label.text = f"No se encontraron SMS con '{filtro}'."
        except Exception as e:
            self.label.text = f"Error: {str(e)}"

if __name__ == '__main__':
    SMSReader().run()
