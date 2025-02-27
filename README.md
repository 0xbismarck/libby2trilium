# libby2trilium
Import your reading notes from [Libby](https://libbyapp.com) into TriliumNext.

## Installation

Python 3 is required on both Linux and Windows.

Download the libby2trilium git repo. 

### On Linux

 ``` 
python3 -m venv venv
source venv/bin/activate
pip install trilium_py
 ``` 

### On Windows

 ``` 
python -m venv venv
venv\Scripts\activate.bat
pip install trilium_py
 ``` 

## API Tokens
Authenticating to TriliumNext Notes requires an API token for each service. 

- Trilium Notes:
  - Click on the "Main menu"
  - Click "Options"
  - Click "ETAPI"
  - Click "Create New ETAPI Token"

Put the token in a text file that will be passed to the command line as a paramater. 

## Usage
Trilium needs to be open for it to receive highlights this tool.

Make sure that the Python virtual environment is activated:

From the Linux terminal:

```source venv/bin/activate```

From the Windows commandline (cmd.exe):

```venv\Scripts\activate.bat```

Note: On Windows type 'python' instead of python3.

Basic execution:

```python3 libby2trilium.py -k key -f libbyjourney-file.json -p BE5Id3adb33f```

This takes the highlights within the libbyjourney-file.json and creates two notes. A top note with the bibliographic information, and a child note that contains highlights and notes from the book. 

### Available options
```
usage: libby2trilium.py [-h] [-k KEY] [-f FILENAME] [-p PARENTNOTE]

options:
  -h, --help            show this help message and exit
  -k KEY, --key KEY     File containing the Trilium authentication key
  -f FILENAME, --filename FILENAME
                        Filename of the json file containing the Libby notes
  -p PARENTNOTE, --parentNote PARENTNOTE
                        ParentNoteId within TriliumNext to send the new note
```
### Locating the NoteID
The noteId for any note can be found by clicking the "Note Info" icon towards the top of the note. After clicking the icon, you will see the field called "Note ID". 

![The NoteId can be found by clicking the Note Info icon](./noteID.png)

This is the value needed for the parentNoteId. 

### Downloading the Libby Reading Notes
For instruction on how to download the json file containing your Libby highlights and notes, visit the following Libby resource for instructions: https://help.libbyapp.com/en-us/6151.htm

Note: This has only been developed against ebooks notes. Audiobook notes have not been tested with this tool.

## Shoutouts
Special thanks to:
- [TriliumNext Notes](https://github.com/TriliumNext/Notes)
- [Trilium-py](https://github.com/Nriver/trilium-py)

These projects made Libby2trilium possibile.
