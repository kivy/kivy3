from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy3 import Material
from kivy3 import Mesh
from kivy3 import Object3D
from kivy3 import Scene, Renderer, PerspectiveCamera
from kivy3.extras.geometries import BoxGeometry
from kivy3.extras.geometries import ConeGeometry
from kivy3.extras.geometries import CylinderGeometry
from kivy3.extras.geometries import GridGeometry
from kivy3.extras.geometries import SphereGeometry
from kivy3.objects.lines import Lines
from kivy3.widgets import OrbitControlWidget
import os

_this_path = os.path.dirname(os.path.realpath(__file__))
shader_file = os.path.join(_this_path, "../blinnphong.glsl")


class GeometryExample(App):
    """This example shows how to create different types of
    Geometry
    """

    def build(self):
        renderer = Renderer(shader_file=shader_file)
        renderer.set_clear_color((0.16, 0.30, 0.44, 1.0))

        base = Object3D()
        geometry = BoxGeometry(0.5, 0.5, 0.5)
        material = Material(
            color=(0.3, 0, 0), diffuse=(0.3, 0, 0), specular=(0.3, 0.3, 0.3)
        )
        obj_1 = Mesh(geometry, material)

        geometry = CylinderGeometry(0.25, 0.5)
        material = Material(
            color=(0, 0.3, 0), diffuse=(0, 0.3, 0), specular=(0.3, 0.3, 0.3)
        )
        obj_2 = Mesh(geometry, material)
        obj_2.pos.y = 1

        geometry = ConeGeometry(0.25, 0.5)
        material = Material(
            color=(0, 0.3, 0.3), diffuse=(0, 0.3, 0.3), specular=(0.3, 0.3, 0.3)
        )
        obj_3 = Mesh(geometry, material)
        obj_3.pos.y = -1

        geometry = SphereGeometry(radius=0.25)
        material = Material(
            color=(0, 0, 1), diffuse=(0, 0, 1), specular=(0.3, 0.3, 0.3)
        )
        obj_4 = Mesh(geometry, material)
        obj_4.pos.x = -1

        geometry = GridGeometry()
        material = Material(
            color=(1.0, 1.0, 1.0),
            diffuse=(1.0, 1.0, 1.0),
            specular=(0.35, 0.35, 0.35),
            transparency=0.3,
        )
        lines = Lines(geometry, material)

        base.add(obj_1)
        base.add(obj_2)
        base.add(obj_3)
        base.add(obj_4)
        base.add(lines)
        base.rot.x = -90

        scene = Scene()
        scene.add(base)

        camera = PerspectiveCamera(90, 0.3, 0.1, 1000)
        camera.pos.z = 1.5
        camera.look_at((0, 0, 0))

        camera.bind_to(renderer)
        renderer.render(scene, camera)

        def _adjust_aspect(inst, val):
            rsize = renderer.size
            aspect = rsize[0] / float(rsize[1])
            renderer.camera.aspect = aspect
        renderer.bind(size=_adjust_aspect)

        orbit = OrbitControlWidget(renderer, 4.0)

        root = FloatLayout()
        root.add_widget(renderer, index=30)
        root.add_widget(orbit, index=99)
        return root


if __name__ == "__main__":
    GeometryExample().run()
