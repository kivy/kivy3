from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy3 import PerspectiveCamera
from kivy3 import Renderer
from kivy3 import Scene
from kivy3.loaders import OBJMTLLoader
import os

# Resources pathes
_this_path = os.path.dirname(os.path.realpath(__file__))
shader_file = os.path.join(_this_path, "./simple.glsl")
obj_file = os.path.join(_this_path, "./orion.obj")
mtl_file = os.path.join(_this_path, "./orion.mtl")


class TextureExample(App):
    """This example shows how to load in textured models.
    """

    def build(self):
        renderer = Renderer(shader_file=shader_file)
        loader = OBJMTLLoader()

        obj = loader.load(obj_file, mtl_file)

        camera = PerspectiveCamera(15, 1, 1, 1000)

        scene = Scene()
        scene.add(*obj.children)
        for obj in scene.children:
            obj.pos.z = -20.0

        orion = scene.children[0]

        Clock.schedule_interval(_rotate_obj, 1 / 20)

        def _rotate_obj(dt):
            orion.rot.x += 2

        def _adjust_aspect(inst, val):
            rsize = renderer.size
            aspect = rsize[0] / float(rsize[1])
            renderer.camera.aspect = aspect
        renderer.bind(size=_adjust_aspect)

        renderer.render(scene, camera)
        root = FloatLayout()
        root.add_widget(renderer)
        return root


if __name__ == "__main__":
    TextureExample().run()
