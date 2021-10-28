import os
import xmltodict
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

def recoverPermissions(manifest_path):
    pemissions = []
    
    with open(manifest_path) as fd:
        manifest_dict = xmltodict.parse(fd.read(), process_namespaces=True)
    
    for permisssion in manifest_dict["manifest"]['uses-permission']:
        permission_str = permisssion['@http://schemas.android.com/apk/res/android:name']

        pemissions.append(str.split(permission_str, '.')[-1])
    return pemissions

def main():
    # Recovering list of APKs.
    apk_list = getFiles("APKs")

    # Defing output folder.
    if not os.path.exists('output'):
        os.makedirs('output')

    # Extracting all APKS to 'output/apk' folder.
    for apk in apk_list:
        extractAPK(apk, 'output', 'APKs')

    apk_dict = {"APKS" : []}

    # For each apk, define an entry in 'apk_dict' storing 'apk name' and it's 'permissions'.
    for apk in apk_list:
        apk_entry = {'name': apk, 'permissions': []}
        apk_entry['permissions'] = recoverPermissions(os.path.join('output', apk, 'AndroidManifest.xml'))
        apk_dict['APKS'].append(apk_entry)
        
    print(apk_dict)

if __name__ == "__main__":
    main()