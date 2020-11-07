import os
import tkinter as tk
import tkinter.messagebox as MessageBox
from tkinter.font import Font
from tkinter.filedialog import askdirectory as askDirectory

import datetime

from pathlib import Path
from threading import Thread

from pytube import YouTube as Youtube

from PIL import ImageTk,Image

#custom module
from formatting import format_views
from image import *

"""
    Youtube Downloader with GUI 
    Created by Aghnat HS
    Using Python,Tkinter and Pytube.
"""
#about
AUTHOR = "Aghnat HS"
VERSION = "1.2.1"
#default download directory
DIRECTORY = os.path.dirname(os.path.abspath('Main.py'))+"\downloaded_videos"
THUMBNAIL_IMG = "tmp_thumbnail/tmp1.png"

class Youtube(Youtube):
    
    def on_finished_downloading(self,stream,file_path):
        if stream.type != "audio":
            MessageBox.showinfo("Finished",f"Download is Finished\nLocation:\n{file_path}")
        else:
            path = Path(file_path)
            new_path = str(path.parent) + "/" + path.stem + ".mp3"
            path=path.rename(new_path)
            MessageBox.showinfo("Finished",f"Download is Finished\nLocation:\n{path}")

    def proceed_download(self,arg):
        def callback(arg):
            global DIRECTORY
            #check if user want to download a video or an audio
            if arg!="mp3":
                #download video version
                stream = self.streams.filter(progressive=True,res=arg)
                MessageBox.showinfo("Downloading Video","Your video is downloading right now.\nPlease dont close or exit application")
                stream.first().download(DIRECTORY)
            else:
                #download audio version only
                stream = self.streams.filter(only_audio=True,mime_type="audio/mp4")
                MessageBox.showinfo("Downloading Audio","Your mp3 is downloading right now.\nPlease dont close or exit application")

                audio_file_name = self.title + " (Audio Only)"
                stream.first().download(DIRECTORY,audio_file_name)

        Thread(target = callback ,args=(arg,)).start()

    def get_resolution(self): 
        _resolution = [stream.resolution for stream in self.streams.filter(progressive=True)]
        _resolution.insert(0,"mp3")
        return _resolution

    def get_info(self):
        _title = self.title
        _author = self.author
        _length = str(datetime.timedelta(seconds=self.length))
        _views = str(self.views)
        _rating = str("{:.2f}".format(self.rating))
        return {
                    "title"  : _title,
                    "author" : _author,
                    "length" : _length,
                    "views"  : _views,
                    "rating" : _rating
               }

