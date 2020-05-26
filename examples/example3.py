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
        # load obj file
        loader = OBJMTLLoader()
        obj_path = os.path.join(os.path.dirname(__file__), "./testnurbs.obj")
        obj = loader.load(obj_path, "./testnurbs.mtl")

        scene = Scene()
        scene.add(*obj.children)
        for obj in scene.children:
            obj.pos.z = -20

        camera = PerspectiveCamera(15, 1, 1, 1000)

        renderer = self.renderer = Renderer()
        renderer.bind(size=self._adjust_aspect)
        renderer.render(scene, camera)

        root = FloatLayout()
        root.add_widget(renderer)
        return root

    def _adjust_aspect(self, inst, val):
        rsize = self.renderer.size
        aspect = rsize[0] / float(rsize[1])
        self.renderer.camera.aspect = aspect


if __name__ == "__main__":
    MainApp().run()
