import numpy as np
import wavio
from dataclasses import dataclass
import operator
import os


@dataclass
class Signal:
    """Beinhaltet alle relevanten Informationen für eine einzige Schwingung"""
    name: str
    freq: float
    factor: float
    start: int
    end: int


class Exporter:
    def __init__(self, rate: int):
        self.rate = rate
        self.signals = []

    def create_new_signal(self, name: str, freq: float, factor: float, start: int, end: int):
        """Neue Schwingung hinzufügen

        :param name: Name zur Identifikation
        :param freq: Frequenz der Schwingung
        :param factor: Vorfaktor der Amplitude, sinnvollerweise zwischen 0 und 1
        :param start: Startzeitpunkt des Signals in s
        :param end: Endzeitpunkt des Signals in s
        """
        self.signals.append(Signal(name, freq, factor, start, end))

    @property
    def file_length(self) -> int:
        """Spätester Endzeitpunkt aller Signale"""
        return sorted(self.signals, key=operator.attrgetter('end'), reverse=True)[0].end

    @property
    def output_array(self) -> np.array:
        """Addiert alle Signale auf

        :returns: np.array
        """
        arrays = []
        for signal in self.signals:
            arrays.append(self.create_array_from_signal(signal))
        array = np.array(arrays).sum(axis=0)
        return array

    def create_array_from_signal(self, signal: Signal) -> np.array:
        """Erstellt Signal aus gegebenen Signal-Parametern, fügt bei Leerlauf Nullen hinzu
        :param signal: Signal-Objekt
        :returns: np.array
        """
        a_start = np.zeros(signal.start * self.rate)
        t_signal = np.linspace(signal.start, signal.end, int((signal.end - signal.start)) * self.rate, endpoint=False)
        a_signal = signal.factor * np.sin(2 * np.pi * signal.freq * t_signal)
        a_end = np.zeros((self.file_length - signal.end) * self.rate)
        array = np.append(a_start, np.append(a_signal, a_end))
        print(f'{signal.name}: {array}')
        return array

    def export_wav_file(self, file_name: str):
        """Exportiert das Gesamt-Array als .wav-Datei in den wav-Ordner
        :param file_name: Dateiname
        """
        if not os.path.exists('wav'):
            os.mkdir('wav')
        wavio.write(f'wav/{file_name}', self.output_array, self.rate, sampwidth=3)


if __name__ == '__main__':
    exporter = Exporter(44100)

    exporter.create_new_signal('s1', 220, 1, 0, 3)
    exporter.create_new_signal('s2', 440, 1, 3, 6)
    exporter.create_new_signal('s3', 880, 1, 6, 9)

    exporter.export_wav_file('test.wav')
