from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy3 import Material
from kivy3 import Mesh
from kivy3 import PerspectiveCamera
from kivy3 import Renderer
from kivy3 import Scene
from kivy3.extras.geometries import SphereGeometry
from kivy3.loaders import STLLoader
import os

_this_path = os.path.dirname(os.path.realpath(__file__))
shader_file = os.path.join(_this_path, "./blinnphong.glsl")
stl_file = os.path.join(_this_path, "./test.stl")


class SceneApp(App):

    def build(self):
        renderer = self.renderer = Renderer(shader_file=shader_file)
        renderer.set_clear_color((0.16, 0.30, 0.44, 1.0))

        loader = STLLoader()

        geometry = SphereGeometry(1)
        material = Material(
            color=(0.3, 0.0, 0.3), diffuse=(0.3, 0.3, 0.3), specular=(0.0, 0.0, 0.0)
        )
        self.item = loader.load(stl_file, material)

        scene = Scene()
        scene.add(self.item)

        self.cube = Mesh(geometry, material)
        self.item.pos.z = -1.5

        camera = PerspectiveCamera(75, 0.3, 0.5, 1000)

        renderer.bind(size=self._adjust_aspect)
        renderer.render(scene, camera)

        root = FloatLayout()
        root.add_widget(renderer)
        Clock.schedule_interval(self._rotate_cube, 1 / 20)

        return root

    def _adjust_aspect(self, inst, val):
        rsize = self.renderer.size
        aspect = rsize[0] / float(rsize[1])
        self.renderer.camera.aspect = aspect

    def _rotate_cube(self, dt):
        self.cube.rotation.x += 1
        self.cube.rotation.y += 1
        self.cube.rotation.z += 1
        self.item.rotation.x += 1
        self.item.rotation.y += 1
        self.item.rotation.z += 1


if __name__ == "__main__":
    SceneApp().run()
