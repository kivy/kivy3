from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy3 import PerspectiveCamera
from kivy3 import Renderer
from kivy3 import Scene
from kivy3.loaders import OBJLoader
import os

# Resources pathes
_this_path = os.path.dirname(os.path.realpath(__file__))
shader_file = os.path.join(_this_path, "./blinnphong.glsl")
obj_file = os.path.join(_this_path, "./MQ-27.obj")


class LightingExample(App):
    """This is a basic example using a light source and a shaded model
    """

    def build(self):
        renderer = Renderer(shader_file=shader_file)
        renderer.main_light.pos = 1, 20, 50
        renderer.main_light.intensity = 1000

        loader = OBJLoader()
        obj = loader.load(obj_file)

        scene = Scene()

        camera = PerspectiveCamera(90, 1, 1, 10000)
        camera.pos = 0, 0, 50
        camera.look_at((0, 0, 0))

        scene.add(*obj.children)
        for obj in scene.children:
            obj.pos.z = -0.0
            obj.scale = 0.1, 0.1, 0.1

        renderer.render(scene, camera)
        orion = scene.children

        def _adjust_aspect(inst, val):
            rsize = renderer.size
            aspect = rsize[0] / float(rsize[1])
            renderer.camera.aspect = aspect
        renderer.bind(size=_adjust_aspect)

        def _rotate_obj(dt):
            for child in orion:
                child.rot.x += 2

        root = FloatLayout()
        root.add_widget(renderer)
        Clock.schedule_interval(_rotate_obj, 1 / 20)
        return root



if __name__ == "__main__":
    LightingExample().run()
