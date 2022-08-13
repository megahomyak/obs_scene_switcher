import wx.adv
import websocket
import json
import uuid
from PIL import Image, ImageDraw, ImageFont

FONT = ImageFont.truetype("arial.ttf", 230)
OP_HELLO = 0
OP_IDENTIFY = 1
OP_IDENTIFIED = 2
OP_REQUEST = 6
socket = websocket.WebSocket()
socket.connect("ws://localhost:4455")


def recv():
    return json.loads(socket.recv())


def send(data):
    return socket.send(json.dumps(data))


def request(request_type, data):
    d = {"requestType": request_type, "requestId": str(uuid.uuid4())}
    if data:
        d["requestData"] = data
    send({"op": OP_REQUEST, "d": d})
    resp = recv()
    try:
        return resp["d"]["responseData"]
    except KeyError:
        return


resp = recv()
assert resp["op"] == OP_HELLO
send({"op": OP_IDENTIFY, "d": {"rpcVersion": resp["d"]["rpcVersion"]}})
assert recv()["op"] == OP_IDENTIFIED
scenes_info = request("GetSceneList", data=None)
scene_names = [scene["sceneName"] for scene in scenes_info["scenes"]]
current_scene_index = scene_names.index(scenes_info["currentProgramSceneName"])


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self):
        super().__init__()
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, lambda _: self.next_scene())
        self.set_text_from_current_scene()

    def next_scene(self):
        global current_scene_index
        current_scene_index += 1
        if current_scene_index == len(scene_names):
            current_scene_index = 0
        request("SetCurrentProgramScene", {"sceneName": scene_names[current_scene_index]})
        self.set_text_from_current_scene()

    def set_text_from_current_scene(self):
        self.set_text(scene_names[current_scene_index][0])

    def set_text(self, text):
        image = Image.new("RGB", (256, 256), color="black")
        draw = ImageDraw.Draw(image)
        text_width = FONT.getmask(text).getbbox()[2]
        draw.text(
            ((image.width - text_width) / 2, 0),
            text,
            font=FONT,
            fill="white"
        )
        icon = wx.Icon()
        icon.CopyFromBitmap(
            wx.Bitmap.FromBuffer(
               image.width, image.height, image.tobytes()
            )
        )
        self.SetIcon(icon)


class App(wx.App):
    def OnInit(self):
        self.tskic = TaskBarIcon()
        return True


App().MainLoop()
