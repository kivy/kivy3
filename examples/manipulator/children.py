from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy3 import Material
from kivy3 import Mesh
from kivy3 import PerspectiveCamera
from kivy3 import Renderer
from kivy3 import Scene
from kivy3.extras.geometries import BoxGeometry
import math
import os

# Resources paths
_this_path = os.path.dirname(os.path.realpath(__file__))
shader_file = os.path.join(_this_path, "../extended.glsl")

JOINT_SIZE_A = [0.140, 0.030, 0.050]
JOINT_OFFSET_A_1 = [0, 0.0325, -0.21382]
JOINT_OFFSET_A_2 = [0, -0.0325, -0.21382]

JOINT_SIZE_B = [0.21382, 0.0408, 0.0408]
JOINT_OFFSET_B = [0.04091, 0, 0]

JOINT_SIZE_C = [0.077, 0.0408, 0.0408]
JOINT_OFFSET_C = [0.0409, 0, -0.2007]

JOINT_SIZE_D = [0.2007, 0.0408, 0.0408]
JOINT_OFFSET_D = [0.0408, 0, 0]

JOINT_SIZE_E = [0.077, 0.0408, 0.0408]
JOINT_OFFSET_E = [0.2896, 0, 0]

JOINT_SIZE_F = [0.290, 0.046, 0.046]
JOINT_OFFSET_F = [0.046, 0, 0.10976]

JOINT_SIZE_G = [0.145, 0.046, 0.046]
JOINT_OFFSET_G = [0, 0, 0]


def create_joint_rectangle(x, y, z):
    geometry = BoxGeometry(x, y, z)
    for vertice in geometry.vertices:
        vertice[0] += x / 2
    return geometry


def get_joint_hypo_length(xyz):
    squares = 0
    for n in xyz:
        squares += math.pow(n, 2)
    return math.sqrt(squares)


class ObjectTrackball(BoxLayout):

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
        phi_angle = -1 * (touch.dy / self.height) * 360
        return phi_angle, theta_angle

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if "button" in touch.profile:
                if touch.button == "scrollup":
                    if self.radius > 0:
                        self.radius *= 1.1
                    self.update_after_scroll()
                elif touch.button == "scrolldown":
                    if self.radius > 0:
                        self.radius *= 0.9
                    self.update_after_scroll()
                else:
                    touch.grab(self)
                    self._touches.append(touch)

    def on_touch_up(self, touch):
        touch.ungrab(self)
        if touch in self._touches:
            self._touches.remove(touch)
        self.camera.update()

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

    def update_after_scroll(self):
        _phi = math.radians(self.phi)
        _theta = math.radians(self.theta)
        z = self.radius * math.cos(_theta) * math.sin(_phi)
        x = self.radius * math.sin(_theta) * math.sin(_phi)
        y = self.radius * math.cos(_phi)
        self.camera.pos = x, y, z
        self.camera.look_at((0, 0, 0))


class BaseBox(BoxLayout):
    theta = ListProperty([0, 0, 0, 0, 0, 0, 0])
    joints = []
    renderer = ObjectProperty()

    def on_theta(self, inst, value):
        self.joints[7].rotation.x = value[6]  # g
        self.joints[6].rotation.z = value[5]  # f
        self.joints[5].rotation.z = value[4]  # e
        self.joints[4].rotation.x = value[3]  # d
        self.joints[3].rotation.z = value[2]  # c
        self.joints[2].rotation.x = value[1]  # b
        self.joints[1].rotation.y = -value[0]
        self.joints[0].rotation.y = value[0]  # a


