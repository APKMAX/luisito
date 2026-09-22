from datetime import datetime
import re

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle

# ============================================================
#  CONFIGURACIÓN DE MODO
# ------------------------------------------------------------
#  0 = Base de datos ficticia (para probar en escritorio)
#  1 = SMS reales de Android
# ============================================================
MODO = 1


# ============================================================
#  BASE DE DATOS FICTICIA (misma estructura que devuelve Android)
#  Cada registro tiene: _id, address, body, date (ms)
# ============================================================
MENSAJES_FICTICIOS = [
    {
        "_id": 1,
        "address": "PAGOxMOVIL",
        "body": "El titular del telefono 5358600596 le ha realizado una transferencia a la cuenta 9204129972759908 de 8000.00 CUP. Nro. Transaccion BR6016GMZ4997. Fecha: 7/9/2026.",
        "date": 1757203200000,
    },
    {
        "_id": 2,
        "address": "PAGOxMOVIL",
        "body": "El titular del telefono 5358200014 le ha realizado una transferencia a la cuenta 9204129972759908 de 1340.00 CUP. Nro. Transaccion BR6016EZJ7997. Fecha: 7/9/2026.",
        "date": 1757206800000,
    },
    {
        "_id": 3,
        "address": "PAGOXMOVIL",
        "body": "El titular del telefono 5358600596 le ha realizado una transferencia a la cuenta 9204129972759908 de 1500.00 CUP. Nro. Transaccion BR6017KQZ3210. Fecha: 8/9/2026.",
        "date": 1757293200000,
    },
    {
        "_id": 4,
        "address": "PAGOXMOVIL",
        "body": "El titular del telefono 5358200014 le ha realizado una transferencia a la cuenta 9204129972759908 de 2500.00 CUP. Nro. Transaccion BR6017MPL6584. Fecha: 8/9/2026.",
        "date": 1757296800000,
    },
    {
        "_id": 5,
        "address": "PAGOXMOVIL",
        "body": "El titular del telefono 5358600596 le ha realizado una transferencia a la cuenta 9204129972759908 de 3200.00 CUP. Nro. Transaccion BR6018TWR1142. Fecha: 9/9/2026.",
        "date": 1757379600000,
    },
    {
        "_id": 6,
        "address": "PAGOXMOVIL",
        "body": "El titular del telefono 5358200014 le ha realizado una transferencia a la cuenta 9204129972759908 de 750.00 CUP. Nro. Transaccion BR6018QNP8890. Fecha: 9/9/2026.",
        "date": 1757383200000,
    },
    {
        "_id": 7,
        "address": "PAGOXMOVIL",
        "body": "El titular del telefono 5358600596 le ha realizado una transferencia a la cuenta 9204129972759908 de 5000.00 CUP. Nro. Transaccion BR6019BCD4471. Fecha: 10/9/2026.",
        "date": 1757466000000,
    },
    {
        "_id": 8,
        "address": "PAGOXMOVIL",
        "body": "El titular del telefono 5358200014 le ha realizado una transferencia a la cuenta 9204129972759908 de 1800.00 CUP. Nro. Transaccion BR6020FGH2298. Fecha: 10/9/2026.",
        "date": 1757469600000,
    },
    {
        "_id": 9,
        "address": "PAGOXMOVIL",
        "body": "El titular del telefono 5358600596 le ha realizado una transferencia a la cuenta 9204129972759908 de 950.00 CUP. Nro. Transaccion BR6021JKL7735. Fecha: 11/9/2026.",
        "date": 1757552400000,
    },
    {
        "_id": 10,
        "address": "PAGOXMOVIL",
        "body": "El titular del telefono 5358200014 le ha realizado una transferencia a la cuenta 9204129972759908 de 4200.00 CUP. Nro. Transaccion BR6022XYZ6612. Fecha: 11/9/2026.",
        "date": 1757556000000,
    },
]


# ============================================================
#  IMPORTS ESPECÍFICOS DE ANDROID (solo si MODO == 1)
# ============================================================
if MODO == 1:
    from jnius import autoclass
    from android.permissions import request_permissions, Permission, check_permission

    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Uri = autoclass('android.net.Uri')


def formatear_fecha(date_ms):
    """Convierte milisegundos epoch a fecha/hora legible."""
    try:
        ts = int(date_ms) / 1000.0
        return datetime.fromtimestamp(ts).strftime('%d/%m/%Y  %H:%M')
    except Exception:
        return str(date_ms)


