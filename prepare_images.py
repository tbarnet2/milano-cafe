from zipfile import ZipFile
from PIL import Image, ImageOps, ImageEnhance
import io, os
root=os.path.dirname(__file__)
archive='/mnt/data/drive-download-20261023T161533Z-1-001.zip'
photos={
 'hero-gallery':'IMG_6220.jpg',
 'dining-room':'IMG_6231.jpg',
 'table-spread':'IMG_6090.jpg',
 'pizza':'IMG_6135.jpg',
 'pasta':'IMG_6161.jpg',
 'dessert':'IMG_6247.jpg',
 'gallery-wall':'IMG_6222.jpg',
 'gallery-portraits':'IMG_6224.jpg',
 'artwork-detail':'IMG_6279.jpg',
 'quiet-corner':'IMG_6208.jpg',
 'color-room':'IMG_6281.jpg',
 'food-spread':'IMG_6182.jpg',
 'window-table':'IMG_6189.jpg',
 'coffee-dessert':'IMG_6273.jpg',
}
with ZipFile(archive) as zipf:
 for target,source in photos.items():
  im=ImageOps.exif_transpose(Image.open(io.BytesIO(zipf.read(source)))).convert('RGB')
  maxwidth=2000 if target=='hero-gallery' else (1600 if target in ('dining-room','table-spread','food-spread','gallery-wall') else 1350)
  if im.width>maxwidth:
   im.thumbnail((maxwidth,1800),Image.Resampling.LANCZOS)
  else:
   im.thumbnail((maxwidth,1800),Image.Resampling.LANCZOS)
  file=os.path.join(root,'assets/photos',target+'.webp')
  im.save(file,format='WEBP',quality=82,method=6)
  print(target,source,im.size,os.path.getsize(file))
