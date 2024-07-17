"""
main.py

Author: Seung Heon Lee (University of Southern California, HaRVI Lab)

This file contains the main application class (MainApplication) which sets up the
GUI window and manages the tab control for the Settings and Experiment interfaces.
It serves as the entry point for the Experiment Generation GUI application.
"""

import tkinter as tk
from tkinter import ttk
from settings_ui import SettingsUI
from experiment_ui import ExperimentUI

class MainApplication(tk.Tk):
    """
    The main application class that represents the GUI application.
    """

    def __init__(self):
        """
        Initializes the MainApplication class.
        """
        # Initialize the Tkinter Application
        super().__init__()
        # Set the title of the main window
        self.title("Main Application")
        # Set the size of the main window
        self.geometry("500x770")
        # Create the tabs in the main window
        self.create_tabs()
        # Record current tab
        self.current_tab = self.tab_control.tabs()[0]

    def create_tabs(self):
        """
        Creates the tab control and adds tabs to it.
        """
        # Create a tab control
        self.tab_control = ttk.Notebook(self)
        
        # Create the settings tab
        self.settings_tab = SettingsUI(self.tab_control)
        self.tab_control.add(self.settings_tab, text="Settings")
        
        # Create the experiment tab
        self.experiment_tab = ExperimentUI(self.tab_control, self.settings_tab.settings)
        self.tab_control.add(self.experiment_tab, text="Experiment")
        
        # Add the tab control to the main window
        self.tab_control.pack(fill="both", expand=True)

        # Bind the tab change event
        self.tab_control.bind("<<NotebookTabChanged>>", self.handle_tab_change)

    def handle_tab_change(self, event):
        """
        Callback function that is called when the tab is changed.
        """
        selected_tab = event.widget.select()

        # If user tries to change the tab while a case window is open, prevent the change
        if self.current_tab == self.tab_control.tabs()[1] and self.experiment_tab.case_window is not None:
            event.widget.select(self.current_tab)
            return
        # If the selected tab is the experiment tab, refresh its content
        if selected_tab == self.tab_control.tabs()[1]:
            self.experiment_tab.refresh(self.settings_tab.settings)

        self.current_tab = selected_tab

# Main.py should be the entry point of the application. 
# It should create an instance of the MainApplication class and run the main application loop.
if __name__ == "__main__":
    # Create the main application
    app = MainApplication()
    # Run the main application
    app.mainloop()