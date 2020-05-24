from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy3 import Geometry
from kivy3 import Material
from kivy3 import Mesh
from kivy3 import PerspectiveCamera
from kivy3 import Renderer
from kivy3 import Scene
from kivy3.core.line2 import Line2
from kivy3.extras.geometries import BoxGeometry
from kivy3.extras.geometries import GridGeometry
from kivy3.objects.lines import Lines
import math
import os

# Resource paths
_this_path = os.path.dirname(os.path.realpath(__file__))
shader_file = os.path.join(_this_path, "./blinnphong.glsl")

clear_color = (0.2, 0.2, 0.2, 1.0)


class RotationExample(App):
    """This example demonstrates how to manipulate the rotation
    of objects in the scene
    """

    def build(self):
        renderer = Renderer(shader_file=shader_file)
        renderer.set_clear_color(clear_color)

        camera = PerspectiveCamera(45, 1, 0.1, 2500)

        id_color_obj_1 = (0, 0, 0x7F)

        geometry = BoxGeometry(1, 1, 1)
        material = Material(
            color=(1.0, 1.0, 1.0),
            diffuse=(1.0, 1.0, 1.0),
            specular=(0.35, 0.35, 0.35),
            id_color=id_color_obj_1,
            shininess=1.0,
        )

        obj_1 = Mesh(geometry, material)

        id_color_obj_2 = (0, 0x7F, 0)
        geometry = BoxGeometry(1, 1, 1)
        material = Material(
            color=(0.0, 0.0, 1.0),
            diffuse=(0.0, 0.0, 1.0),
            specular=(0.35, 0.35, 0.35),
            id_color=id_color_obj_2,
            shininess=1.0,
        )
        obj_2 = Mesh(geometry, material)
        obj_2.position.x = 2

        # create a grid on the xz plane
        geometry = GridGeometry(size=(30, 30), spacing=1)
        material = Material(
            color=(1.0, 1.0, 1.0),
            diffuse=(1.0, 1.0, 1.0),
            specular=(0.35, 0.35, 0.35),
            transparency=0.5,
        )
        lines_1 = Lines(geometry, material)
        lines_1.rotation.x = 90

        geometry = Geometry()
        geometry.vertices = [[0.0, 0.0, 0.0], [3.0, 0.0, 0.0]]
        geometry.lines = [Line2(a=0, b=1)]
        material = Material(
            color=(1.0, 0.0, 0.0), diffuse=(1.0, 0.0, 0.0), specular=(0.35, 0.35, 0.35)
        )
        lines_2 = Lines(geometry, material)
        lines_2.position.y = -0.01

        geometry = Geometry()
        geometry.vertices = [[0.0, 0.0, 0.0], [0.0, 3.0, 0.0]]
        geometry.lines = [Line2(a=0, b=1)]
        material = Material(
            color=(0.0, 1.0, 0.0), diffuse=(0.0, 1.0, 0.0), specular=(1.0, 1.0, 1.0)
        )
        lines_3 = Lines(geometry, material)

        geometry = Geometry()
        geometry.vertices = [[0.0, 0.0, 0.0], [0.0, 0.0, 3.0]]
        geometry.lines = [Line2(a=0, b=1)]
        material = Material(
            color=(0.0, 0.0, 1.0), diffuse=(0.0, 0.0, 1.0), specular=(0.35, 0.35, 0.35)
        )
        lines_4 = Lines(geometry, material)
        lines_4.position.y = -0.01

        # make the triad
        geometry = Geometry()
        geometry.vertices = [[0.0, 0.0, 0.0], [3.0, 0.0, 0.0]]
        geometry.lines = [Line2(a=0, b=1)]
        material = Material(
            color=(1.0, 0.0, 0.0), diffuse=(1.0, 0.0, 0.0), specular=(0.35, 0.35, 0.35)
        )
        x_line = Lines(geometry, material)


        geometry = Geometry()
        geometry.vertices = [[0.0, 0.0, 0.0], [0.0, 3.0, 0.0]]
        geometry.lines = [Line2(a=0, b=1)]
        material = Material(
            color=(0.0, 1.0, 0.0), diffuse=(0.0, 1.0, 0.0), specular=(1.0, 1.0, 1.0)
        )
        y_line = Lines(geometry, material)


        geometry = Geometry()
        geometry.vertices = [[0.0, 0.0, 0.0], [0.0, 0.0, 3.0]]
        geometry.lines = [Line2(a=0, b=1)]
        material = Material(
            color=(0.0, 0.0, 1.0), diffuse=(0.0, 0.0, 1.0), specular=(0.35, 0.35, 0.35)
        )
        z_line = Lines(geometry, material)

        x_line.position.y = 0.5
        x_line.position.x = 0.5
        x_line.position.z = 0.5

        root = ObjectTrackball(camera, 10, renderer)
        root.triad = x_line
        
        scene = Scene()
        scene.add(obj_1)
        scene.add(obj_2)
        scene.add(lines_1)
        scene.add(lines_2)
        scene.add(lines_3)
        scene.add(lines_4)
        scene.add(x_line)
        x_line.add(y_line)
        x_line.add(z_line)
        root.object_list.append({"id": id_color_obj_1, "obj": obj_1})
        root.object_list.append({"id": id_color_obj_2, "obj": obj_2})

        renderer.render(scene, camera)
        renderer.main_light.intensity = 1000
        renderer.main_light.pos = (10, 10, -10)

        root.add_widget(renderer)

        box = BoxLayout()
        box.add_widget(root)

        controls = Controls()
        root.controls = controls
        box.add_widget(controls)

        def _adjust_aspect(inst, val):
            rsize = renderer.size
            aspect = rsize[0] / float(rsize[1])
            renderer.camera.aspect = aspect
        renderer.bind(size=_adjust_aspect)
        
        return box


