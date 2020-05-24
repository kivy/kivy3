from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy3 import PerspectiveCamera
from kivy3 import Renderer
from kivy3 import Scene
from kivy3 import shaders
from kivy3.loaders.urdfloader import URDFLoader
from kivy3.widgets import OrbitControlWidget
import os

base_path = os.path.dirname(os.path.realpath(__file__))
urdf_file = os.path.join(base_path, "reach7.urdf")


class URDFLoaderApp(App):
    """Demonstrate URDF file loading.
    """

    def build(self):
        renderer = Renderer(shader_file=shaders.blinnphong)

        loader = URDFLoader()
        obj = loader.load(urdf_file)
        obj.pos.z = 0

        camera = PerspectiveCamera(75, 0.3, 0.5, 1000)
        camera.pos.z = 1.5
        camera.look_at((0, 0, 0))
        camera.bind_to(renderer)

        scene = Scene()
        scene.add(obj)

        renderer.set_clear_color((0.16, 0.30, 0.44, 1.0))
        renderer.render(scene, camera)

        root = FloatLayout()
        root.add_widget(renderer)
        root.add_widget(OrbitControlWidget(renderer, 4.0))

        def adjust_aspect(inst, val):
            size = renderer.size
            camera.aspect = size[0] / float(size[1])
        renderer.bind(size=adjust_aspect)

        return root


if __name__ == "__main__":
    URDFLoaderApp().run()
