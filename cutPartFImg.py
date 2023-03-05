import os
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import RectangleSelector
from gxml import generate
from pathlib import Path

try:
    if not os.path.exists('annotated'):
        os.makedirs('annotated')

except OSError:
    print('Error: Creating directory of annotated')

try:
    if not os.path.exists('annotated/hands'):
        os.makedirs('annotated/hands')

except OSError:
    print('Error: Creating directory of hands')

try:
    if not os.path.exists('annotated/humanhands'):
        os.makedirs('annotated/humanhands')

except OSError:
    print('Error: Creating directory of human hands')

try:
    if not os.path.exists('annotated/head'):
        os.makedirs('annotated/head')

except OSError:
    print('Error: Creating directory of head')

try:
    if not os.path.exists('annotated/humanhead'):
        os.makedirs('annotated/humanhead')

except OSError:
    print('Error: Creating directory of human head')

try:
    if not os.path.exists('annotated/feet'):
        os.makedirs('annotated/feet')

except OSError:
    print('Error: Creating directory of feet')

try:
    if not os.path.exists('annotated/humanfeet'):
        os.makedirs('annotated/humanfeet')

except OSError:
    print('Error: Creating directory of human feet')

try:
    if not os.path.exists('annotated/core'):
        os.makedirs('annotated/core')

except OSError:
    print('Error: Creating directory of core')

try:
    if not os.path.exists('annotated/humantrunk'):
        os.makedirs('annotated/humantrunk')

except OSError:
    print('Error: Creating directory of human trunk')

try:
    if not os.path.exists('annotated/hips'):
        os.makedirs('annotated/hips')

except OSError:
    print('Error: Creating directory of hips')

try:
    if not os.path.exists('annotated/humanhips'):
        os.makedirs('annotated/humanhips')

except OSError:
    print('Error: Creating directory of human hips')
    
try:
    if not os.path.exists('annotated/legs'):
        os.makedirs('annotated/legs')

except OSError:
    print('Error: Creating directory of legs')

try:
    if not os.path.exists('annotated/humanlegs'):
        os.makedirs('annotated/humanlegs')

except OSError:
    print('Error: Creating directory of human legs')

try:
    if not os.path.exists('annotated/arms'):
        os.makedirs('annotated/arms')

except OSError:
    print('Error: Creating directory of arms')

try:
    if not os.path.exists('annotated/humanarms'):
        os.makedirs('annotated/humanarms')

except OSError:
    print('Error: Creating directory of human arms')

container = os.listdir('data')

container = container[1:]

docker = []

for i in range(len(container)):
    if container[i].endswith('mp4') != True:
        docker.append(container[i])

print('all data folder for this task:\n{}'.format(
    docker
))

path = input('input the folder you want to annotate here >>> ')

image_folder = 'data' + '/' + path
savedir = 'annotated'
tl_list = []
br_list = []
object_list = []
img = None
obj = 'Head'

def line_select_callback(clk, rls):
    global tl_list
    global br_list
    
    tl_list.append((int(clk.xdata), int(clk.ydata)))
    br_list.append((int(rls.xdata), int(rls.ydata)))
    object_list.append(obj)
    print(f'Recorded: \n{object_list}\n')
    print(f'Top Left: \n{tl_list}\n')
    print(f'Bottom Right: \n{br_list}\n')

def change_object(event):
    global obj
    if event.key == 'c':
        print('[Changed to Head]\n')
        obj = 'Head'

    if event.key == 'h':
        print('[Changed to Hand]\n')
        obj = 'Hand'
    
    if event.key == 'e':
        print('[Changed to Feet]\n')
        obj = 'Feet'
    
    if event.key == "q":
        print('[Changed to Core]\n')
        obj = 'Core'
        
    if event.key == "t":
        print('[Changed to Hips]\n')
        obj = 'Hips'
        
    if event.key == "w":
        print('[Changed to Legs]\n')
        obj = 'Legs'
        
    if event.key == "j":
        print('[Changed to Arms]\n')
        obj = 'Arms'

    if event.key == 'r':
        del tl_list[-1]
        del br_list[-1]
        del object_list[-1]
        print('[Deleted Previous Object]\n')
        print(f'Recorded: \n{object_list}\n')
        print(f'Top Left: \n{tl_list}\n')
        print(f'Bottom Right: \n{br_list}\n')

def onkeypress(event):
    global object_list
    global tl_list
    global br_list
    global img
    if event.key == 's':
        generate(image_folder, img, object_list,tl_list, br_list, savedir)
        print(f'[Final] \n{tl_list}\n{br_list}\n{object_list}\n')
        tl_list = []
        br_list = []
        img = None
        object_list = []
        plt.close()

    if event.key == 'd':
        os.remove(img)
        print('[Deleted the image]\n')
        plt.close()

def toggle_selector(event):
    toggle_selector.RS.set_active(True)

if __name__ == '__main__':
    for image_file in sorted(Path(image_folder).glob('*.png')):
        img = image_file
        fig, ax = plt.subplots(1)
        image = cv2.imread(str(img))
        print(image_file)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        ax.imshow(image)

        toggle_selector.RS = RectangleSelector(
            ax, line_select_callback,
            drawtype = 'box', useblit = True,
            button = [1], minspanx = 3, minspany = 3,
            spancoords = 'pixels', interactive = True
        )
        bbox = plt.connect('key_press_event', toggle_selector)
        obj_changed = plt.connect('key_press_event', change_object)
        key = plt.connect('key_press_event', onkeypress)
        plt.tight_layout()
        plt.show()
