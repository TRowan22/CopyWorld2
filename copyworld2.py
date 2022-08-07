import json, utils, os
import argparse

# to do
# no arg run
# choose specific pack and name


def main():
    parser = argparse.ArgumentParser(description='Copy a Minecraft CurseForge Modded World '
                                                 'to and from a Google Drive backup')

    try:
        check_data_setup()
    except json.decoder.JSONDecodeError as e:
        print(f"json.decorder.JSONDecodeError: {e}")
        return

    parser.add_argument('-pack', '-pa', action="store_true", help="change the pack you want to use")
    parser.add_argument('-world', '-w',  action="store_true", help="change the world you want to use")
    parser.add_argument('-upload', '-u', action="store_true", help="upload file from local computer to drive")
    parser.add_argument('-download', '-d', action="store_true", help="download file from drive to local computer")
    parser.add_argument('-print', '-p', action="store_true", help="print the current world path")

    data = find_data()

    local = f"{data['installation']}/{data['pack']}/saves/{data['world']}"
    strife = f"{data['drive_location']}/{data['pack']}/{data['world']}"

    args = parser.parse_args()
    if args.upload:
        utils.copy_world(local, strife)
        print("World uploaded")
    elif args.download:
        if not os.path.exists(strife):
            print("Error: Cloud location does not exist yet. Please upload the world first.")
        else:
            utils.copy_world(strife, local)
            print("World downloaded")

    elif args.pack:
        change_p_w(data)

    elif args.world:
        change_p_w(data, False)

    elif args.print:
        print(local)


def change_p_w(data, choice=True):
    g = open("last_world.json", "w")
    try:
        if choice:
            data["pack"] = pack_or_world(data["installation"], "Enter which pack you want to play: ")
        data["world"] = pack_or_world(f"{data['installation']}/{data['pack']}/saves",
                                      "Enter which world you want to play: ")
    except FileNotFoundError:
        print("World not found")
        return
    finally:
        json.dump(data, g)
        g.close()


def find_data():
    h = open("last_world.json", "r")
    data = json.load(h)
    h.close()
    return data


def check_data_setup():
    # initializes data if first time setup, otherwise checks for any data tampering/missing data
    if not os.path.exists("last_world.json") or os.path.getsize("last_world.json") == 0:
        g = open("last_world.json", "w+")
        json.dump({"installation": "", "drive_location": "", "pack": "", "world": ""}, g)
        g.close()
        print("First time setup")

    f = open("last_world.json", "r")
    data = json.load(f)
    f.close()

    while any(x[1] == "" for x in data.items()):
        print(data.items())
        check_data(data, "last_world.json")


def check_data(data, file):
    # first time setup - user manually writes in path data
    g = open(file, "w")

    try:
        if data["installation"] == "":
            data["installation"] = get_installations("Enter the path of your Minecraft Curseforge installation here: ",
                                                     "/minecraft/Instances")
            print("Installation recognized.")

        if data["drive_location"] == "":
            data["drive_location"] = get_installations("Enter the letter of your Google Drive installation: ",
                                                       ":/My Drive")
            print("Drive recognized.")

        if data["pack"] == "":
            data["pack"] = pack_or_world(data["installation"], "Enter which pack you want to play: ")
            print("Pack recognized.")

        if data["world"] == "":
            data["world"] = pack_or_world(f"{data['installation']}/{data['pack']}/saves",
                                          "Enter which world you want to play: ")
            print("World recognized.")
    except FileNotFoundError as e:
        print(e)
    finally:
        json.dump(data, g)
        g.close()


def get_installations(input_message, addition):
    # sets up the path for Curseforge installation and drive installation
    # other two path setups are fundamentally different so they have different function
    install = input(input_message)
    install += addition
    if not os.path.exists(install):
        print("Error: Path not found.")
        raise FileNotFoundError
    return install


def pack_or_world(dir, input_message):
    # set up path for choosing the Pack and World that will be copied
    dirs = os.listdir(dir)
    choices = {i:x for i, x in enumerate(dirs, 1)}
    [print(f"{x[0]}) {x[1]}") for x in choices.items()]
    try:
        choice = int(input(input_message))
        if choice in choices:
            print(choices[choice])
            return choices[choice]
        else:
            print("Error: Pack or world not found")
            raise FileNotFoundError
    except ValueError as e:
        print(e)


if __name__ == '__main__':
    main()
