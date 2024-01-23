import os, sys

def main():

    args = sys.argv
    if (len(args) != 2):
        print("""
              Incorrect number of arguments: Supply only the case-sensitive
              name of the profile you wish to make the default.
              """)
        exit(0)
        
    # with open(f"{os.getenv('APPDATA')}\\Mozilla\\Firefox\\profiles.ini", 'r+') as f:
    with open(f"C:\\Users\\realr\\Desktop\\profiles.ini", 'r+') as f:
        file_content = [
            line.strip() 
            for line 
            in f.readlines()
        ]

        profile_mapping = get_profiles(file_content)

        # handle command line args to switch to profile

        



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


        




if __name__ == "__main__":
    main()