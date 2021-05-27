
#paramiko is imported for use of SSH
import paramiko
#csv is imported to write to csv files
import csv

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
    password = input("Enter the password:")

    print("Enter 1 for just apt-list, enter 2 for apt-mark, enter 3 for both")
    command_choice = helpers.getValidNumber(constants.MIN_FILES, constants.MAX_FILES)

    if command_choice == 1:
        commands = ["apt list --installed"]
        apt_list = open('aptlist.csv', 'w', newline='')
        files = [apt_list]

    if command_choice == 2:
        commands = ["apt-mark showmanual"]
        apt_mark = open('aptmark.csv', 'w', newline='')
        files = [apt_mark]

    if command_choice == 3:
        commands = ["apt list --installed", "apt-mark showmanual"]
        apt_list = open('aptlist.csv', 'w', newline='')
        apt_mark = open('aptmark.csv', 'w', newline='')
        files = [apt_list, apt_mark]

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


    for i in range(len(commands)):
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(commands[i])

        data = ssh_stdout.readlines()
        writer = csv.writer(files[i])
        for j in data:
            writer.writerow([j])

if __name__ == "__main__":
    main()