from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy3 import PerspectiveCamera
from kivy3 import Renderer
from kivy3 import Scene
from kivy3 import Vector3
from kivy3.loaders import OBJMTLLoader
import os

# Resources pathes
_this_path = os.path.dirname(os.path.realpath(__file__))
shader_file = os.path.join(_this_path, "../textures/simple.glsl")
obj_file = os.path.join(_this_path, "../textures/orion.obj")
mtl_file = os.path.join(_this_path, "../textures/orion.mtl")


class CameraExample(App):
    """This example demonstrates navigation using the 
    scene camera
    """

    def build(self):
        renderer = Renderer(shader_file=shader_file)

        loader = OBJMTLLoader()
        obj = loader.load(obj_file, mtl_file)

        scene = Scene()
        scene.add(*obj.children)

        self.camera = PerspectiveCamera(75, 1, 1, 1000)
        self.camera.pos.z = 5
        renderer.render(scene, self.camera)

        def _adjust_aspect(inst, val):
            rsize = renderer.size
            aspect = rsize[0] / float(rsize[1])
            renderer.camera.aspect = aspect
        renderer.bind(size=_adjust_aspect)

        self.look_at = Vector3(0, 0, -1)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, root)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.orion = scene.children[0]

        Clock.schedule_interval(self._rotate_obj, 1 / 20)
        root = FloatLayout()
        root.add_widget(renderer)
        return root


    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == "w":
            self.camera.pos.z -= 0.2
        elif keycode[1] == "s":
            self.camera.pos.z += 0.2
        elif keycode[1] == "a":
            self.camera.pos.y -= 0.2
        elif keycode[1] == "d":
            self.camera.pos.y += 0.2

        elif keycode[1] == "up":
            self.look_at.y += 0.2
        elif keycode[1] == "down":
            self.look_at.y -= 0.2
        elif keycode[1] == "right":
            self.look_at.x += 0.2
        elif keycode[1] == "left":
            self.look_at.x -= 0.2

        self.camera.look_at(self.look_at)

    def _rotate_obj(self, dt):
        self.orion.rot.x += 2
        self.orion.rot.z += 2


if __name__ == "__main__":
    CameraExample().run()
