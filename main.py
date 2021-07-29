
#importing getpass to obfuscate passwords
import getpass

import paramiko


#helpers contains the integer validation function
import helpers

#constants contains well... constants
import constants

import ExcelWriter
import DataCollector

def main():

    #proceed will be filled once the user reads the instructions and enters a key, used to terminate loop below
    proceed = None

    while proceed is None:
        print("PackageScribe will SSH into an IPv4 enabled Ubuntu server and retrieve package information.")
        print("In particular, PackageScribe will record the version and whether or not the package was manually installed")
        print("Press any key to continue")
        proceed = input()
    #looking for a valid IPv4 address
    print("Enter the host IP e.g 10.0.0.1:")
    host = helpers.validIPAddress()

    print("Enter the SSH port you wish to use -- default is port 22, press enter for default:")
    port = helpers.getValidNumber(constants.MIN_PORT, constants.MAX_PORT)

    #hackey way of waiting for user to input enter, relies on validation above to avoid other characters aside from numbers
    if port == "":
        port = constants.SSH_DEFAULT_PORT

    username = input("Enter the username you want to SSH in to:")
    password = getpass.getpass(prompt="Please enter a password:")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    data = {"Package Name:":[], "Version:":[], "Installation Method":[]}


    #passes in dict called data to be filled
    collector = DataCollector.DataCollector(data, ssh)

    collector.getPackageNames()

    collector.getPackageVersions()

    collector.isManualInstall()

    data = collector.getData()

    # ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("apt list --installed | awk -F/ '{print $1}'")
    # apt_list_PackageName_stripped = []
    # apt_list_PackageName = ssh_stdout.readlines()
    # for i in apt_list_PackageName:
    #     if i != "Listing...\n":
    #         i = i.strip('\n')
    #         data["Package Name:"].append(i)
    #         apt_list_PackageName_stripped.append(i)
    #
    # #This grabs the second line of apt list --installed and appends it to a dictionary
    #
    # ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("apt-mark showmanual")
    # apt_list_ManualInstall = []
    # apt_list_ManualInstall = ssh_stdout.readlines()
    #
    # #complicated for loop that searches for correlation between list of all packages installed and those manually installed
    # for i in apt_list_PackageName_stripped:
    #     switch = True
    #     for j in apt_list_ManualInstall:
    #         j = j.strip()
    #         if i == j:
    #             data["Installation Method"].append("Yes")
    #             switch = False
    #             break
    #     if switch == True:
    #         data["Installation Method"].append("No")

    createExcel = ExcelWriter.ExcelWriter(data)

    writer = createExcel.writeSheet()

    createExcel.formatSheet(writer, 60)
    #
    # df = pandas.DataFrame.from_dict(data, orient= 'index')
    # df = df.transpose()
    #
    # writer = pandas.ExcelWriter('AptList.xlsx', engine = 'xlsxwriter')
    # df.to_excel(writer, sheet_name = "Sheet", index = False)

if __name__ == "__main__":
    main()