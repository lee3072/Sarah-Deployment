import os
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import soundfile as sf
import json
from custom_widget import ScrollableFrame, EditableList, LabelEntryRow

class LatencyUI(tk.Toplevel):
    def __init__(self, parent, settings):
        super().__init__(parent)
        self.settings = settings
        self.title("Latency Management")
        self.geometry("500x770")
        self.latency = 0.5  # Default latency
        self.audio_files = []
        self.haptic_files = []
        
        self.create_widgets()

    def create_widgets(self):
        main_frame = ScrollableFrame(self)
        main_frame.pack(fill="both", expand=True)
        main_frame = main_frame.content_frame

        # Latency input
        LabelEntryRow(main_frame, "Latency (seconds):", str(self.latency), entry_callback=self.update_latency)
        
        # Audio files
        audio_frame = ttk.LabelFrame(main_frame, text="Audio Files")
        audio_frame.pack(fill="x", padx=10, pady=5)
        
        self.audio_list = EditableList(
            audio_frame,
            [],
            self.update_audio_files,
            dropdown_values=self.load_audio_files(),
            add_enabled=True
        )
        self.audio_list.pack(fill="both", expand=True)

        # Haptic files
        haptic_frame = ttk.LabelFrame(main_frame, text="Haptic Files")
        haptic_frame.pack(fill="x", padx=10, pady=5)
        
        self.haptic_list = EditableList(
            haptic_frame,
            [],
            self.update_haptic_files,
            dropdown_values=self.load_haptic_files(),
            add_enabled=True
        )
        self.haptic_list.pack(fill="both", expand=True)

        # Convert button
        convert_button = ttk.Button(main_frame, text="Convert", command=self.convert_files)
        convert_button.pack(pady=10)

    def load_audio_files(self):
        audio_files = [f for f in os.listdir(self.settings['FolderVariables']['OriginalAudioFolder']) if f.endswith('.wav')]
        return [''] + audio_files  # Empty string instead of 'None'

    def load_haptic_files(self):
        haptic_files = [f for f in os.listdir(self.settings['FolderVariables']['OriginalHapticFolder']) if f.endswith('.ahap')]
        return [''] + haptic_files  # Empty string instead of 'None'

    def update_latency(self, value):
        try:
            self.latency = float(value)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for latency.")

    def update_audio_files(self, files):
        self.audio_files = [file[0] for file in files if file[0]]  # Ignore empty strings

    def update_haptic_files(self, files):
        self.haptic_files = [file[0] for file in files if file[0]]  # Ignore empty strings

    def convert_files(self):
        converted_count = 0
        for audio_file in self.audio_files:
            self.audio_latency(audio_file)
            converted_count += 1
        
        for haptic_file in self.haptic_files:
            self.haptic_latency(haptic_file)
            converted_count += 1
        
        if converted_count > 0:
            messagebox.showinfo("Conversion Complete", f"{converted_count} file(s) have been converted with {self.latency} seconds latency.")
        else:
            messagebox.showinfo("No Conversion", "No files were selected for conversion.")

    def audio_latency(self, file_name):
        input_folder = self.settings['FolderVariables']['OriginalAudioFolder']
        output_folder = self.settings['FolderVariables']['LatencyAudioFolder']
        file_path = os.path.join(input_folder, file_name)
        data, fs = sf.read(file_path)
        latency_samples = int(self.latency * fs)
        if data.ndim == 1:  # mono
            latency_data = np.zeros(latency_samples, dtype=data.dtype)
        else:  # stereo
            latency_data = np.zeros((latency_samples, data.shape[1]), dtype=data.dtype)
        data_with_latency = np.concatenate([latency_data, data])
        output_file_path = os.path.join(output_folder, file_name)
        sf.write(output_file_path, data_with_latency, fs)

    def haptic_latency(self, file_name):
        input_folder = self.settings['FolderVariables']['OriginalHapticFolder']
        output_folder = self.settings['FolderVariables']['LatencyHapticFolder']
        file_path = os.path.join(input_folder, file_name)
        with open(file_path, 'r') as f:
            ahap_data = json.load(f)
        for pattern in ahap_data['Pattern']:
            if 'Event' in pattern:
                pattern['Event']['Time'] += self.latency
            elif 'ParameterCurve' in pattern:
                pattern['ParameterCurve']['Time'] += self.latency
        output_file_path = os.path.join(output_folder, file_name)
        with open(output_file_path, 'w') as f:
            json.dump(ahap_data, f, indent=4)