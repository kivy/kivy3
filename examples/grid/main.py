from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy3 import Material
from kivy3 import Mesh
from kivy3 import PerspectiveCamera
from kivy3 import Renderer
from kivy3 import Scene
from kivy3.extras.geometries import BoxGeometry
from kivy3.extras.geometries import GridGeometry
from kivy3.objects.lines import Lines
import math


class GridExample(App):
    """This example demonstrates the use of a grid floor
    """

    def build(self):
        renderer = Renderer()
        renderer.set_clear_color((0.2, 0.2, 0.2, 1.0))

        scene = Scene()
        camera = PerspectiveCamera(45, 1, 0.1, 2500)
        
        geometry = BoxGeometry(1, 1, 1)
        material = Material(
            color=(1.0, 1.0, 1.0), diffuse=(1.0, 1.0, 1.0), specular=(0.35, 0.35, 0.35)
        )
        obj = Mesh(geometry, material)

        geometry = GridGeometry(size=(30, 30), spacing=1)
        material = Material(
            color=(1.0, 1.0, 1.0),
            diffuse=(1.0, 1.0, 1.0),
            specular=(0.35, 0.35, 0.35),
            transparency=0.1,
        )
        lines = Lines(geometry, material)
        lines.rotation.x = 90

        scene.add(obj)
        scene.add(lines)

        def _adjust_aspect(inst, val):
            rsize = renderer.size
            aspect = rsize[0] / float(rsize[1])
            renderer.camera.aspect = aspect
        renderer.bind(size=_adjust_aspect)

        renderer.render(scene, camera)
        renderer.main_light.intensity = 500

        root = ObjectTrackball(camera, 10)
        root.add_widget(renderer)
        return root


class ObjectTrackball(FloatLayout):
    def __init__(self, camera, radius, *args, **kw):
        super(ObjectTrackball, self).__init__(*args, **kw)
        self.camera = camera
        self.radius = radius
        self.phi = 90
        self.theta = 0
        self._touches = []
        self.camera.pos.z = radius
        camera.look_at((0, 0, 0))

    def define_rotate_angle(self, touch):
        theta_angle = (touch.dx / self.width) * -360
        phi_angle = (touch.dy / self.height) * 360
        return phi_angle, theta_angle

    def on_touch_down(self, touch):
        touch.grab(self)
        self._touches.append(touch)

    def on_touch_up(self, touch):
        touch.ungrab(self)
        self._touches.remove(touch)

    def on_touch_move(self, touch):
        if touch in self._touches and touch.grab_current == self:
            if len(self._touches) == 1:
                self.do_rotate(touch)
            elif len(self._touches) == 2:
                pass

    def do_rotate(self, touch):
        d_phi, d_theta = self.define_rotate_angle(touch)
        self.phi += d_phi
        self.theta += d_theta

        _phi = math.radians(self.phi)
        _theta = math.radians(self.theta)
        z = self.radius * math.cos(_theta) * math.sin(_phi)
        x = self.radius * math.sin(_theta) * math.sin(_phi)
        y = self.radius * math.cos(_phi)
        self.camera.pos = x, y, z
        self.camera.look_at((0, 0, 0))


if __name__ == "__main__":
    GridExample().run()
