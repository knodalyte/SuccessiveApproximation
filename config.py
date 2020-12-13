""" ~/.config/qtile/config.py
"""
from libqtile.config import Key, Screen, Group, Click, Drag, Match
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from subprocess import call, Popen
#### check fonts, maybe need to install ms fonts using ttf-mscorefonts-installer

mod = "mod4"
alt = "mod1"
ctrl = "control"
shift = "shift"

font = 'Andika-R'
foreground = '#BBBBBB'
alert = "#FFFF00"
fontsize = 16

font_params = {
    'font': font,
    'fontsize': fontsize,
    'foreground': foreground,
}
##-> Commands to spawn
class Commands(object):
    dmenu = '/home/cba/.menu/menu main'
    startup = '/home/cba/.config/qtile/startup-script'
    #dmenu = 'dmenu_run -i -b -p ">>>" -fn "%s" -nb "#000" -nf "#fff" -sb "#00BF32" -sf "#fff"' % (font)
    dmenu_desktop = 'i3-dmenu-desktop'
    screenshot = 'scrot_s'
    volume_up = 'amixer -q -c 0 sset Master 5dB+'
    volume_down = 'amixer -q -c 0 sset Master 5dB-'
    volume_toggle = 'amixer -q set Master toggle'
    dmenu_session = 'dmenu-session'
    dmenu_mocp = 'dmenu-mocp'
    dmenu_windows = '/home/cba/.config/qtile/dmenu-qtile-windowlist.py' # in examples/zordsdavin/bin
    terminal = 'evilvte'
    trackpad_toggle = "synclient TouchpadOff=$(synclient -l | grep -c 'TouchpadOff.*=.*0')"
    #terminal = 'urxvt -e bash -c "tmux -q has-session && exec tmux attach-session -d || exec tmux new-session -n$USER -s$USER@$HOSTNAME"'

