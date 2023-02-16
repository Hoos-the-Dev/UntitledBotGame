Snipe = {

}


Edit_Snipe = {

}

def add_snipe(user, message, channel):
    try:
        Snipe[channel] = {user: message}
    except Exception as e:
        print("no snipe")
        print(e)

def get_snipe(channel):
    return Snipe[channel]

def del_snipe(channel):
    try: del Snipe[channel]
    except KeyError: pass

def get_author(channel):
    return list(Snipe[channel].keys())[0]
def get_message(channel):
    return list(Snipe[channel].values())[0]

def edit_snipe_add(user, og_message, new_message, channel):
    try:
        Edit_Snipe[channel] = {user: {og_message: new_message}}
    except Exception as e:
        raise e

def get_og_message(channel):
    cont = list(Edit_Snipe[channel].values())[0].keys()
    return list(cont)[0]

def get_new_message(channel):
    cont = list(Edit_Snipe[channel].values())[0].values()
    return list(cont)[0]

def get_edit_author(channel):
    return list(Edit_Snipe[channel].keys())[0]

def del_edit_snipe(channel):
    del Edit_Snipe[channel]
        