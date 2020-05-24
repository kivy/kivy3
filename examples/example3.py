from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy3 import PerspectiveCamera
from kivy3 import Renderer
from kivy3 import Scene
from kivy3.loaders import OBJMTLLoader
import os


class MainApp(App):
    """This example loads simple objects from .obj file and shows how
    to use custom shader file
    """

    def build(self):
        root = FloatLayout()
        renderer = Renderer()
        scene = Scene()
        camera = PerspectiveCamera(15, 1, 1, 1000)
        # load obj file
        loader = OBJMTLLoader()
        obj_path = os.path.join(os.path.dirname(__file__), "./testnurbs.obj")
        obj = loader.load(obj_path, "./testnurbs.mtl")

        scene.add(*obj.children)
        for obj in scene.children:
            obj.pos.z = -20

        renderer.render(scene, camera)
        root.add_widget(renderer)

        def _adjust_aspect(inst, val):
            rsize = renderer.size
            aspect = rsize[0] / float(rsize[1])
            renderer.camera.aspect = aspect
        renderer.bind(size=_adjust_aspect)
        return root



if __name__ == "__main__":
    MainApp().run()
