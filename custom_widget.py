"""
custom_widget.py

Author: Seung Heon Lee (University of Southern California, HaRVI Lab)

This file contains custom Tkinter widget classes used throughout the application.
It includes implementations for ScrollableFrame, EditableList, EditableRow, and
LabelEntryRow, providing reusable UI components for the application.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog

class EditableRow(ttk.Frame):
    """
    A frame that contains entries for multiple text variables and buttons to remove the entry or change its order.

    Args:
        parent (tk.Widget): The parent widget for this frame.
        text_vars (list): A list of text variables for the entries.
        remove_callback (function): The callback function to remove the entry.
        move_up_callback (function): The callback function to move the entry up.
        move_down_callback (function): The callback function to move the entry down.
        order_change_enabled (bool): Whether the order change buttons are enabled.
        delete_enabled (bool): Whether the delete buttons are enabled.
    """
    def __init__(self, parent, text_vars, remove_callback, move_up_callback, move_down_callback, order_change_enabled=True, delete_enabled=True, dropdown_values=None, label_text=None, folder_path=None):
        super().__init__(parent)
        
        self.text_vars = text_vars

        # Set a fixed height for the row
        self.configure(height=28)  # Adjust this value as needed
        self.pack_propagate(False)  # Prevent the frame from shrinking to fit its contents

        if folder_path:
            # Button to open a file dialog
            self.browse_button = ttk.Button(self, text="\U0001F4C2", command=lambda: self.text_vars[0].set(os.path.relpath(filedialog.askopenfilename(initialdir=folder_path)) or self.text_vars[0].get()), width=2)
            self.browse_button.pack(side="right", padx=(0, 5))


        if order_change_enabled:
            # Button to move the entry up
            self.up_button = ttk.Button(self, text="\u2191", command=move_up_callback, width=2)
            self.up_button.pack(side="right", padx=(0, 5))

            # Button to move the entry down
            self.down_button = ttk.Button(self, text="\u2193", command=move_down_callback, width=2)
            self.down_button.pack(side="right", padx=(0, 5))

        if delete_enabled:
            # Button to remove the entry
            self.remove_button = ttk.Button(self, text="X", command=remove_callback, width=2)
            self.remove_button.pack(side="right", padx=(0, 5))

        # Frame to hold the entries
        self.entries_frame = ttk.Frame(self)
        self.entries_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Label if provided
        if label_text:
            self.label = ttk.Label(self.entries_frame, text=label_text)
            self.label.grid(row=0, column=0, sticky="ew", padx=(0, 5))
            self.entries_frame.columnconfigure(0, weight=1)

        # Create entries for each text variable using grid manager
        for i, text_var in enumerate(self.text_vars):
            if dropdown_values:
                entry = ttk.Combobox(self.entries_frame, textvariable=text_var, values=dropdown_values)
            else:
                entry = ttk.Entry(self.entries_frame, textvariable=text_var)
            entry.grid(row=0, column=i + int(label_text is not None), sticky="ew", padx=(0, 5))
            self.entries_frame.columnconfigure(i + int(label_text is not None), weight=1)



    def set_state(self, state):
        """
        Sets the state of all widgets in the entry.

        Args:
            state (str): The state to set ('normal' or 'disabled').
        """
        for widget in self.winfo_children():
            try:
                widget.configure(state=state)
            except tk.TclError:
                pass
        for widget in self.entries_frame.winfo_children():
            try:
                widget.configure(state=state)
            except tk.TclError:
                pass

class EditableList(ttk.Frame):
    """
    A frame that contains a list of entries with buttons to add new entries and optionally change their order.

    Args:
        parent (tk.Widget): The parent widget for this frame.
        entries (list): A list of initial entries. Each entry can be a list of text values.
        entry_callback (function): The callback function to update the entries.
        entry_factory (function, optional): A factory function to create default text variables for a new entry.
        order_change_enabled (bool): Whether the order change buttons are enabled.
        delete_enabled (bool): Whether the delete buttons are enabled.
    """
    def __init__(self, parent, entries, entry_callback, entry_factory=None, order_change_enabled=True, delete_enabled=True, add_enabled=True, move_up_callback=None, move_down_callback=None, dropdown_values=None, label_texts=None, folder_path=None):
        super().__init__(parent)
        
        # List of entry variables and the callback function
        self.entries = []
        self.entry_callback = entry_callback
        self.entry_factory = entry_factory if entry_factory else self.default_entry_factory
        self.order_change_enabled = order_change_enabled
        self.delete_enabled = delete_enabled
        self.dropdown_values = dropdown_values

        if add_enabled:
            # Button to add a new entry
            self.add_button = ttk.Button(self, text="Add Entry", command=lambda: self.add_entry(dropdown_values=dropdown_values,folder_path=folder_path))
            self.add_button.pack(fill="x", padx=10, pady=5, side="bottom")

        # Create a scrollable frame for the list entries
        self.scrollable_frame = ScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True)
        self.scrollable_frame = self.scrollable_frame.content_frame

        self.move_up_callback = move_up_callback
        self.move_down_callback = move_down_callback

        if label_texts:
            # Initialize with existing entries
            for entry, label_text in zip(entries, label_texts):
                self.add_entry(entry, dropdown_values, label_text, folder_path)
        else:
            # Initialize with existing entries
            for entry in entries:
                self.add_entry(entry, dropdown_values, folder_path=folder_path)
    def default_entry_factory(self):
        return [tk.StringVar(value="")]

    def add_entry(self, text_vars=None, dropdown_values=None, label_text=None, folder_path=None):
        """
        Adds a new entry to the list.

        Args:
            text_vars (list[str]): The initial text variables for the entry.
        """
        # Create text variables for the entry
        if text_vars is None:
            text_vars = [tk.StringVar(value="") for _ in range(len(self.entry_factory()))]
        else:
            text_vars = [tk.StringVar(value=text) for text in text_vars]

        # Bind the text variables to update the entries
        for text_var in text_vars:
            text_var.trace_add("write", self.update_entries)

        # Create an entry and add it to the list
        entry = EditableRow(self.scrollable_frame, text_vars, 
                                  lambda: self.remove_entry(entry, text_vars),
                                  lambda: self.move_entry_up(entry) if self.move_up_callback is None else self.move_up_callback(self.scrollable_frame.winfo_children().index(entry)),
                                  lambda: self.move_entry_down(entry) if self.move_down_callback is None else self.move_down_callback(self.scrollable_frame.winfo_children().index(entry)),
                                  self.order_change_enabled,
                                  self.delete_enabled,
                                  dropdown_values=dropdown_values,
                                  label_text=label_text,
                                  folder_path=folder_path)
        entry.pack(fill="x", expand=True, padx=10, pady=5)
        
        # Add the entry to the list
        self.entries.append(text_vars)
        # Update the entries using the callback function
        self.update_entries()

    def remove_entry(self, entry_frame, text_vars):
        """
        Removes an entry from the list.
        
        Args:
            entry_frame (EditableRow): The entry frame to remove.
            text_vars (list): The text variables for the entry.
        """
        entry_frame.destroy()
        self.entries.remove(text_vars)
        self.update_entries()

    def move_entry_up(self, entry_frame):
        """
        Moves an entry up in the list.

        Args:
            entry_frame (EditableRow): The entry frame to move up.
        """
        index = self.scrollable_frame.winfo_children().index(entry_frame)
        if index > 0:
            above_frame = self.scrollable_frame.winfo_children()[index - 1]
            self.swap_entry_text(entry_frame, above_frame)

    def move_index_up(self, index):
        """
        Moves an entry up in the list.

        Args:
            index (int): The index of the entry to move up.
        """
        if index > 0:
            entry_frame = self.scrollable_frame.winfo_children()[index]
            above_frame = self.scrollable_frame.winfo_children()[index - 1]
            self.swap_entry_text(entry_frame, above_frame)

    def move_entry_down(self, entry_frame):
        """
        Moves an entry down in the list.

        Args:
            entry_frame (EditableRow): The entry frame to move down.
        """
        index = self.scrollable_frame.winfo_children().index(entry_frame)
        if index < len(self.scrollable_frame.winfo_children()) - 1:
            below_frame = self.scrollable_frame.winfo_children()[index + 1]
            self.swap_entry_text(entry_frame, below_frame)

    def move_index_down(self, index):
        """
        Moves an entry down in the list.

        Args:
            index (int): The index of the entry to move down.
        """
        if index < len(self.scrollable_frame.winfo_children()) - 1:
            entry_frame = self.scrollable_frame.winfo_children()[index]
            below_frame = self.scrollable_frame.winfo_children()[index + 1]
            self.swap_entry_text(entry_frame, below_frame)

    def swap_entry_text(self, frame1, frame2):
        """
        Swaps the text between two entry frames.

        Args:
            frame1 (EditableRow): The first entry frame.
            frame2 (EditableRow): The second entry frame.
        """
        for text_var1, text_var2 in zip(frame1.text_vars, frame2.text_vars):
            temp = text_var1.get()
            text_var1.set(text_var2.get())
            text_var2.set(temp)

    def update_entries(self, *args):
        """
        Updates the list of entries.
        """
        updated_entries = [[var.get() for var in vars] for vars in self.entries]
        self.entry_callback(updated_entries)
    
    def set_state(self, state):
        """
        Sets the state of all widgets in the list.

        Args:
            state (str): The state to set ('normal' or 'disabled').
        """
        for entry_frame in self.scrollable_frame.winfo_children():
            entry_frame.set_state(state)
        self.add_button.configure(state=state) if hasattr(self, 'add_button') else None
class ScrollableFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Create a canvas
        self.canvas = tk.Canvas(self)
        
        # Add a scrollbar to the canvas
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        
        # Pack the canvas after the scrollbar to make sure scrollbar always appears
        self.canvas.pack(side="left", fill="both", expand=True)

        # Configure the canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Create a frame to contain the content
        self.content_frame = ttk.Frame(self.canvas)
        
        # Create window inside canvas to place the frame
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        
        # Bind the frame size to the canvas
        self.content_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # """ Debugging purpose only """
        # s = ttk.Style()
        # s.configure('My.TFrame', background='red')
        # self.content_frame.configure(style='My.TFrame')
        # """ Debugging purpose only """

    def on_frame_configure(self, event):
        # Update the canvas scroll region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        # Update the scrollable region to encompass the inner frame
        self.canvas.itemconfig(self.canvas_window, width=event.width)

class LabelEntryRow(ttk.Frame):
    def __init__(self, parent, label_text, default_text, dropdown_values=None, entry_callback=None, toggle_val=False, toggle_callback=None):
        """
        Creates a row with a label and an entry widget.

        Args:
            parent (tk.Widget): The parent widget for the row.
            label_text (str): The text for the label.
            textvariable (tk.StringVar): The text variable for the entry widget.
        """
         # Create a frame for the row
        super().__init__(parent)
        self.pack(fill="x", padx=10, pady=5)
        self._dropdown_values = dropdown_values
        self._toggle_callback = toggle_callback

        self.enable_var = tk.BooleanVar(value=toggle_val)
        if self._toggle_callback:
            self.enable_var.trace_add("write", lambda *args: toggle_callback(self.enable_var.get()))
            # Create a toggle button for the row
            self._toggle = ttk.Checkbutton(self, text="Enable", variable=self.enable_var, command=self.toggle_element)
            self._toggle.pack(side="left", padx=10, pady=5)

        # Create a label
        self._label = ttk.Label(self, text=label_text)
        self._label.pack(side="left", padx=10, pady=5)

        self._string_var = tk.StringVar(value=default_text)
        # Call the callback function when the entry is modified and use string_var as its value
        if entry_callback is not None:
            self._string_var.trace_add("write", lambda *args: entry_callback(self._string_var.get()))

        if self._dropdown_values:
             # Create a dropdown widget
            self._dropdown = ttk.Combobox(self, values=dropdown_values, textvariable=self._string_var)
            self._dropdown.pack(side="left", padx=10, pady=5, fill="x", expand=True)
        else:
             # Create an entry widget where entry will expand to fill the remaining space
            self._entry = ttk.Entry(self, textvariable=self._string_var)
            self._entry.pack(side="left", padx=10, pady=5, fill="x", expand=True)
    
        self.toggle_element()

    def toggle_element(self, parent_state = True):
        if self._toggle_callback:
            # Toggle the visibility of the entry or dropdown based on whether it is enabled or disabled.
            if self._dropdown_values:
                self._dropdown["state"] = "enabled" if self.enable_var.get() and parent_state else "disabled"
            else:
                self._entry["state"] = "enabled" if self.enable_var.get() and parent_state else "disabled"

    def set_state(self, state):
        for widge in self.winfo_children():
            widge.configure(state=state)
        self.toggle_element(state != 'disabled')