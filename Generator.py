import os
from Parser import Parser
from Parser import Class
from EntityGenerator import EntityGenerator
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
              "M2.Business.Entities",
              "M2.Business.Repositories",
              "System",
              "System.Collections.Generic",
              "System.Text",
              "System.Threading.Tasks"
          }

class Generator:
    overall_text = ""
    package_name = ""
    parent_dir = "/"
    mode = 0o666

    new_entity = []

    eg = EntityGenerator()
    fc = FilesCreator("Event")

    _class = None

    def __init__(self):
        print("Init Generator")

    def insert_using(self, region):
        for u in usings:
            self.add_line("using " + u + ";")

        self.add_line("using M2.Business.Entities."+self.package_name+";")
        self.insert_namespace(region)

    def insert_namespace(self, region):
        self.add_line("")
        self.add_line("namespace "+"M2.Business.Services."+self.package_name)
        self.add_line("{")
        #add interface
        self.insert_interface(region)
        self.add_line("}")
    
    def insert_interface(self, region):
        if region.functions is None:
            return
        self.add_line("    public interface "+"I"+region.name+"Service")
        self.add_line("    {")

        #add methods
        self.isnert_functions(region)
        
        self.add_line("    }")
        
    def isnert_functions(self, region):
        if self._class != None:
            for f in region.functions: #TODO: change regions[0]
                if f == None:
                    continue
                if self.function_return_list(f):
                    self.insert_function_list(f)
                else:
                    self.insert_function_value(f)
        else:
            print("no class")
        
    def insert_function_value(self, function):
        return_type = self.get_csharp_dtype(function._return)
        function_name = function.name
        input_params = []
        input_params_str = ""

        for _input in function._input:
            input_type = ""
            if(_input.nullable):
                input_type = "Nullable<"+self.get_csharp_dtype(_input._type)+">"
            else:
                input_type = self.get_csharp_dtype(_input._type)
            input_params.append(input_type+" "+_input.name)
            
        input_params_str = ",".join(input_params)
        
        self.add_line("        ValueTask<"+return_type+"> "+function_name+"("+input_params_str+");")

    def extract_return_type(self, _return):
        parts = _return.split(".")
        last_part = parts[len(parts)-1]
        last_part = last_part.replace("DataTable","")
        return last_part

    def insert_function_list(self,function):
        return_type = self.get_csharp_dtype(self.extract_return_type(function._return))
        function_name = function.name
        input_params = []
        input_params_str = ""

        list1 = ["",""]
        for _input in function._input:
            input_params.append(self.get_csharp_dtype(_input._type)+" "+_input.name)
            
        input_params_str = ",".join(input_params)
        
        self.add_line("        Task<IList<"+return_type+">> "+function_name+"("+input_params_str+");")

    def function_return_list(self, function):
        if function._return.endswith("DataTable"):
            return True
        else:
            return False

    def get_csharp_dtype(self, vb_type):
        if vb_type in data_type_map:
            return data_type_map[vb_type]
        else:
            self.append_not_found_type(vb_type)
            return vb_type

    def add_line(self, text):
        self.overall_text = self.overall_text + text + "\n"

    def run(self, package_name):
        self.package_name = package_name
        self.fc.create_dir(package_name)
        p = Parser()
        vb = p.read_file_as_one_line("Event\\"+package_name+".txt")
        self._class = p.run(vb)

        for r in self._class.regions:

            if len(r.functions) == 0:
                continue
            
            self.overall_text = ""
            self.insert_using(r)
            #self.create_file(p.create_camel_case(r.name)+".cs",package_name,self.overall_text)
            self.fc.create_file("I"+r.name+"Service.cs",package_name,self.overall_text)
            
            print(self.overall_text)

    def append_not_found_type(self,_type):
        if _type not in self.new_entity:
            #self.fc.append_file("not_found","types",_type+"\n")
            self.new_entity.append(_type)
            self.eg.create_new_entity(self.package_name,_type)
        
import os
files = os.listdir("Event")
print(files)
for f in files:
    continue
    file_name = f.split(".")[0]
    print(file_name)
    g = Generator()
    g.run(file_name)
    
g = Generator()
g.run("Event")



