"""
case_ui.py

Author: Seung Heon Lee (University of Southern California, HaRVI Lab)

This file contains the CaseUI class, which implements the user interface for
creating and editing individual experiment cases. It manages UI elements for
configuring interaction types, timers, scores, and linked audio/haptic files
for each experimental case.
"""

import os
import json, jsonschema
import random
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from custom_widget import ScrollableFrame, EditableList, LabelEntryRow
from default_configs import load_case_config, update_last_used_file_record, LAST_ACCESSED_CASE_PATH, DEFAULT_CASE_FOLDER

class CaseUI(tk.Frame):
    def __init__(self, parent, settings):
        super().__init__(parent)
        self.settings = settings
        self.case = load_case_config()

        self.create_widgets()

    def create_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        button_frame = ttk.Frame(self)
        button_frame.pack(fill='x', side="bottom", pady=10)

        save_button = ttk.Button(button_frame, text="Save", command=self.save_case)
        save_button.pack(side="left", padx=10)

        load_button = ttk.Button(button_frame, text="Load", command=self.load_case)
        load_button.pack(side="left", padx=10)

        generate_button = ttk.Button(button_frame, text="Generate", command=self.generate_case_json)
        generate_button.pack(side="left", padx=10)

        main_frame = ScrollableFrame(self)
        main_frame.pack(fill="both", expand=True)
        main_frame = main_frame.content_frame

        ## Create a frame for the Case ID
        case_id_frame = ttk.LabelFrame(main_frame, text="Case ID", height=60)
        case_id_frame.pack(fill="x", expand=True, side="top", padx=10, pady=10)
        case_id_frame.pack_propagate(False)  # Prevent resizing of the frame

        ### Create a label and textfield for Case ID
        LabelEntryRow(case_id_frame, "Case ID:", self.case['case_id'], entry_callback=lambda x : self.case.update({'case_id': x}))

        ## Create a frame for the General Settings
        general_settings_frame = ttk.LabelFrame(main_frame, text="General Settings", height=670)
        general_settings_frame.pack(fill="x", expand=True, side="top", padx=10, pady=10)
        general_settings_frame.pack_propagate(False)  # Prevent resizing of the frame

        ### Create a dropdown for the Interaction Type (tap & continue, tap & restart, swipe & restart)
        interaction_type = LabelEntryRow(general_settings_frame, "Interaction Type:", self.case['interaction'], ["tap & continue", "tap & restart", "swipe_through & restart"], entry_callback=lambda x : self.case.update({'interaction': x}))

        ### Create a frame for the Array Settings
        array_settings_frame = ttk.Frame(general_settings_frame, height=420, width=600)
        array_settings_frame.pack(side="left", padx=0, pady=10)
        array_settings_frame.pack_propagate(False)  # Prevent resizing of the frame

        ### Create a order_array Frame
        order_array_frame = ttk.LabelFrame(array_settings_frame, text="Order Array", height=420, width=50)
        order_array_frame.pack(fill="x", expand=True, side="left", padx=10, pady=10)
        order_array_frame.pack_propagate(False)  # Prevent resizing of the frame

        #### Create a EditableList without delete button and add button for order_array
        self.order_list = EditableList(
            order_array_frame,
            [[idx] for idx in self.case['order_array']],
            lambda x: self.case.update({'order_array': [idx[0] for idx in x]}),
            delete_enabled=False,
            add_enabled=False,
            move_up_callback=self.synchronize_move_up,
            move_down_callback=self.synchronize_move_down
        )
        self.order_list.pack(fill="both", expand=True)

        ### Create a Enable/Disable button for the custom_text_array Frame
        self.custom_text_enabled_var = tk.BooleanVar(value=self.case['custom_text_enabled'])
        custom_text_enabled_checkbutton = ttk.Checkbutton(general_settings_frame, text="Enable Custom Text Array", variable=self.custom_text_enabled_var, command=self.toggle_custom_text_array)
        custom_text_enabled_checkbutton.pack(fill="x", expand=True, side="top", padx=10, pady=10, after=interaction_type)

        ### Create a custom_text_array Frame
        self.custom_text_array_frame = ttk.LabelFrame(array_settings_frame, text="Custom Text Array", height=420, width=50)
        self.custom_text_array_frame.pack(fill="x", expand=True, side="left", padx=10, pady=10)
        self.custom_text_array_frame.pack_propagate(False)  # Prevent resizing of the frame

        #### Create a EditableList without delete button and add button for custom_text_array
        self.custom_text_list = EditableList(
            self.custom_text_array_frame,
            [[idx] for idx in self.case['custom_text_array']],
            lambda x: self.case.update({'custom_text_array': [idx[0] for idx in x]}),
            delete_enabled=False,
            add_enabled=False,
            order_change_enabled=False
        )
        self.custom_text_list.pack(fill="both", expand=True)

        self.toggle_custom_text_array()

        ### Create a interaction_delay Frame
        interaction_delay_frame = ttk.LabelFrame(array_settings_frame, text="Interaction Delay", height=420, width=50)
        interaction_delay_frame.pack(fill="x", expand=True, side="left", padx=10, pady=10)
        interaction_delay_frame.pack_propagate(False)  # Prevent resizing of the frame

        #### Create a EditableList without delete button and add button for interaction_delay
        self.interaction_delay_list = EditableList(
            interaction_delay_frame,
            [[idx] for idx in self.case['interaction_delay']],
            lambda x: self.case.update({'interaction_delay': [idx[0] for idx in x]}),
            delete_enabled=False,
            add_enabled=False,
            order_change_enabled=False
        )
        self.interaction_delay_list.pack(fill="both", expand=True)


        ### Create a Enable/Disable button for the location_array Frame
        self.location_array_enabled_var = tk.BooleanVar(value=self.case['location_array_enabled'])
        location_array_enabled_checkbutton = ttk.Checkbutton(general_settings_frame, text="Enable Location Array", variable=self.location_array_enabled_var, command=self.toggle_location_array)
        location_array_enabled_checkbutton.pack(fill="x", expand=True, side="top", padx=10, pady=10, after=custom_text_enabled_checkbutton)

        ### Create a Randomize Location button
        randomize_location_button = ttk.Button(general_settings_frame, text="Randomize Location", command=self.randomize_location)
        randomize_location_button.pack(fill="x", expand=True, side="top", padx=10, pady=10, after=location_array_enabled_checkbutton)

        ### Create a location_array Frame
        self.location_array_frame = ttk.LabelFrame(array_settings_frame, text="Location Array", height=420, width=50)
        self.location_array_frame.pack(fill="x", expand=True, side="left", padx=10, pady=10)
        self.location_array_frame.pack_propagate(False)  # Prevent resizing of the frame

        #### Create a EditableList without delete button and add button for location_array
        #### Location array is a list of (x, y) coordinates
        self.location_list = EditableList(
            self.location_array_frame,
            [[loc['x'], loc['y']] for loc in self.case['location_array']],
            lambda x: self.case.update({'location_array': [{'x': loc[0], 'y': loc[1]} for loc in x]}),
            entry_factory=lambda: [tk.StringVar(value="50"), tk.StringVar(value="50")],
            delete_enabled=False,
            add_enabled=False,
            order_change_enabled=False
        )
        
        self.location_list.pack(fill="both", expand=True)

        self.toggle_location_array()

        ## Create a frame for the Haptic and Audio Files
        # haptic_audio_frame = ttk.LabelFrame(main_frame, text="Haptic and Audio Files", height=800)
        # haptic_audio_frame.pack(fill="x", expand=True, side="top", padx=10, pady=10)
        # haptic_audio_frame.pack_propagate(False)  # Prevent resizing of the frame

        ### Create a frame for Haptic Files
        haptic_frame = ttk.Frame(general_settings_frame, height=420)
        haptic_frame.pack(fill="x", expand=True, side="left", padx=0, pady=10)
        haptic_frame.pack_propagate(False)  # Prevent resizing of the frame
        
        ### Create a Correct Haptic Frame
        correct_haptic_frame = ttk.LabelFrame(haptic_frame, text="Correct Interaction Haptic Files", height=420, width=50)
        correct_haptic_frame.pack(fill="x", expand=True, side="left", padx=10, pady=10)
        correct_haptic_frame.pack_propagate(False)  # Prevent resizing of the frame

        #### Create a label and dropdown for Correct Haptic File using the settings folder path
        self.correct_haptic = EditableList(
            correct_haptic_frame,
            [[idx] for idx in self.case['linked_files']['correct_haptic']],
            lambda x: self.case['linked_files'].update({'correct_haptic': [idx[0] for idx in x]}),
            delete_enabled=False,
            add_enabled=False,
            dropdown_values=self.load_haptic_files(),
            order_change_enabled=False
        )
        self.correct_haptic.pack(fill="both", expand=True)

        ### Create a Wrong Haptic Frame
        wrong_haptic_frame = ttk.LabelFrame(haptic_frame, text="Wrong Interaction Haptic Files", height=420, width=50)
        wrong_haptic_frame.pack(fill="x", expand=True, side="left", padx=10, pady=10)
        wrong_haptic_frame.pack_propagate(False)   # Prevent resizing of the frame

        #### Create a label and dropdown for Incorrect Haptic File using the settings folder path
        self.wrong_haptic = EditableList(
            wrong_haptic_frame,
            [[idx] for idx in self.case['linked_files']['wrong_haptic']],
            lambda x: self.case['linked_files'].update({'wrong_haptic': [idx[0] for idx in x]}),
            delete_enabled=False,
            add_enabled=False,
            dropdown_values=self.load_haptic_files(),
            order_change_enabled=False
        )
        self.wrong_haptic.pack(fill="both", expand=True)

        ### Create a frame for Audio Files
        audio_frame = ttk.Frame(general_settings_frame, height=420)
        audio_frame.pack(fill="x", expand=True, side="left", padx=0, pady=10)
        audio_frame.pack_propagate(False)  # Prevent resizing of the frame

        ### Create a frame for Correct Audio File
        correct_audio_frame = ttk.LabelFrame(audio_frame, text="Correct Interaction Audio Files", height=420, width=50)
        correct_audio_frame.pack(fill="x", expand=True, side="left", padx=10, pady=10)
        correct_audio_frame.pack_propagate(False)    # Prevent resizing of the frame

        #### Create a label and dropdown for Correct Audio File using the settings folder path
        self.correct_audio = EditableList(
            correct_audio_frame,
            [[idx] for idx in self.case['linked_files']['correct_audio']],
            lambda x: self.case['linked_files'].update({'correct_audio': [idx[0] for idx in x]}),
            delete_enabled=False,
            add_enabled=False,
            dropdown_values=self.load_audio_files(),
            order_change_enabled=False
        )
        self.correct_audio.pack(fill="both", expand=True)

        ### Create a frame for Incorrect Audio File
        wrong_audio_frame = ttk.LabelFrame(audio_frame, text="Incorrect Interaction Audio Files", height=420, width=50)
        wrong_audio_frame.pack(fill="x", expand=True, side="left", padx=10, pady=10)
        wrong_audio_frame.pack_propagate(False)     # Prevent resizing of the framet_file_path

        #### Create a label and dropdown for Incorrect Audio File using the settings folder path
        self.wrong_audio = EditableList(    
            wrong_audio_frame,
            [[idx] for idx in self.case['linked_files']['wrong_audio']],
            lambda x: self.case['linked_files'].update({'wrong_audio': [idx[0] for idx in x]}),
            delete_enabled=False,
            add_enabled=False,
            dropdown_values=self.load_audio_files(),
            order_change_enabled=False
        )
        self.wrong_audio.pack(fill="both", expand=True)

        ## Create a frame for the Highlight Settings
        highlight_frame = ttk.LabelFrame(main_frame, text="Highlight Settings", height=450)
        highlight_frame.pack(fill="x", expand=True, side="top", padx=10, pady=10)
        highlight_frame.pack_propagate(False)

        ### Create a Enable/Disable button for the highlight_array Frame
        self.highlight_array_enabled_var = tk.BooleanVar(value=self.case['highlight_array_enabled'])
        highlight_array_enabled_checkbutton = ttk.Checkbutton(highlight_frame, text="Enable Highlight Array", variable=self.highlight_array_enabled_var, command=self.toggle_highlight_array)
        highlight_array_enabled_checkbutton.pack(fill="x", expand=True, side="top", padx=10, pady=10)

        ### Create a highlight_array Frame
        self.highlight_array_frame = ttk.LabelFrame(highlight_frame, text="Highlight Array", height=420, width=50)
        self.highlight_array_frame.pack(fill="x", expand=True, side="left", padx=10, pady=10)
        self.highlight_array_frame.pack_propagate(False)  # Prevent resizing of the frame

        #### Create a EditableList without delete button and add button for highlight_array
        self.highlight_list = EditableList(
            self.highlight_array_frame,
            [[idx] for idx in self.case['highlight_array']],
            lambda x: self.case.update({'highlight_array': [idx[0] for idx in x]}),
            delete_enabled=False,
            add_enabled=False,
            # order_change_enabled=False
        )
        self.highlight_list.pack(fill="both", expand=True)

        self.toggle_highlight_array()



        ## Create a frame for the Timer Settings
        timer_frame = ttk.LabelFrame(main_frame, text="Timer Settings", height=250)
        timer_frame.pack(fill="x", expand=True, side="top", padx=10, pady=10)
        timer_frame.pack_propagate(False)

        ### Create a checkbox for enabling/disabling timer settings
        self.timer_enabled_var = tk.BooleanVar(value=self.case['timer']['enabled'])
        timer_enabled_checkbutton = ttk.Checkbutton(timer_frame, text="Enable Timer", variable=self.timer_enabled_var, command=self.toggle_timer_settings)
        timer_enabled_checkbutton.pack(fill="x", padx=10, pady=5)

        ### Create a frame for the timer settings (this will be toggled)
        self.timer_settings_frame = ttk.Frame(timer_frame)
        self.timer_settings_frame.pack(fill="x", padx=10, pady=5)

        #### Create inputs for timer settings
        LabelEntryRow(self.timer_settings_frame, "Direction:", self.case['timer']['direction'], ["up", "down"], entry_callback=lambda x: self.case['timer'].update({'direction': x}))

        LabelEntryRow(self.timer_settings_frame, "Max Time (ms):", self.case['timer']['max_time'], entry_callback=lambda x: self.case['timer'].update({'max_time': x}))

        LabelEntryRow(self.timer_settings_frame, "Format:", self.case['timer']['format'], ["S", "s", "m", "s.SSS", "mm:ss", "mm:ss.SSS"], entry_callback=lambda x: self.case['timer'].update({ 'format': x }))

        LabelEntryRow(self.timer_settings_frame, "Fake Ranking:", self.case['timer']['fake_ranking'], entry_callback=lambda x: self.case['timer'].update({'fake_ranking': x}), toggle_val=self.case['timer']['fake_ranking_enabled'], toggle_callback=lambda x: self.case['timer'].update({'fake_ranking_enabled': x}))

        self.toggle_timer_settings() 

        ## Create a frame for the Scoreboard Settings
        scoreboard_frame = ttk.LabelFrame(main_frame, text="Scoreboard Settings", height=290)
        scoreboard_frame.pack(fill="x", expand=True, side="top", padx=10, pady=10)
        scoreboard_frame.pack_propagate(False)  # Prevent resizing of the frame

        ### Create a checkbox for enabling/disabling scoreboard settings
        self.scoreboard_enabled_var = tk.BooleanVar(value=self.case['scoreboard']['enabled'])
        scoreboard_enabled_checkbutton = ttk.Checkbutton(scoreboard_frame, text="Enable Scoreboard", variable=self.scoreboard_enabled_var, command=self.toggle_scoreboard_settings)
        scoreboard_enabled_checkbutton.pack(fill="x", padx=10, pady=5)

        ### Create a frame for the scoreboard settings (this will be toggled)
        self.scoreboard_settings_frame = ttk.Frame(scoreboard_frame)
        self.scoreboard_settings_frame.pack(fill="x", padx=10, pady=5)

        #### Create inputs for scoreboard settings
        LabelEntryRow(self.scoreboard_settings_frame, "Reward Score:", self.case['scoreboard']['reward_score'], entry_callback=lambda x: self.case['scoreboard'].update({'reward_score': x}))

        LabelEntryRow(self.scoreboard_settings_frame, "Penalty Percentage:", self.case['scoreboard']['penalty_percentage'], [str(i) for i in range(0,101)], entry_callback=lambda x: self.case['scoreboard'].update({'penalty_percentage': x}))

        LabelEntryRow(self.scoreboard_settings_frame, "Decimal Places:", self.case['scoreboard']['decimal_places'], ["0","1","2","3"], entry_callback=lambda x: self.case['scoreboard'].update({'decimal_places': x}))

        LabelEntryRow(self.scoreboard_settings_frame, "Display Negative:", "True" if self.case['scoreboard']['display_negative'] else "False", ["True", "False"], entry_callback=lambda x: self.case['scoreboard'].update({'display_negative': x == "True"}))

        LabelEntryRow(self.scoreboard_settings_frame, "Fake Ranking:", self.case['scoreboard']['fake_ranking'], entry_callback=lambda x: self.case['scoreboard'].update({'fake_ranking': x}), toggle_val=self.case['scoreboard']['fake_ranking_enabled'], toggle_callback=lambda x: self.case['scoreboard'].update({'fake_ranking_enabled': x}))

        self.toggle_scoreboard_settings()

        ## Create a frame for the Tutorial Text
        tutorial_frame = ttk.LabelFrame(main_frame, text="Tutorial Text", height=160)
        tutorial_frame.pack(fill="x", expand=True, side="top", padx=10, pady=10)
        tutorial_frame.pack_propagate(False)  # Prevent resizing of the frame

        ### Create input fields for tutorial text
        LabelEntryRow(tutorial_frame, "Interaction Type:", self.case['tutorial_text']['interaction_type'], ["", "tap on the button from 1 to 9", "swipe through the buttons from 1 to 9", "Please Enter Custom Instruction After Deleting This Text"], entry_callback=lambda x: self.case['tutorial_text'].update({'interaction_type': x}))

        LabelEntryRow(tutorial_frame, "Penalty:", self.case['tutorial_text']['penalty'], ["", "incorrect interaction will result in a penalty", "Please Enter Custom Instruction After Deleting This Text"], entry_callback=lambda x: self.case['tutorial_text'].update({'penalty': x}))

        LabelEntryRow(tutorial_frame, "Game Mode:", self.case['tutorial_text']['game_mode'], ["","you will be able to continue from the button you left off if you make a mistake", "you will need to restart from the button 1 if you make a mistake", "Please Enter Custom Instruction After Deleting This Text"], entry_callback=lambda x: self.case['tutorial_text'].update({'game_mode': x}))

        ## Create an input field for Game Over Text
        LabelEntryRow(main_frame, "Game Over Text:", self.case['game_over_text'], ["", "Congratulations! You have completed the game!", "Please Enter Custom Instruction After Deleting This Text"], entry_callback=lambda x: self.case.update({'game_over_text': x}))

        ## Create an input field for Survey URL
        LabelEntryRow(main_frame, "Survey URL:", self.case['survey_url'], [""]+[f"{link['nickname']} - {link['url']}" for link in self.settings['Links']], entry_callback=lambda x: self.case.update({'survey_url': x}))


    def toggle_scoreboard_settings(self):
        """
        Toggles the scoreboard settings based on the state of the checkbutton.
        """
        state = "normal" if self.scoreboard_enabled_var.get() else "disabled"
        for child in self.scoreboard_settings_frame.winfo_children():
            child.set_state(state)

        self.case['scoreboard']['enabled'] = self.scoreboard_enabled_var.get()

    def toggle_timer_settings(self):
        state = "normal" if self.timer_enabled_var.get() else "disabled"
        for child in self.timer_settings_frame.winfo_children():
            child.set_state(state)

        self.case['timer'] = self.case.get('timer', {})
        self.case['timer']['enabled'] = self.timer_enabled_var.get()

    def toggle_custom_text_array(self):
        """
        Toggles the custom_text_array based on the state of the checkbutton.
        """
        self.case['custom_text_enabled'] = self.custom_text_enabled_var.get()
        # Enable or disable the custom_text_array frame based on the checkbutton state
        state = "normal" if self.case['custom_text_enabled'] else "disabled"
        self.custom_text_list.set_state(state)

    def toggle_highlight_array(self):
        """
        Toggles the highlight_array based on the state of the checkbutton.
        """
        self.case['highlight_array_enabled'] = self.highlight_array_enabled_var.get()
        # Enable or disable the highlight_array frame based on the checkbutton state
        state = "normal" if self.case['highlight_array_enabled'] else "disabled"
        self.highlight_list.set_state(state)

    def toggle_location_array(self):
        """
        Toggles the location_array based on the state of the checkbutton.
        """
        self.case['location_array_enabled'] = self.location_array_enabled_var.get()
        # Enable or disable the location_array frame based on the checkbutton state
        state = "normal" if self.case['location_array_enabled'] else "disabled"
        self.location_list.set_state(state)

    def randomize_location(self):
        """
        Randomizes the location_array based on the state of the checkbutton.
        """
        if not self.case['location_array_enabled']:
            return
        
        self.case['location_array'] = self.generate_location_array()
        # destroy current location list
        self.location_list.destroy()
        # Create a new location list with the updated location array
        self.location_list = EditableList(
            self.location_array_frame,
            [[loc['x'], loc['y']] for loc in self.case['location_array']],
            lambda x: self.case.update({'location_array': [{'x': loc[0], 'y': loc[1]} for loc in x]}),
            entry_factory=lambda: [tk.StringVar(value="50"), tk.StringVar(value="50")],
            delete_enabled=False,
            add_enabled=False,
            order_change_enabled=False
        )
        self.location_list.pack(fill="both", expand=True)
    
    def generate_location_array(self, width=15, height=10, allow_overlap=False):
        location_array = []
        occupied = set()  # Set to track occupied (x, y) pairs

        while len(location_array) < 9:
            x = random.randint(0, 85)
            y = random.randint(0, 90)

            if not allow_overlap:
                # Check if the chosen area overlaps with any occupied area
                overlap = False
                for dx in range(width + 1):
                    for dy in range(height + 1):
                        if (x + dx, y + dy) in occupied:
                            overlap = True
                            break
                    if overlap:
                        break
                if overlap:
                    continue

            # Add the area to the occupied set if overlap is not allowed
            if not allow_overlap:
                for dx in range(width + 1):
                    for dy in range(height + 1):
                        occupied.add((x + dx, y + dy))

            location = {"x": x, "y": y}
            location_array.append(location)

        return location_array

    # Load ahap files from the haptic folder
    def load_haptic_files(self):
        """
        Load the haptic files from the haptic folder.
        """
        haptic_files = [f"{f} - {os.path.join(self.settings['FolderVariables']['OriginalHapticFolder'],f)}" for f in os.listdir(self.settings['FolderVariables']['OriginalHapticFolder']) if f.endswith('.ahap')]
        latency_files = [f"{f} - {os.path.join(self.settings['FolderVariables']['LatencyHapticFolder'],f)}" for f in os.listdir(self.settings['FolderVariables']['LatencyHapticFolder']) if f.endswith('.ahap')]
        return ['None'] + haptic_files + latency_files

    # Load audio files from the audio folder
    def load_audio_files(self):
        """
        Load the audio files from the audio folder.
        """
        audio_files = [f"{f} - {os.path.join(self.settings['FolderVariables']['OriginalAudioFolder'],f)}" for f in os.listdir(self.settings['FolderVariables']['OriginalAudioFolder']) if f.endswith('.wav') or f.endswith('.mp3')]
        latency_files = [f"{f} - {os.path.join(self.settings['FolderVariables']['LatencyAudioFolder'],f)}" for f in os.listdir(self.settings['FolderVariables']['LatencyAudioFolder']) if f.endswith('.wav') or f.endswith('.mp3')]
        return ['None'] + audio_files + latency_files

    def save_case(self):
        """
        Save the case configurations to a file using a file dialog.
        """
        # Open a file dialog to select the file path, defaulting to the case folder, and JSON file type
        file_path = filedialog.asksaveasfilename(initialdir=DEFAULT_CASE_FOLDER, title="Save File", defaultextension=".json", filetypes=[("JSON files", "*.json")])
        # If a file path is selected, save the case config to the file
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.case, file, indent=4)
                update_last_used_file_record(LAST_ACCESSED_CASE_PATH, file_path)
                # Show a message box indicating that the case were saved successfully
                messagebox.showinfo("Save Case Configuration", "Case configuration saved successfully.")

    def load_case(self):
        """
        Load the case configurations from a file using a file dialog.
        """
        # Open a file dialog to select the file path, defaulting to the case folder, and JSON file type
        file_path = filedialog.askopenfilename(initialdir=DEFAULT_CASE_FOLDER, title="Select File", defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            self.case = load_case_config(file_path)
            messagebox.showinfo("Load Case Configuration", "Case configuration loaded successfully.")
            self.create_widgets()

    def generate_case_json(self):
        if not self.case['case_id']:
            messagebox.showerror("Error", "Please enter a Case ID")
            return

        if 'swipe' in self.case['interaction'] and not self.case['location_array_enabled']:
            messagebox.showerror("Error", "Please enable Location Array for swipe interaction")
            return

        # Determine the root URL
        if self.settings['use_server_address']:
            root = self.settings['ServerAddress']
        else:
            root = f"https://{self.settings['github_id']}.github.io/{self.settings['github_repo']}"

        # Prepare the case data
        case_data = {
            "order_array": [int(x) for x in self.case['order_array']],
            "interaction_delay": [int(x) for x in self.case['interaction_delay']],
            "tutorial_text": self.case['tutorial_text'],
        }

        # if swipe interaction and interaction_delay has a value larger than 0
        # show error message
        if 'swipe' in self.case['interaction'] and any(case_data['interaction_delay']):
            messagebox.showerror("Error", "Interaction Delay should be 0 for swipe interaction")
            return
            
        # Handle interaction
        interaction_type, game_mode = self.case['interaction'].split(" & ")
        case_data["interaction"] = {
            "interaction_type": interaction_type,
            "game_mode": game_mode
        }

        # Handle location_array and custom_text_array
        if self.case['location_array_enabled']:
            case_data["location_array"] = [{"x": int(loc['x']), "y": int(loc['y'])} for loc in self.case['location_array']]
        if self.case['custom_text_enabled']:
            case_data["custom_text_array"] = self.case['custom_text_array']
        if self.case['highlight_array_enabled']:
            case_data["highlight_array"] = [int(x) for x in self.case['highlight_array']]

        # Handle timer
        if self.case['timer']['enabled']:
            timer_data = {k: v for k, v in self.case['timer'].items() if k != 'enabled' and k != 'fake_ranking_enabled'}
            if self.case['timer']['fake_ranking_enabled']:
                timer_data['fake_ranking'] = float(self.case['timer']['fake_ranking'])
            else:
                timer_data.pop('fake_ranking', None)
            timer_data.pop('fake_ranking_enabled', None)
            timer_data['max_time'] = int(timer_data['max_time'])
            case_data["timer"] = timer_data

        # Handle scoreboard
        if self.case['scoreboard']['enabled']:
            scoreboard_data = {k: v for k, v in self.case['scoreboard'].items() if k != 'enabled' and k != 'fake_ranking_enabled'}
            if self.case['scoreboard']['fake_ranking_enabled']:
                scoreboard_data['fake_ranking'] = float(self.case['scoreboard']['fake_ranking'])
            else:
                scoreboard_data.pop('fake_ranking', None)
            scoreboard_data.pop('fake_ranking_enabled', None)
            scoreboard_data['reward_score'] = float(scoreboard_data['reward_score'])
            scoreboard_data['penalty_percentage'] = int(scoreboard_data['penalty_percentage'])
            scoreboard_data['decimal_places'] = int(scoreboard_data['decimal_places'])
            case_data["score"] = scoreboard_data

        # Handle survey_url
        survey_url = self.case['survey_url'].split(" - ", 1)[-1] if " - " in self.case['survey_url'] else self.case['survey_url']
        if survey_url:
            case_data["survey_url"] = survey_url

        # Handle game_over_text
        if self.case['game_over_text']:
            case_data["game_over_text"] = self.case['game_over_text']

        # Handle linked_files
        linked_files = {}
        for file_type in ['correct_haptic', 'wrong_haptic', 'correct_audio', 'wrong_audio']:
            files = [f"{root}/{file.split(' - ',1)[-1]}" if file != "None" else "" for file in self.case['linked_files'][file_type]]
            if any(files):
                linked_files[file_type] = files
        if linked_files:
            case_data["linked_files"] = linked_files

        # Configure the file name and path
        file_name = f"{self.case['case_id']}.json"
        file_path = os.path.join("Files", "Case", file_name)  # Using predefined folder structure

        # Verify if case data is valid with json schema before writing to file
        format_json = json.dumps(case_data, indent=4)
        
        def validate_json(json_data, schema):
            try:
                jsonschema.validate(json.loads(json_data), schema)
                return True
            except jsonschema.exceptions.ValidationError as e:
                messagebox.showerror("Validation Error", str(e))
                return False

        with open('Schema/case.json') as file:
            schema = json.load(file)

        if not validate_json(format_json, schema):
            return 

        try:
            with open(file_path, 'w') as f:
                f.write(format_json)
            messagebox.showinfo("Success", f"Case JSON generated: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate case JSON: {str(e)}")

    def synchronize_move_up(self, index):
            self.order_list.move_index_up(index)
            self.interaction_delay_list.move_index_up(index)
            self.custom_text_list.move_index_up(index)
            # self.highlight_list.move_index_up(index)
            self.location_list.move_index_up(index)
            self.correct_haptic.move_index_up(index)
            self.wrong_haptic.move_index_up(index)
            self.correct_audio.move_index_up(index)
            self.wrong_audio.move_index_up(index)

    def synchronize_move_down(self, index):
            self.order_list.move_index_down(index)
            self.interaction_delay_list.move_index_down(index)
            self.custom_text_list.move_index_down(index)
            # self.highlight_list.move_index_down(index)
            self.location_list.move_index_down(index)
            self.correct_haptic.move_index_down(index)
            self.wrong_haptic.move_index_down(index)
            self.correct_audio.move_index_down(index)
            self.wrong_audio.move_index_down(index)
