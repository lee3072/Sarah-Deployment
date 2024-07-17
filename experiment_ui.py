"""
experiment_ui.py

Author: Seung Heon Lee (University of Southern California, HaRVI Lab)

This file contains the ExperimentUI class, which implements the user interface for
creating and managing experiments. It handles the selection of cases, experiment
configuration, and provides functionality to create new cases within the experiment context.
"""

import os
import json, jsonschema
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from custom_widget import ScrollableFrame, EditableList, LabelEntryRow
from default_configs import load_experiment_config, update_last_used_file_record, LAST_ACCESSED_EXPERIMENT_PATH, DEFAULT_EXPERIMENT_FOLDER
from case_ui import CaseUI

class ExperimentUI(tk.Frame):
    """
    The ExperimentUI class represents the Experiment tab in the GUI application.

    The Experiment tab allows users to create and manage experiment configurations.

    Args:
        parent (tk.Widget): The parent widget for this frame.
    """

    def __init__(self, parent, settings):
        """
        Initializes the ExperimentUI class.

        Args:
            parent (tk.Widget): The parent widget for this frame.
            settings (dict): The application settings.
        """
        super().__init__(parent)
        self.settings = settings
        self.experiment = load_experiment_config()
        self.case_window = None

        self.create_widgets()

    def create_widgets(self):
        # Clear existing widgets if any
        for widget in self.winfo_children():
            if widget != self.case_window:
                widget.destroy()

        # Frame for the save and load buttons at the bottom of the window #
        button_frame = ttk.Frame(self)
        button_frame.pack(fill='x', side="bottom", pady=10)

        ## Create save button
        save_button = ttk.Button(button_frame, text="Save", command=self.save_experiment)
        save_button.pack(side="left", padx=10)

        ## Create load button
        load_button = ttk.Button(button_frame, text="Load", command=self.load_experiment)
        load_button.pack(side="left", padx=10)

        # Create Generate button 
        generate_button = ttk.Button(button_frame, text="Generate", command=self.generate_experiment_json)
        generate_button.pack(side="left", padx=10)

        # Create a scrollable main frame to contain the experiment configurations
        main_frame = ScrollableFrame(self)
        main_frame.pack(fill="both", expand=True)
        main_frame = main_frame.content_frame

        ## Create a frame for the Experiment ID
        experiment_id_frame = ttk.LabelFrame(main_frame, text="Experiment ID", height=60)
        experiment_id_frame.pack(fill="x", expand=True, side="top", padx=10, pady=10)
        experiment_id_frame.pack_propagate(False)  # Prevent resizing of the frame

        ### Create a label and textfield for Experiment ID
        LabelEntryRow(experiment_id_frame, "Experiment ID:", self.experiment['ExperimentID'], entry_callback=lambda x: self.experiment.update({'ExperimentID': x}))

        ## Create a frame for selecting from existing case files
        existing_case_frame = ttk.LabelFrame(main_frame, text="Existing Cases in Case Folder", height=250)
        existing_case_frame.pack(fill="x", expand=True, side="top", padx=10, pady=10)
        existing_case_frame.pack_propagate(False)  # Prevent resizing of the frame

        ### Create a scrollable frame for displaying existing cases in case folder
        self.existing_case_scroll_frame = ScrollableFrame(existing_case_frame)
        self.existing_case_scroll_frame.pack(fill="both", expand=True)
        self.existing_case_scroll_frame = self.existing_case_scroll_frame.content_frame

        self.refresh_available_cases()

        ## Create an Add Selected button
        add_selected_button = ttk.Button(main_frame, text="Add Selected Case To The Experiment", command=self.add_selected_cases)
        add_selected_button.pack(fill="x", padx=10, pady=0)

        ## Create a frame for selected case files
        selected_case_frame = ttk.LabelFrame(main_frame, text="Selected Case Files", height=200)
        selected_case_frame.pack(fill="x", expand=True, side="top", padx=10, pady=10)
        selected_case_frame.pack_propagate(False)  # Prevent resizing of the frame

        ### Create an EditableList for displaying selected case files
        self.selected_case_list = EditableList(
            selected_case_frame,
            [[cf] for cf in self.experiment['CaseFiles']],
            lambda x: self.experiment.update({'CaseFiles': [cf[0] for cf in x]}),
            folder_path=self.settings['FolderVariables']['CaseFolder']
        )
        self.selected_case_list.pack(fill="both", expand=True)

        ## Create a button to generate the new case file
        open_case_creation_window_button = ttk.Button(main_frame, text="Create New Case", command=self.open_case_creation_window)
        open_case_creation_window_button.pack(fill="x", padx=10, pady=10)

        ## Create an input field for Survey URL
        LabelEntryRow(main_frame, "Survey URL:", self.experiment['survey_url'], [""]+[f"{link['nickname']} - {link['url']}" for link in self.settings['Links']], entry_callback=lambda x: self.experiment.update({'survey_url': x}))

    def refresh_available_cases(self):
        """
        Updates the list of case files displayed in the case frame.
        """
        # Clear existing widgets in the case list frame
        for widget in self.existing_case_scroll_frame.winfo_children():
            widget.destroy()

        # Get the case folder path from the settings
        case_folder = self.settings['FolderVariables']['CaseFolder']

        # List all case files in the case folder
        if os.path.exists(case_folder):
            case_files = [f for f in os.listdir(case_folder) if os.path.isfile(os.path.join(case_folder, f))]
        else:
            case_files = []

        # Create a checkbutton for each case file
        self.case_file_vars = {}
        for case_file in case_files:
            var = tk.BooleanVar()
            full_case_path = os.path.join(case_folder, case_file)
            case_checkbutton = ttk.Checkbutton(self.existing_case_scroll_frame, text=case_file, variable=var)
            case_checkbutton.pack(fill="x", padx=10, pady=5)
            self.case_file_vars[full_case_path] = var

    def add_selected_cases(self):
        """
        Adds the selected case files to the list of selected case files.
        """
        for case_file, var in self.case_file_vars.items():
            if var.get():
                self.selected_case_list.add_entry([case_file], folder_path=self.settings['FolderVariables']['CaseFolder'])
                var.set(False)  # Uncheck the case file after adding

    def refresh(self, settings):
        """
        Refresh the file information.
        Update UI elements to reflect the changes.
        """
        self.settings = settings
        self.create_widgets()

    def open_case_creation_window(self):
        """
        Create a new case file using a new window. 
        CaseUI will be separated into case_Ui.py just like SettingsUI and ExperimentUI.
        Only create new window when window doesn't exist.
        """
        
        if not hasattr(self, 'case_window') or self.case_window is None: 
            self.case_window = tk.Toplevel(self)
            self.case_window.title("Create New Case")
            self.case_window.geometry("1450x770")
            self.case_ui = CaseUI(self.case_window, self.settings)
            self.case_ui.pack(fill="both", expand=True)
            # Closing the window will set case_window to None, and destroy the window using lambda function
            self.case_window.protocol("WM_DELETE_WINDOW", lambda: [self.case_window.destroy(), setattr(self, 'case_window', None)])

    def save_experiment(self):
        """
        Save the experiment configurations to a file using a file dialog.
        """
        # Open a file dialog to select the file path, defaulting to the experiment folder, and JSON file type
        file_path = filedialog.asksaveasfilename(initialdir=DEFAULT_EXPERIMENT_FOLDER, title="Save File", defaultextension=".json", filetypes=[("JSON files", "*.json")])
        # If a file path is selected, save the experiment config to the file
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.experiment, file, indent=4)
                update_last_used_file_record(LAST_ACCESSED_EXPERIMENT_PATH, file_path)
                # Show a message box indicating that the experiment were saved successfully
                messagebox.showinfo("Save Experiment Configuration", "Experiment configuration saved successfully.")

    def load_experiment(self):
        """
        Load the experiment configurations from a file using a file dialog.
        """
        # Open a file dialog to select the file path, defaulting to the experiment folder, and JSON file type
        file_path = filedialog.askopenfilename(initialdir=DEFAULT_EXPERIMENT_FOLDER, title="Select File", defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            self.experiment = load_experiment_config(file_path)
            messagebox.showinfo("Load Experiment Configuration", "Experiment configuration loaded successfully.")
            self.create_widgets()

    def generate_experiment_json(self):
        if not self.experiment['ExperimentID']:
            messagebox.showerror("Error", "Please enter an Experiment ID")
            return

        if not self.experiment['CaseFiles']:
            messagebox.showerror("Error", "Please select at least one case file")
            return 

        # Determine the root URL
        if self.settings['use_server_address']:
            root = self.settings['ServerAddress']
        else:
            root = f"https://{self.settings['github_id']}.github.io/{self.settings['github_repo']}"

        # Prepare the layout descriptions with full URLs
        layout_descriptions = []
        for layout in self.settings['layout_descriptions']:
            layout_copy = layout.copy()
            layout_copy['image'] = f"{root}/{layout['image']}"
            layout_descriptions.append(layout_copy)

        # Prepare the case ID array
        case_id_array = [os.path.splitext(os.path.basename(case_file))[0] for case_file in self.experiment['CaseFiles'] if case_file]

        # Extract the survey URL
        survey_url = self.experiment['survey_url'].split(" - ", 1)[-1] if " - " in self.experiment['survey_url'] else self.experiment['survey_url']

        # Prepare the experiment data for required fields
        experiment_data = {
            "user_agreements": self.settings['user_agreements'],
            "layout_descriptions": layout_descriptions,
            "case_id_array": case_id_array,
        }
        # Prepare the experiment data for optional fields
        if survey_url != "": experiment_data["survey_url"] = survey_url 

        # Configure the file name and path
        file_name = f"{self.experiment['ExperimentID']}.json"
        file_path = os.path.join("Files", "Experiment", file_name)  # Using predefined folder structure

        # Verify if experiment data is valid with json schema before writing to file

        format_json = json.dumps(experiment_data, indent=4)
        
        def validate_json(json_data, schema):
            try:
                jsonschema.validate(json.loads(json_data), schema)
                return True
            except jsonschema.exceptions.ValidationError:
                return False

        with open('Schema/experiment.json') as file:
            schema = json.load(file)

        if not validate_json(format_json, schema):
            messagebox.showerror(f"JSON file is not valid for {file_name}")
            return 
        try:
            with open(file_path, 'w') as f:
               f.write(format_json)
            messagebox.showinfo("Success", f"Experiment JSON generated: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate experiment JSON: {str(e)}")