import PySimpleGUI as sg
import password_manager as pm
from functools import reduce

# MASTER-KEY INPUT
event, values = sg.Window('Passwordz - Login',
                          [[sg.T('Enter your Master Key'), sg.In(key='-MASTER-', password_char='*')],
                           [sg.B('Enter', bind_return_key=True)]]).read(close=True)

master_key = values['-MASTER-']

# TMP
print(master_key)
password_ids = ('steam', 'reddit', 'twitter', 'twitch')
max_length = reduce(lambda x, y: max(x, y), map(lambda x: len(x), password_ids))

# SHOW PASSWORDS
layout = [[sg.Text(size=(max_length, 1), text=pwid), sg.Text(size=(15, 1), key=pwid), sg.Button('B')] for pwid in password_ids]
window = sg.Window('Passwordz', layout, finalize=True, element_padding=(0, 0))


for pwid in password_ids:
    pw_tmp = pm.generatePassword(master_key, pwid)
    print(pwid, pw_tmp)
    window[pwid].update(pw_tmp)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Show':
        window['-OUTPUT-'].update(values['-IN-'])

window.close()
