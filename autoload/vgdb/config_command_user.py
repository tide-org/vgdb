from config import Config

def check_split_command(command):
    split_command = command.split(' ')
    if len(split_command) > 1:
        return (split_command[0], split_command[1:])
    return (command, [])

def set_user_input_args(command_args):
    if len(command_args) > 0:
        Config().get()["variables"]["user_input_args"] = " ".join(command_args)
