
#paramiko is imported for use of SSH
import paramiko
#csv is imported to write to csv files
import csv

#importing getpass to obfuscate passwords
import getpass

#helpers contains the integer validation function
import helpers

#constants contains well... constants
import constants

def main():
    #empty list to be filled later
    commands = []
    #empty list to be filled later
    files = []

    print("You can choose to run apt list --installed, apt-mark showmanual or both and save them to separate csv files")
    print("For more information on run apt list --installed and the information it provides enter 1 now. Press enter to skip.")
    choice = helpers.getValidNumber(constants.MIN_COMMAND,constants.MIN_COMMAND)

    if choice == 1:
        print("This command will generate a list of all packages installed on the server")
    print("For more information on apt-mark showmanual enter 2 now. Press enter to skip")
    choice = helpers.getValidNumber(constants.MAX_COMMAND, constants.MAX_COMMAND)

    if choice == 2:
        print("This command will generate a list of packages either manually installed by the user using apt-get or installed at \"install time\"")

    print("Enter the host IP e.g 10.0.0.1:")
    host = helpers.validIPAddress()
    port = input("Enter the SSH port you wish to use -- default is port 22, press enter for default:")

    if port == "":
        port = constants.SSH_DEFAULT_PORT

    username = input("Enter the username you wish to SSH in to:")
    password = getpass.getpass(prompt="Please enter a password:")

    print("Enter 1 for just apt-list, enter 2 for apt-mark, enter 3 for both")
    command_choice = helpers.getValidNumber(constants.MIN_FILES, constants.MAX_FILES)

    if command_choice == 1:
        commands = ["apt list --installed | awk -F/ '{print $1}", "apt list --installed | awk -F/ '{print $2}'"]
        apt_list = open('aptlist.csv', 'w', newline='')
        files = [apt_list]

    if command_choice == 2:
        commands = ["apt-mark showmanual"]
        apt_mark = open('aptmark.csv', 'w', newline='')
        files = [apt_mark]

    if command_choice == 3:
        commands = ["apt list --installed | awk -F/ '{print $1}", "apt list --installed | awk -F/ '{print $2}'" "apt-mark showmanual"]
        apt_list = open('aptlist.csv', 'w', newline='')
        apt_mark = open('aptmark.csv', 'w', newline='')
        files = [apt_list, apt_mark]

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    data2 = {"Package Name:":[], "Version:":[]}

    if command_choice == 1:
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("apt list --installed | awk -F/ '{print $1}'")
        apt_list_PackageName = []
        apt_list_PackageName_stripped = []
        apt_list_PackageName = ssh_stdout.readlines()
        for i in apt_list_PackageName:
            if i != "Listing...\n":
                i = i.strip('\n')
                apt_list_PackageName_stripped.append(i)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("apt list --installed | awk -F/ '{print $2}'")
        apt_list_Version = []
        apt_list_Version = ssh_stdout.readlines()

        for j in apt_list_Version:
            j = j.strip('\n')
            data2["Version:"].append(j)

        #writer = csv.DictWriter(apt_list, data2.keys())
        writer = csv.writer(apt_list, data2.keys())

        writer.writerows(zip(["Package Name:"], ["Version:"]))

        writer.writerows(zip(apt_list_PackageName_stripped, apt_list_Version))


        #writer.writerows(zip(data2["Package Name":].values(), data2["Version:":].values()))




    # for i in range(len(commands)):
    #     ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(commands[i])
    #
    #     data = ssh_stdout.readlines()
    #
    #     if commands[i] == "apt list --installed | awk -F/ '{print $1}":
    #         for i in data:
    #             data2["Package Name:"].append(i)
    #     if commands[i] == "apt list --installed | awk -F/ '{print $2}'":
    #         for k in data:
    #             if k != '\n':
    #                 data2["Version:"].append(k)
    #     fieldnames = data2.keys()
    #
    #     if command_choice == 1:
    #         writer = csv.DictWriter(apt_list, fieldnames=fieldnames)
    #
    #     writer.writeheader()
    #
    #     for key,value in data2.items():
    #         writer.writerow([key, value])
    #     #     writer.writerow(data2["Package Name:"][l])
    #
    #     #writer.writerow(data2)
    #     # for j in data:
    #     #     writer.writerow([j])

if __name__ == "__main__":
    main()