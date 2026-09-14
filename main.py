from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.clock import Clock
from jnius import autoclass
from android.permissions import request_permissions, Permission
from datetime import datetime

class SMSReader(App):
    def build(self):
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Entrada para el encabezado/remitente a buscar
        self.filtro_input = TextInput(
            text="PAGOXMOVIL",
            hint_text="Escribe el encabezado a buscar",
            multiline=False,
            size_hint_y=None,
            height=50
        )
        root.add_widget(self.filtro_input)

        # Botón de búsqueda
        self.btn = Button(text="Buscar SMS", size_hint_y=None, height=50)
        self.btn.bind(on_press=self.pedir_permiso)
        root.add_widget(self.btn)

        # Área de resultados
        self.scroll = ScrollView()
        self.label = Label(
            text="Escribe un encabezado y presiona 'Buscar SMS'...",
            size_hint_y=None,
            halign="left",
            valign="top"
        )
        self.label.bind(texture_size=lambda inst, val: setattr(inst, 'height', val[1]))
        self.scroll.bind(width=lambda inst, val: setattr(self.label, 'text_size', (val, None)))
        self.scroll.add_widget(self.label)
        root.add_widget(self.scroll)

        return root

    def pedir_permiso(self, instance):
        # Validar que el usuario haya escrito algo
        filtro = self.filtro_input.text.strip()
        if not filtro:
            self.label.text = "⚠️ Escribe un encabezado antes de buscar."
            return
        request_permissions([Permission.READ_SMS], self.callback_permiso)

    def callback_permiso(self, permissions, grants):
        if all(grants):
            self.label.text = f"Permiso concedido. Buscando '{self.filtro_input.text.strip()}'..."
            Clock.schedule_once(lambda dt: self.leer_sms(), 0.3)
        else:
            self.label.text = "Permiso denegado. No se pueden leer SMS."

    def leer_sms(self):
        try:
            # Tomar el valor de la entrada en el momento de buscar
            filtro = self.filtro_input.text.strip().upper()

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
                    address = cursor.getString(cursor.getColumnIndex("address")) or ""
                    body = cursor.getString(cursor.getColumnIndex("body")) or ""
                    date_ms = cursor.getLong(cursor.getColumnIndex("date"))

                    # Coincidencia en remitente o cuerpo
                    if filtro in address.upper() or filtro in body.upper():
                        fecha = datetime.fromtimestamp(date_ms / 1000).strftime("%Y-%m-%d %H:%M:%S")
                        mensajes.append(
                            f"De: {address}\n"
                            f"Fecha: {fecha}\n"
                            f"Mensaje:\n{body}\n"
                            f"{'-'*40}"
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
