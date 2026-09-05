from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.utils import platform
from kivy.clock import Clock

from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient


class ContadorApp(App):
    def build(self):
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        self.label = Label(
            text="Contador: 0\n(servicio no iniciado)",
            font_size="24sp",
            halign="center",
            valign="middle"
        )
        self.label.bind(size=self.label.setter("text_size"))

        self.btn_start = Button(
            text="Iniciar / Reiniciar Servicio",
            size_hint_y=None,
            height=60
        )
        self.btn_start.bind(on_press=self.start_service)

        self.btn_stop = Button(
            text="Detener Servicio",
            size_hint_y=None,
            height=60
        )
        self.btn_stop.bind(on_press=self.stop_service)

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.btn_start)
        self.layout.add_widget(self.btn_stop)

        return self.layout

    def on_start(self):
        # Servidor OSC en la app (recibe mensajes del servicio)
        self.server = OSCThreadServer()
        self.server.listen(address="127.0.0.1", port=3002, default=True)
        self.server.bind(b"/contador", self.on_contador)

        if platform == "android":
            # Arrancamos el servicio automáticamente
            Clock.schedule_once(lambda dt: self.start_service(None), 0.8)

    def on_contador(self, valor):
        """Se llama cada vez que el servicio envía el contador"""
        self.label.text = f"Contador: {valor}\n(servicio activo)"

    def start_service(self, instance):
        if platform != "android":
            self.label.text = "Solo funciona en Android"
            return

        from jnius import autoclass
        from android import mActivity

        context = mActivity.getApplicationContext()
        service_class = context.getPackageName() + ".ServiceCounter"
        service = autoclass(service_class)

        service.start(mActivity, "")
        self.label.text = "Servicio iniciado...\nEsperando datos..."

    def stop_service(self, instance):
        if platform != "android":
            return

        # Enviamos señal de parada al servicio por OSC
        try:
            client = OSCClient("127.0.0.1", 3001)
            client.send_message(b"/stop", [])
            self.label.text = "Señal de parada enviada"
        except Exception as e:
            self.label.text = f"Error al detener: {e}"

    def on_stop(self):
        if hasattr(self, "server"):
            try:
                self.server.stop()
                self.server.close()
            except Exception:
                pass


if __name__ == "__main__":
    ContadorApp().run()
