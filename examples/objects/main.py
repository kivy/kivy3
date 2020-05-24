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
    """This example showcases some special objects
    """

    def build(self):
        renderer = Renderer(shader_file=shader_file)
        renderer.set_clear_color((0.16, 0.30, 0.44, 1.0))

        base = Object3D()

        axis = AxisObject(length=0.5, alpha=0.4)

        material = Material(
            color=(0, 0.3, 0), diffuse=(0, 0.3, 0), specular=(0.3, 0.3, 0.3)
        )
        arrow = ArrowObject(material, length=0.5, radius=0.04)
        arrow.pos.y = 1

        base.add(axis)
        base.add(arrow)

        camera = PerspectiveCamera(90, 0.3, 0.1, 1000)
        camera.pos.z = 1.5
        camera.look_at((0, 0, 0))
        camera.bind_to(renderer)

        scene = Scene()

        base.rot.x = -90
        scene.add(base)

        renderer.render(scene, camera)

        def _adjust_aspect(inst, val):
            rsize = renderer.size
            aspect = rsize[0] / float(rsize[1])
            renderer.camera.aspect = aspect
        renderer.bind(size=_adjust_aspect)

        root = FloatLayout()
        root.add_widget(renderer, index=30)
        orbit = OrbitControlWidget(renderer, 4.0)
        root.add_widget(orbit, index=99)

        return root


if __name__ == "__main__":
    ObjectsExample().run()
