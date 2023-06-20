# gesture input program for first task

from recognizer import DollarRecognizer, Point
import pyglet

# constants 
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 400
CANVAS_X_Y_START = 10
CANVAS_WIDTH_HEIGHT = 280
MIN_RECORDED_NUMS = 40

# holds the UI elements
class UIManager:
    batch = pyglet.graphics.Batch()
    def __init__(self) -> None:
        self.shapes = []
        self._create_shapes()
        self.help_image_path = './assets/input_help_task01.png' # what gestures are possible
        self.help_image = pyglet.image.load(self.help_image_path)
        self.header = pyglet.text.Label("draw gesture down here:",
                                        font_name="Arial",
                                        font_size=18,
                                        x = 10,
                                        y = 330,
                                        color=(31, 32, 65, 255))
        self.prediction_text = pyglet.text.Label("prediction:",
                                        font_name="Arial",
                                        font_size=13,
                                        x = 10,
                                        y = 300,
                                        color=(31, 32, 65, 255))
        self.input_too_short = False # if input points were too short (wrong predictions)

    # canvas borders
    def _create_shapes(self):
        outer_border = pyglet.shapes.Rectangle(0,0,300,400,color=(255,255,255))
        inner_border = pyglet.shapes.Rectangle(10,10,280,280,color=(105, 103, 115))
        self.shapes.append(outer_border)
        self.shapes.append(inner_border)

    # change text to prediction label
    def _show_prediction(self, label):
        self.prediction_text.text = f"prediction: {label}"

    # draws all ui elements
    def _draw(self):
        self.help_image.blit(300,0,0)
        for shape in self.shapes:
            shape.draw()
        self.header.draw()
        self.prediction_text.draw()

# helper functions
class InputManager:

    def __init__(self) -> None:
        self.points = [] # mouse detected points

    def get_mirrored_y(self, y):
        return WINDOW_HEIGHT-y # pyglet to recognizer y

    def mouse_is_inbounds(self, x,y): # if mouse is only in inner bounds of canvas -> draw
        if x > CANVAS_X_Y_START + 5 and x < CANVAS_WIDTH_HEIGHT - 5 and y > CANVAS_X_Y_START + 5 and y < CANVAS_WIDTH_HEIGHT - 5:
            return True
        return False

dollar_recognizer = DollarRecognizer()
window = pyglet.window.Window(WINDOW_WIDTH,WINDOW_HEIGHT)
ui_manager = UIManager()
input_manager = InputManager()

@window.event
def on_mouse_press(x,y, button, modifiers):
    input_manager.points.clear()
    if input_manager.mouse_is_inbounds(x,y):
        input_manager.points.append(Point(x,input_manager.get_mirrored_y(y)))

@window.event
def on_mouse_drag(x,y,dx,dy,buttons,modifiers):
    if input_manager.mouse_is_inbounds(x,y):
        input_manager.points.append(Point(x,input_manager.get_mirrored_y(y)))

@window.event
def on_mouse_release(x,y,button,modifiers):
    if len(input_manager.points) > MIN_RECORDED_NUMS:
        result = dollar_recognizer.recognize(input_manager.points)
        ui_manager._show_prediction(result.name)
    else:
        ui_manager._show_prediction("input too short")

@window.event
def on_draw():
    window.clear()
    ui_manager._draw()
    for point in input_manager.points:
        circle = pyglet.shapes.Circle(point.x, input_manager.get_mirrored_y(point.y), 5, color=(237, 155, 64))
        circle.draw()

if __name__ == "__main__":
    pyglet.app.run()
