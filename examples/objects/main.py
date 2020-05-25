from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy3 import Material
from kivy3 import Object3D
from kivy3 import Scene, Renderer, PerspectiveCamera
from kivy3.extras.objects import ArrowObject
from kivy3.extras.objects import AxisObject
from kivy3.widgets import OrbitControlWidget
import os

_this_path = os.path.dirname(os.path.realpath(__file__))
shader_file = os.path.join(_this_path, "../blinnphong.glsl")


class ObjectsExample(App):
    """This example showcases ArrowObject and AxisObject."""

    def build(self):
        base = Object3D()
        base.rot.x = -90

        axis = AxisObject(length=0.5, alpha=0.4)

        material = Material(
            color=(0, 0.3, 0),
            diffuse=(0, 0.3, 0),
            specular=(0.3, 0.3, 0.3)
        )
        arrow = ArrowObject(material, length=0.5, radius=0.04)
        arrow.pos.y = 1

        base.add(axis)
        base.add(arrow)

        scene = Scene()
        scene.add(base)

        camera = PerspectiveCamera(90, 0.3, 0.1, 1000)
        camera.pos.z = 1.5
        camera.look_at((0, 0, 0))

        renderer = self.renderer = Renderer(shader_file=shader_file)
        renderer.bind(size=self._adjust_aspect)
        renderer.set_clear_color((0.16, 0.30, 0.44, 1.0))
        renderer.render(scene, camera)

        camera.bind_to(renderer)

        root = FloatLayout()
        root.add_widget(renderer, index=30)
        orbit = OrbitControlWidget(renderer, 4.0)
        root.add_widget(orbit, index=99)
        return root

    def _adjust_aspect(self, inst, val):
        rsize = self.renderer.size
        aspect = rsize[0] / float(rsize[1])
        self.renderer.camera.aspect = aspect


if __name__ == "__main__":
    ObjectsExample().run()