def extraer_monto(body):
    """
    Extrae el número que va justo antes de 'CUP'.
    Ejemplo: '... de 950.00 CUP. ...'  →  950.00
    Busca la sigla CUP y toma el número (con decimales) que la precede.
    """
    if not body:
        return None
    # Número con o sin decimales seguido de espacios y CUP
    m = re.search(r'(\d+(?:\.\d+)?)\s*CUP', body, re.IGNORECASE)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            return None
    return None


class MensajeCard(BoxLayout):
    """
    Cada SMS se muestra como un bloque separado:
      - Cabecera (remitente + fecha)
      - Cuerpo del mensaje en párrafo
    """

    def __init__(self, address, fecha, body, **kwargs):
        super().__init__(
            orientation='vertical',
            size_hint_y=None,
            padding=(dp(14), dp(12)),
            spacing=dp(6),
            **kwargs,
        )
        self.bind(minimum_height=self.setter('height'))

        with self.canvas.before:
            Color(0.15, 0.17, 0.21, 1)
            self._bg = RoundedRectangle(radius=[dp(10)] * 4)
        self.bind(pos=self._sync_bg, size=self._sync_bg)

        header = Label(
            text=f'[b]De: {address}[/b]\nFecha: {fecha}',
            markup=True,
            size_hint_y=None,
            font_size='14sp',
            color=(0.75, 0.85, 1, 1),
            halign='left',
            valign='top',
            line_height=1.25,
        )
        header.bind(
            texture_size=lambda inst, val: setattr(inst, 'height', val[1]),
            width=lambda inst, val: setattr(inst, 'text_size', (val, None)),
        )
        self.add_widget(header)

        cuerpo = Label(
            text=body.strip(),
            size_hint_y=None,
            font_size='14sp',
            color=(0.95, 0.95, 0.95, 1),
            halign='left',
            valign='top',
            line_height=1.35,
        )
        cuerpo.bind(
            texture_size=lambda inst, val: setattr(inst, 'height', val[1]),
            width=lambda inst, val: setattr(inst, 'text_size', (val, None)),
        )
        self.add_widget(cuerpo)

    def _sync_bg(self, *args):
        self._bg.pos = self.pos
        self._bg.size = self.size


