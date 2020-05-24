from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy3 import PerspectiveCamera
from kivy3 import Renderer
from kivy3 import Scene
from kivy3.loaders import OBJLoader
import os

# Resources pathes
_this_path = os.path.dirname(os.path.realpath(__file__))
shader_file = os.path.join(_this_path, "./simple.glsl")
obj_file = os.path.join(_this_path, "./monkey.obj")


class MainApp(App):
    def build(self):
        root = FloatLayout()
        self.renderer = Renderer(shader_file=shader_file)
        scene = Scene()
        # load obj file
        loader = OBJLoader()
        obj = loader.load(obj_file)
        self.monkey = obj.children[0]

        scene.add(*obj.children)
        camera = PerspectiveCamera(15, 1, 1, 1000)

        self.renderer.render(scene, camera)
        root.add_widget(self.renderer)
        Clock.schedule_interval(self._update_obj, 1.0 / 20)
        self.renderer.bind(size=self._adjust_aspect)
        return root

    def _update_obj(self, dt):
        obj = self.monkey
        if obj.pos.z > -30:
            obj.pos.z -= 0.5

    def _adjust_aspect(self, inst, val):
        rsize = self.renderer.size
        aspect = rsize[0] / float(rsize[1])
        self.renderer.camera.aspect = aspect


if __name__ == "__main__":
    MainApp().run()