class ManipulatorExample(App):
    """Demonstrate relative transform of children of a Mesh object in the
    scene.
    """

    joints = []

    def build(self):
        manipulator = self.construct_manipulator()

        scene = Scene()
        scene.add(manipulator)

        camera = PerspectiveCamera(75, 0.01, 0.01, 1500)

        renderer = self.renderer = Renderer(shader_file=shader_file)
        renderer.set_clear_color((0.2, 0.2, 0.2, 1.0))
        renderer.bind(size=self._adjust_aspect)
        renderer.render(scene, camera)
        renderer.main_light.intensity = 3000

        trackball = ObjectTrackball(camera, 2)
        trackball.add_widget(renderer)

        root = BaseBox()
        root.add_widget(trackball)

        root.joints = self.joints
        root.renderer = renderer
        return root

    def _adjust_aspect(self, inst, val):
        rsize = self.renderer.size
        aspect = rsize[0] / float(rsize[1])
        self.renderer.camera.aspect = aspect

    def _rotate_cube(self, dt):
        self.axis_e.rotation.x += 0
        self.axis_e.rotation.y += 1
        self.axis_e.rotation.z += 1

    def _rotate_rect(self, dt):
        self.axis_d.rotation.x += 0.5

    def construct_manipulator(self):
        material = Material(
            color=(0.0, 0.0, 1.0),
            diffuse=(1.0, 1.0, 0.0),
            specular=(0.35, 0.35, 0.35)
        )

        # axis a one jaw
        axis_a_dimensions = (
            JOINT_SIZE_A[0],
            JOINT_SIZE_A[2],
            JOINT_SIZE_A[1]
        )
        axis_a_geometry = create_joint_rectangle(*axis_a_dimensions)
        axis_a_left_mesh = Mesh(axis_a_geometry, material)
        axis_a_right_mesh = Mesh(axis_a_geometry, material)
        self.joints.append(axis_a_left_mesh)
        self.joints.append(axis_a_right_mesh)

        # axis b wrist
        axis_b_dimensions = (
            get_joint_hypo_length(JOINT_OFFSET_A_1),
            JOINT_SIZE_B[1],
            JOINT_SIZE_B[2],
        )
        axis_b_geometry = create_joint_rectangle(*axis_b_dimensions)
        material = Material(
            color=(1.0, 0.0, 0.0),
            diffuse=(1.0, 0.0, 0.0),
            specular=(0.35, 0.35, 0.35)
        )
        axis_b_mesh = Mesh(axis_b_geometry, material)
        self.joints.append(axis_b_mesh)

        axis_b_mesh.add(axis_a_left_mesh)
        axis_a_left_mesh.pos.x = axis_b_dimensions[0]
        axis_a_left_mesh.pos.z = axis_b_dimensions[2] / 2

        axis_b_mesh.add(axis_a_right_mesh)
        axis_a_right_mesh.pos.x = axis_b_dimensions[0]
        axis_a_right_mesh.pos.z = -axis_b_dimensions[2] / 2

        # axis c bend
        axis_c_dimensions = (
            get_joint_hypo_length(JOINT_OFFSET_B),
            JOINT_SIZE_C[1],
            JOINT_SIZE_C[2],
        )
        axis_c_geometry = create_joint_rectangle(*axis_c_dimensions)
        material = Material(
            color=(1.0, 1.0, 0.0),
            diffuse=(1.0, 1.0, 0.0),
            specular=(0.35, 0.35, 0.35)
        )
        axis_c_mesh = Mesh(axis_c_geometry, material)
        self.joints.append(axis_c_mesh)

        axis_c_mesh.add(axis_b_mesh)
        axis_b_mesh.pos.x = axis_c_dimensions[0]

        # axis d bend
        axis_d_dimensions = (
            get_joint_hypo_length(JOINT_OFFSET_C),
            JOINT_SIZE_D[1],
            JOINT_SIZE_D[2],
        )
        axis_d_geometry = create_joint_rectangle(*axis_d_dimensions)
        material = Material(
            color=(1.0, 0.0, 1.0),
            diffuse=(1.0, 0.0, 1.0),
            specular=(0.35, 0.35, 0.35)
        )
        axis_d_mesh = Mesh(axis_d_geometry, material)
        self.joints.append(axis_d_mesh)

        axis_d_mesh.add(axis_c_mesh)
        axis_c_mesh.pos.x = axis_d_dimensions[0]

        # axis e mesh
        axis_e_dimensions = (
            get_joint_hypo_length(JOINT_OFFSET_D),
            JOINT_SIZE_E[1],
            JOINT_SIZE_E[2],
        )
        axis_e_geometry = create_joint_rectangle(*axis_e_dimensions)
        material = Material(
            color=(0.0, 1.0, 0.0),
            diffuse=(0.0, 1.0, 0.0),
            specular=(0.35, 0.35, 0.35)
        )
        axis_e_mesh = Mesh(axis_e_geometry, material)
        self.joints.append(axis_e_mesh)

        axis_e_mesh.add(axis_d_mesh)
        axis_d_mesh.pos.x = axis_e_dimensions[0]

        # axis f
        axis_f_dimensions = (
            get_joint_hypo_length(JOINT_OFFSET_E),
            JOINT_SIZE_F[1],
            JOINT_SIZE_F[2],
        )
        axis_f_geometry = create_joint_rectangle(*axis_f_dimensions)
        material = Material(
            color=(0.0, 1.0, 1.0),
            diffuse=(0.0, 1.0, 1.0),
            specular=(0.35, 0.35, 0.35)
        )
        axis_f_mesh = Mesh(axis_f_geometry, material)
        self.joints.append(axis_f_mesh)

        axis_f_mesh.add(axis_e_mesh)
        axis_e_mesh.pos.x = axis_f_dimensions[0]

        # axis g
        axis_g_dimensions = (
            get_joint_hypo_length(JOINT_OFFSET_F),
            JOINT_SIZE_G[1],
            JOINT_SIZE_G[2],
        )
        axis_g_geometry = create_joint_rectangle(*axis_g_dimensions)
        material = Material(
            color=(1.0, 0.4, 0.1),
            diffuse=(1.0, 0.4, 0.1),
            specular=(0.35, 0.35, 0.35)
        )
        axis_g_mesh = Mesh(axis_g_geometry, material)
        self.joints.append(axis_g_mesh)

        axis_g_mesh.add(axis_f_mesh)
        axis_f_mesh.pos.x = axis_g_dimensions[0]
        axis_f_mesh.rotation.z = -90

        # base
        base_dimensions = (
            0.05,
            axis_b_dimensions[1],
            axis_b_dimensions[2]
        )
        base_geometry = create_joint_rectangle(*base_dimensions)
        material = Material(
            color=(0.0, 1.0, 1.0),
            diffuse=(0.0, 1.0, 1.0),
            specular=(0.35, 0.35, 0.35)
        )
        base_mesh = Mesh(base_geometry, material)
        self.joints.append(base_mesh)

        base_mesh.add(axis_g_mesh)
        base_mesh.rotation.z = 90

        axis_g_mesh.pos.x = base_dimensions[0]
        axis_g_mesh.rotation.z = -90

        return base_mesh


if __name__ == "__main__":
    Builder.load_file("children.kv")
    ManipulatorExample().run()