keys = [
        # applications
        Key([mod],          "Return",   lazy.spawn(Commands.terminal)),
        Key([mod],          "d",        lazy.spawn(Commands.dmenu)),
        Key([mod, shift],   "d",        lazy.spawn(Commands.dmenu_desktop)),
        Key([mod],          "w",        lazy.spawn(Commands.dmenu_windows)),
        Key([mod],          "z",        lazy.spawn(Commands.dmenu_windows)),
        Key([mod],          "x",        lazy.window.kill()),
        Key([mod],          "c",        lazy.spawn('xclip -o -selection primary | xclip -selection clipboard')),
        Key([mod],          "v",        lazy.spawn('xclip -o -selection clipboard | xclip -selection primary')),
        Key([mod],          "F2",       lazy.spawncmd(prompt=':')), # this is for programs, but can prompt for windows, groups, etc.

        #layouts ################################################################
        Key([mod],          "s",        lazy.group.setlayout('stack')),
        Key([mod],          "e",        lazy.group.setlayout('xmonad-tall')),
        Key([mod, shift],   "a",        lazy.group.setlayout('max')),
        # Toggle between different layouts
        Key([mod],          "Tab",  lazy.nextlayout()),
            # Split = all windows displayed
            # Unsplit = 1 window displayed, like Max layout, but still with multiple stack panes
        Key([mod, shift],   "slash",lazy.layout.toggle_split()),

        # groups
        Key([mod],          "Left", lazy.screen.prev_group()),
        #Key([mod],          "Next", lazy.screen.prev_group()),
        Key([mod],          "Right",lazy.screen.next_group()),
        #Key([mod],          "Prior",lazy.screen.next_group()),
        Key([mod],          "b",    lazy.screen.togglegroup()),

        # windows
        Key([mod],          "space",lazy.layout.next()),
        Key([alt],          "Tab",  lazy.group.next_window()),
        Key([mod, shift],   "space",lazy.layout.previous()),
        Key([alt, shift],   "Tab",  lazy.group.prev_window()),
        Key([mod],          "f",    lazy.window.toggle_fullscreen()),
        Key([mod],          "t",    lazy.window.toggle_floating()),
        Key([mod, shift],   "f",    lazy.window.enable_floating()), # if window wants to float, let it
        # this is usefull when floating windows get buried
        Key( [alt],         "grave",lazy.window.bring_to_front()),
        # for tiled layouts:
            # Switch window focus to other pane(s) of stack
            # Swap panes of split stack
        Key([mod],          "slash",lazy.layout.flip()), # xmonadtall: toggle side of main pane
        Key([mod],          "r",    lazy.layout.rotate()), # put last window first in stack

        # stacked layouts:
            # Switch between windows in current stack pane
        Key( [mod],         "j",    lazy.layout.down()),
        Key( [mod],         "k",    lazy.layout.up()),
        Key([mod],          "h",    lazy.layout.left()),
        Key([mod],          "l",    lazy.layout.right()),
            # Move windows up or down in current stack
        Key([mod, shift],   "j",    lazy.layout.shuffle_down()),
        Key([mod, shift],   "k",    lazy.layout.shuffle_up()),
        Key([mod],          "Prior",lazy.layout.swap_left()),
        Key([mod],          "Next", lazy.layout.swap_right()),
        Key([mod],          "Home", lazy.layout.swap_main()),

        # changing stacked or tiled window sizes
        Key([mod],          "u",    lazy.layout.grow()), # for pane with focus
        Key([mod],          "comma",lazy.layout.shrink()), # for pane with focus
        Key([mod],          "n",    lazy.layout.normalize()), #xmonadtall, verticaltile: restore all client windows to their default size ratios
        Key([mod],          "o",    lazy.layout.maximize()), # for pane with focus
        # dec ratio of current window: tree, ratiotile, tile
        Key([alt],          "equal",lazy.layout.decrease_ratio()),
        # inc ratio of current window: tree, ratiotile, tile
        Key([alt],          "plus",    lazy.layout.increase_ratio()),

        # qtile
        Key([mod, ctrl],    "q",        lazy.shutdown()),
        Key([mod, ctrl],    "r",        lazy.restart()),

        # Multiple function keys
        # Also allow changing volume the old fashioned way.
        Key([], "XF86AudioRaiseVolume",     lazy.spawn(Commands.volume_up)),
        Key([], "XF86AudioLowerVolume",     lazy.spawn(Commands.volume_down)),
        Key([], "XF86AudioMute",            lazy.spawn(Commands.volume_toggle)), #need toggle function here
        #Key([], "XF86AudioPlay", lazy.spawn("ncmpcpp play")),
        #Key([], "XF86AudioStop", lazy.spawn("ncmpcpp pause")),
        #Key([], "XF86AudioPrev", lazy.spawn("ncmpcpp prev")),
        #Key([], "XF86AudioNext", lazy.spawn("ncmpcpp next")),
        #Key([], "XF86AudioMicMute", lazy.spawn("")), #
        #Key([], "KP_0", lazy.spawn("")),
        #Key([], "KP_0", lazy.spawn("")),
        #Key([], "comma", lazy.spawn("")),
        #Key([], "period", lazy.spawn("")),
        #Key([], "", lazy.spawn("")),
        #Key([], "", lazy.spawn("")),
        #Key([], "XF86ScreenSaver", lazy.spawn("")), # F2
        #Key([], "XF86Battery", lazy.spawn("")), # F3
        #Key([], "XF86Sleep", lazy.spawn("")), #F4
        #Key([], "XF86WLAN", lazy.spawn("")), # F5
        #Key([], "XF86WebCam", lazy.spawn("")), #F6
        #Key([], "XF86Display", lazy.spawn("")), # F7
        #Key([], 'XF86TouchpadToggle', lazy.spawn(Commands.trackpad_toggle)), #F8 but not working
        #Key([], "Print", lazy.spawn("")), # PrtScr
        #Key([], "Sys_Req", lazy.spawn("")), # Fn-PrtScr
        #Key([], "Scroll_Lock", lazy.spawn("")), # ScrLk
        #Key([], "Pause", lazy.spawn("")), # Pause
        #Key([], "Break", lazy.spawn("")), # Fn-Pause
        #Key([], "XF86Suspend", lazy.spawn("")), # F12
        #Key([], "XF86MonBrightnessDown", lazy.spawn("")), # End
        #Key([], "XF86MonBrightnessUp", lazy.spawn("")), # Home
        #Key([], "XF86Launch1", lazy.spawn("")), # ThinkVantage

        # avail: a g i p r s y z
        ]
