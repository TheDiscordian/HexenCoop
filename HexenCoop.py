# This script currently only supports Windows and has only been tested with the original Hexen.
import os, socket

GZDOOM_PATH = ""

CLASSES = [
    {
        'name': 'Fighter',
        'difficulties': ['Squire', 'Knight', 'Warrior', 'Berserker', 'Titan'],
        'stats': {
            'speed': 20,
            'armor': 20,
            'magic': 2,
            'strength': 20
        }
    },
    {
        'name': 'Cleric',
        'difficulties': ['Altar Boy', 'Acolyte', 'Priest', 'Cardinal', 'Pope'],
        'stats': {
            'speed': 13,
            'armor': 16,
            'magic': 12,
            'strength': 11
        }

    },
    {
        'name': 'Mage',
        'difficulties': ['Apprentice', 'Enchanter', 'Sorcerer', 'Wizard', 'Archmage'],
        'stats': {
            'speed': 7,
            'armor': 3,
            'magic': 20,
            'strength': 7
        }
    },
    {
        'name': 'Random',
        'difficulties': ['Very Easy', 'Easy', 'Normal', 'Hard', 'Very Hard']
    }
]

# If GZDOOM_PATH is not set, assume it's in the same directory as the script
if not GZDOOM_PATH:
    GZDOOM_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gzdoom.exe')

# Get the user's home directory
user_profile = os.environ.get('USERPROFILE')

# Construct the path dynamically
gzdoom_save_path = os.path.join(user_profile, 'Saved Games', 'GZDoom', 'hexen.hexen')

# Get all files in path
save_files = []
try:
    save_files = os.listdir(gzdoom_save_path)
except:
    None

def get_name(file):
    with open(file, 'rb') as f:
        data = f.read()
        KEY = b'tEXtTitle'
        OFFSET = len(KEY)+1
        index = data.find(KEY)
        length = data[index-1]-6
        return data[index+OFFSET:index+OFFSET+length].decode('utf-8')

# Simple, lightweight function to get the local IP address
def get_local_ip():
    try:
        # Create a socket for UDP communication
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Bind to a non-routable IP address and a random port
            # This ensures we get the local IP address of an active interface
            s.connect(("10.255.255.255", 1))  # Dummy address in a non-routable range
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception as e:
        return f"Error retrieving local IP: {e}"

# Make a bar of 10 characters long, ▮ == 2, - == 1 (remaining characters are spaces)
def format_bar(length):
    out = "▮" * (length // 2) + "-" * (length % 2)
    return out + " " * (10 - len(out))

print("Welcome to Discordian's simple Hexen Co-op script!")

hosting = input("Are you hosting today? (y/N) ").lower() == 'y'
players = 1
ip = ""

# Output local IP address
if hosting:
    print("Your local IP address is: ", get_local_ip())
else:
    ip = input("Please enter the host's IP address: ")
    if not ip:
        input("No IP address entered. Exiting...")
        exit()

print()

if hosting:
    players = int(input("How many players will be playing (including you)? "))

new_game = True
if len(save_files) > 0:
    new_game = input("Would you like to start a new game? (y/N) ").lower() == 'y'

if new_game:
    print()
    # Pick class
    print("Available classes:")
    for i in range(len(CLASSES)-1):
        print("""\t%d. %s\n\t\tSpeed:    [%s]\n\t\tArmor:    [%s]\n\t\tMagic:    [%s]\n\t\tStrength: [%s]""" % (i, CLASSES[i]['name'], format_bar(CLASSES[i]['stats']['speed']), format_bar(CLASSES[i]['stats']['armor']), format_bar(CLASSES[i]['stats']['magic']), format_bar(CLASSES[i]['stats']['strength'])))
    print("\t%d. %s" % (len(CLASSES)-1, CLASSES[len(CLASSES)-1]['name']))
    class_index = int(input("Please enter the number of the class you'd like to play: "))
    if class_index < 0 or class_index >= len(CLASSES):
        input("Invalid class selection. Exiting...")
        exit()

    difficulty = 2
    if hosting:
        print()
        print("Available difficulties:")
        for i in range(len(CLASSES[class_index]['difficulties'])):
            print(f"\t{i}. {CLASSES[class_index]['difficulties'][i]}")
        difficulty_str = input("Please enter the number of the difficulty you'd like to play [%d]: " % difficulty)
        if difficulty_str != "":
            try:
                difficulty = int(difficulty_str)
            except:
                difficulty = -1
        if difficulty < 0 or difficulty >= len(CLASSES[class_index]['difficulties']):
            input("Invalid difficulty selection. Exiting...")
            exit()

    print("Starting a new game...")
    # Launch GZDoom with the appropriate parameters
    if hosting:
        os.system(f'"{GZDOOM_PATH}" -host {players} -iwad hexen.wad +playerclass {CLASSES[class_index]['name']} +skill {difficulty} +map MAP01')
    else:
        os.system(f'"{GZDOOM_PATH}" -join {ip} -iwad hexen.wad +playerclass {CLASSES[class_index]['name']}')
    exit()

print("Available save files:")
for i in range(len(save_files)):
    print("\t%d. %s" % (i, get_name(os.path.join(gzdoom_save_path, save_files[i]))))
print()
file_index = int(input("Please enter the number of the save file you'd like to load: "))
if file_index < 0 or file_index >= len(save_files):
    input("Invalid file index. Exiting...")
    exit()

print("Loading save file '%s'..." % get_name(os.path.join(gzdoom_save_path, save_files[file_index])))
if hosting:
    os.system(f'"{GZDOOM_PATH}" -host {players} -loadgame {save_files[file_index].split(".")[0]} -iwad hexen.wad')
else:
    os.system(f'"{GZDOOM_PATH}" -join {ip} -loadgame {save_files[file_index].split(".")[0]} -iwad hexen.wad')