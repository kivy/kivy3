from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy3 import Material
from kivy3 import PerspectiveCamera
from kivy3 import Renderer
from kivy3 import Scene
from kivy3 import shaders
from kivy3.loaders.stlloader import STLLoader
from kivy3.widgets import OrbitControlWidget
import os

base_path = os.path.dirname(os.path.realpath(__file__))
stl_file = os.path.join(base_path, "stl_mesh.stl")


class STLLoaderApp(App):
    """Demonstrate STL file loading.
    """

    def build(self):
        renderer = Renderer(shader_file=shaders.blinnphong)
        renderer.set_clear_color((0.16, 0.30, 0.44, 1.0))
        
        loader = STLLoader()
        material = Material(
            color=(0.3, 0.0, 0.3),
            diffuse=(0.3, 0.3, 0.3),
            specular=(0.0, 0.0, 0.0)
        )
        obj = loader.load(stl_file, material)
        obj.pos.z = 0

        scene = Scene()
        scene.add(obj)

        camera = PerspectiveCamera(75, 0.3, 0.5, 1000)
        camera.pos.z = 1.5
        camera.look_at((0, 0, 0))
        camera.bind_to(renderer)

        renderer.render(scene, camera)

        def adjust_aspect(inst, val):
            size = renderer.size
            camera.aspect = size[0] / float(size[1])
        renderer.bind(size=adjust_aspect)

        root = FloatLayout()
        root.add_widget(renderer)
        root.add_widget(OrbitControlWidget(renderer, 4.0))
        return root


if __name__ == "__main__":
    STLLoaderApp().run()
