import subprocess
import threading

from sound import PAPLAY_MAX_VOLUME_VAL


def play_sound(path: str, volume: float) -> None:
    print(path, volume)
    volume_val: int = int(volume * PAPLAY_MAX_VOLUME_VAL)
    cmd: str = "paplay {} --volume {} -v".format(path, volume_val)
    process = subprocess.Popen(cmd, shell=True)
    process.wait()
    return


def play_sound_in_background(path: str, volume: float) -> None:
    thread = threading.Thread(target=play_sound, args=(path, volume))
    thread.daemon = False
    thread.start()
    return

# play_sound_in_background(os.path.join(ANIMATIONS_ROOT_DIR, 'test_animation/never_gonna_give_you_up.wav'), 0.5)
# play_sound(os.path.join(ANIMATIONS_ROOT_DIR, 'test_animation/never_gonna_give_you_up.wav'), 0.5)

