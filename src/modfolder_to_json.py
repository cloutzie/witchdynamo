from pathlib import Path
import zipfile
import toml
import argparse
import json


def create_unique_file(name: str) -> None:
    """Create a file given a name, and add a number if exists.
    
    """ 

    file = Path(name)
    stem: str = file.stem
    extension: str = file.suffix

    counter: int = 1
    while file.exists():
        file = Path(stem+str(counter)+extension)
        counter += 1

    file.touch()

    return file

def get_mod_display_name(jar_path):
    with zipfile.ZipFile(jar_path, 'r') as jar:
        try:
            with jar.open('META-INF/neoforge.mods.toml') as f:
                content = f.read().decode('utf-8')  # decode binary to string
                mods_toml = toml.loads(content)     # parse from string
                mods = mods_toml.get('mods', [])
                if mods:
                    return mods[0].get('displayName', 'Unknown Mod Name')
                else:
                    return 'No mods found in mods.toml'

        except KeyError:
            return 'mods.toml not found'
        except Exception as e:
            return f'Error reading mods.toml: {e}'

def get_modlist(folder: str) -> list[str]:
    """""" 

    mods = Path(folder)

    modlist = []
    for file in mods.iterdir():
        if file.is_file():
            modlist.append(get_mod_display_name(file))

    return modlist


parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, help='Absolute path of mods folder')

args = parser.parse_args()

modlist = get_modlist(args.path)

jsonschema = {
    "version": "1.21.1",
    "loader": "neoforge",
    "mods": modlist
}

file = create_unique_file("mods.json")
 
with open(file, "w") as f:
    json.dump(jsonschema, f, indent=4)

print(f"File {file} created.")