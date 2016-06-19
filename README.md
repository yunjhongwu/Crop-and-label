# Crop-and-label

Recently I have to manually crop a bunch of photos to create training data for my work related to image processing. I wrote this and it does make my life less miserable.

* Only tested in Python 3.5.1

## How to use this script
 1. Create folders `data/`, `done/`, `samples/` in the same place as the script.
 2. Put photos that you want to crop in *data/*.
 3. Edit `CATEGORIES` line 8 in the script.
 4. Run the script. Once a photo is displayed, crop it by draw rectangles. Once an area is selected, a pop-up window will display options in `CATEGORIES`. Click a category to label the selected area or select `None` to cancel.
 5. Close the image. All crop pieces will be saved to `samples/` and the processed photo will be moved to `done/`.
 6. Next photo will be displayed automatically. Repeat steps 4 and 5 until all photos in `data/` are processed.

If you want to take a break, press `x` to save it and close the window or press `c` to close without saving the cropped pieces.

![Example](https://cloud.githubusercontent.com/assets/6327275/16175193/e9c1cca8-35b2-11e6-8df9-dd80e437fb1e.png)

