import os
from subprocess import Popen, PIPE


def getFiles(path):
    onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return onlyfiles

def extractAPK(apk_name, output, input):

    output_path = os.path.join(output, apk_name)
    input_path = os.path.join(input, apk_name)

    print(f"Extracting '{input_path}' to '{input_path}' ...")
    if not os.path.exists(output_path):
        process = Popen(['./apktool.jar', 'd', input_path, '-o', output_path], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        print(stdout.decode())
        print(f"DONE !")
    else:
        print(f"PREVIOUSLY DONE!")


def main():
    apk_list = getFiles("APKs")

    if not os.path.exists('output'):
        os.makedirs('output')

    for apk in apk_list:
        extractAPK(apk, 'output', 'APKs')



if __name__ == "__main__":
    main()