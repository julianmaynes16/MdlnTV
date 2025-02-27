from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtGui import QPixmap, QMovie
from PySide6.QtCore import Qt, QRect, QByteArray, QBuffer, QSize
import sys
import requests
import urllib.request

import asyncio
import seventv

class GifWindow(QMainWindow):

    def __init__(self, type , emote):
        super().__init__()
        self.emote_url = None
        self.SearchEmote(self.emote_url)
        self.setStyleSheet("background-color: #1E1E1E;")
        
        self.MovieLabel = QLabel(self)
        asyncio.run(self.SearchEmote(emote))
        self.load_gif()
        

    def load_gif(self):

        response = requests.get(self.emote_url)
        if response.status_code == 200:
            gif_data = response.content  

            
            self.buffer = QBuffer()
            self.buffer.setData(QByteArray(gif_data))
            self.buffer.open(QBuffer.ReadOnly)

       
        self.MovieLabel.setGeometry(QRect(0, 0, 480, 290))
        self.MovieLabel.setAlignment(Qt.AlignCenter)
        self.movie = QMovie(self.buffer)
        self.MovieLabel.setMovie(self.movie)
        self.movie.start()
        

    def change_emote(self, new_gif):
        self.emote_url = self.SearchEmote(new_gif)

    async def SearchEmote(self, emote : str) -> str:
        mySevenTvSession = seventv.seventv()
        # initialize an instance of the seventv() class. this must happen in an asynchronous context

        emotes = await mySevenTvSession.emote_search(emote, case_sensitive=True)

        mySevenTvSession.close() # later close the session
        self.emote_url = "https:" + emotes[0].host_url + "/4x.gif" # get the url from the emote object
        await mySevenTvSession.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GifWindow("name", "AINTNOWAY")
    window.setFixedSize(QSize(480, 290))
    
    # window = GifWindow("https://cdn.7tv.app/emote/01JFEY3QWV7EW547PAVX19ZWNF/4x.webp")
    window.show()
    sys.exit(app.exec_())

