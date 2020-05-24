from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy3 import PerspectiveCamera
from kivy3 import Renderer
from kivy3 import Scene
from kivy3.loaders import OBJLoader
import os

# Resources pathes
_this_path = os.path.dirname(os.path.realpath(__file__))
shader_file = os.path.join(_this_path, "./simple.glsl")
obj_path = os.path.join(_this_path, "./testnurbs.obj")


class MainApp(App):
    """This example loads simple objects from .obj file and shows how
    to use custom shader file
    """

    def build(self):
        renderer = Renderer(shader_file=shader_file)

        # load obj file
        loader = OBJLoader()
        obj = loader.load(obj_path)

        camera = PerspectiveCamera(15, 1, 1, 1000)

        scene = Scene()
        scene.add(*obj.children)
        for obj in scene.children:
            obj.pos.z = -20
        
        def _adjust_aspect(inst, val):
            rsize = renderer.size
            aspect = rsize[0] / float(rsize[1])
            renderer.camera.aspect = aspect
        renderer.bind(size=_adjust_aspect)

        root = FloatLayout()
        renderer.render(scene, camera)
        root.add_widget(renderer)
        return root


if __name__ == "__main__":
    MainApp().run()
