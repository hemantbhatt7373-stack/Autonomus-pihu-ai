import urllib.request
import zipfile
import io
import os
import shutil

target_dir = os.path.abspath('gui/live2d/model')

# ?????? ?????? ?? ???? ?? ???? ??? ????? ????
if os.path.exists(target_dir):
    if os.path.isdir(target_dir):
        shutil.rmtree(target_dir, ignore_errors=True)
    else:
        os.remove(target_dir)

os.makedirs(target_dir, exist_ok=True)

print('? Downloading Shizuka-Style Live2D Model...')
url = 'https://github.com/Live2D/CubismWebSamples/archive/refs/heads/develop.zip'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

with urllib.request.urlopen(req) as resp:
    zip_data = zipfile.ZipFile(io.BytesIO(resp.read()))
    
    # Mao (Shizuka style) ?????? ??????
    prefix = 'CubismWebSamples-develop/Samples/TypeScript/Demo/public/Resources/Mao/'
    for item in zip_data.namelist():
        if item.startswith(prefix) and item != prefix:
            rel_path = item[len(prefix):]
            dest_path = os.path.join(target_dir, rel_path)
            
            if item.endswith('/'):
                os.makedirs(dest_path, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                with open(dest_path, 'wb') as f:
                    f.write(zip_data.read(item))

print('? Shizuka-Style Live2D Model Successfully Installed!')
