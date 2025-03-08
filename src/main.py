
import tkinter as tk
from tkinter import Label, Button
from tkinter.scrolledtext import ScrolledText

from Indexing import start_indexing
from Search import start_search_gui


def main():
    """
    Main function to create and run the Tkinter GUI for the File Indexer & Search application.
    It sets up the main window, adds buttons for searching and indexing files, and initializes
    a ScrolledText widget for output display.
    """
    root = tk.Tk()
    root.title("File Indexer & Search")
    root.geometry("500x400")

    output_widget = ScrolledText(
        root,
        height=10,
        width=60,
        state=tk.NORMAL)

    Label(
        root,
        text="Choose an option:").pack(pady=10)

    Button(
        root,
        text="Search Files",
        command=start_search_gui, width=20, bg="light blue", cursor="hand2").pack(pady=5)

    Button(
        root,
        text="Index Files",
        command=lambda: start_indexing(output_widget), width=20, cursor="hand2").pack(pady=5)

    output_widget.pack_forget()

    root.mainloop()


if __name__ == "__main__":
    main()
