
import tkinter as tk
import mosaic
import helper_mosaic


def main():
    global picture
    ProcessesImage.place(x=InfLoc[0], y=InfLoc[1])
    picture = helper_mosaic.mosaic.load_image(image_name_entry.get())
    ProcessesImage.place_forget()
    ProcessesTiles.place(x=InfLoc[0], y=InfLoc[1])
    tiles = mosaic.build_tile_base(folder_name_entry.get(), int(tiles_height_entry.get()))
    ProcessesTiles.place_forget()
    num_candidates = int(num_candidates_entry.get())
    CreateMosaic.place(x=InfLoc[0], y=InfLoc[1])
    helper_mosaic.make_mosaic(picture, tiles, num_candidates)
    helper_mosaic.mosaic.save(picture, mosaic_name_entry.get())
    CreatedSuccess.place(x=InfLoc[0], y=InfLoc[1])
    if show.get():
        helper_mosaic.mosaic.show(picture)


"""
GUI app for PhotoMosaic creator
"""
win = tk.Tk()
win.title("PhotoMosaic")
win.geometry("600x300")

image_name_label = tk.Label(win, text="The image's name:").place(x=40, y=40)  # x=width, y=height
image_name_entry = tk.Entry(win)
image_name_entry.place(x=40, y=60)

folder_name_label = tk.Label(win, text="Enter the name of the tiles folder:").place(x=40, y=90)
folder_name_entry = tk.Entry(win)
folder_name_entry.place(x=40, y=110)

tiles_height_label = tk.Label(win, text="Enter the height of the tiles: ", justify="left").place(x=40, y=140)
tiles_height_entry = tk.Entry(win)
tiles_height_entry.place(x=40, y=160)

num_candidates_label = tk.Label(win, text="How many candidates?", justify="left").place(x=250, y=40)
num_candidates_entry = tk.Entry(win)
num_candidates_entry.place(x=250, y=60)

mosaic_name_label = tk.Label(win, text="What name would you like to give your mosaic?"
                                       "\n(as well add the extension.jpg at the end)").place(x=250, y=90)
mosaic_name_entry = tk.Entry(win)
mosaic_name_entry.place(x=250, y=130)

show = tk.IntVar()
show_mosaic = tk.Checkbutton(win, text="Open the mosaic at the end to see ", variable=show)
show_mosaic.place(x=250, y=160)


picture = ''
create_mosaic = tk.Button(win, text="Create mosaic!", fg="white", bg="red", command=main).place(x=60, y=200)

# information labels
InfLoc = (40, 230)
ProcessesImage = tk.Label(win, text="Processes image...", fg='blue')
ProcessesTiles = tk.Label(win, text="Processes tiles...", fg='blue')
CreateMosaic = tk.Label(win, text="Create mosaic, pleas wait...", fg='blue')
CreatedSuccess = tk.Label(win, text="Mosaic Created Successfully", fg='blue')

credit = tk.Label(win, text="Written by Shmuel Safrin and Eytan Ahvivi").place(x=350, y=200)

if __name__ == '__main__':
    win.mainloop()

