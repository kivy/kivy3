from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy3 import PerspectiveCamera
from kivy3 import Renderer
from kivy3 import Scene
from kivy3.loaders import OBJLoader
import os


class MainApp(App):
    """Same as example1 but with using default shader file and colorizing
    of the objects
    """

    def build(self):
        root = FloatLayout()
        renderer = Renderer()
        scene = Scene()
        camera = PerspectiveCamera(15, 1, 1, 1000)

        # load obj file
        loader = OBJLoader()
        obj_path = os.path.join(os.path.dirname(__file__), "./testnurbs-2.obj")
        obj = loader.load(obj_path)

        scene.add(*obj.children)
        for obj in scene.children:
            obj.pos.z = -20
            obj.material.specular = 0.35, 0.35, 0.35

        # set colors to 3d objects
        scene.children[0].material.color = 0.0, 0.7, 0.0  # green
        scene.children[1].material.color = 0.7, 0.0, 0.0  # red
        scene.children[2].material.color = 0.0, 0.0, 0.7  # blue
        scene.children[3].material.color = 0.7, 0.7, 0.0  # yellow

        scene.children[0].material.diffuse = 0.0, 0.7, 0.0  # green
        scene.children[1].material.diffuse = 0.7, 0.0, 0.0  # red
        scene.children[2].material.diffuse = 0.0, 0.0, 0.7  # blue
        scene.children[3].material.diffuse = 0.7, 0.7, 0.0  # yellow

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
