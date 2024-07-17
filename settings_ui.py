"""
settings_ui.py

Author: Seung Heon Lee (University of Southern California, HaRVI Lab)

This file contains the SettingsUI class, which implements the user interface for
managing application settings. It handles the creation and management of UI elements
for server configuration, folder paths, user agreements, and other global settings.
"""

import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from default_configs import load_setting, update_last_used_file_record, DEFAULT_SETTINGS_FOLDER, LAST_ACCESSED_SETTINGS_PATH
from custom_widget import ScrollableFrame, EditableList, LabelEntryRow
from latency_ui import LatencyUI

class SettingsUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.settings = load_setting()
        self.create_widgets()

    def create_widgets(self):
        # Clear existing widgets if any
        for widget in self.winfo_children():
            widget.destroy()

        # Frame for the save and load buttons at the bottom of the window #
        button_frame = ttk.Frame(self)
        button_frame.pack(fill='x', side="bottom", pady=10)

        ## Create save button
        save_button = ttk.Button(button_frame, text="Save", command=self.save_setting)
        save_button.pack(side="left", padx=10)

        ## Create load button
        load_button = ttk.Button(button_frame, text="Load", command=self.load_setting)
        load_button.pack(side="left", padx=10)

        # Create a scrollable main frame to contain the settings 
        main_frame = ScrollableFrame(self)
        main_frame.pack(fill="both", expand=True)
        main_frame = main_frame.content_frame

        ## ----Server Settings---- ##

        ## Create a frame for the server settings
        server_frame = ttk.LabelFrame(main_frame, text="Server Settings", width=500, height=120)
        server_frame.pack(fill="x", padx=10, pady=5)
        server_frame.pack_propagate(False)  # Prevent resizing of the frame

        ### Create a checkbox for using server address
        self.use_server_address_var = tk.BooleanVar(value=self.settings['use_server_address'])
        use_server_address_checkbox = ttk.Checkbutton(server_frame, text="Use Server Address", variable=self.use_server_address_var, command=self.switch_between_url_github)
        use_server_address_checkbox.pack(side="top", padx=10, pady=5)

        ### Create a frame for the server address settings
        self.server_address_frame = ttk.LabelFrame(server_frame, text="Server Address")
        self.server_address_frame.pack(fill="x", padx=10, pady=5)

        #### Create a label and textfield for server address
        server_address_label = ttk.Label(self.server_address_frame, text="Server Address:")
        server_address_label.pack(side="left", padx=10, pady=5)
        self.server_address_var = tk.StringVar(value=self.settings['ServerAddress'])
        self.server_address_var.trace_add("write", lambda *args: self.settings.update({'ServerAddress': self.server_address_var.get()}))
        server_address_entry = ttk.Entry(self.server_address_frame, textvariable=self.server_address_var)
        server_address_entry.pack(side="left", padx=10, pady=5, fill="x", expand=True)

        ### Create a frame for the GitHub settings
        self.github_settings_frame = ttk.LabelFrame(server_frame, text="GitHub Settings")
        self.github_settings_frame.pack(fill="x", padx=10, pady=5)

        #### Create a label and textfield for GitHub ID
        github_id_label = ttk.Label(self.github_settings_frame, text="GitHub ID:")
        github_id_label.pack(side="left", padx=0, pady=5)
        self.github_id_var = tk.StringVar(value=self.settings['github_id'])
        self.github_id_var.trace_add("write", lambda *args: self.settings.update({'github_id': self.github_id_var.get()}))
        github_id_entry = ttk.Entry(self.github_settings_frame, textvariable=self.github_id_var)
        github_id_entry.pack(side="left", padx=10, pady=5)

        #### Create a label and textfield for GitHub Repo
        self.github_repo_var = tk.StringVar(value=self.settings['github_repo'])
        self.github_repo_var.trace_add("write", lambda *args: self.settings.update({'github_repo': self.github_repo_var.get()}))
        github_repo_entry = ttk.Entry(self.github_settings_frame, textvariable=self.github_repo_var)
        github_repo_entry.pack(side="right", padx=10, pady=5)
        github_repo_label = ttk.Label(self.github_settings_frame, text="GitHub Repo:")
        github_repo_label.pack(side="right", padx=0, pady=5)

        ## Make sure the correct settings are displayed based on the checkbox value 
        self.switch_between_url_github()


        # Add this button after the folder settings
        latency_button = ttk.Button(main_frame, text="Open Latency Generator", command=self.open_latency_ui)
        latency_button.pack(fill="x", padx=10, pady=5)

        ## ----Folder Settings---- ##
        ## Create a hide and show button for the folder settings
        folder_button = ttk.Button(main_frame, text="Show Folder Settings", command=lambda: (folder_frame.pack_forget() or folder_button.config(text="Show Folder Settings")) if folder_frame.winfo_ismapped() else (folder_frame.pack(fill="x", padx=10, pady=5, before=user_agreement_frame) or folder_button.config(text="Hide Folder Settings")))
        folder_button.pack(fill="x", padx=10, pady=5)

        ## Create a frame for the folder settings
        folder_frame = ttk.LabelFrame(main_frame, text="Folder Settings", width=500, height=340) # Do not pack this frame yet
        folder_frame.pack_propagate(False)  # Prevent resizing of the frame

        ### Create a frame for the audio folders
        audio_folder_frame = ttk.LabelFrame(folder_frame, text="Audio Folders", width=500, height=120)
        audio_folder_frame.pack(fill="x", padx=10, pady=5)
        audio_folder_frame.pack_propagate(False)  # Prevent resizing of the frame

        #### Create a label and textfield for Original Audio Folder
        LabelEntryRow(audio_folder_frame, "Original Audio Folder:", self.settings['FolderVariables']['OriginalAudioFolder'], entry_callback=lambda x: self.settings['FolderVariables'].update({'OriginalAudioFolder': x}))

        #### Create a label and textfield for Latency Audio Folder
        LabelEntryRow(audio_folder_frame, "Latency Audio Folder:", self.settings['FolderVariables']['LatencyAudioFolder'], entry_callback=lambda x: self.settings['FolderVariables'].update({'LatencyAudioFolder': x}))

        ### Create a frame for the haptic folders
        haptic_folder_frame = ttk.LabelFrame(folder_frame, text="Haptic Folders", width=500, height=120)
        haptic_folder_frame.pack(fill="x", padx=10, pady=5)
        haptic_folder_frame.pack_propagate(False)  # Prevent resizing of the frame

        #### Create a label and textfield for Original Haptic Folder
        LabelEntryRow(haptic_folder_frame, "Original Haptic Folder:", self.settings['FolderVariables']['OriginalHapticFolder'], entry_callback=lambda x: self.settings['FolderVariables'].update({'OriginalHapticFolder': x}))

        #### Create a label and textfield for Latency Haptic Folder
        LabelEntryRow(haptic_folder_frame, "Latency Haptic Folder:", self.settings['FolderVariables']['LatencyHapticFolder'], entry_callback=lambda x: self.settings['FolderVariables'].update({'LatencyHapticFolder': x}))

        ### Create a label and textfield for Image Folder
        LabelEntryRow(folder_frame, "Image Folder:", self.settings['FolderVariables']['ImageFolder'], entry_callback=lambda x: self.settings['FolderVariables'].update({'ImageFolder': x}))

        # ### Create a label and textfield for Case Folder
        # LabelEntryRow(folder_frame, "Case Folder:", self.settings['FolderVariables']['CaseFolder'], entry_callback=lambda x: self.settings['FolderVariables'].update({'CaseFolder': x}))

        # ### Create a label and textfield for Experiment Folder
        # LabelEntryRow(folder_frame, "Experiment Folder:", self.settings['FolderVariables']['ExperimentFolder'], entry_callback=lambda x: self.settings['FolderVariables'].update({'ExperimentFolder': x}))
        
        ## ----User Agreement Settings---- ##
        ## Create a User Agreement Settings Frame
        user_agreement_frame = ttk.LabelFrame(main_frame, text="User Agreement Settings", width=500, height=270)
        user_agreement_frame.pack(fill="x", padx=10, pady=5)
        user_agreement_frame.pack_propagate(False)  # Prevent resizing of the frame

        # Use the EditableList for user agreements
        self.user_agreement_list = EditableList(
            user_agreement_frame, 
            [[ua] for ua in self.settings.get('user_agreements', [])],   # Wrap user agreement strings in lists to match expected format
            lambda x: self.settings.update({'user_agreements': [ua[0] for ua in x]}),
            entry_factory=lambda: [tk.StringVar(value="")]
        )
        self.user_agreement_list.pack(fill="both", expand=True)

        ## Create a hide and show button for the Layout Descriptions
        layout_button = ttk.Button(main_frame, text="Show Layout Descriptions", command=lambda: (layout_frame.pack_forget() or layout_button.config(text="Show Layout Descriptions")) if layout_frame.winfo_ismapped() else (layout_frame.pack(fill="x", padx=10, pady=5, before=survey_link_frame) or folder_button.config(text="Hide Layout Descriptions")))
        layout_button.pack(fill="x", padx=10, pady=5)

        ## Create a frame for the folder settings
        layout_frame = ttk.LabelFrame(main_frame, text="Layout Descriptions", width=500, height=130) # Do not pack this frame yet
        layout_frame.pack_propagate(False)  # Prevent resizing of the frame

        ### Create EditableList for Layout Descriptions
        self.layout_list = EditableList(
            layout_frame,
            [[description['image']] for description in self.settings['layout_descriptions']],
            lambda x: self.settings.update({'layout_descriptions': [
                {
                    'image': image[0],
                    "location_array_available": self.settings['layout_descriptions'][i]['location_array_available'],
                    "interaction_type": self.settings['layout_descriptions'][i]['interaction_type']
                } for i, image in enumerate(x)
            ]}) if len(x) == len(self.settings['layout_descriptions']) else None, # Wait until all entries are filled before updating settings
            delete_enabled=False,
            add_enabled=False,
            order_change_enabled=False,
            label_texts=['Tap with NumPad:', 'Tap with Touch Pad:', 'Swipe with Touch Pad:'],
            folder_path=self.settings['FolderVariables']['ImageFolder']
        )
        self.layout_list.pack(fill="both", expand=True)

        ## ----Survey Link Settings---- ##
        ## Create a Survey Link Settings Frame
        survey_link_frame = ttk.LabelFrame(main_frame, text="Survey Link Settings", width=500, height=150)
        survey_link_frame.pack(fill="x", padx=10, pady=5)
        survey_link_frame.pack_propagate(False)  # Prevent resizing of the frame

        # Use the EditableList for survey links
        self.survey_link_list = EditableList(
            survey_link_frame, 
            [[link['nickname'], link['url']] for link in self.settings['Links']],
            lambda x: self.settings.update({'Links': [{'nickname': entry[0], 'url': entry[1]} for entry in x]}),
            entry_factory=lambda: [tk.StringVar(value=""), tk.StringVar(value="")]
        )
        self.survey_link_list.pack(fill="both", expand=True)

    def switch_between_url_github(self):
        """
        Toggles between server address and GitHub settings based on checkbox value.
        """
        # Update the settings based on the checkbox value
        use_server_address = self.use_server_address_var.get()
        self.settings['use_server_address'] = use_server_address

        # Show or hide the server address frame based on the checkbox value
        # Hide or show the GitHub settings frame based on the checkbox value
        if use_server_address:
            self.server_address_frame.pack(fill="x", padx=10, pady=5)
            self.github_settings_frame.pack_forget()
        else:
            self.server_address_frame.pack_forget()
            self.github_settings_frame.pack(fill="x", padx=10, pady=5)

    def save_setting(self):
        """
        Saves the current settings to a file using a file dialog.
        """
        # Open a file dialog to select the file path, defaulting to the settings folder, and JSON file type
        file_path = filedialog.asksaveasfilename(initialdir=DEFAULT_SETTINGS_FOLDER, title="Save File", defaultextension=".json", filetypes=[("JSON files", "*.json")])
        # If a file path is selected, save the settings to the file
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.settings, file, indent=4)
                update_last_used_file_record(LAST_ACCESSED_SETTINGS_PATH, file_path)
                # Show a message box indicating that the settings were saved successfully
                messagebox.showinfo("Save Settings", "Settings saved successfully.")

    def load_setting(self):
        """
        Loads the settings from a file using a file dialog.
        Updates the current UI with the loaded settings.
        """
        # Open a file dialog to select the file path, defaulting to the settings folder, and JSON file type
        file_path = filedialog.askopenfilename(initialdir=DEFAULT_SETTINGS_FOLDER, title="Select File", defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            self.settings = load_setting(file_path)
            messagebox.showinfo("Load Settings", "Settings loaded successfully.")
            self.create_widgets()

    def open_latency_ui(self):
        LatencyUI(self, self.settings)