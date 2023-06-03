
# Map_Marker_w_Photos

  

## Installation

Use git clone or download the zip from Github to obtain the code.  
The Jupyter notebook demonstrates how the code works. The Python script is the standard routine. To use the Python script, run
$$
\text{python3 map\_marker.py folder\_path\_1 folder\_path\_2 ... }
$$
where folder_path is the file path to the folder containing the pictures you are interested in putting on a map.

## Result
![Result HTML](./images/result1.png)  
The above image shows the result of the code.  
![Produced HTML](./images/result2.png)  
After the software finished running, you'll see things like "0th_map.html" or "1th_map.html." These are the html produced by the Python script. They will locate **AT** the folder from which you run the Python script. Use a browser to see the resulting html. 

## Note:

1. Adjustment of photo metadata in IPhone will not be reflected in the EXIF data despite what some articles have told you.

	1. You can verify this yourdelf by adjusting the photo, upload it to a EXIF reader website, and see it yourself.

	2. You can also right click the image, go to details, and see the metadata, aka EXIF data, to verify it yourself.

	3. However, you can see the adjusted metadata using another IPhone correctly.

	4. My guess is that when IPhone adjusts the photo, it does not overwrite the exif data but add info about how to get to the desire value.

2. You NEED to enable GPS tracking when taking the photos for this software to work.