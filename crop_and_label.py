import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
import tkinter

CATEGORIES = ('Cake', 'Cat', 'None')
RAW_FOLDER = "data/"
DONE_FOLDER = "done/"
SAMPLE_FOLDER = "samples/"

class Selector:
    def __init__(self, filenames):
        self.filenames = filenames

        try:
            self.filename = next(self.filenames)            
        except:
            print("No more images to be labelled")
        
        self.image = Image.open(RAW_FOLDER + self.filename)
        print("Labeling", self.filename)

        self.counter = 0
        self.fig, self.ax = plt.subplots(1, 1, figsize=(14, 8))
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.x = [0, 0]
        self.y = [0, 0]
        self.samples = {}
        self.on = False
        self.hasNext = True
        self.options = None

        self.ax.imshow(self.image)      

        self.rect = Rectangle((0,0), 0, 0, fill=None, linewidth=2, color="r")
        self.ax.add_patch(self.rect)
        
        self.ax.figure.canvas.mpl_connect('button_press_event', self.press)
        self.ax.figure.canvas.mpl_connect('motion_notify_event', self.move)
        self.ax.figure.canvas.mpl_connect('button_release_event', self.release)
        
        self.fig.canvas.mpl_connect('key_press_event', self.terminate)
        self.fig.canvas.mpl_connect('close_event', self.close)

        plt.show()
        
    def terminate(self, event):
        """
        x: close and save
        c: close without saving
        """
        
        if event.key:
            if event.key == "x":
                self.hasNext = False
                plt.close()
                self.close()
            elif event.key == "c":
                plt.close()
        
    def press(self, event):
        """
        Mouse click event
        """

        if (-1 < event.xdata < self.image.size[0]) and (-1 < event.ydata < self.image.size[1]):
            self.on = True
            self.x[0], self.y[0] = event.xdata, event.ydata

            self.rect.set_visible(True)
            self.rect.set_animated(True)
            self.fig.canvas.draw()
            self.background = self.fig.canvas.copy_from_bbox(self.rect.axes.bbox)
            self.ax.draw_artist(self.rect)
            self.fig.canvas.blit(self.ax.bbox)

    def move(self, event):
        """
        Mousemove event
        """        
        
        if self.on:
            if event.xdata is not None and event.ydata is not None:
                self.x[1], self.y[1] = event.xdata, event.ydata
                self.rect.set_width(abs(self.x[1] - self.x[0]))
                self.rect.set_height(abs(self.y[1] - self.y[0]))
                self.rect.set_xy((min(self.x), min(self.y)))
                
                self.fig.canvas.restore_region(self.background)
                self.ax.draw_artist(self.rect)
                self.fig.canvas.blit(self.ax.bbox)

    def release(self, event):
        """
        Mouse release event
        """
        
        if self.on:
            self.on = False
            self.background = None

            if self.options is not None:
                self.options.window.destroy()
  
            self.options = Select()
            self.options.window.mainloop()            
            self.rect.set_width(0)
            self.rect.set_height(0)
            self.rect.set_visible(False)
            self.fig.canvas.draw()
            self.rect.set_animated(False)

            if self.options.selected != "None":
                points = (int(min(self.x)), int(min(self.y)), 
                          int(max(self.x)), int(max(self.y)))

                self.ax.add_patch(
                    Rectangle(points[:2], 
                              points[2] - points[0], 
                              points[3] - points[1], 
                              fill=None, linewidth=2, 
                              hatch='\\', color="y", alpha=0.5))

                self.ax.text(points[0] + 6, points[1] + 21, 
                             self.options.selected, color="w")
                self.ax.text(points[0] + 5, points[1] + 20, 
                             self.options.selected, color="k")

                self.samples[self.counter] = (self.options.selected, points)
                self.counter += 1
                self.fig.canvas.draw()

            self.options = None        
        
    def close(self, event):
        """
        Close the current image and open the next one
        """
        
        counts = {c: 0 for c in CATEGORIES}
        for i in self.samples:
            label = self.samples[i][0]
            filename = SAMPLE_FOLDER + label + "_" 

            while os.path.exists(filename + str(counts[label]).zfill(5) + ".jpg"):
                counts[label] += 1
                
            self.image.crop(self.samples[i][1]).save(filename + str(counts[label]).zfill(5) + ".jpg")
            
        os.rename(RAW_FOLDER + self.filename, DONE_FOLDER + self.filename)

        if self.options is not None:
            self.options.window.destroy()
        if self.hasNext:
            global sel
            sel = Selector(self.filenames)
        
        
class Select:
    """
    Display options
    """
    def __init__(self):
        self.window = tkinter.Tk()

        self.window.wm_title("Category")
        self.window.bind("<Key>", lambda i: self.key(i))
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.option("None"))

        for category in CATEGORIES:
            tkinter.Button(self.window, text=category, width=30, 
                           command=lambda category=category: self.option(category)).pack()
        self.window.after(100, lambda: self.window.focus_force())
       
    def key(self, event):
        """
        Define shortcuts
        """
        if event.char: 
            i = ord(event.char) - 49
            if 0 <= i < len(CATEGORIES):
                self.option(CATEGORIES[i])

    def option(self, category):
        """
        Save selected option and close the window
        """
        
        self.selected = category
        self.window.destroy()
        
    
if __name__ == '__main__':        
    if not os.path.exists(DONE_FOLDER):
        os.makedirs(DONE_FOLDER)
    if not os.path.exists(SAMPLE_FOLDER):
        os.makedirs(SAMPLE_FOLDER)
 
    files = (f for f in os.listdir("data/") if f[-4:] == ".jpg")
    sel = Selector(files)