class App():

    def __init__(self,width,height):
        #init main window
        self.app = tk.Tk()
        self.app.geometry(f"{width}x{height}")
        self.app.resizable(0,0)
        self.app.title(f"Youtube Downloader by Aghnat HS ({VERSION})")
        #font
        self.fontTitle = Font(family="Helvetica",size=15,weight="bold")
        #create button layout for main window
        self.create_layout()
        #loop main window
        self.app.mainloop()
    
    def create_layout(self):
        #create the layout
        self.yt_label = tk.Label(self.app,text="Please Enter a Youtube Link")
        self.yt_link_entry = tk.Entry(self.app,width=50,bg="white",fg="blue")
        self.yt_proceed = tk.Button(self.app,text="Proceed",bg="blue",fg="white",cursor="hand2",
                                    command=lambda:self.create_download_window(self.yt_link_entry.get()),
                                    relief=tk.RAISED)
        self.yt_link_clear = tk.Button(self.app,text="Clear",bg="blue",fg="white",cursor="hand2",
                                    command=lambda:self.yt_link_entry.delete(0,"end"),
                                    relief=tk.RAISED)
        #packing the layout
        self.yt_label.place(relx=0.5,rely=0.23,anchor=tk.CENTER)
        self.yt_link_entry.place(relx=0.5,rely=0.35,anchor=tk.CENTER)
        self.yt_proceed.place(relx=0.45,rely=0.55,anchor=tk.CENTER)
        self.yt_link_clear.place(relx=0.55,rely=0.55,anchor=tk.CENTER)
    def create_download_window(self,link):
        #width and height for canvas
        canvas_width = 16 * 30
        canvas_height = 9 * 30
        #width and height for TopLevel window
        window_width = 500
        window_heigth = 400
        #main function
        def callback():
            global DIRECTORY
            try:
                #instantianting Youtube Object
                youtube = Youtube(link)
                youtube.register_on_complete_callback(youtube.on_finished_downloading)
            except Exception as er:
                print (er)
                MessageBox.showwarning("Error","Something went wrong,please try again")
            else:
                self.download_window = tk.Toplevel(self.app)
                self.download_window.resizable(0,0)
                self.download_window.title("Download")
                self.download_window.geometry(f"{window_width}x{window_heigth}")
                self.download_window.focus()
                #create thumbnail
                image_download(youtube.thumbnail_url)
                self.thumbnail =ImageTk.PhotoImage(Image.open(THUMBNAIL_IMG).resize((canvas_width,canvas_height)))
                #------CREATE GUI
                #create the thumbnail canvas
                video_thumbnail_canvas = tk.Canvas(self.download_window,width=canvas_width,height=canvas_height)
                video_thumbnail_canvas.create_image(0,0,anchor=tk.NW,image=self.thumbnail)
                video_thumbnail_canvas.pack()
                #create the button
                video_output_folder = tk.Button(self.download_window,text="Folder",font=self.fontTitle,relief=tk.RIDGE,command=lambda:self.select_directory())
                video_output_folder.place(relx=0.19,rely=0.75,anchor=tk.CENTER)

                video_info = tk.Button(self.download_window,text="Info",font=self.fontTitle,relief=tk.RIDGE,command=lambda:self.create_video_info(youtube))
                video_info.place(relx=0.325,rely=0.75,anchor=tk.CENTER)

                video_download = tk.Button(self.download_window,text="Download",bg="green",fg="white",font=self.fontTitle,relief=tk.RIDGE,command=lambda:youtube.proceed_download(self.res.get()))
                video_download.place(relx=0.5,rely=0.75,anchor=tk.CENTER)

                res_list = tuple(youtube.get_resolution())
                self.res = tk.StringVar()
                self.res.set(res_list[len(res_list)-1])
                video_res_option = tk.OptionMenu(self.download_window, self.res, *res_list)
                video_res_option.config(font=self.fontTitle,width=5,relief=tk.RIDGE)
                video_res_option.place(relx=0.72,rely=0.75,anchor=tk.CENTER) 
                #create another gui
                self.dir_label = tk.Label(self.download_window,text=f"Download Directory\n{DIRECTORY}",wraplength=window_width-5)
                self.dir_label.place(relx=0.5,rely=0.85,anchor=tk.CENTER) 
            
        Thread(target = callback ,args=()).start()

    def create_video_info(self,video):
        #width and height for top level
        width = 550
        heigth = 300
        #create main
        self.video_info_window = tk.Toplevel(self.download_window)
        self.video_info_window.resizable(0,0)
        self.video_info_window.title("Video Info")
        self.video_info_window.geometry(f"{width}x{heigth}")
        self.video_info_window.focus()
        #get video info
        video_info = video.get_info()
        video_info_title = video_info["title"]
        video_info_author = video_info["author"]
        video_info_length = video_info["length"]
        video_info_views = format_views(video_info["views"])
        video_info_rating = video_info["rating"]
        #create the label
        wraplength = width - 5
        info_title_label = tk.Label(self.video_info_window,text=f"-Title-\n{video_info_title}",font=self.fontTitle,wraplength=wraplength)
        info_author_label = tk.Label(self.video_info_window,text=f"-Author-\n{video_info_author}",font=self.fontTitle,wraplength=wraplength)
        info_length_label = tk.Label(self.video_info_window,text=f"-Length-\n{video_info_length}",font=self.fontTitle,wraplength=wraplength)
        info_views_label = tk.Label(self.video_info_window,text=f"-Views-\n{video_info_views}",font=self.fontTitle,wraplength=wraplength)
        info_rating_label = tk.Label(self.video_info_window,text=f"-Rating-\n{video_info_rating}",font=self.fontTitle,wraplength=wraplength)

        
        info_title_label.pack()
        info_author_label.pack()
        info_length_label.pack()
        info_views_label.pack()
        info_rating_label.pack()

    def select_directory(self):
        global DIRECTORY
        DIRECTORY = askDirectory(title="Select Directory",initialdir=DIRECTORY)
        self.dir_label.config(text=f"Download Directory\n{DIRECTORY}")
        self.download_window.focus()
        
app = App(500,150)