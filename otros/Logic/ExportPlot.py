import dearpygui.dearpygui as dpg
from math import sin, cos
import numpy as np

file = ""
x_left, y_left, x_span, y_span = 0, 0, 0, 0

def _framebuffer_callback(sender, user_data):
    global file, x_left, y_left, x_span, y_span
    w, h = user_data.get_width(), user_data.get_height()
    image = np.frombuffer(user_data, dtype=np.float32, count=w*h*4)
    image = np.reshape(image, (h, w, 4)) # reshape to row major
    image = image[y_left:y_left + y_span, x_left: x_left + x_span, :] # crop
    image = image.flatten() # back to 1D
    image[:] *= 255 # pct to 8-bit range value
    dpg.save_image(file, x_span, y_span, image)

def crop_region_and_save(filepath, start, end):
    start, end = clip_region(start, end)
    global file, x_left, y_left, x_span, y_span
    file = filepath
    x_left, x_right, y_left, y_right = start[0], end[0], start[1], end[1]
    x_span, y_span = abs(x_right-x_left), abs(y_right-y_left)
    dpg.output_frame_buffer(callback=_framebuffer_callback)
    
def clip_region(start, end):
    # discretize and clip
    clip_x = np.clip([round(start[0]), round(end[0])], a_min=0, a_max=dpg.get_viewport_client_width())
    clip_y = np.clip([round(start[1]), round(end[1])], a_min=0, a_max=dpg.get_viewport_client_height())

    start = (clip_x[0], clip_y[0])
    end = (clip_x[1], clip_y[1])

    return start, end

def save_item(sender, user_data, args):
    plot_tag, filepath = args[0], args[1]
    win_start_x,win_start_y =dpg.get_item_pos(dpg.get_item_parent(plot_tag)) 
    start_x, start_y = dpg.get_item_pos(plot_tag)
    end_x, end_y = dpg.get_item_rect_size(plot_tag)
    start_x = start_x + win_start_x 
    start_y = start_y + win_start_y
    end_x = end_x + win_start_x
    end_y = end_y + win_start_y
    crop_region_and_save(filepath, (start_x, start_y), (start_x + end_x, start_y + end_y))