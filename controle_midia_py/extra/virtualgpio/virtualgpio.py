from gpiozero.pins.mock import MockFactory, MockTriggerPin, MockPWMPin
from gpiozero import Device
from tkinter import *
from PIL import ImageTk, Image, ImageEnhance
from threading import Thread, Timer
from time import sleep, perf_counter
from sounddevice import play, stop
import numpy
import scipy.signal
from os import path
import sys
from pathlib import Path
from platform import system
from functools import partial
from math import sqrt

class PreciseMockTriggerPin(MockTriggerPin, MockPWMPin):
    def _echo(self):
        sleep(0.001)
        self.echo_pin.drive_high()
        
        # sleep(), time() and monotonic() dont have enough precision!
        init_time = perf_counter()
        while True:
            if perf_counter() - init_time >= self.echo_time:
                break
        
        self.echo_pin.drive_low()
        
        
class PreciseMockFactory(MockFactory):
    @staticmethod
    def ticks():
        # time() and monotonic() dont have enough precision!
        return perf_counter()
    

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class TkDevice():
    _images = {}
    
    def __init__(self, root, x, y, name):
        self._root = root
        self._name = name
        self._x = x
        self._y = y
        self._widget = None
        self._image_states = {}
        
        text_label = Label(root, text=name, background="white", anchor="w")
        text_label.place(x=x, y=y-20)
        
    def _redraw(self):
        self._root.update()
    
    def _create_main_widget(self, widget_class, initial_state=None):
        self._widget = widget_class(self._root, background="white")
        self._widget.place(x=self._x, y=self._y)
        
        if initial_state != None:
            self._change_widget_image(initial_state)
        
        return self._widget
    
    def _set_image_for_state(self, image_file_name, state, dimensions=None):
        if image_file_name in TkDevice._images:
            image = TkDevice._images[image_file_name]
        else:
            current_folder = path.dirname(__file__)
            file_path = path.join(current_folder, "images/" + image_file_name)

            image = Image.open(file_path)
            if dimensions != None:
                image = image.resize(dimensions, Image.ANTIALIAS)
            
            TkDevice._images[image_file_name] = image
            
        self._image_states[state] = image
        
        return image
        
    def _change_widget_image(self, image_or_state):
        if self._widget != None:
            if isinstance(image_or_state, str):
                state = image_or_state
                image = self._image_states[state]
            else:
                image = image_or_state
        
            self._photo_image = ImageTk.PhotoImage(image)
            self._widget.configure(image=self._photo_image)
        
            self._redraw()
        
class TkLCD(TkDevice):
    def __init__(self, root, x, y, name, pins, columns, lines):
        super().__init__(root, x, y, name)
        self._redraw()
     
        self._pins = pins
        self._columns = columns
        self._lines = lines
        
        if system() == "Darwin":
            font=("Courier", 25)
        else:
            font=("Courier", 20)
        self._label = Label(root,
            font=font, justify="left", anchor="nw",
            width=columns, height=lines, padx=5, pady=5,
            background="#82E007", borderwidth=2, relief="solid")
        self._label.place(x=x, y=y)
        
    def update_text(self, pins, text):
        if pins == self._pins:
            self._label.configure(text = text)
            self._root.update()
        
        
