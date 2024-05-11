import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pytube import YouTube
import threading
import os

class VideoDownloader:
    def __init__(self):
        self.stream = None
        self.path = None
        self.finished = False
        self.total_size = 0
        self.bytes_downloaded = 0

    def download_video(self, url, path, quality, audio_only):
        try:
            self.finished = False
            self.path = path

            yt = YouTube(url)
            if audio_only:
                self.stream = yt.streams.filter(only_audio=True).first()
            else:
                self.stream = yt.streams.filter(res=quality).first()
            
            self.total_size = self.stream.filesize

            download_thread = threading.Thread(target=self.download)
            download_thread.start()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def download(self):
        try:
            temp_filename = f"{self.path}/_temp_{self.stream.default_filename}"
            self.stream.download(output_path=self.path, filename='_temp_' + self.stream.default_filename, timeout=None, max_retries=10)
            os.rename(temp_filename, f"{self.path}/{self.stream.default_filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.finished = True

def browse_path():
    path = filedialog.askdirectory()
    if path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, path)

def download_video():
    global downloader
    url = url_entry.get()
    path = path_entry.get()
    quality = quality_var.get()
    audio_only = audio_only_var.get()

    if not url:
        messagebox.showerror("Error", "Please enter a valid YouTube URL.")
        return

    if not os.path.isdir(path):
        messagebox.showerror("Error", "Please select a valid save path.")
        return

    downloader.download_video(url, path, quality, audio_only)

# Create the main window
root = tk.Tk()
root.title("YouTube Video Downloader")

# Create style
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#008CBA", foreground="white")
style.configure("TLabel", padding=6, background="white")
style.configure("TCheckbutton", padding=6, background="white")

# Create labels for URL, save path, and quality
url_label = ttk.Label(root, text="Enter YouTube Video URL:")
url_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
save_label = ttk.Label(root, text="Save Path:")
save_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
quality_label = ttk.Label(root, text="Quality:")
quality_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

# Create entry fields for URL and save path
url_entry = ttk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=5, columnspan=2)
path_entry = ttk.Entry(root, width=50)
path_entry.grid(row=1, column=1, padx=10, pady=5, columnspan=2)

# Create quality dropdown menu
quality_var = tk.StringVar()
quality_choices = ["360p", "480p", "720p", "1080p"]
quality_var.set(quality_choices[0])  # Default quality
quality_menu = ttk.Combobox(root, textvariable=quality_var, values=quality_choices)
quality_menu.grid(row=2, column=1, padx=10, pady=5, columnspan=2)

# Create checkbox for audio-only download
audio_only_var = tk.BooleanVar()
audio_only_checkbox = ttk.Checkbutton(root, text="Download Audio Only", variable=audio_only_var)
audio_only_checkbox.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="w")

# Create browse button to select save path
browse_button = ttk.Button(root, text="Browse", command=browse_path)
browse_button.grid(row=1, column=3, padx=10, pady=5)

# Create download button to initiate download process
download_button = ttk.Button(root, text="Download", command=download_video)
download_button.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

# Initialize downloader object
downloader = VideoDownloader()

# Start the GUI application
root.mainloop()
