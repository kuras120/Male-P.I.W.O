import subprocess
import threading

from sound import PAPLAY_MAX_VOLUME_VAL


def play_sound(path: str, volume: float) -> None:
    print(path, volume)
    volume_val: int = int(volume * PAPLAY_MAX_VOLUME_VAL)
    cmd: str = "paplay {} --volume {} -v".format(path, volume_val)
    cmd1 = subprocess.Popen(['echo', 'simbadcore'], stdout=subprocess.PIPE)
    cmd2 = subprocess.Popen(['sudo', '-S', cmd], stdin=cmd1.stdout, stdout=subprocess.PIPE)
    cmd2.wait()
    return


def play_sound_in_background(path: str, volume: float) -> None:
    print("Playing {} in background...".format(path))
    thread = threading.Thread(target=play_sound, args=(path, volume))
    thread.daemon = False
    thread.start()
    return


