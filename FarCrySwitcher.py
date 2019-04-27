import os
import shutil
import datetime

PATH = r"E:\Ubisoft\Ubisoft Game Launcher\savegames"
DIR = "ba85dcb8-2355-46b0-a192-3fc2ca7a4b77"


class FarCrySwitcher:
    def __init__(self):
        self.saves = []

        self.current_save = None
        self.current_save_exists = False
        self.find_all_saves()
        self.read_current_save()

    def find_all_saves(self):
        # r=root, d=directories, f = files
        self.saves = []
        for save_dir in os.listdir(PATH):
            if not os.path.isdir(os.path.join(PATH, save_dir)):
                continue

            if DIR in save_dir:
                continue

            with open(os.path.join(PATH, save_dir, "save_name"), 'w') as file:
                file.write(save_dir)

            self.saves.append(save_dir)

    def get_saves(self):
        return self.saves

    def read_current_save(self):
        self.current_save_exists = False
        self.current_save = None
        save_dir = os.path.join(PATH, DIR)
        if not os.path.exists(save_dir):
            return
        if not os.path.isdir(save_dir):
            shutil.rmtree(save_dir)

        self.current_save_exists = True
        current_save_path = os.path.join(PATH, DIR, "save_name")
        # noinspection PyBroadException
        try:
            with open(current_save_path, 'r') as file:
                self.current_save = file.read()
        except:
            pass

    def get_current_save(self):
        return self.current_save

    def saveas(self, save_name):
        current_save_path = os.path.join(PATH, DIR, "save_name")
        with open(current_save_path, 'w') as file:
            file.write(save_name)
        self.current_save = save_name
        self.save()
        self.load(save_name)

    def switch_save(self, save_name):
        if save_name not in self.saves:
            raise Exception("Invalid Save")
        if self.current_save_exists:
            self.save()
        self.load(save_name)

    def save(self):
        if self.current_save is None:
            raise Exception("Current save needs to be saved first")

        current_save_path = os.path.join(PATH, self.current_save)
        if os.path.exists(current_save_path):
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

            backupfile = os.path.join(PATH, self.current_save + "_" + timestamp)
            shutil.make_archive(backupfile, 'zip', current_save_path)
            shutil.rmtree(current_save_path)

        shutil.copytree(os.path.join(PATH, DIR), current_save_path)
        self.find_all_saves()

    def load(self, save_name):
        if not os.path.exists(os.path.join(PATH, save_name)):
            raise Exception("Save directory does not exist")
        save_dir = os.path.join(PATH, DIR)
        if os.path.exists(save_dir):
            shutil.rmtree(save_dir)
        shutil.copytree(os.path.join(PATH, save_name), save_dir)
        self.read_current_save()


switcher = FarCrySwitcher()


def save():
    if switcher.get_current_save() is None:
        save_file = input("Input save name: ")
        switcher.saveas(save_file)
    else:
        try:
            switcher.save()
        except Exception as e:
            print(str(e))


def load():
    saves = switcher.get_saves()
    if len(saves) is 0:
        print("No saves to load")
        return

    i = 1
    for save_name in saves:
        print("%i) %s" % (i, save_name))
        i += 1
    print("%d) Exit" % i)
    while True:
        # noinspection PyBroadException
        try:
            index = int(input("Type the save number to load: "))
        except:
            print("Invalid Choice")
            continue

        if index == len(saves) + 1:
            return

        if index > len(saves) + 1 or index < 1:
            print("Invalid Choice")
            continue

        save_name = saves[index - 1]
        if save_name is None:
            print("Invalid Choice")
            continue
        try:
            switcher.switch_save(save_name)
            return
        except Exception as e:
            print(str(e))


def main():
    print("Welcome to the Far Cry New Dawn save manager")
    print("======================================================================================")
    print("DO NOT RUN WHILE FAR CRY OR UPLAY IS RUNNING, USE AT YOUR OWN RISK, BACK YOUR SHIT UP.")
    print("======================================================================================")
    while True:
        print("Current Save: %s" % switcher.get_current_save())
        print("Options:")
        print("1) Save game")
        print("2) Load game")
        print("3) Exit")
        # noinspection PyBroadException
        try:
            choice = int(input("> "))
            if choice == 1:
                save()
            elif choice == 2:
                load()
            elif choice == 3:
                print("Goodbye :D")
                return
        except:
            pass


if __name__ == "__main__":
    main()
