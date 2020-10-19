import PySimpleGUI as sg
from passwordz.password_generation import password_generation as pm
from functools import reduce


def windowMasterInput():
    e, v = sg.Window('Passwordz',
                     [[sg.T('Enter your Master Key'), sg.In(size=(10, 1), key='-MASTER-', password_char='*')],
                      [sg.B('Enter', bind_return_key=True), sg.B('Config')]]).read(close=True)

    if v['-MASTER-'] is None:
        print("closing..")
        exit()

    if e is 'Config':
        cfg = windowConfig(default=False)
        pm.saveConfig(cfg)
        return windowMasterInput()
    else:
        return v['-MASTER-']


def windowConfig(default: bool):
    if default:
        cfg = pm.createConfig()  # use default config
    else:
        cfg = pm.loadConfig()  # show existing config

    e, v = sg.Window('Config',
                     [[sg.T('Password Length:'),
                       sg.Input(default_text=cfg.get('pw_length'), key='-PWLENGTH-', size=(5, 1))],
                      [sg.T('Char-Map:'), sg.Input(default_text=cfg.get('char_map'), key='-CHARMAP-')],
                      [sg.T('ID\'s:')], [sg.Multiline(size=(15, 5), key='-IDS-',
                                                      default_text='<enter id\'s here>') if default else sg.Multiline(
                         size=(15, 5), key='-IDS-', default_text=reduce(lambda x, y: x + '\n' + y, cfg.get('pw_ids')))],
                      [sg.Checkbox(text='Clear clipboard on exit?', key='-CLRONEXT-',
                                   default=cfg.get('clear_on_exit'))],
                      [sg.Text('Clear after Seconds:', size=(16, 1)), sg.Input(default_text=cfg.get('clear_after'),
                                                                               key='-CLRAFTER-', size=(2, 1)),
                       sg.Text(' (set to -1 to disable)')],
                      [sg.B('Confirm')]
                      ]).read(close=True)

    try:
        cfg = pm.createConfig(pw_length=int(v['-PWLENGTH-']), char_map=v['-CHARMAP-'],
                              clear_on_exit=bool(v['-CLRONEXT-']),
                              clear_after=int(v['-CLRAFTER-']))
    except TypeError:
        print('invalid input or window was closed without saving, exiting..')
        exit()

    for i in filter(lambda x: len(x) > 0, v['-IDS-'].split('\n')):
        pm.addPasswordID(cfg, i)
    return cfg


if __name__ == "__main__":

    # First Time -> Create Default Config
    if pm.loadConfig() is None:
        print("No Config Found! Creating default config..")
        config = windowConfig(default=True)
        pm.saveConfig(config)

    # MASTER-KEY INPUT
    master_key = windowMasterInput()

    # Load Config from Disc
    config = pm.loadConfig()

    # Extract Data from Config
    print("loading Config")
    password_ids = config.get('pw_ids')
    password_length = config.get('pw_length')
    password_char_map = config.get('char_map')
    max_length = reduce(lambda x, y: max(x, y), map(lambda x: len(x), password_ids))

    # Set Window Layout
    id_col = [[sg.Text(text=pwid)] for pwid in password_ids]
    pw_col = [[sg.Text(key=pwid, size=(password_length, 1))] for pwid in password_ids]
    button_col = [[sg.Button("C", key=pwid + "0")] for pwid in password_ids]
    layout = [[sg.Column(id_col, element_justification='l'), sg.VerticalSeparator(),
               sg.Column(pw_col, element_justification='l'), sg.VerticalSeparator(), sg.Column(button_col)]]
    window = sg.Window('Passwordz', layout, finalize=True)

    # Generate Passwords
    print('generating passwords')
    for pwid in password_ids:
        pw_tmp = pm.generatePassword(master_key, pwid, password_length, password_char_map)
        window[pwid].update(pw_tmp)

    # Main Loop
    while True:  # Event Loop
        event, values = window.read()
        #print("event:", event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            if config.get('clear_on_exit'):
                pm.clearClipboard(None)  # clear Clipboard on exit!
            break
        elif event[:-1] in password_ids:
            pw = pm.generatePassword(master_key, event[:-1], password_length, password_char_map)
            pm.saveToClipboard(pw, config.get('clear_after'))

    window.close()