class SMSReader(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=dp(8), padding=dp(10), **kwargs)

        self.input_address = TextInput(
            hint_text='Remitente exacto (ej: PAGOXMOVIL)',
            multiline=False,
            size_hint_y=None,
            height=dp(45),
            font_size='18sp',
        )
        self.add_widget(self.input_address)

        self.input_body = TextInput(
            hint_text='Texto a buscar en el mensaje (parcial)',
            multiline=False,
            size_hint_y=None,
            height=dp(45),
            font_size='18sp',
        )
        self.add_widget(self.input_body)

        self.btn = Button(
            text='Buscar mensajes',
            size_hint_y=None,
            height=dp(50),
            font_size='18sp',
        )
        self.btn.bind(on_press=self.buscar_sms)
        self.add_widget(self.btn)

        # Resumen breve
        self.resumen = Label(
            text='Escribe el remitente y el texto (ambos obligatorios) y pulsa Buscar...',
            size_hint_y=None,
            height=dp(28),
            font_size='14sp',
            color=(0.8, 0.8, 0.8, 1),
            halign='left',
            valign='middle',
        )
        self.resumen.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        self.add_widget(self.resumen)

        # ---- Label grande de capital / totales ----
        self.capital = Label(
            text='',
            size_hint_y=None,
            height=0,
            font_size='17sp',
            color=(0.3, 1.0, 0.55, 1),
            markup=True,
            halign='left',
            valign='top',
            line_height=1.35,
        )
        self.capital.bind(
            texture_size=self._ajustar_altura_capital,
            width=lambda inst, val: setattr(inst, 'text_size', (val, None)),
        )
        self.add_widget(self.capital)

        # Zona de resultados con scroll
        self.scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(8),
            scroll_type=['bars', 'content'],
        )
        self.lista = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(12),
            padding=(0, 0, dp(6), dp(12)),
        )
        self.lista.bind(minimum_height=self.lista.setter('height'))
        self.scroll.add_widget(self.lista)
        self.add_widget(self.scroll)

    def _ajustar_altura_capital(self, instance, value):
        # Si no hay texto, ocultar (altura 0); si hay, usar el tamaño del texto
        if not instance.text.strip():
            instance.height = 0
        else:
            instance.height = value[1] + dp(8)

    def _limpiar_lista(self):
        self.lista.clear_widgets()

    def _mostrar_aviso(self, texto):
        self._limpiar_lista()
        self.capital.text = ''
        aviso = Label(
            text=texto,
            size_hint_y=None,
            font_size='15sp',
            color=(0.9, 0.9, 0.9, 1),
            halign='left',
            valign='top',
            line_height=1.3,
        )
        aviso.bind(
            texture_size=lambda inst, val: setattr(inst, 'height', val[1]),
            width=lambda inst, val: setattr(inst, 'text_size', (val, None)),
        )
        self.lista.add_widget(aviso)

    def on_start(self):
        if MODO == 1:
            request_permissions([Permission.READ_SMS])

    def buscar_sms(self, instance):
        address_filtro = self.input_address.text.strip()
        body_filtro = self.input_body.text.strip()

        if not address_filtro:
            self.resumen.text = 'Debes escribir el remitente exacto.'
            self._mostrar_aviso('Debes escribir el remitente exacto.')
            return

        if not body_filtro:
            self.resumen.text = 'Debes escribir el texto a buscar en el mensaje.'
            self._mostrar_aviso('Debes escribir el texto a buscar en el mensaje.')
            return

        if MODO == 1:
            mensajes = self._leer_sms_android()
        else:
            mensajes = self._leer_sms_local()

        if mensajes is None:
            return

        # Filtros sensibles a mayúsculas/minúsculas (case-sensitive)
        resultados = []
        total_monto = 0.0
        cantidad = 0

        for m in mensajes:
            address = (m.get('address', '') or '').strip()
            body = m.get('body', '') or ''
            date = m.get('date', 0)

            # Filtro 1: address EXACTO y case-sensitive
            # PAGOXMOVIL ≠ pagoxmovil ≠ PAGOxMOVIL
            if address != address_filtro:
                continue
            # Filtro 2: body CONTIENE la cadena (también case-sensitive)
            if body_filtro not in body:
                continue

            # Rebanar el monto guiándose por la sigla CUP
            monto = extraer_monto(body)
            if monto is not None:
                total_monto += monto
                cantidad += 1

            resultados.append((address, date, body, monto))

        self._limpiar_lista()

        if resultados:
            self.resumen.text = (
                f'Se encontraron {len(resultados)} mensaje(s)  ·  más recientes arriba'
            )
            # Label grande de capital
            self.capital.text = (
                f'[b]Total de dinero transferido: {total_monto:,.2f} CUP[/b]\n'
                f'[b]Cantidad de transferencias: {cantidad}[/b]'
            )
            for address, date, body, monto in resultados:
                self.lista.add_widget(
                    MensajeCard(address, formatear_fecha(date), body)
                )
            Clock.schedule_once(lambda *_: setattr(self.scroll, 'scroll_y', 1), 0)
        else:
            self.resumen.text = 'No se encontraron mensajes con esos criterios.'
            self.capital.text = ''
            self._mostrar_aviso('No se encontraron mensajes con esos criterios.')

    def _leer_sms_android(self):
        if not check_permission(Permission.READ_SMS):
            self.resumen.text = 'Sin permiso READ_SMS'
            self._mostrar_aviso(
                'No tienes permiso READ_SMS.\n'
                'Concédelo en Ajustes → Apps → Permisos.'
            )
            return None

        try:
            activity = PythonActivity.mActivity
            content_resolver = activity.getContentResolver()

            uri = Uri.parse('content://sms/inbox')
            projection = ['_id', 'address', 'body', 'date']

            cursor = content_resolver.query(
                uri, projection, None, None, 'date DESC'
            )

            mensajes = []
            if cursor is not None:
                while cursor.moveToNext():
                    mensajes.append({
                        '_id': cursor.getLong(cursor.getColumnIndex('_id')),
                        'address': cursor.getString(cursor.getColumnIndex('address')) or '',
                        'body': cursor.getString(cursor.getColumnIndex('body')) or '',
                        'date': cursor.getLong(cursor.getColumnIndex('date')),
                    })
                cursor.close()

            return mensajes

        except Exception as e:
            self.resumen.text = 'Error al leer SMS'
            self._mostrar_aviso(f'Error al leer SMS:\n{str(e)}')
            return None

    def _leer_sms_local(self):
        return sorted(
            MENSAJES_FICTICIOS,
            key=lambda m: m['date'],
            reverse=True,
        )


class SMSApp(App):
    def build(self):
        return SMSReader()

    def on_start(self):
        self.root.on_start()


if __name__ == '__main__':
    SMSApp().run()
