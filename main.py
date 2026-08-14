from kivy.app import App
from kivy.uix.label import Label
from jnius import autoclass


SERVICE_NAME = "Backgroundservice"


class SumApp(App):

    def build(self):
        self.label = Label(
            text="Servicio en segundo plano iniciando..."
        )

        return self.label

    def on_start(self):
        self.iniciar_servicio()

    def iniciar_servicio(self):
        try:
            service = autoclass(
                "org.example.myapp.ServiceBackgroundservice"
            )

            activity = autoclass(
                "org.kivy.android.PythonActivity"
            ).mActivity

            service.start(
                activity,
                ""
            )

            self.label.text = "Servicio en segundo plano activo"

            print("[APP] Servicio iniciado")

        except Exception as e:
            self.label.text = f"Error iniciando servicio: {e}"
            print("[APP] Error:", e)


if __name__ == "__main__":
    SumApp().run()
