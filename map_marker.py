from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
import sys
import statistics
import folium
import base64
from folium import IFrame

def get_GPS(iname):
    image = Image.open(iname)
    exif = { TAGS[k]: v for k, v in image._getexif().items() if k in TAGS } # get metadata

    # flip image if needed and update orientation, 
    # check http://sylvana.net/jpegcrop/exif_orientation.html for details
    need_flip = [2,4,5,7]
    correspond_orientation = [1,3,8,6]
    mapping = res = dict(zip(need_flip, correspond_orientation))
    if exif['Orientation'] in need_flip:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
        exif['Orientation'] = mapping(exif['Orientation'])

    # rotate image if needed
    if exif['Orientation'] == 3:
        image = image.rotate(180, expand=True)
    elif exif['Orientation'] == 6:
        image = image.rotate(270, expand=True)
    elif exif['Orientation'] == 8:
        image = image.rotate(90, expand=True)
        
    image = image.resize((350, 350), Image.Resampling.LANCZOS)
    image.save(iname + ".temp", 'jpeg', quality=100)
    
    return exif['GPSInfo'] if 'GPSInfo' in exif else None

def convert_to_degress(value):
    return value[0] + (value[1] / 60.0) + (value[2] / 3600.0)

def get_coord(gps):
    if gps is None:
        return ()
    latitude = gps[2]
    latitude_ref = gps[1]
    longitude = gps[4]
    longitude_ref = gps[3]
    if latitude:
        lat_value = convert_to_degress(latitude)
        if latitude_ref != 'N':
            lat_value = -lat_value
    else:
        return ()
    if longitude:
        lon_value = convert_to_degress(longitude)
        if longitude_ref != 'E':
            lon_value = -lon_value
    else:
        return ()
    return (lat_value, lon_value)

def add_to_map(m,iname,coord):
    encoded = base64.b64encode(open(iname, 'rb').read())
    html = '<img src="data:image/png;base64,{}">'.format
    iframe = IFrame(html(encoded.decode('UTF-8')), width=370, height=370)

    popup = folium.Popup(iframe, max_width=550)
    icon=folium.Icon(color = 'gray',icon='globe')
    folium.Marker(location=coord, popup = popup, icon=icon).add_to(m)

if __name__ == "__main__":
    if len(sys.argv[1:]) == 0:
        print("You need to provide file path to folders containing pictures in this format:")
        print("python3 map_marker.py file_path1 file_path2 ...")
    for path in sys.argv[1:]:
        flst = os.listdir(path)
        flst = [os.path.join(path,f) for f in flst if f.lower().endswith('.jpg')]
        if len(flst) == 0:
            print(f"{path} doesn't have any pictures.")
            continue
        lst_coord = [get_coord(get_GPS(f)) for f in flst]
        center = (statistics.mean([i[0] for i in lst_coord if len(i) > 0]), statistics.mean([i[1] for i in lst_coord if len(i) > 0]))
        m = folium.Map(location = center, zoom_start = 6, tiles = "OpenStreetMap")
