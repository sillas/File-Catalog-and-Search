import os
import json
from time import sleep
import threading
import tkinter as tk
from tkinter import filedialog
from db_connect import collection


def index_files(base_path, output_widget=None):
    """
    Index files in the given base path and log the process.
    This function traverses the directory tree rooted at `base_path`, indexing files with specific extensions.
    It logs the progress to an optional output widget, stores the indexed files in a MongoDB collection, and
    saves duplicate files in a JSON file.
    Args:
        base_path (str): The root directory to start indexing from.
        output_widget (tk.Text, optional): A Tkinter Text widget to log messages. Defaults to None.
    Returns:
        None
    """
    dic = {}
    copy = {}

    # default extensions
    accept = ["pdf", "xml",
              "doc", "mobi", "epub",
              "rar", "zip"]

    def log(message=None):
        """
        Logs a message to the output widget.

        If a message is provided, it inserts the message into the output widget,
        scrolls to the end, and makes the widget visible. If no message is provided,
        it clears the output widget and hides it.

        Args:
            message (str, optional): The message to log. Defaults to None.
        """
        if output_widget:
            if message:
                output_widget.insert(tk.END, message + "\n")
                output_widget.see(tk.END)
                output_widget.pack(pady=5)
            else:
                output_widget.delete(1.0, tk.END)
                output_widget.pack_forget()

    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            accept = config.get(
                "accepted_extensions",
                accept
            )

    except FileNotFoundError:
        log("Configurtion file not found. Using default extensions.")

    except json.JSONDecodeError:
        log("Error loading configurations. Using default extensions.")

    except Exception as e:
        print(f"Error loading configurations: {e}")
        return

    log("Iniciando indexação...")

    for root, _, files in os.walk(base_path, topdown=False):
        root = root.replace('\\', '/')
        log(f"Indexando: {root}")

        for name in files:
            if name.split(".")[-1].lower() in accept:
                if root not in dic:
                    dic[root] = []
                dic[root].append(name)

                if name not in copy:
                    copy[name] = []
                copy[name].append(root)

    # Remove arquivos únicos do dicionário de duplicatas
    new_copy = {k: v for k, v in copy.items() if len(v) > 1}

    # Inserção no MongoDB
    for root, files in dic.items():
        collection.update_one({"path": root},
                              {"$set": {"files": files}},
                              upsert=True)

    # Salvar duplicatas em JSON
    if new_copy:
        with open("DuplicateFiles.json", 'w', encoding='utf-8') as f:
            json.dump(new_copy, f, indent=4, ensure_ascii=False)

    log("Finished indexing.")
    log(', '.join(accept))
    sleep(5)
    log()


def start_indexing(output_widget):
    """
    Initiates the file indexing process by prompting the user to select a directory and 
    starting a new thread to perform the indexing.

    Args:
        output_widget: A widget to display the output of the indexing process.
    """
    base_path = filedialog.askdirectory()
    if base_path:
        threading.Thread(target=index_files, args=(
            base_path, output_widget), daemon=True).start()
