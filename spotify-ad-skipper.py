import osascript
import time


DURATION = """
    set trackDuration to duration of current track
    set trackPosition to player position
    return trackDuration/1000 - trackPosition
"""

TRACK = """
    set currentArtist to artist of current track as string
    set currentTrack to name of current track as string
    set trackDuration to duration of current track
    return currentArtist & " - " & currentTrack  & " @ " & trackDuration
"""

RUNNING = """
    if it is running then
        return true
    else
        return false
    end if
"""

BACKGROUND = """
    set visible of process "Spotify" to false
"""

VISIBLE = """
    get visible of process "Spotify"
"""


def check(command, app="Spotify"):
    template = 'tell application "{}" \n{}\nend tell'
    _, x, _ = osascript.run(template.format(app, command))
    if x:
        print(x)
    return x

def restart():
    implement = check
    implement("quit")
    implement("play")
    
    for _ in range(30):
        if check(VISIBLE, "System Events"):
            implement(BACKGROUND, "System Events")
            break
        time.sleep(1)
        if _ % 10 == 0:
            print('relaunch')
            implement("play")
    
    time.sleep(9)
    for _ in range(3):
        if check(VISIBLE, "System Events") == 'true':
            implement(BACKGROUND, "System Events")
            break
        time.sleep(1)
    
    implement("play")
    time.sleep(15)

def is_adv(track):
    duration = float(track[track.index("@")+2:])/1000
    if "Advertisement" not in track and duration > 31:
        return
    print("rerun!")
    restart()


if check(RUNNING)=='true':
    while True:
        track = check(TRACK)
        is_adv(track)
        t = float(check(DURATION))
        time.sleep(t)
else:
    print("Spotify not running.")
