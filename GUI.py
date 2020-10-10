import PySimpleGUI as sg
import password_manager as pm
from functools import reduce

# MASTER-KEY INPUT
event, values = sg.Window('Passwordz - Login',
                          [[sg.T('Enter your Master Key'), sg.In(key='-MASTER-', password_char='*')],
                           [sg.B('Enter', bind_return_key=True)]]).read(close=True)

master_key = values['-MASTER-']
print("masterkey: ", master_key)  # TODO: delete me

# Load Config from Disc
config = pm.loadConfig()

# Create Default Config
if config is None:
    print("No Config Found! Creating default config..")
    config = pm.createConfig()  # create default config
    pm.addPasswordID(config, 'steam')
    pm.saveConfig(config)

# Extract Data from Config
print("loading Config...")
password_ids = config.get('pw_ids')
password_length = config.get('pw_length')
password_char_map = config.get('char_map')
print(password_ids, password_length, password_char_map)
max_length = reduce(lambda x, y: max(x, y), map(lambda x: len(x), password_ids))

# Set Window Layout
layout = [[sg.Text(size=(max_length, 1), text=pwid), sg.Text(size=(15, 1), key=pwid), sg.Button('C')] for pwid in password_ids]
window = sg.Window('Passwordz', layout, finalize=True, element_padding=(0, 0))

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

window.close()
