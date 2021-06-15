
#paramiko is imported for use of SSH
import paramiko
#csv is imported to write to csv files
import csv
import xlwt
from xlwt import Workbook
#from openpyxl import Workbook
import pandas

import xlsxwriter

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

    print("You can choose to run apt list --installed, apt-mark showmanual or both and save them as excel sheets")
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


    port = helpers.getValidNumber(constants.MIN_PORT, constants.MAX_PORT)
    if port == "":
        port = constants.SSH_DEFAULT_PORT

    username = input("Enter the username you wish to SSH in to:")
    password = getpass.getpass(prompt="Please enter a password:")

    print("Enter 1 for apt-list, enter 2 for apt-mark, enter 3 for both")
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
                data2["Package Name:"].append(i)
                apt_list_PackageName_stripped.append(i)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("apt list --installed | awk -F/ '{print $2}'")
        apt_list_Version = []
        apt_list_Version = ssh_stdout.readlines()

        for j in apt_list_Version:
            j = j.strip('\n')
            data2["Version:"].append(j)

        df = pandas.DataFrame.from_dict(data2, orient= 'index')
        df = df.transpose()

        writer = pandas.ExcelWriter('AptList.xlsx', engine = 'xlsxwriter')
        df.to_excel(writer, sheet_name = "Sheet", index = False)

        # for column in df:
        #     column_width = max(df[column].astype(str).map(len).max(), len(column))
        #     col_idx = df.columns.get_loc(column)
        #     writer.sheets['Sheet'].set_column(col_idx, col_idx, column_width)

        workbook = writer.book

        worksheet = writer.sheets['Sheet']

        # format = workbook.add_format({'text_wrap': True})

        worksheet.set_column('A:B', 60)

        writer.save()


        # wb = Workbook()
        #
        # ws = wb.active
        #
        # ws_aptlist = wb.create_sheet("aptlist")
        #
        # for i in apt_list_PackageName_stripped:
        #     ws_aptlist.append(i)
        #
        # ws.title = "Apt List Results"
        #
        # wb.save("aptlist.xlsx")

        # writer = csv.writer(apt_list, data2.keys())
        # writer.writerows(zip(["Package Name:"], ["Version:"]))
        # writer.writerows(zip(apt_list_PackageName_stripped, apt_list_Version))


        #writer.writerows(zip(data2["Package Name":].values(), data2["Version:":].values()))


if __name__ == "__main__":
    main()