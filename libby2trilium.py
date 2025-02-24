import argparse
import json
import datetime
from trilium_py.client import ETAPI

blanknote = """<h2>Plot</h2>
                            <p>… describe main plot lines …</p>
                            <p>&nbsp;</p>
                            <h2>Main characters</h2>
                            <p>… here put main characters …</p>
                            <p>&nbsp;</p>
                            <h2>Themes</h2>
                            <p>&nbsp;</p>
                            <h2>Genre</h2>
                            <p>scifi / drama / romance</p>
                            <p>&nbsp;</p>
                            <h2>Similar books</h2>
                            <ul>
                            <li>…</li>
                            </ul>"""



def authTrilium(key):
    server_url = 'http://localhost:37840'
    ea = ETAPI(server_url, key)
    # print(ea.app_info())
    return ea

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument( '-k', '--key', action = 'store', type = str, 
        help="File containing the Trilium authentication key")
    parser.add_argument( '-f', '--filename', action = 'store', type = str,
        help="Filename of the json file containing the Libby notes")
    parser.add_argument( '-p', '--parentNote', action = "store", type = str,
        help="ParentNoteId within TriliumNext to send the new note")

    args = parser.parse_args( )

    f = open(args.key, "r")
    lines = f.readlines()
    # print(lines[0])
    ea = authTrilium(lines[0].strip())
    # print (ea)
    rawdata = open(args.filename)
    data = json.loads(rawdata.read())
    # print(data.keys())

    # print(data['readingJourney']['title']['text'])
    # print(data['readingJourney']['title']['url'])
    # print(data['readingJourney']['author'])
    title = data['readingJourney']['title']['text']
    attributemap = {
        "label:readingStart": "promoted,single,date",
        "label:readingEnd": "promoted,single,date",
        "label:link":"promoted,single,url",
        "label:author":"promoted,single,text",
        "iconClass": "bx bx-book-reader",
        "link": data['readingJourney']['title']['url'],
        "author": data['readingJourney']['author'],
        "libbynotes": None
    }


    timestamp_borrowed = 32503622524000 # wake up Fry
    timestamp_returned = 0
    for entry in data["circulation"]: # get first time the book was checked-out.
        if entry["activity"] == 'Borrowed' and entry["timestamp"] < timestamp_borrowed:
            timestamp_borrowed = entry["timestamp"]

        if entry["activity"] == 'Returned' and entry["timestamp"] > timestamp_returned:
            timestamp_returned = entry["timestamp"]
    if timestamp_borrowed < 32503622524000:
        attributemap["readingStart"]  = datetime.datetime.fromtimestamp(timestamp_borrowed/1000).strftime("%Y-%m-%d")
    if timestamp_returned > 0: 
        attributemap["readingEnd"]  = datetime.datetime.fromtimestamp(timestamp_returned/1000).strftime("%Y-%m-%d")

    # print(f'Borrowed on {datetime.datetime.fromtimestamp(timestamp_borrowed/1000).strftime("%Y-%m-%d")}')
    # print(f'Returned on {datetime.datetime.fromtimestamp(timestamp_returned/1000).strftime("%Y-%m-%d")}')
    # print(attributemap)
    note = ea.create_note (args.parentNote, title , "text", None, blanknote)

    for key, val in attributemap.items(): 
        attr = ea.create_attribute(note["note"]["noteId"], type="label", name=key, value=val, isInheritable=False)

    highlights = data["highlights"]
    chapter = ""
    highlightnotes = ""
    for entry in reversed(highlights):
        if chapter != entry["chapter"]:
            chapter = entry["chapter"]
            highlightnotes+=(f"<h2>{chapter}</h2>")
        highlightnotes+=f"<blockquote><p>{entry['quote']}</p></blockquote>"

        if "note" in entry.keys():
            highlightnotes+= f"<p>{entry['note']}</p>"
    ea.create_note (note["note"]["noteId"], "highlights" , "text", None, highlightnotes)
