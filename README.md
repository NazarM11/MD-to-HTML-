MD to HTML

MD to HTML is a lightweight, "zero-dependency" Python utility designed to convert Markdown files into clean, structured HTML. Built using pure Python, this tool provides a fast and transparent way to transform your documents without the bloat of external libraries.
✨ Features

    Pure Python: No pip install required. Uses only Python’s powerful standard library.

    Custom Parser: Employs a bespoke parsing logic to handle Markdown syntax (headers, lists, links, and more).

    Recursive Processing: Scans your entire source directory and mirrors the folder structure in the output.

    Template Injection: Easily wraps your content in a custom base.html or string-based layout for consistent styling.

    Portable: Just one or two scripts—perfect for minimal environments or quick automation tasks.

🛠️ Installation

Since this project uses only the Python Standard Library, there is no setup required.

    Clone the repository:

    git clone https://github.com/NazarM11/MD-to-HTML.git
    cd MD-to-HTML

    Verify Python version:
    Make sure you have Python 3.x installed:

    python --version

🚀 Usage

    Add your Markdown:
    Place your .md files into the source directory (e.g., /content).

    Run the script:

    python main.py

    View the Output:
    Find your converted files in the target directory (e.g., /public).

📂 Project Structure
Plaintext

.
├── content/           # Your raw .md files
├── public/            # The generated .html output
├── main.py            # The core conversion logic (Standard Library only)
└── README.md          # Project documentation

⚙️ How it Works

The tool relies on Python's built-in modules (like os and sys) to handle the heavy lifting:

    File System: Uses os.walk to traverse directories and os.path to manage file naming.

    String Processing: Utilizes Python’s robust string manipulation and regex (re module) to identify Markdown patterns and replace them with HTML tags.

    IO Operations: Efficiently reads source files and writes the final HTML strings to disk.
