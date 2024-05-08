import os, sys

def main() -> None:

    file_path = f"{os.getenv('APPDATA')}\\Mozilla\\Firefox\\profiles.ini"

    args = sys.argv
    if (len(args) != 2):
        handle_error("""
              Incorrect number of arguments: Supply only the case-sensitive
              name of the profile you wish to make the default.
        """)


    with open(file_path, 'r') as f:
        file_content = f.readlines()


    profile_mapping = get_profiles(file_content)

    desired_profile = args[1]
    if desired_profile not in profile_mapping:
        print("The given profiles are as follows:")
        for key in profile_mapping:
            if 'default' in key:
                continue
            print(f'> {key}')
            
        handle_error(f"""
            Given profile: {desired_profile}, is not among the
            available profiles.
        """)


    line_to_edit = profile_mapping['current-default']

    file_content[line_to_edit] = \
        f'Default={profile_mapping[desired_profile]}\n'


    with open(file_path, 'w') as f:
        f.writelines(file_content)



"""
Gets the profile paths for the available Firefox profiles,
and the line number where the default profile is listed.

Parameters
----------
file_content : list[str]
    list of lines that the given file contains

Returns
-------
dict[str, str | int]
    mapping of profile name to profile path, or to line number for
    where the default profile line is located
"""
def get_profiles(file_content: list[str]) -> dict[str, str | int]:

    profile_mapping = {}

    for line_num, line in enumerate(file_content):
        if line == '\n':
            continue

        # get the current default profile line number
        # from the next line 
        if line.startswith('[Install'):
            profile_mapping['current-default'] = line_num+1
            continue

        if not line.startswith('[Profile'):
            continue

        profile_name = file_content[line_num+1].split('=')[1].strip()
        profile_path = file_content[line_num+3].split('=')[1].strip()

        profile_mapping[profile_name] = profile_path

    return profile_mapping


        
"""
Handles errors in the running of the script, and then exits the script

Parameters
----------
message : str
    the error message to send before exiting the script
"""
def handle_error(message: str) -> None:
    print(message)
    exit(1)



if __name__ == "__main__":
    main()