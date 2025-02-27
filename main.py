from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtGui import QPixmap, QMovie
from PySide6.QtCore import Qt, QRect, QByteArray, QBuffer, QSize
import sys
import requests
import urllib.request

import asyncio
import seventv

class GifWindow(QMainWindow):

    def __init__(self, name_type, emote_type, emote):
        super().__init__()
        self.setWindowTitle("MdlnTV")
        self.emote_url = None
        self.buffer = None

        if emote_type not in ["gif", "pic"]:
            print("ERROR: Please identify the type of emote (either \"gif\" or \"pic\")")
            return

        if name_type == "name":
            self.SearchEmote(self.emote_url, emote_type)
        elif name_type == "id":
            self.emote_url = "https://cdn.7tv.app/emote/" + emote + "/4x.gif" if emote_type == "gif" else "https://cdn.7tv.app/emote/" + emote + "/4x.webp"
        else:
            print("ERROR: Please input a valid name type of the emote (either \"name\" or \"id\")")
            return
        
        self.setStyleSheet("background-color: #1E1E1E;")
        
        self.emote_label = QLabel(self)
        self.emote_label.setGeometry(QRect(0, 0, 480, 290))
        self.emote_label.setAlignment(Qt.AlignCenter)

        asyncio.run(self.SearchEmote(emote, emote_type))
        self.load_gif(emote_type)
        

    def load_gif(self, emote_type):

        response = requests.get(self.emote_url)
        
        if response.status_code == 200:
            emote_data = response.content
            emote_to_display = None
            
            
            if emote_type == "gif": 
                self.buffer = QBuffer()
                self.buffer.setData(QByteArray(emote_data))
                self.buffer.open(QBuffer.ReadOnly)
                
                self.movie = QMovie(self.buffer)
                self.emote_label.setMovie(self.movie)
                self.movie.start()

            else:
                pixmap = QPixmap()
                if not pixmap.loadFromData(emote_data):
                    print("ERROR: Failed to load image from data")
                self.emote_label.setPixmap(pixmap)
                self.emote_label.show()
       
        

    def change_emote(self, new_gif):
        self.emote_url = self.SearchEmote(new_gif)

    # The library can only do async stuff and I probably butchered how im doing it. 
    async def SearchEmote(self, emote : str, emote_type : str) -> str:
        mySevenTvSession = seventv.seventv()
        # initialize an instance of the seventv() class. this must happen in an asynchronous context

        emotes = await mySevenTvSession.emote_search(emote, case_sensitive=True)

        mySevenTvSession.close() # later close the session
        self.emote_url = "https:" + emotes[0].host_url + "/4x.gif" if emote_type == "gif" else "https:" + emotes[0].host_url + "/4x.webp"
        await mySevenTvSession.close()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Please provide more arguments.")
    else:
        app = QApplication(sys.argv)
        window = GifWindow(sys.argv[1], sys.argv[2], sys.argv[3])
        window.setFixedSize(QSize(480, 290))
        
        # window = GifWindow("https://cdn.7tv.app/emote/01JFEY3QWV7EW547PAVX19ZWNF/4x.webp")
        window.show()
        sys.exit(app.exec())

