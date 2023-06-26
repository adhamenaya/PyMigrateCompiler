import os

class FilesCreator:
    parent_dir = "Entities"
    _class = None
    wroking_dir = "Entities"

    def __init__(self):
        print("Init FilesCreator")

    def __init__(self, wroking_dir= ""):
       self.wroking_dir = wroking_dir

    def create_dir(self, name):
        path = os.path.join(self.parent_dir, name)

        if not os.path.exists(self.wroking_dir+"/"+name):
            os.mkdir(self.wroking_dir+"/"+name) 
            print("Directory '% s' created" % self.wroking_dir+"/"+name)
        else:
            print("Directory is already exist")

    def create_file(self, file, folder, content):
        content = '\n'.join([i for i in content.replace("\r","").split('\n') if len(i) > 0])
        f = open(self.wroking_dir+"/"+folder+"/"+file, 'w')
        f.write(content)
        f.close()

    def append_file(self, file, folder, content):
        f = open(self.wroking_dir+"/"+folder+"/"+file, 'a')
        f.write(content)
        f.close()

    def add_line(self, text):
        self.overall_text = self.overall_text + text + "\n"


fc = FilesCreator("Entities")
#fc.create_dir("adham")



