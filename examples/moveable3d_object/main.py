from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy3 import Material
from kivy3 import Mesh
from kivy3 import Object3D
from kivy3 import PerspectiveCamera
from kivy3 import Renderer
from kivy3 import Scene
from kivy3.extras.geometries import BoxGeometry
from kivy3.extras.Widgets3D.moveable3Dwidget import Moveable3DWidget
from kivy3.widgets import Object3DWidget
from kivy3.widgets import OrbitControlWidget
from kivy3.widgets import SelectionWidget
import os

_this_path = os.path.dirname(os.path.realpath(__file__))
shader_file = os.path.join(_this_path, "../blinnphong.glsl")


class Moveable3DObjectExample(App):
    """This example shows how to make use of the Moveable3DWidget
    """

    def build(self):
        renderer = Renderer(shader_file=shader_file)
        renderer.set_clear_color((0.16, 0.30, 0.44, 1.0))

        orbit = OrbitControlWidget(renderer, 4.0)

        selection_widget = SelectionWidget(renderer)

        camera = PerspectiveCamera(90, 0.3, 0.1, 1000)
        camera.pos.z = 1.5
        camera.look_at((0, 0, 0))

        base = Object3D()
        id_color = (1, 0, 0)
        geometry = BoxGeometry(1, 1, 1)
        material = Material(
            color=(0.3, 0, 0),
            diffuse=(0.3, 0, 0),
            specular=(0.3, 0.3, 0.3),
            id_color=(id_color),
        )
        obj_1 = Mesh(geometry, material)

        widget_1 = Object3DWidget(obj_1, renderer)
        selection_widget.register(id_color, widget_1)

        id_color = (2, 0, 0)
        geometry = BoxGeometry(1, 1, 1)
        material = Material(
            color=(00, 0.3, 0),
            diffuse=(0, 0.3, 0),
            specular=(0.3, 0.3, 0.3),
            id_color=(id_color),
        )
        obj_2 = Mesh(geometry, material)
        obj_2.pos.x = 1

        widget_2 = Moveable3DWidget(obj_2, renderer, orbit)
        selection_widget.register(id_color, widget_2)

        base.rot.x = -90
        base.add(obj_1)
        base.add(obj_2)

        scene = Scene()
        scene.add(base)

        camera.bind_to(renderer)
        renderer.render(scene, camera)

        root = FloatLayout()
        root.add_widget(selection_widget, index=98)
        root.add_widget(orbit, index=99)
        root.add_widget(renderer, index=100)

        def _adjust_aspect(inst, val):
            rsize = renderer.size
            aspect = rsize[0] / float(rsize[1])
            renderer.camera.aspect = aspect
        renderer.bind(size=_adjust_aspect)
        return root


if __name__ == "__main__":
    Moveable3DObjectExample().run()
