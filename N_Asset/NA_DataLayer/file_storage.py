from django.core.files.storage import FileSystemStorage


class NAFileStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        return name

    def _save(self, name, content):
        if self.exists(name):
            # if the file exists, do not call the superclasses _save method
            return name
        # if the file is new, do call it
        return super(NAFileStorage, self)._save(name, content)