class TkBuzzer(TkDevice):
    SAMPLE_RATE = 44000
    PEAK = 0.1
    DUTY_CICLE = 0.5
    
    on_image = None
    off_image = None
    
    def __init__(self, root, x, y, name, pin, frequency=440):
        super().__init__(root, x, y, name)
        
        self._pin = Device.pin_factory.pin(pin)
        self._previous_state = None
        
        self._set_image_for_state("buzzer_on.png", "on", (50, 33))
        self._set_image_for_state("buzzer_off.png", "off", (50, 33))
        self._create_main_widget(Label, "off")
        
        if frequency != None:
            n_samples = self.SAMPLE_RATE
            t = numpy.linspace(0, 1, int(500 * 440/frequency), endpoint=False)
            wave = scipy.signal.square(2 * numpy.pi * 5 * t, duty=self.DUTY_CICLE)
            wave = numpy.resize(wave, (n_samples,))
            self._sample_wave = (self.PEAK / 2 * wave.astype(numpy.int16))
        else:
            self._sample_wave = numpy.empty(0)
        
    def update(self):
        if self._previous_state != self._pin.state:
            if self._pin.state == True:
                self._change_widget_image("on")
                if len(self._sample_wave) > 0:
                    play(self._sample_wave, self.SAMPLE_RATE, loop=True)
            else:
                self._change_widget_image("off")
                if len(self._sample_wave) > 0:
                    stop()
            
            self._previous_state = self._pin.state
            
            self._redraw()
    

class TkLED(TkDevice):
    on_image = None
    
    def __init__(self, root, x, y, name, pin):
        super().__init__(root, x, y, name)
        
        self._pin = Device.pin_factory.pin(pin, pin_class=MockPWMPin)
        
        self._previous_state = None
        
        TkLED.on_image = self._set_image_for_state("led_on.png", "on", (30, 30))
        self._set_image_for_state("led_off.png", "off", (30, 30))
        self._create_main_widget(Label, "off")
        
    def update(self):
        if self._previous_state != self._pin.state:
            if isinstance(self._pin.state, float):
                converter = ImageEnhance.Color(TkLED.on_image)
                desaturated_image = converter.enhance(self._pin.state)
                self._change_widget_image(desaturated_image)
            elif self._pin.state == True:
                self._change_widget_image("on")
            else:
                self._change_widget_image("off")
             
            self._previous_state = self._pin.state
            
            self._redraw()
        
class TkButton(TkDevice):
    def __init__(self, root, x, y, name, pin):
        super().__init__(root, x, y, name)
        
        self._pin = Device.pin_factory.pin(pin)
        
        self._set_image_for_state("button_pressed.png", "on", (30, 30))
        self._set_image_for_state("button_released.png", "off", (30, 30))
        button = self._create_main_widget(Button, "off")
        self._widget.bind("<ButtonPress>", self._on_press)
        self._widget.bind("<ButtonRelease>", self._on_release)
        
        #self._widget = Button(root, compound=LEFT, borderwidth=0, highlightthickness = 0,background="white", highlightbackground="white")
        
    def _on_press(self, botao):
        self._change_widget_image("on")
        
        thread = Thread(target=self._change_pin, daemon=True, args=(True,))
        thread.start()

    def _on_release(self, botao):
        self._change_widget_image("off")
        
        thread = Thread(target=self._change_pin, daemon=True, args=(False,))
        thread.start()
        
    def _change_pin(self, is_press):
        if is_press:
            self._pin.drive_low()
        else:
            self._pin.drive_high()
            
class TkMotionSensor(TkDevice):
    on_image = None
    off_image = None
    
    def __init__(self, root, x, y, name, pin, detection_radius=50, delay_duration=5, block_duration=3):
        super().__init__(root, x, y, name)
        
        self._pin = Device.pin_factory.pin(pin)
        
        self._detection_radius = detection_radius
        self._delay_duration = delay_duration
        self._block_duration = block_duration
        
        self._motion_timer = None
        self._block_timer = None
        
        self._set_image_for_state("motion_sensor_on.png", "motion", (80, 60))
        self._set_image_for_state("motion_sensor_off.png", "no motion", (80, 60))
        self._set_image_for_state("motion_sensor_wait.png", "wait", (80, 60))
        self._create_main_widget(Label, "no motion")
        
        root.bind('<Motion>', self._motion_detected)
        
    def _motion_detected(self, event):
        x_pointer = self._root.winfo_pointerx() - self._root.winfo_rootx()
        y_pointer = self._root.winfo_pointery() - self._root.winfo_rooty()
        x_center = self._widget.winfo_x() + self._widget.winfo_width() / 2
        y_center = self._widget.winfo_y() + self._widget.winfo_height() / 2
        distance = sqrt(pow(x_pointer - x_center, 2) + pow(y_pointer - y_center, 2))
        
        if distance < self._detection_radius and self._block_timer == None:
            if self._motion_timer == None:
                self._change_widget_image("motion")
            else:
                self._motion_timer.cancel()
                
            self._pin.drive_high()
                 
            self._motion_timer = Timer(self._delay_duration, self._remove_detection)
            self._motion_timer.start()
            
    def _remove_detection(self):
        self._pin.drive_low()
        self._change_widget_image("wait")
        
        self._motion_timer = None
        
        self._block_timer = Timer(self._block_duration, self._remove_block)
        self._block_timer.start()
    
    def _remove_block(self):
        self._change_widget_image("no motion")
        self._block_timer = None
            
            
