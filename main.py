from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.clock import Clock
from jnius import autoclass
from android.permissions import request_permissions, Permission
from datetime import datetime

class SMSReader(App):
    def build(self):
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.btn = Button(text="Buscar SMS PAGOXMOVIL", size_hint_y=None, height=50)
        self.btn.bind(on_press=self.pedir_permiso)
        root.add_widget(self.btn)

        self.scroll = ScrollView()
        self.label = Label(
            text="Presiona el botón para buscar...",
            size_hint_y=None,
            halign="left",
            valign="top"
        )
        # Ajustar altura automáticamente al contenido
        self.label.bind(texture_size=lambda inst, val: setattr(inst, 'height', val[1]))
        # Ajustar ancho del texto al ancho del ScrollView
        self.scroll.bind(width=lambda inst, val: setattr(self.label, 'text_size', (val, None)))
        self.scroll.add_widget(self.label)
        root.add_widget(self.scroll)

        return root

    def pedir_permiso(self, instance):
        request_permissions([Permission.READ_SMS], self.callback_permiso)

    def callback_permiso(self, permissions, grants):
        if all(grants):
            self.label.text = "Permiso concedido. Buscando..."
            Clock.schedule_once(lambda dt: self.leer_sms(), 0.5)
        else:
            self.label.text = "Permiso denegado. No se pueden leer SMS."

    def leer_sms(self):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Uri = autoclass('android.net.Uri')
            activity = PythonActivity.mActivity

            columnas = ["address", "body", "date"]
            uri = Uri.parse("content://sms/inbox")

            cursor = activity.getContentResolver().query(
                uri, columnas, None, None, "date DESC"
            )

            mensajes = []
            if cursor:
                while cursor.moveToNext():
                    address = cursor.getString(cursor.getColumnIndex("address"))
                    body = cursor.getString(cursor.getColumnIndex("body"))
                    date_ms = cursor.getLong(cursor.getColumnIndex("date"))

                    # Filtrar por remitente o contenido (sin distinguir mayúsculas)
                    if (address and "PAGOXMOVIL" in address.upper()) or \
                       (body and "PAGOXMOVIL" in body.upper()):
                        fecha = datetime.fromtimestamp(date_ms / 1000).strftime("%Y-%m-%d %H:%M:%S")
                        mensajes.append(
                            f"De: {address}\n"
                            f"Fecha: {fecha}\n"
                            f"Mensaje:\n{body}\n"
                            f"{'-'*40}"
                        )
                cursor.close()

            if mensajes:
                self.label.text = "\n\n".join(mensajes)
            else:
                self.label.text = "No se encontraron SMS con 'PAGOXMOVIL'."

        except Exception as e:
            self.label.text = f"Error: {str(e)}"

if __name__ == '__main__':
    SMSReader().run()