class Controls(BoxLayout):
    """Sidebar, using .kv only
    """
    pass


class ObjectTrackball(FloatLayout):
    selected_object = None
    object_list = []
    controls = ObjectProperty()
    triad = None

    def __init__(self, camera, radius, renderer, *args, **kw):
        super(ObjectTrackball, self).__init__(*args, **kw)
        self.renderer = renderer
        self.camera = camera
        self.radius = radius
        self.phi = 90
        self.theta = 0
        self._touches = []
        self.camera.pos.z = radius
        camera.look_at((0, 0, 0))

    def on_controls(self, inst, controls):
        controls.bind(x_rot=self.set_rotation)
        controls.bind(y_rot=self.set_rotation)
        controls.bind(z_rot=self.set_rotation)
        controls.bind(x_trans=self.set_rotation)
        controls.bind(y_trans=self.set_rotation)
        controls.bind(z_trans=self.set_rotation)

    def set_rotation(self, inst, value):
        if self.triad:
            self.triad.rot.x = self.controls.x_rot
            self.triad.rot.y = self.controls.y_rot
            self.triad.rot.z = self.controls.z_rot
            self.triad.pos.x = self.controls.x_trans
            self.triad.pos.y = self.controls.y_trans
            self.triad.pos.z = self.controls.z_trans
            self.camera.look_at((0, 0, 0))

    def define_rotate_angle(self, touch):
        theta_angle = (touch.dx / self.width) * -360
        phi_angle = (touch.dy / self.height) * 360
        return phi_angle, theta_angle

    def on_touch_down(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]):
            touch.grab(self)
            self._touches.append(touch)
            self.select_clicked_object(touch)

    def select_clicked_object(self, touch):
        self.renderer.fbo.shader.source = os.path.join(_this_path, "./select_mode.glsl")
        self.renderer.set_clear_color((0.0, 0.0, 0.0, 0.0))
        self.renderer.fbo.ask_update()
        self.renderer.fbo.draw()
        print(self.renderer.fbo.get_pixel_color(touch.x, touch.y))

        selection_id = self.renderer.fbo.get_pixel_color(touch.x, touch.y)
        print(self.get_selected_object(selection_id))

        self.renderer.fbo.shader.source = shader_file
        self.renderer.set_clear_color(clear_color)
        self.renderer.fbo.ask_update()
        self.renderer.fbo.draw()

    def on_touch_up(self, touch):
        if touch in self._touches:
            touch.ungrab(self)
            self._touches.remove(touch)

    def on_touch_move(self, touch):
        if touch in self._touches and touch.grab_current == self:
            if self.selected_object:
                self.move_object(touch)
            elif len(self._touches) == 1:
                self.do_rotate(touch)
            elif len(self._touches) == 2:
                pass

    def do_rotate(self, touch):
        d_phi, d_theta = self.define_rotate_angle(touch)
        self.phi += d_phi
        self.theta += d_theta

        while self.phi < -180:
            self.phi += 360
        while self.phi > 180:
            self.phi -= 360

        while self.theta < -180:
            self.theta += 360
        while self.theta > 180:
            self.theta -= 360

        _phi = math.radians(self.phi)
        _theta = math.radians(self.theta)
        z = self.radius * math.cos(_theta) * math.sin(_phi)
        x = self.radius * math.sin(_theta) * math.sin(_phi)
        y = self.radius * math.cos(_phi)
        self.camera.pos = x, y, z
        self.camera.look_at((0, 0, 0))
        # print("phi", round(self.phi, 2), "theta", round(self.theta, 2),
        #       'camera pos', round(x, 2), round(y, 2), round(z, 2))

    def move_object(self, touch):
        mouse_x = [0, 0, 0]
        mouse_y = [0, 0, 0]

        if -135 < self.phi < -45:
            if -135 < self.theta < -45:
                # print('a -zy')
                mouse_x = [0, 0, -1]
                mouse_y = [0, 1, 0]
            elif -45 < self.theta < 45:
                # print('b -xy')
                mouse_x = [-1, 0, 0]
                mouse_y = [0, 1, 0]
            elif 45 < self.theta < 135:
                # print('c zy')
                mouse_x = [0, 0, 1]
                mouse_y = [0, 1, 0]
            else:  # self.theta > 135 or self.theta < -135
                # print('d xy')
                mouse_x = [1, 0, 0]
                mouse_y = [0, 1, 0]

        elif -45 < self.phi < 0:
            if -135 < self.theta < -45:
                # print('e -z-x')
                mouse_x = [0, 0, -1]
                mouse_y = [-1, 0, 0]
            elif -45 < self.theta < 45:
                # print('f -xz')
                mouse_x = [-1, 0, 0]
                mouse_y = [0, 0, 1]
            elif 45 < self.theta < 135:
                # print('g zx')
                mouse_x = [0, 0, 1]
                mouse_y = [1, 0, 0]
            else:  # self.theta > 135 or self.theta < -135
                # print('h x-z')
                mouse_x = [1, 0, 0]
                mouse_y = [0, 0, -1]

        elif 0 < self.phi < 45:
            if -135 < self.theta < -45:
                # print('e2 zx')
                mouse_x = [0, 0, 1]
                mouse_y = [1, 0, 0]
            elif -45 < self.theta < 45:
                # print('f2 x-z')
                mouse_x = [1, 0, 0]
                mouse_y = [0, 0, -1]
            elif 45 < self.theta < 135:
                # print('g2 -z-x')
                mouse_x = [0, 0, -1]
                mouse_y = [-1, 0, 0]
            else:  # self.theta > 135 or self.theta < -135
                # print('h2 -xz')
                mouse_x = [-1, 0, 0]
                mouse_y = [0, 0, 1]

        elif 45 < self.phi < 135:
            if -135 < self.theta < -45:
                # print('i zy')
                mouse_x = [0, 0, 1]
                mouse_y = [0, 1, 0]
            elif -45 < self.theta < 45:
                # print('j xy')
                mouse_x = [1, 0, 0]
                mouse_y = [0, 1, 0]
            elif 45 < self.theta < 135:
                # print('k -zy')
                mouse_x = [0, 0, -1]
                mouse_y = [0, 1, 0]
            else:  # self.theta > 135 or self.theta < -135
                # print('l -xy')
                mouse_x = [-1, 0, 0]
                mouse_y = [0, 1, 0]

        elif self.phi > 135:
            if -135 < self.theta < -45:
                # print('m z-x')
                mouse_x = [0, 0, 1]
                mouse_y = [-1, 0, 0]
            elif -45 < self.theta < 45:
                # print('n xz')
                mouse_x = [1, 0, 0]
                mouse_y = [0, 0, 1]
            elif 45 < self.theta < 135:
                pass
                # print('o -zx')
                mouse_x = [0, 0, -1]
                mouse_y = [1, 0, 0]
            else:  # self.theta > 135 or self.theta < -135
                # print('p -x-z')
                mouse_x = [-1, 0, 0]
                mouse_y = [0, 0, -1]

        else:  # self.phi < -135
            if -135 < self.theta < -45:
                # print('m2 -zx')
                mouse_x = [0, 0, -1]
                mouse_y = [1, 0, 0]
            elif -45 < self.theta < 45:
                # print('n2 -x-z')
                mouse_x = [-1, 0, 0]
                mouse_y = [0, 0, -1]
            elif 45 < self.theta < 135:
                # print('o2 z-x')
                mouse_x = [0, 0, 1]
                mouse_y = [-1, 0, 0]
            else:  # self.theta > 135 or self.theta < -135
                # print('p2 xz')
                mouse_x = [1, 0, 0]
                mouse_y = [0, 0, 1]

        mouse_x = [touch.dx * 0.01 * i for i in mouse_x]
        mouse_y = [touch.dy * 0.01 * i for i in mouse_y]
        self.selected_object.position.x += mouse_x[0] + mouse_y[0]
        self.selected_object.position.y += mouse_x[1] + mouse_y[1]
        self.selected_object.position.z += mouse_x[2] + mouse_y[2]

    def get_selected_object(self, selected_id):
        for obj in self.object_list:
            if list(obj["id"][0:3]) == selected_id[0:3]:
                self.selected_object = obj["obj"]
                return self.selected_object
        self.selected_object = None


if __name__ == "__main__":
    RotationExample().run()
