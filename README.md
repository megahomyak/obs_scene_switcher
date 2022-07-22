# What?

This program allows to switch OBS scenes by clicking the toolbar icon, on which the first letter of
the name of the current scene is written.

# Why?

I needed a convenient way to switch the scenes and know which one is active right now. Since this is
a personal tool, there are a few considerations:

* It does not account for any changes in scenes list after the launch
* It does not account for sudden disconnects from OBS
* It does not allow for easy customization, you'll have to edit the source code
* It is not guaranteed to work anywhere, but was successfully used on Windows 10
* It is up to the user to run this program in the background

# How?

* If you have OBS Studio < 28.0.0, install [obs-websocket](https://github.com/obsproject/obs-websocket)
* Run `pip install -r requirements.txt`
* Run `obs_scene_switcher.py` using Python (e.g. `python obs_scene_switcher.py`)

Just stop the script to shut this utility down.