groups = [
        Group("1:terms"),
        Group('2:files'),
        Group("3:web"),
        Group("4:system"),
        Group("5:pkm"),
        Group("6:misc"),
        Group('7:root'),
        ]
for i in groups:
    keys.append(
            Key([mod], i.name[0], lazy.group[i.name].toscreen())
            )
    keys.append(
            Key([mod, shift], i.name[0], lazy.window.togroup(i.name))
            )

border = dict(
        border_normal='#808080',
        border_focus='#ff0000',
        border_width=2,
        )

my_float_rules = [dict(type='popup'),]
layouts = [
        layout.Max(), #first is default
        layout.Floating(float_rules=my_float_rules, **border), # auto_float_types=set(['dialog', 'notification', 'splash', 'toolbar', 'utility'])
        #layout.Matrix(),
        layout.Tile(**border),
        layout.Stack(**border),
        layout.MonadTall(name="Tall", **border),
        #layout.TreeTab(),
        #layout.Zoomy(),
        #layout.RatioTile(),
        #layout.Slice('left', 320, wmclass='pino',
            #fallback=layout.Slice('right', 320, role='roster',
                #fallback=layout.Stack(1, **border))),
            #layout.Slice('left', 192, role='gimp-toolbox',
                #fallback=layout.Slice('right', 256, role='gimp-dock',
                    #fallback=layout.Stack(1, **border))),
]

##-> Theme + widget options
class Theme(object):
    bar = {
        'size': 24,
        'background': '15181a',
        }
    widget = {
        'font': 'Andika-R',
        'fontsize': 11,
        'background': bar['background'],
        'foreground': '00ff00',
        }
    graph = {
        'background': '000000',
        'border_width': 0,
        'border_color': '000000',
        'line_width': 1,
        'margin_x': 0,
        'margin_y': 0,
        'width': 50,
        }
    groupbox = widget.copy()
    groupbox.update({
        'padding': 2,
        'borderwidth': 3,
        })
    sep = {
        'background': bar['background'],
        'foreground': '444444',
        'height_percent': 75,
        }
    systray = widget.copy()
    systray.update({
        'icon_size': 16,
        'padding': 3,
        })
    pacman = widget.copy()
    pacman.update({
        'foreground': 'ff0000',
        'unavailable': '00ff00',
        })
    battery = widget.copy()
    battery_text = battery.copy()
    battery_text.update({
        'low_foreground': 'FF0000',
        'charge_char': "↑ ",
        'discharge_char': "↓ ",
        'format': '{char}{hour:d}:{min:02d}',
        })

# orange text on grey background
default_data = dict(fontsize=14,
                    foreground="FF6600",
                    background="1D1D1D",
                    font="Droid Sans")

screens = [
        Screen(
            top = bar.Bar(
                [
                    widget.GroupBox(font='Andika-R', fontsize=14, margin_x=0, margin_y=0, padding=2, borderwidth=3, active="00ff00", inactive="b0b0b0"),
                    widget.Sep(linewidth=2),
                    #widget.GroupBox(**Theme.groupbox),
                    #widget.GroupBox(),
                    #widget.GroupBox(**default_data),
                    #widget.CurrentLayout(),
                    #widget.CurrentLayout(font='Liberation Sans Narrow', fontsize=16, foreground="FF6600"),
                    widget.CurrentLayout(font='Andika-R', fontsize=14, foreground="66FFFF"),
                    widget.Sep(linewidth=2),
                    widget.Prompt(),
                    #widget.WindowName(), #need width else default is STRETCH, and only one stretch widget allowed per bar
                    widget.WindowName(font='Andika-R', fontsize=16), #need width else default is STRETCH, and only one stretch widget allowed per bar
                    #widget.WindowName(font='Liberation Sans Narrow', fontsize=14), #need width else default is STRETCH, and only one stretch widget allowed per bar
                    #widget.TaskList(),
                    #widget.TaskList(**default_data),
                    #widget.WindowTabs(font='Liberation Sans Narrow', fontsize=16, foreground='FFFF00', selected=("=","=")), #one of these is redundant
                    #widget.CPUGraph(samples=20),
                    #widget.NetGraph(samples=20),
                    #widget.HDDGraph(samples=20),
                    widget.Sep(linewidth=2),
                    widget.Battery(fontsize=14),
                    widget.Sep(linewidth=2),
                    #widget.BatteryIcon(),
                    widget.Volume(fontsize=14),
                    #widget.Notify(),
                    #widget.Notify(**default_data),
                    widget.Systray(),
                    #widget.Clock(),
                    widget.Clock('%l:%M:%S %e.%b.%Y', font='Inconsolata', fontsize=14, padding=3),
                    ],
                30,
                #**default_data
                ),
            ),
        ]

