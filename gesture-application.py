# application for task 3

from recognizer import DollarRecognizer, Point
from pynput.keyboard import Key, Controller
import pyglet

# constants 
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 400
CANVAS_X_Y_START = 10
CANVAS_WIDTH_HEIGHT = 280
MIN_RECORDED_NUMS = 20

# holds the media control code
class ControlManager:
    
    def __init__(self) -> None:
        self.keyboard = Controller()

    # gets the predicted label from recognizer
    # if correct label was predicted -> media key press
    def _media_controlled(self, label):
        if label == "circle": # pause / play
            self.keyboard.press(Key.media_play_pause)
            self.keyboard.release(Key.media_play_pause)
        elif label == "v": # volume down
            self.keyboard.press(Key.media_volume_down)
            self.keyboard.release(Key.media_volume_down)
        elif label == "caret": # volume up
            self.keyboard.press(Key.media_volume_up)
            self.keyboard.release(Key.media_volume_up)
        elif label == "left_sq_bracket": # previous track
            self.keyboard.press(Key.media_previous)
            self.keyboard.release(Key.media_previous)
        elif label == "right_sq_bracket": # next track
            self.keyboard.press(Key.media_next)
            self.keyboard.release(Key.media_next)
        else:
            return False
        return True

# holds the UI elements
class UIManager:

    def __init__(self) -> None:
        self.shapes = []
        self._create_shapes()
        self.help_image_path = './assets/input_help_task03.png' # what gestures are possible
        self.help_image = pyglet.image.load(self.help_image_path)
        self.header = pyglet.text.Label("draw gesture down here:",
                                        font_name="Arial",
                                        font_size=16,
                                        x = 15,
                                        y = 300,
                                        color=(31, 32, 65, 255))
        self.input_text = pyglet.text.Label("input was too short",
                                        font_name="Arial",
                                        font_size=13,
                                        x = 50,
                                        y = 340,
                                        color=(186, 59, 70, 255))
        self.recognition_text = pyglet.text.Label("",
                                        font_name="Arial",
                                        font_size=13,
                                        x = 50,
                                        y = 340,
                                        color=(31, 32, 65, 255))
        self.input_too_short = False # if input points were too short (wrong predictions)

    # canvas borders
    def _create_shapes(self):
        outer_border = pyglet.shapes.Rectangle(0,0,300,400,color=(255,255,255))
        inner_border = pyglet.shapes.Rectangle(10,10,280,280,color=(105, 103, 115))
        self.shapes.append(outer_border)
        self.shapes.append(inner_border)

    # draws all ui elements
    def _draw(self):
        self.help_image.blit(300,0,0)
        for shape in self.shapes:
            shape.draw()
        self.header.draw()

    # if input points are too short -> some information for user
    def _draw_short_input(self):
        self.input_text.draw()

# helper functions
class InputManager:

    def __init__(self) -> None:
        self.points = [] # mouse detected points
        self.input_recognized = False

    def get_mirrored_y(self, y):
        return WINDOW_HEIGHT-y # pyglet to recognizer y

    def mouse_is_inbounds(self, x,y): # if mouse is only in inner bounds of canvas -> draw
        if x > CANVAS_X_Y_START + 5 and x < CANVAS_WIDTH_HEIGHT - 5 and y > CANVAS_X_Y_START + 5 and y < CANVAS_WIDTH_HEIGHT - 5:
            return True
        return False

dollar_recognizer = DollarRecognizer()
window = pyglet.window.Window(WINDOW_WIDTH,WINDOW_HEIGHT)
ui_manager = UIManager()
control_manager = ControlManager()
input_manager = InputManager()

@window.event
def on_mouse_press(x,y, button, modifiers):
    ui_manager.input_too_short = False
    ui_manager.recognition_text.text = ""
    if input_manager.mouse_is_inbounds(x,y):
        input_manager.points.append(Point(x,input_manager.get_mirrored_y(y))) # y coordinate mirror for correct result

@window.event
def on_mouse_drag(x,y,dx,dy,buttons,modifiers):
    if input_manager.mouse_is_inbounds(x,y):
        input_manager.points.append(Point(x,input_manager.get_mirrored_y(y)))

@window.event
def on_mouse_release(x,y,button,modifiers):
    if len(input_manager.points) > MIN_RECORDED_NUMS:
        result = dollar_recognizer.recognize(input_manager.points) # get the result
        input_manager.input_recognized = control_manager._media_controlled(result.name) # control media with result
        if not input_manager.input_recognized:
            ui_manager.recognition_text.text = "input not recognized"
        else:
            ui_manager.recognition_text.text = "input recognized"
    else:
        ui_manager.input_too_short = True
    input_manager.points.clear() # clear canvas for new input

@window.event
def on_draw():
    window.clear()
    ui_manager._draw()
    for point in input_manager.points:
        circle = pyglet.shapes.Circle(point.x, input_manager.get_mirrored_y(point.y), 5, color=(237, 155, 64))
        circle.draw()
    if ui_manager.input_too_short:
        ui_manager._draw_short_input()
    if not input_manager.input_recognized and not ui_manager.input_too_short:
            ui_manager.recognition_text.draw()
    elif input_manager.input_recognized and not ui_manager.input_too_short:
            ui_manager.recognition_text.draw()

if __name__ == "__main__":
    pyglet.app.run() 