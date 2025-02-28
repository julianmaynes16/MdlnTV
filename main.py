from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtGui import QPixmap, QMovie
from PySide6.QtCore import Qt, QRect, QByteArray, QBuffer, QSize
import sys
import requests
import urllib.request

import asyncio
import seventv

class GifWindow(QMainWindow):

    def __init__(self, i_type, emote):
        super().__init__()
        self.setWindowTitle("MdlnTV")
        self.emote_url = None
        self.buffer = None
        self.animated = None
        self.type = i_type

        self.emote_label = QLabel(self)
        self.emote_label.setGeometry(QRect(0, 0, 480, 290))
        self.emote_label.setAlignment(Qt.AlignCenter)
        
        if self.type == "id":
            self.isAnimated(emote)
            self.emote_url = "https://cdn.7tv.app/emote/" + emote + "/4x.gif" if self.animated else "https://cdn.7tv.app/emote/" + emote + "/4x.png"
        elif self.type != "name":
            print("ERROR: Please input a valid name type of the emote (either \"name\" or \"id\")")
            return
        
        self.setStyleSheet("background-color: #1E1E1E;")
        
        if self.type != id:
            asyncio.run(self.SearchEmote(emote))
        self.load_gif()
        

    def load_gif(self):
        
        response = requests.get(self.emote_url)
        
        if response.status_code == 200:
            emote_data = response.content
            
            if self.animated: 
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
       
    def isAnimated(self, emote_id : str):
        response = requests.get("https://7tv.io/v3/emotes/" + emote_id)
        if(response.status_code == 200):
            emote_json = response.json()
            self.animated = emote_json["animated"]

    def change_emote(self, new_gif):
        self.emote_url = self.SearchEmote(new_gif)

    # The library can only do async stuff and I probably butchered how im doing it. 
    async def SearchEmote(self, emote : str) -> str:
        mySevenTvSession = seventv.seventv()
        # initialize an instance of the seventv() class. this must happen in an asynchronous context

        emotes = await mySevenTvSession.emote_search(emote, case_sensitive=True)

        mySevenTvSession.close() # later close the session
        if(self.type != "id"):
            self.isAnimated(emotes[0].id)
            self.emote_url = "https:" + emotes[0].host_url + "/4x.gif" if self.animated else "https:" + emotes[0].host_url + "/4x.png"
        await mySevenTvSession.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please provide more arguments.")
    else:
        app = QApplication(sys.argv)
        window = GifWindow(sys.argv[1], sys.argv[2])
        window.setFixedSize(QSize(480, 290))
        
        # window = GifWindow("https://cdn.7tv.app/emote/01JFEY3QWV7EW547PAVX19ZWNF/4x.webp")
        window.show()
        sys.exit(app.exec())

