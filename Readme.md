# File Catalog and Search

This project is a file cataloging application that allows users to index and search for files within a specified directory. The application uses MongoDB to store the indexed files and provides a graphical user interface (GUI) built with Tkinter for easy interaction.

## Features

- Index files in a specified directory and store the information in MongoDB.
- Search for files by name using a search term.
- Open files or their containing directories directly from the search results.
- Log indexing progress and display it in the GUI.

## Installation and Setup

### Prerequisites

- Python 3.x
- MongoDB

### MongoDB Installation and Configuration

1. **Download and Install MongoDB:**
   - Follow the instructions on the [MongoDB installation page](https://docs.mongodb.com/manual/installation/) to download and install MongoDB for your operating system.

2. **Start MongoDB:**
   - After installation, start the MongoDB server. You can do this by running the following command in your terminal or command prompt:
     ```sh
     mongod
     ```

### Project Setup

1. **Clone the Repository:**
   - Clone the project repository from GitHub:
     ```sh
     git clone git@github.com:sillas/File-Catalog-and-Search.git
     cd File-Catalog-and-Search
     ```

2. **Install Dependencies:**
   - Install the required Python packages using pip:
     ```sh
     pip install -r requirements.txt
     ```

3. **Run the Application:**
   - Start the application by running the main script:
     ```sh
     python main.py
     ```

## Usage

1. **Index Files:**
   - Click the "Index Files" button to select a directory and start indexing the files. The progress will be logged in the output widget.

2. **Search Files:**
   - Click the "Search Files" button to open the search GUI. Enter a search term to find files by name. Double-click a result to open the file, or right-click to open the containing directory.

## Generating an Executable

To generate an executable for the application, you can use a tool like PyInstaller.

1. **Install PyInstaller:**
   ```sh
   pip install pyinstaller
   ```

2. **Generate the Executable:**
   ```sh
   pyinstaller --onefile main.py
   ```

3. **Run the Executable:**
   - The executable will be created in the `dist` directory. You can run it by navigating to the `dist` directory and executing the file.

## Future Goals
- **Separate GUI creation into main.py:**
    - Refactor the code to ensure that the graphical user interface (GUI) is created and managed solely within the `main.py` file. This will help in organizing the code better and making it more maintainable.

- **Improve Search Functionality:**
  - Add advanced search options, such as filtering by file type or date modified.

- **Enhance the GUI:**
  - Improve the user interface with additional features and better design.

- **Add Error Handling:**
  - Implement more robust error handling and logging mechanisms.

- **Create a Web Interface:**
  - Develop a web-based interface for remote access and management of the file catalog.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.