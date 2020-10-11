import PySimpleGUI as sg
import password_manager as pm
from functools import reduce

if __name__ == "__main__":
    # MASTER-KEY INPUT
    event, values = sg.Window('Passwordz',
                              [[sg.T('Enter your Master Key'), sg.In(size=(10,1),key='-MASTER-', password_char='*')],
                               [sg.B('Enter', bind_return_key=True)]]).read(close=True)

    master_key = values['-MASTER-']
    if master_key is None:
        print("closing..")
        exit()

    # Load Config from Disc
    config = pm.loadConfig()

    # Create Default Config
    if config is None:
        print("No Config Found! Creating default config..")
        config = pm.createConfig()  # create default config
        pm.addPasswordID(config, 'steam')
        pm.addPasswordID(config, 'twitter')
        pm.addPasswordID(config, 'reddit')
        pm.addPasswordID(config, 'twitch')
        pm.saveConfig(config)

    # Extract Data from Config
    print("loading Config...")
    password_ids = config.get('pw_ids')
    password_length = config.get('pw_length')
    password_char_map = config.get('char_map')
    print(password_ids, password_length, password_char_map)
    max_length = reduce(lambda x, y: max(x, y), map(lambda x: len(x), password_ids))
    print("max_length is", max_length)

    # Set Window Layout
    id_col = [[sg.Text(text=pwid)] for pwid in password_ids]
    pw_col = [[sg.Text(key=pwid, size=(password_length, 1))] for pwid in password_ids]
    button_col = [[sg.Button("C", key=pwid + "0")] for pwid in password_ids]
    layout = [[sg.Column(id_col, element_justification='l'), sg.VerticalSeparator(),
               sg.Column(pw_col, element_justification='l'), sg.VerticalSeparator(), sg.Column(button_col)],
              [sg.Button("asd")]]
    window = sg.Window('Passwordz', layout, finalize=True)

    # Generate Passwords
    for pwid in password_ids:
        pw_tmp = pm.generatePassword(master_key, pwid, password_length)
        window[pwid].update(pw_tmp)

    # Main Loop
    while True:  # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event[:-1] in password_ids:
            pw = pm.generatePassword(master_key, event[:-1], password_length)
            print(pw)
            pm.saveToClipboard(pw)

    window.close()
