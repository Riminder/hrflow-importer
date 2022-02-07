import os
from datetime import datetime


class FileHandler:
    VALID_EXTENSIONS = ['.pdf', '.PNG', '.png', '.jpg', '.jpeg', '.bmp', '.doc', '.docx', '.rtf', '.dotx', '.odt', '.odp', '.ppt', '.pptx', '.rtf', '.msg']
    INVALID_FILENAME = ['.', '..']
    
    def __init__(self, root_directory, filename):
        assert os.path.isdir(root_directory)
        assert os.path.isfile(os.path.join(root_directory, filename))
        self.root_directory = root_directory
        self.filename = filename
        self.created_at = self.get_file_creation()
        self.file_reference = None


    def get_file_creation(self):
        timestamp = os.path.getmtime(os.path.join(self.root_directory, self.filename)) #TODO : check floating number
        return datetime.fromtimestamp(timestamp).isoformat() 
        

    def read_file(self):
        #filepath = PosixPath(config.STORAGE_DIRECTORY_PATH) / LOCAL_FILES_FOLDER / filename
        filepath = os.path.join(self.root_directory, self.filename)
        if not self.is_valid_extension(filepath) or not self.is_valid_filename(filepath):
            return 
        with open(filepath, "rb") as f:
            file = f.read()
        return file

    @staticmethod
    def is_valid_extension(file_path):
        """Check if an file extension is valid."""
        ext = os.path.splitext(file_path)[1]
        if not ext:
            return False
        return ext in FileHandler.VALID_EXTENSIONS

    @staticmethod
    def is_valid_filename(file_path):
        """Check if a filename is valid."""
        name = os.path.basename(file_path)
        return name not in FileHandler.INVALID_FILENAME

    @staticmethod
    def get_filepaths_to_send(paths, is_recursive):
        raise NotImplementedError

    @staticmethod
    def get_files_from_dir():
        raise NotImplementedError
