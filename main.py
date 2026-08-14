from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from jnius import autoclass

class SumApp(App):
    def build(self):
        self.label = Label(text="Esperando...")
        self.total = 0
        Clock.schedule_interval(self.sumar, 30)

        # Arrancar servicio Java adaptado a versiones modernas
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Intent = autoclass('android.content.Intent')
        Build = autoclass('android.os.Build')
        SumService = autoclass('org.example.myapp.SumService')

        activity = PythonActivity.mActivity
        intent = Intent(activity, SumService)

        if Build.VERSION.SDK_INT >= 26:
            activity.startForegroundService(intent)
        else:
            activity.startService(intent)

        return self.label

    def sumar(self, dt):
        self.total += sum(range(1, 101))
        self.label.text = f"Total acumulado: {self.total}"

if __name__ == "__main__":
    SumApp().run()