class TkDistanceSensor(TkDevice):
    def __init__(self, root, x, y, name, trigger_pin, echo_pin, min_distance=0, max_distance=50):
        super().__init__(root, x, y, name)
        
        self._echo_pin = Device.pin_factory.pin(echo_pin)
        self._trigger_pin = Device.pin_factory.pin(trigger_pin,
            pin_class=PreciseMockTriggerPin, echo_pin=self._echo_pin, echo_time=0.004)
        
        self._echo_pin._bounce = 0
        self._trigger_pin._bounce = 0
        
        self._set_image_for_state("distance_sensor.png", "normal", (86, 50))
        self._create_main_widget(Label, "normal")
        
        self._scale = Scale(root, from_=min_distance, to=max_distance,
            orient=HORIZONTAL, command=self._scale_changed, sliderlength=20, length=150, highlightthickness = 0, background="white")
        self._scale.place(x=x+100, y=y)
        self._scale.set(round((min_distance + max_distance) / 2))
        self._scale_changed(self._scale.get())
        
    def _scale_changed(self, value):
        speed_of_sound = 343.26 # m/s
        distance = float(value) / 100 # cm -> m
        self._trigger_pin.echo_time = distance * 2 / speed_of_sound

class TkCircuit(metaclass=SingletonMeta):
    SAMPLE_RATE = 44000
    
    def __init__(self, setup):
        Device.pin_factory = PreciseMockFactory(pin_class=MockPWMPin)
        
        sys.path.insert(0, str(Path(__file__).parent.absolute()))
        
        default_setup = {
            "name": "Virtual GPIO",
            "width": 500, "height": 500,
            "leds":[], "buzzers":[], "buttons":[],
            "lcds":[],
            "motion_sensors": [],
            "distance_sensors": [],
            "infrared_receiver": None,
            "infrared_emitter": None
        }
        
        default_setup.update(setup)
        setup = default_setup
                
        self._root = Tk()
        self._root.title(setup["name"])
        self._root.geometry("%dx%d" % (setup["width"], setup["height"]))
        self._root.resizable(False, False)
        self._root["background"] = "white"
        self._root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        self._outputs = []
        self._outputs += [self.add_device(TkLED, parameters) for parameters in setup["leds"]]
        self._outputs += [self.add_device(TkBuzzer, parameters) for parameters in setup["buzzers"]]
        
        self._lcds = [self.add_device(TkLCD, parameters) for parameters in setup["lcds"]]
        
        [self.add_device(TkButton, parameters) for parameters in setup["buttons"]]
        [self.add_device(TkDistanceSensor, parameters) for parameters in setup["distance_sensors"]]
        [self.add_device(TkMotionSensor, parameters) for parameters in setup["motion_sensors"]]
        
        if setup["infrared_receiver"] != None:
            self.add_device(TkInfraredReceiver, setup["infrared_receiver"])
