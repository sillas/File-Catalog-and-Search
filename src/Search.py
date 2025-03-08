import os
import subprocess as sp
import tkinter as tk
from tkinter import Menu, Entry, Listbox, END, Frame, Scrollbar, RIGHT, Y, Label, BOTH
from db_connect import collection


def start_search_gui():
    """
    Initializes and starts the file search GUI application.
    This function sets up the main window, search entry, listbox, and context menu
    for the file search application. It allows users to search for files by name,
    view the search results in a listbox, and open files or their locations from
    the search results.
    Functions:
    - search_files(term): Searches for files matching the given term.
    - update_listbox(event): Updates the listbox with search results.
    - open_file(index): Opens the selected file.
    - open_file_location(index): Opens the location of the selected file.
    - on_select(event): Handles double-click event to open the selected file.
    - show_context_menu(event): Displays the context menu for the selected item.
    - highlight_selection(event): Highlights the selected item in the listbox.
    Widgets:
    - root: The main Tkinter window.
    - frame: A frame to hold the search entry and listbox.
    - search_label: A label for the search entry.
    - search_entry: An entry widget for entering search terms.
    - scrollbar: A scrollbar for the listbox.
    - listbox: A listbox to display search results.
    - context_menu: A context menu for additional actions on search results.
    Bindings:
    - <KeyRelease>: Updates the listbox when a key is released in the search entry.
    - <Double-1>: Opens the selected file on double-click.
    - <Button-3>: Shows the context menu on right-click.
    - <Button-1>: Highlights the selected item on left-click.
    """

    # Global variable to store search results
    results = []

    def search_files(term):
        """
        Searches for files in the collection that match the given term.
        Args:
            term (str): The search term to look for in the file names.
        Returns:
            list: A list of tuples where each tuple contains the path and the file name 
                  that matches the search term. Returns an empty list if the search term 
                  is empty or no matches are found.
        Note:
            The search is case-insensitive and uses regular expressions to match the term 
            within the file names.
        """
        if not term.strip():
            return []  # Retorna uma lista vazia se a pesquisa estiver vazia

        query = {"files": {"$regex": term, "$options": "i"}}
        search_results = []

        for doc in collection.find(query):
            for file in doc["files"]:
                if term.lower() in file.lower():
                    search_results.append((doc["path"], file))
        return search_results

    def update_listbox(event):
        """
        Updates the listbox with search results based on the term entered in the search entry.
        This function is triggered by an event (e.g., a key press) and performs the following steps:
        1. Retrieves the search term from the search entry widget.
        2. Searches for files matching the term using the search_files function.
        3. Clears the current contents of the listbox.
        4. Inserts the search results into the listbox, displaying the file name and its path.
        Args:
            event: The event that triggered the function (e.g., a key press event).
        """
        nonlocal results

        term = search_entry.get()
        results = search_files(term)

        listbox.delete(0, END)
        for path, file in results:
            listbox.insert(END, f"{file} ({path})")

    def open_file(index):
        """
        Opens a file from the search results using the default application.

        Args:
            index (int): The index of the file in the search results to open.

        Raises:
            IndexError: If the provided index is out of range of the search results.
            FileNotFoundError: If the file does not exist at the specified path.
        """
        path, file = results[index]
        file_path = os.path.realpath(os.path.join(path, file))
        sp.Popen([file_path], shell=True)

    def open_file_location(index):
        """
        Opens the file explorer and selects the file at the given index in the results list.

        Args:
            index (int): The index of the file in the results list to be opened.

        Raises:
            IndexError: If the index is out of range of the results list.
        """
        path, file = results[index]
        file_path = os.path.realpath(os.path.join(path, file))
        sp.Popen(f'explorer /select,"{file_path}"')

    def on_select(event):
        """
        Event handler for selecting an item from a widget.

        Args:
            event: The event object containing information about the selection event.

        This function retrieves the widget from the event, gets the index of the selected item,
        and calls the open_file function with the selected index.
        """
        w = event.widget
        index = int(w.curselection()[0])
        open_file(index)

    def show_context_menu(event):
        """
        Displays a context menu at the location of the event.

        Args:
            event (tkinter.Event): The event object containing information about the event that triggered this function.

        The function performs the following actions:
            1. Identifies the widget that triggered the event.
            2. Determines the index of the nearest item in the widget to the event's y-coordinate.
            3. Clears any existing selection in the listbox.
            4. Selects the item at the identified index.
            5. Configures the context menu to open the file location corresponding to the selected item.
            6. Displays the context menu at the event's root x and y coordinates.
        """
        w = event.widget
        index = w.nearest(event.y)
        listbox.selection_clear(0, END)
        listbox.selection_set(index)  # Destaca o item selecionado
        context_menu.entryconfig(
            "Abrir local do arquivo", command=lambda: open_file_location(index))
        context_menu.post(event.x_root, event.y_root)

    def highlight_selection(event):
        """
        Highlights the item in the listbox closest to the y-coordinate of the event.

        Args:
            event: The event object containing information about the mouse event.
        """
        listbox.selection_clear(0, END)
        index = listbox.nearest(event.y)
        listbox.selection_set(index)

    root = tk.Tk()
    root.title("File Search")

    frame = Frame(root)
    frame.pack(fill=BOTH, expand=True, pady=10)

    search_label = Label(frame, text="Search")
    search_label.pack(side="top", anchor="w", padx=10)

    search_entry = Entry(frame, width=50)
    search_entry.pack(side="top", fill=BOTH, padx=10)
    search_entry.bind("<KeyRelease>", update_listbox)

    scrollbar = Scrollbar(frame, orient="vertical")
    scrollbar.pack(side=RIGHT, fill=Y)

    listbox = Listbox(frame, width=100, yscrollcommand=scrollbar.set)
    listbox.pack(side="left", fill=BOTH, expand=True)
    scrollbar.config(command=listbox.yview)

    listbox.bind("<Double-1>", on_select)
    listbox.bind("<Button-3>", show_context_menu)
    listbox.bind("<Button-1>", highlight_selection)

    # Menu de contexto
    context_menu = Menu(root, tearoff=0)
    context_menu.add_command(label="Abrir local do arquivo")

    root.mainloop()
