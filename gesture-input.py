# gesture input program for first task

from recognizer import DollarRecognizer, Point
import pyglet

WINDOW_WIDTH = 300
WINDOW_HEIGHT = 300

dollar_recognizer = DollarRecognizer()

#to_test_circle = [Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0), Point(0, 1)]
to_test = [Point(137,139),Point(135,141),Point(133,144),Point(132,146),Point(130,149),Point(128,151),Point(126,155),Point(123,160),Point(120,166),Point(116,171),Point(112,177),Point(107,183),Point(102,188),Point(100,191),Point(95,195),Point(90,199),Point(86,203),Point(82,206),Point(80,209),Point(75,213),Point(73,213),Point(70,216),Point(67,219),Point(64,221),Point(61,223),Point(60,225),Point(62,226),Point(65,225),Point(67,226),Point(74,226),Point(77,227),Point(85,229),Point(91,230),Point(99,231),Point(108,232),Point(116,233),Point(125,233),Point(134,234),Point(145,233),Point(153,232),Point(160,233),Point(170,234),Point(177,235),Point(179,236),Point(186,237),Point(193,238),Point(198,239),Point(200,237),Point(202,239),Point(204,238),Point(206,234),Point(205,230),Point(202,222),Point(197,216),Point(192,207),Point(186,198),Point(179,189),Point(174,183),Point(170,178),Point(164,171),Point(161,168),Point(154,160),Point(148,155),Point(143,150),Point(138,148),Point(136,148)]

window = pyglet.window.Window(WINDOW_WIDTH,WINDOW_HEIGHT)
points = []

def get_mirrored_y(y):
    return WINDOW_HEIGHT-y

@window.event
def on_mouse_press(x,y, button, modifiers):
    print(x,y)
    points.append(Point(x,get_mirrored_y(y)))

@window.event
def on_mouse_drag(x,y,dx,dy,buttons,modifiers):
    points.append(Point(x,get_mirrored_y(y)))

@window.event
def on_mouse_release(x,y,button,modifiers):
    dollar_recognizer.recognize(points)
    points.clear()

@window.event
def on_draw():
    window.clear()
    for point in points:
        circle = pyglet.shapes.Circle(point.x, get_mirrored_y(point.y), 5, color=(0,255,0))
        circle.draw()



if __name__ == "__main__":
    #recognition = dollar_recognizer.recognize(to_test)
    pyglet.app.run()

