import os
from Parser import Parser
from Parser import Class
from FilesCreator import FilesCreator

data_type_map = {"Byte":"byte",
                 "Long":"long",
                 "Short":"short",
                 "Integer":"int",
                 "Double":"double",
                 "Date":"DateTime",
                 "Char":"char",
                 "String":"string",
                 "Boolean":"bool"}
usings = {
              "System",
              "System.Collections.Generic",
              "System.Text",
          }

class EntityGenerator:
    overall_text = ""
    _class = None
    fc = FilesCreator("Entities")

    def __init__(self):
        print("Init EntityGenerator")

    def insert_class(self, class_name):
        self.add_line("    public class "+class_name)
        self.add_line("    {")
        self.add_line("        public "+class_name+"() { }")
        self.add_line("    }")

    def insert_using(self):
        for u in usings:
            self.add_line("using " + u + ";")

    def insert_namespace(self, package_name, class_name):
        self.add_line("")
        self.add_line("namespace "+"M2.Business.Entities."+package_name)
        self.add_line("{")
        #add interface
        self.insert_class(class_name)
        self.add_line("}")
        
    def add_line(self, text):
        self.overall_text = self.overall_text + text + "\n"

    def create_new_entity(self, package_name, class_name):
        self.insert_using()
        self.insert_namespace( package_name, class_name)
        self.fc.create_dir(package_name)
        self.fc.create_file(class_name+".cs", package_name, self.overall_text)
        self.overall_text = ""

ec = EntityGenerator()
#ec.create_new_entity("TestPackage","TestClass")


