from src.artificial_bee_colony import ArtificialBeeColony
import os, shutil


def remove_files(folder: str) -> None:
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def main():
    shutil.rmtree("data/")
    os.mkdir("data/")
    abc = ArtificialBeeColony(max_cycles=100)
    abc.run()

if __name__ == "__main__":
    main()
