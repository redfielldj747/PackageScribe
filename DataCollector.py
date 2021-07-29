#paramiko is imported for use of SSH
import paramiko

class DataCollector():

    def __init__(self, data,ssh):
        self.__data = data
        self.__ssh = ssh

    def getPackageNames(self):
        ssh_stdin, ssh_stdout, ssh_stderr = self.__ssh.exec_command("apt list --installed | awk -F/ '{print $1}'")
        self.__apt_list_PackageName_stripped = []
        apt_list_PackageName = ssh_stdout.readlines()
        for i in apt_list_PackageName:
            if i != "Listing...\n":
                i = i.strip('\n')
                self.__data["Package Name:"].append(i)
                self.__apt_list_PackageName_stripped.append(i)

    def getPackageVersions(self):
        ssh_stdin, ssh_stdout, ssh_stderr = self.__ssh.exec_command("apt list --installed | awk -F/ '{print $2}'")
        apt_list_VersionName = []
        apt_list_VersionName = ssh_stdout.readlines()
        for i in apt_list_VersionName:
            if i != "Listing...\n":
                i = i.strip('\n')
                self.__data["Package Name:"].append(i)
                apt_list_VersionName.append(i)

    def isManualInstall(self):
        ssh_stdin, ssh_stdout, ssh_stderr = self.__ssh.exec_command("apt-mark showmanual")
        apt_list_ManualInstall = []
        apt_list_ManualInstall = ssh_stdout.readlines()

        for i in self.__apt_list_PackageName_stripped:
            switch = True
            for j in apt_list_ManualInstall:
                j = j.strip()
                if i == j:
                    self.__data["Installation Method"].append("Yes")
                    switch = False
                    break
            if switch == True:
                self.__data["Installation Method"].append("No")

    def getData(self):
        return self.__data
