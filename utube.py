import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pytube import YouTube

# Main Application Class
class StreamSaverPro(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("StreamSaver Pro")
        self.geometry("600x450")
        self.resizable(False, False)  # Prevent window from being resized

        # Create and place widgets
        self.create_widgets()

    def create_widgets(self):
        # Styling configuration
        label_font = ('Arial', 12)
        entry_font = ('Arial', 12)
        
        # URL Label and Entry Field
        self.url_label = tk.Label(self, text="YouTube URL:", font=label_font)
        self.url_label.pack(pady=10)
        
        self.url_entry = tk.Entry(self, font=entry_font, width=50)
        self.url_entry.pack(pady=5)
        
        # Fetch Video Info Button
        self.fetch_btn = tk.Button(self, text="Fetch Video Info", font=label_font, command=self.fetch_video_info)
        self.fetch_btn.pack(pady=10)
        
        # Video Title Label (dynamically updated)
        self.title_label = tk.Label(self, text="Video Title:", font=label_font)
        self.title_label.pack(pady=10)
        
        # Video Quality Options
        self.quality_label = tk.Label(self, text="Select Quality:", font=label_font)
        self.quality_label.pack(pady=5)

        self.quality_combobox = ttk.Combobox(self, font=entry_font, state="readonly", width=30)
        self.quality_combobox.pack(pady=5)

        # Select Directory Button
        self.dir_btn = tk.Button(self, text="Select Download Folder", font=label_font, command=self.select_directory)
        self.dir_btn.pack(pady=10)
        
        # Download Button
        self.download_btn = tk.Button(self, text="Download Video", font=label_font, command=self.download_video, state="disabled")
        self.download_btn.pack(pady=20)

        # Progress Bar for download progress
        self.progress = ttk.Progressbar(self, length=400, mode="determinate")
        self.progress.pack(pady=10)
        
        # Output directory for downloaded files
        self.output_dir = ""

    def fetch_video_info(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a valid YouTube URL.")
            return

        try:
            # Fetch video info using pytube
            self.yt = YouTube(url, on_progress_callback=self.progress_callback)
            self.title_label.config(text=f"Video Title: {self.yt.title}")
            
            # Populate quality combobox with available streams
            self.streams = self.yt.streams.filter(progressive=True, file_extension='mp4')
            self.quality_combobox['values'] = [f"{stream.resolution} ({round(stream.filesize / 1048576, 2)} MB)" for stream in self.streams]
            self.quality_combobox.current(0)  # Select the first quality option
            self.download_btn.config(state="normal")  # Enable the download button

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch video info: {str(e)}")

    def select_directory(self):
        self.output_dir = filedialog.askdirectory()
        if self.output_dir:
            messagebox.showinfo("Directory Selected", f"Selected Folder: {self.output_dir}")

    def download_video(self):
        selected_quality = self.quality_combobox.get()
        if not selected_quality:
            messagebox.showerror("Error", "Please select a video quality.")
            return
        if not self.output_dir:
            messagebox.showerror("Error", "Please select a download folder.")
            return

        # Find the selected stream from quality combo
        stream_index = self.quality_combobox.current()
        stream = self.streams[stream_index]

        try:
            # Reset progress bar
            self.progress['value'] = 0
            # Start download
            stream.download(output_path=self.output_dir)
            messagebox.showinfo("Success", "Download completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download video: {str(e)}")

    def progress_callback(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        self.progress['value'] = percentage_of_completion
        self.update_idletasks()

# Main loop
if __name__ == "__main__":
    app = StreamSaverPro()
    app.mainloop()
