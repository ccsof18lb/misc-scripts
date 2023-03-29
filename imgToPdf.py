import os
import sys
from PIL import Image

address = sys.argv[1] "./imgs"

pdfName = sys.argv[2] "./new.pdf or new.pdf"

allfile = os.listdir(address)

allimages = [os.getcwd()+'/'+address.split('./')[1]+'/'+g for g in allfile if g.endswith('png') == True or g.endswith('jpeg') == True]

counter = 0

opened = []

while counter < len(allimages):
    img = Image.open(r'%s'%allimages[counter]).convert('RGB')
    opened.append(img)
    counter += 1

rest = opened[1:]

opened[0].save(r'%s'%pdfName,save_all=True,append_images=rest)