#             
#         if setup["infrared_emitter"] != None:
#             TkInfraredEmitter(self._root, setup["infrared_emitter"])
            
    def add_device(self, device_class, parameters):
        return device_class(self._root, **parameters)
        
    def run(self, function):
        thread = Thread(target=function, daemon=True)
        thread.start()
        
        self._root.after(10, self._update_outputs)    
        self._root.mainloop()
        
    def _update_outputs(self):
        for output in self._outputs:
            output.update()
            
        self._root.after(10, self._update_outputs)
        
    def update_lcds(self, pins, text):
        for lcds in self._lcds:
            lcds.update_text(pins, text)
            
    def _on_closing(self):
        sys.exit();
            
            
class TkInfraredReceiver(TkDevice, metaclass=SingletonMeta):

    def __init__(self, root, x, y, name, config, remote_control):
        super().__init__(root, x, y, name)
        
        remote = remote_control
        
        frame = Frame(root, bg = remote["color"], width = remote["width"], height = remote["height"])
        frame.place(x=x, y=y)
        
        self._config = config
        self._key_codes = []
        self._pressed_key_codes = []
        
        for i in range(0, len(remote["key_rows"])):
            row = remote["key_rows"][i]
            for j in range(0, len(row["buttons"])):
                button_setup = row["buttons"][j]
                if button_setup != None:
                    code = button_setup.get("code", "KEY_" + button_setup["name"])
                    self._key_codes.append(code)
                    
                    command = partial(self._key_press, code)
                    
                    button = Button(frame, text=button_setup["name"],
                                    width=remote["key_width"], height=remote["key_height"],
                                    command=command,
                                    justify=CENTER, borderwidth=0, highlightthickness = 0)
                    button.grid(row=i, column=j, padx=8, pady=8)
        
        frame.configure(width = remote["width"], height = remote["height"])
    
    def config_name(self):
        return self._config
    
    def clear_codes(self):
        self._pressed_key_codes = []
    
    def get_next_code(self):
        if len(self._pressed_key_codes) == 0:
            return []
        else:
            return [self._pressed_key_codes.pop(0)]
    
    def _key_press(self, code):
        self._pressed_key_codes.append(code)
        
        
        
class TkInfraredEmitter(TkDevice, metaclass=SingletonMeta):
    on_image = None
    off_image = None
    _timer = None
    
    def __init__(self, root, data):
        super().__init__(root, data)
        
        remote_controls = data["remote_controls"]
        
        if TkInfraredEmitter.on_image == None:
            TkInfraredEmitter.on_image = self.load_image("emitter_on.png", (50, 30))
            TkInfraredEmitter.off_image = self.load_image("emitter_off.png", (50, 30))
        
        self._widget = Label(root, background="white")
        self._widget.place(x=self.x, y=self.y)
        self.change_widget_image(TkInfraredEmitter.off_image)
        
        self._remote_controls = remote_controls
        
    def list_remotes(self, remote):
        return self._remote_controls.keys()
    
    def list_codes(self, remote):
        valid_codes = self._remote_controls.get(remote, None)
        
        if valid_codes == None:
             print("\x1b[1;37;41m" + remote + ": INVALID REMOTE CONTROL!" + "\x1b[0m")
             
        return valid_codes
        
    def send_once(self, remote, codes, count):
        valid_codes = self.list_codes(remote)
        if valid_codes == None:
            return
        
        has_valid_code = False
        for code in codes:
            if code in valid_codes:
                print("\x1b[1;37;42m" + code + " of remote \"" + remote + "\" transmitted!" + "\x1b[0m")
                has_valid_code = True
            else:
                print("\x1b[1;37;41m" + code + ": INVALID CODE FOR REMOTE \"" + remote +  "\"!" + "\x1b[0m")
                
        if has_valid_code:
            if self._timer != None:
                self._timer.cancel()
                
            self.change_widget_image(TkInfraredEmitter.on_image)
                
            self._timer = Timer(1, self._turn_off_emitter).start()
            
    def _turn_off_emitter(self):
        self.change_widget_image(TkInfraredEmitter.off_image)
        self._timer = None

