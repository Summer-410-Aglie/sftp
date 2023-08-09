import pysftp
import os 
from simple_term_menu import TerminalMenu


LIST_DIR: str =         '[1] List remote directories'
CHANGE_DIR: str =       '[2] Change remote directories'
EXIT: str =             '[3] Exit'

OPTIONS: str = [
    LIST_DIR,
    CHANGE_DIR,
    EXIT
    ]

class SFTPClient:
    """ A wrapper class for SFTP Client
    """    
    def __init__(
            self,
            host_name: str,
            user_name: str,
            password: str,
    ) -> None:
        """Constructs the necessary data for the SFTP client object.

        :param host_name: host name or IP address
        :type host_name: str
        :param user_name: user name for the host id
        :type user_name: str
        :param password: password for the user name
        :type password: str
        """          

        self.host_name: str = host_name
        self.user_name: str = user_name
        self.password: str = password
        pass

    def connect(self) -> bool:
        """Establishes the SFTP connection

        :return: connection was successful or not
        :rtype: bool
        """
        try:      
            self.connection = pysftp.Connection(host=self.host_name, username=self.user_name, password=self.password)
        except Exception as e:
            return False
            pass
        
        return True

    def close(self) -> bool:
        """"Closes the established SFTP connection

        :return: disconnection was successful or not
        :rtype: bool
        """
        try:        
            self.connection.close()
        except Exception as e:
            return False
        
        return True
    
    def get_remote_file(self, src: str, dest: str = None) -> None:
        try:
            src = self.connection.normalize(src)
            if dest == ".":	dest = None
            self.connection.get(src, dest)
        except Exception as e:
            print(str(e))
        pass
    
    def get_many_remote_files(self, src: list[str], dest: str = None) -> None:
        pass

    def removeRemoteFile(self, fileName: str) -> bool: 
        """Remove the remote file

        :return: remove file from remote server
        :rtype: bool
        """
        try:
            self.connection.remove(fileName)
        except Exception as e:
            print(str(e))
            return ValueError('Unable to remove file: ' + fileName)

        return True

    def removeRemoteDirectory(self, dirName: str) -> bool: 
        """Remove the remote directory

        :return: remove directory from remote server
        :rtype: bool
        """
        try:
            self.connection.rmdir(dirName)
        except Exception as e:
            print(str(e))
            return ValueError('Unable to remove directory: ' + dirName)

        return True

    def renameRemote(self, src, dest):
        """Rename the file or directory on a remote host
        
        :return: rename file or directory from remote server
        :rtype: bool
        """
        try:
            self.connection.rename(src, dest)
        except Exception as e:
            print(str(e))
            return ValueError('Unable to rename file or directory: ' + src + ' to: ' + dest)
        
        return True
      
    def renameLocal(self, src, dest) -> bool:
        """Rename the file or directory on the local server

        :return: rename the file/directory or not
        :rtype: bool
        """
        try: 
            os.rename(src, dest)
        except FileNotFoundError as e:
            return FileNotFoundError(f"{src} does not exist")

        return True
    
    def getCurrentDir(self) -> None:    
        """Gets a list of contents in current directory

        :return: file names
        :rtype: list
        """          
        return self.connection.listdir()

        pass

    def listCurrentDir(self) -> None:
        """List all the current content of current directory
        """      
        for i in self.getCurrentDir():
            print(i)
        pass

    def changeCurrentDir(self) -> None:
        """Changes directory
        """   
        current_dir = self.getCurrentDir()
        current_dir.append("..")
        current_dir.append("Quit")
        current_path: str = self.connection.pwd
        choosen_index = self.ChooseMenu(options=current_dir, title_name="Current path: " + current_path)
        if choosen_index == len(current_dir) -1:
            return
        self.connection.chdir(current_dir[choosen_index])
        print(self.listCurrentDir())
        pass



    def ChooseMenu(self, options: list, title_name: str = "MENU") -> int:
        """Allows you to choose from list of options

        :param options: the data to display
        :type options: list
        :param title_name: the title you want to have for the menu, defaults to "MENU"
        :type title_name: str, optional
        :return: the choosen menu
        :rtype: int
        """        
        terminal_menu: TerminalMenu = TerminalMenu(
        menu_entries=options,
        title=title_name,
        )
        return terminal_menu.show()
        pass

    def mainMenu(self) -> None:
        """Menu for this class
        """        
        exit_flag: bool = False 

        while not exit_flag:
            index: int = self.ChooseMenu(OPTIONS, "User Name: "+ self.user_name+" Host: "+ str(self.host_name))

            if OPTIONS.index(LIST_DIR) == index:
                self.listCurrentDir()
                pass
            elif OPTIONS.index(CHANGE_DIR) == index:
                self.changeCurrentDir()
                pass
            elif OPTIONS.index(EXIT) == index:
                return
                pass

            pass       

        pass


    


    pass
