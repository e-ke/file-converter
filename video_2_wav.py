import os
from tkinter import Button, Label, Entry, filedialog, ttk
import tkinterdnd2 as tkdnd
from moviepy.editor import VideoFileClip
import threading


def browse_file():
    global video_file_path
    new_video_file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.mkv;*.mov;*.avi;*.wmv"), ("All files", "*.*")])
    if new_video_file_path:
        video_file_path = new_video_file_path
    else:
        return
    mp4_entry.delete(0, "end")
    mp4_entry.insert(0, video_file_path)
    output_folder_path = os.path.join(os.path.dirname(video_file_path), "output")
    output_entry.delete(0, "end")
    output_entry.insert(0, output_folder_path)


def convert_to_wav():
    def threaded_convert():
        progress.start()
        file_path = video_file_path
        if file_path:
            input_video = VideoFileClip(file_path)
            input_audio = input_video.audio
            if input_audio is None:
                result_label["text"] = "No audio found in the video."
                progress.stop()
                return

            output_folder_path = output_entry.get()
            if not os.path.exists(output_folder_path):
                os.makedirs(output_folder_path)
            output_file_name = os.path.splitext(os.path.basename(file_path))[0] + "_converted.wav"
            wav_output_path = os.path.join(output_folder_path, output_file_name)
            if os.path.exists(wav_output_path):
                i = 1
                while True:
                    new_output_file_name = os.path.splitext(os.path.basename(file_path))[0] + f"_converted_{i}.wav"
                    new_wav_output_path = os.path.join(output_folder_path, new_output_file_name)
                    if not os.path.exists(new_wav_output_path):
                        wav_output_path = new_wav_output_path
                        break
                    i += 1
            try:
                input_audio.write_audiofile(wav_output_path)
                result_label["text"] = f"Converted: {wav_output_path}"
            except Exception as error:
                result_label["text"] = f"Error: {error}"
        else:
            result_label["text"] = "No file selected."
        progress.stop()

    result_label["text"] = "Converting..."
    convert_thread = threading.Thread(target=threaded_convert)
    convert_thread.start()


def select_output_folder():
    global output_folder_path
    new_output_folder_path = filedialog.askdirectory()
    if new_output_folder_path:
        output_folder_path = new_output_folder_path
        output_entry.delete(0, "end")
        output_entry.insert(0, output_folder_path)
    else:
        print("No output folder selected!")


def open_output_folder():
    output_folder_path = output_entry.get()
    if output_folder_path:
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)
        try:
            os.startfile(output_folder_path)
        except Exception:
            result_label["text"] = "Cannot open output folder."
    else:
        result_label["text"] = "No output folder selected."


def drop(event):
    try: 
        file_path = event.data.strip().strip("{}")  # {}削除: mov, mkv用対処
        print(file_path)
        if file_path.lower().endswith((".mp4", ".mkv", ".mov", ".avi", ".wmv")):  # MOV対応
            mp4_entry.delete(0, "end")
            mp4_entry.insert(0, file_path)
            global video_file_path
            video_file_path = file_path
            output_folder_path = os.path.join(os.path.dirname(file_path), "output")
            output_entry.delete(0, "end")
            output_entry.insert(0, output_folder_path)
            print("drop_ofp:", output_folder_path)
            result_label["text"] = "loaded"
        else:
            result_label["text"] = "Unsupported file format."
    except:
        result_label["text"] = "Unknown error."


app = tkdnd.TkinterDnD.Tk()
app.title("Video to WAV Converter")
app.minsize(400, 345)

video_file_path = ""
output_folder_path = ""

mp4_frame = Label(app)
mp4_frame.pack(fill="x", padx=5, pady=5)

mp4_label = Label(mp4_frame, text="Video file:")
mp4_label.pack(side="left", padx=5, pady=5)

mp4_entry = Entry(mp4_frame)
mp4_entry.pack(side="left", expand=True, fill="x", padx=5, pady=5)

mp4_button = Button(mp4_frame, text="Browse", command=browse_file)
mp4_button.pack(side="left", padx=5, pady=5)


output_frame = Label(app)
output_frame.pack(fill="x", padx=5, pady=5)

output_label = Label(output_frame, text="Output Directory:")
output_label.pack(side="left", padx=5, pady=5)

output_entry = Entry(output_frame)
output_entry.pack(side="left", expand=True, fill="x", padx=5, pady=5)

output_button = Button(output_frame, text="Browse", command=select_output_folder)
output_button.pack(side="left", padx=5, pady=5)

open_output_button = Button(output_frame, text="Open", command=open_output_folder)
open_output_button.pack(side="left", padx=5, pady=5)


dnd_label = Label(app, text="Drop video file here", height=10, relief="groove")
dnd_label.pack(fill="x", padx=5, pady=5)

dnd_label.drop_target_register('DND_Files')
dnd_label.dnd_bind('<<Drop>>', drop)


result_label = Label(app, text="")
result_label.pack(padx=5, pady=5)

convert_button = Button(app, text="Convert", command=convert_to_wav)
convert_button.pack(pady=5)

# Progress bar
progress = ttk.Progressbar(app, mode="determinate", style="black.Horizontal.TProgressbar")
progress.pack(fill="x", padx=5, pady=5)

app.mainloop()