import kivy
kivy.require('1.9.0')
import cv2
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import imrecog as ir


Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        play: True
        
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp' 
         
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
        
''')

class CameraClick(BoxLayout):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''

        camera = self.ids['camera']
        camera.export_to_png("image/IMG.png")
        print("Captured")
        self.ids['camera'].play = False
        self.clear_widgets()
        self.main()

    def main(self):
        ir.maybe_download_and_extract()
        img = (ir.FLAGS.image_file if ir.FLAGS.image_file else
                 ir.os.path.join('image/', 'IMG.png'))
        string = ir.run_inference_on_image(img)
        self.add_widget(Label(text=string, text_size=(600, None), line_height=1.5))

class ImageRecognition(App):

    def build(self):
        return CameraClick()

if __name__ == "__main__":
    imagerecognition = ImageRecognition()
    imagerecognition.run()
