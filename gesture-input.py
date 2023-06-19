# gesture input program for first task

from recognizer import DollarRecognizer, Point
import pyglet

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 400


class UIManager:
    batch = pyglet.graphics.Batch()
    def __init__(self) -> None:
        self.shapes = []
        self._create_shapes()
        self.help_image_path = './assets/input_help_task01.png'
        self.help_image = pyglet.image.load(self.help_image_path)
        self.header = pyglet.text.Label("draw gesture down here:",
                                        font_name="Arial",
                                        font_size=18,
                                        x = 10,
                                        y = 330,
                                        color=(0,0,0,255))
        self.prediction_text = pyglet.text.Label("prediction:",
                                        font_name="Arial",
                                        font_size=13,
                                        x = 10,
                                        y = 300,
                                        color=(0,0,0,255))

    def _create_shapes(self):
        outer_border = pyglet.shapes.Rectangle(0,0,300,400,color=(255,255,255), batch=UIManager.batch)
        inner_border = pyglet.shapes.Rectangle(10,10,280,280,color=(200,200,200), batch=UIManager.batch)

        self.shapes.append(outer_border)
        self.shapes.append(inner_border)

    def _show_prediction(self, label):
        self.prediction_text.text = f"prediction: {label}"

    def _draw(self):
        self.help_image.blit(300,0,0)
        for shape in self.shapes:
            shape.draw()
        self.header.draw()
        self.prediction_text.draw()



dollar_recognizer = DollarRecognizer()
window = pyglet.window.Window(WINDOW_WIDTH,WINDOW_HEIGHT)
ui_manager = UIManager()
points = []

def get_mirrored_y(y):
    return WINDOW_HEIGHT-y

def mouse_is_inbounds(x,y):
    if x > 15 and x < 275 and y > 15 and y < 275:
        return True
    return False

@window.event
def on_mouse_press(x,y, button, modifiers):
    if mouse_is_inbounds(x,y):
        points.append(Point(x,get_mirrored_y(y)))

@window.event
def on_mouse_drag(x,y,dx,dy,buttons,modifiers):
    if mouse_is_inbounds(x,y):
        points.append(Point(x,get_mirrored_y(y)))

@window.event
def on_mouse_release(x,y,button,modifiers):
    result = dollar_recognizer.recognize(points)
    ui_manager._show_prediction(result.name)
    points.clear()

@window.event
def on_draw():
    window.clear()
    ui_manager._draw()
    for point in points:
        circle = pyglet.shapes.Circle(point.x, get_mirrored_y(point.y), 5, color=(255,255,0))
        circle.draw()

if __name__ == "__main__":
    pyglet.app.run()

# TODO
# cancel rectangle or v (confusion because no idea) OR x - 400