@hook.subscribe.client_new
def floating_dialogs(window): # other types are handled by defaults or init for Floating layout
    #popup = window.window.get_wm_type() == 'popup'
    transient = window.window.get_wm_transient_for()
    if transient:
        window.floating = True

mouse = [
        Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
        Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
        Click([mod], "Button2", lazy.window.bring_to_front())
        ]

#@hook.subscribe.client_new
#def libreoffice_dialogues(window):
    #if((window.window.get_wm_class() == ('VCLSalFrame', 'libreoffice-calc')) or
            #(window.window.get_wm_class() == ('VCLSalFrame', 'LibreOffice 3.4'))):
        #window.floating = True

# start the applications at Qtile startup
@hook.subscribe.startup_once
def startup():
    Popen(Commands.startup)
    #rc_dir = "/home/arkchar/.config/wmStartupScripts/"
    #subprocess.Popen("sleep 3".split())
    #execute_once("nm-applet")
    #execute_once("kupfer --no-splash")
    #execute_once("xcompmgr")
    #execute_once(rc_dir + "xmodmap.py")
    #execute_once("ibus-daemon --xim")
    #execute_once("hsetroot -tile /home/arkchar/Pictures/desktop.jpg")
    #execute_once(rc_dir + "trackpoint.sh")
    #execute_once("xsetroot -cursor_name left_ptr")
    # execute_once("xset m 4 0")

# look for new monitor
"""@hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
    call("setup_screens")
    qtile.cmd_restart()
"""
# keep track when we change groups - WIP
#prevScreen = None
#currentScreen = None
"""@hook.subscribe.setgroup
def changed_group(qtile, ev):
    prevScreen = currentScreen
    currentScreen = qtile.currentGroup.name
"""

main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False #True
floating_layout = layout.Floating(**border)
auto_fullscreen = True
#widget_defaults = {}
wmname = "LG3D"

"""def window_sorter(win):
patterns = (
('Google Chrome', 'web'),
('xfe', 'files'),
('evilvte', 'terms'),
('synaptic', 'system'),
)
for k, v in patterns:
if k in win.name:
return v
return 'misc'

# Utils
# ------

def to_urgent(qtile):
    cg = qtile.currentGroup
    for group in qtile.groupMap.values():
        if group == cg:
            continue
        if len([w for w in group.windows if w.urgent]) > 0:
            qtile.currentScreen.setGroup(group)
            return


def switch_to(name):
    def callback(qtile):
        for window in qtile.windowMap.values():
            if window.group and window.match(wname=name):
                qtile.currentScreen.setGroup(window.group)
                window.group.focus(window, False)
                break
    return callback


class SwapGroup(object): #cba - this seems to work like i3 scratch container, but at the group level
    def __init__(self, group):
        self.group = group
        self.last_group = None

    def group_by_name(self, groups, name):
        for group in groups:
            if group.name == name:
                return group

    def __call__(self, qtile):
        group = self.group_by_name(qtile.groups, self.group)
        cg = qtile.currentGroup
        if cg != group:
            qtile.currentScreen.setGroup(group)
            self.last_group = cg
        elif self.last_group:
            qtile.currentScreen.setGroup(self.last_group)

    # fast switches
    Key([mod], "t", lazy.function(switch_to("Gajim"))),

    Key([], "F12", lazy.function(SwapGroup('h4x'))),
    Key(['shift'], "F12", lazy.function(to_urgent)),

    # Control the notify widget
    Key(
    [mod], "n",
    lazy.widget['notify'].toggle()
    ),
    Key(
    [mod, alt], "n",
    lazy.widget['notify'].prev()
    ),
    Key(
    [mod, alt], "m",
    lazy.widget['notify'].next()
    ),

"""
