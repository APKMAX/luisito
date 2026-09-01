from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from jnius import autoclass
import os


class SumApp(App):


    def build(self):

        self.label = Label(
            text="Esperando servicio..."
        )


        self.carpeta = self.user_data_dir


        os.makedirs(
            self.carpeta,
            exist_ok=True
        )


        self.ruta_archivo = os.path.join(
            self.carpeta,
            "Info.txt"
        )


        return self.label



    def on_start(self):

        self.iniciar_servicio()


        Clock.schedule_interval(
            self.leer_archivo,
            1
        )



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


        except Exception as e:

            self.label.text = (
                "Error servicio:\n"
                + str(e)
            )



    def leer_archivo(self, dt):

        try:

            if os.path.exists(
                self.ruta_archivo
            ):

                with open(
                    self.ruta_archivo,
                    "r"
                ) as archivo:

                    contenido = archivo.read()


                self.label.text = contenido


        except Exception as e:

            self.label.text = str(e)



if __name__ == "__main__":
    SumApp().run()
