import os, sys

def main():

    file_path = f"C:\\Users\\realr\\Desktop\\profiles.ini"
    # file_path = f"{os.getenv('APPDATA')}\\Mozilla\\Firefox\\profiles.ini"

    args = sys.argv
    if (len(args) != 2):
        handle_error("""
              Incorrect number of arguments: Supply only the case-sensitive
              name of the profile you wish to make the default.
        """)


    with open(file_path, 'r') as f:
        file_content = [
            line.strip() 
            for line 
            in f.readlines()
        ]

    profile_mapping = get_profiles(file_content)

    desired_profile = args[1]

    if desired_profile not in profile_mapping:
        handle_error(f"""
            Given profile: {desired_profile}, is not among the
            available profiles.
        """)

    line_to_edit = profile_mapping['current-default']

    print(file_content)

    file_content[line_to_edit] = f'Default={profile_mapping[desired_profile]}'

    print(file_content)

    with open(file_path, 'w') as f:
        f.writelines([line + '\n' for line in file_content])




def get_profiles(file_content: list[str]) -> dict[str, str | int]:

    profile_mapping = {}

    for line_num, line in enumerate(file_content):
        if line == '':
            continue

        # get the current default profile line number
        # from the next line 
        if line.startswith('[Install'):
            profile_mapping['current-default'] = line_num+1
            continue

        if not line.startswith('[Profile'):
            continue

        profile_name = file_content[line_num+1].split('=')[1]
        profile_path = file_content[line_num+3].split('=')[1]

        profile_mapping[profile_name] = profile_path

    return profile_mapping


        

def handle_error(message: str) -> None:
    print(message)
    exit(1)


if __name__ == "__main__":
    main()