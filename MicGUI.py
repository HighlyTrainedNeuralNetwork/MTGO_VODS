import pyaudio
import tkinter as tk
from tkinter import ttk
import sounddevice as sd

class AudioRecorderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Audio Recorder")
        self.devices = self.get_wasapi_devices()

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="Select an input device:")
        self.label.grid(row=0, column=0)

        self.combobox = ttk.Combobox(self.master, values=self.devices, state="readonly", width=50)
        self.combobox.grid(row=0, column=1)

        self.record_button = tk.Button(self.master, text="Test", command=self.test_device)
        self.record_button.grid(row=1, column=0, columnspan=2)

        self.confirm_label = tk.Label(self.master, text="Not Confirmed")
        self.confirm_label.grid(row=2, column=0, columnspan=2)

    def get_wasapi_devices(self):
        p = pyaudio.PyAudio()
        device_count = p.get_device_count()
        wasapi_host_api_index = None

        for i in range(p.get_host_api_count()):
            host_api_info = p.get_host_api_info_by_index(i)
            if host_api_info['name'] == "Windows WASAPI":
                wasapi_host_api_index = host_api_info['index']
                break

        if wasapi_host_api_index is None:
            return []

        devices = []
        for i in range(device_count):
            device_info = p.get_device_info_by_index(i)

            if device_info['maxInputChannels'] > 0 and device_info['hostApi'] == wasapi_host_api_index:
                devices.append((device_info['index'], device_info['name']))

        return devices

    def test_device(self):
        device_index = self.combobox.current()
        if device_index == -1:
            return

        selected_device = self.devices[device_index][0]
        device_info = sd.query_devices(selected_device, 'input')
        samplerate = device_info['default_samplerate']
        duration = 2.5

        recording = sd.rec(
            int(duration * samplerate),
            samplerate=samplerate,
            channels=1,
            device=selected_device,
            dtype='int16',
            blocking=True
        )

        sd.play(recording, samplerate=samplerate, blocking=True)

        self.confirm_label.configure(text="Confirmed")


def main():
    root = tk.Tk()
    app = AudioRecorderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
