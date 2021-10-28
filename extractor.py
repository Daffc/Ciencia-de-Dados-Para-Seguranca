import os
import xmltodict
from subprocess import Popen, PIPE


def getFiles(path):
    onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return onlyfiles

def extractAPK(apk_name, output, input):

    output_path = os.path.join(output, apk_name)
    input_path = os.path.join(input, apk_name)

    if not os.path.exists(output_path):
        process = Popen(['./apktool.jar', 'd', input_path, '-o', output_path], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        if stderr:
            print(stderr.decode())


def recoverPermissions(manifest_path):
    pemissions = []
    with open(manifest_path) as fd:
        manifest_dict = xmltodict.parse(fd.read(), process_namespaces=True)
    for permisssion in manifest_dict["manifest"]['uses-permission']:
        permission_str = permisssion['@http://schemas.android.com/apk/res/android:name']
        pemissions.append(str.split(permission_str, '.')[-1])
    
    return pemissions

def permissionsIntersection(apk_dict_list):
    permissions_intersection = apk_dict_list[0]['permissions']

    for apk in apk_dict_list[1:]:
        permissions_intersection = list(set(permissions_intersection) & set(apk['permissions']))

    return permissions_intersection

def main():
    # Recovering list of APKs.
    apk_list = getFiles("APKs")

    # Defing output folder.
    if not os.path.exists('output'):
        os.makedirs('output')

    # Extracting all APKS to 'output/apk' folder.
    for apk in apk_list:
        extractAPK(apk, 'output', 'APKs')

    apk_dict_list = []

    # For each apk, define an entry in 'apk_dict_list' storing 'apk name' and it's 'permissions'.
    for apk in apk_list:
        apk_entry = {'name': apk, 'permissions': []}
        apk_entry['permissions'] = recoverPermissions(os.path.join('output', apk, 'AndroidManifest.xml'))
        apk_dict_list.append(apk_entry)

    # Extracting Commum permissions among APKs
    perm_intersection = permissionsIntersection(apk_dict_list)

    # Outputing commum permissions
    print("COMMUM PERMISSIONS:")
    print("\t", perm_intersection)

    # Outputting distinctint permissions for each APK.
    print("SPECIFIC PERMISSIONS:")
    for apk in apk_dict_list:
        print("\t", apk['name'])
        per_specific = [p for p in apk['permissions'] if p not in perm_intersection]   
        print("\t\t", per_specific)
        
if __name__ == "__main__":
    main()