import os
from FilesCreator import FilesCreator


all_adapters_calls = []    
all_adapters_calls2 = {}

def extract_adapter(self, name, text):
    
    for line in text:
        if "public" in line and "(" in line and ")" in line:
            latest_function_params = {}
            params = line.split("(")
            params = params[1].replace(")","")
            params_list = params.split(",")

            for p in params_list:
                p = p.lstrip()
                p = p.rstrip()
                p = p.replace("\n","")
                p_pair = p.split(" ")
                if len(p_pair) == 2:
                    latest_function_params[p_pair[1]] = p_pair[0]
        elif "." in line:
            
            adapter = line.split(".")
            if "Adapter" in adapter[0] or "adapter" in adapter[0]:
                adapter_name = adapter[0].split(" ")[len(adapter[0].split(" "))-1]
                function_part = adapter[1].split("(")
                function_name = function_part[0]
                try:
                    function_params = function_part[1].split(")")[0]
                    function_params = function_params.replace(" ","").split(",")
                except:
                    print("")
                    function_params = []

                funtion_params_types = []
                if function_params is not None:
                    for fp in function_params:
                        #print(latest_function_params)
                        try:
                            fp_with_type = latest_function_params[fp]+" "+fp
                        except KeyError:
                            fp_with_type = "N/A "+ fp

                        funtion_params_types.append(fp_with_type)
                    if adapter_name not in all_adapters_calls2:
                        all_adapters_calls2[adapter_name] = []
                    else:
                        all_adapters_calls2[adapter_name].append(function_name+"("+",".join(funtion_params_types)+")")
                    #adapetr_call = adapter_name+"."+function_name+"("+",".join(funtion_params_types)+")"
                    #all_adapters_calls2[adapter_name].append(function_name+"("+",".join(funtion_params_types)+")")
                    #all_adapters_calls.append(adapetr_call)

                                    



folders = os.listdir("Implementations")
#folders = ["Event"]
adapters = []

for f in folders:
    files = os.listdir("Implementations\\"+f)
    print(f)
    for fi in files:
        with open("Implementations\\"+f+"\\"+fi) as fp:
            lines = fp.readlines()
            ads = extract_adapter("","Adapter", lines)

### Generate Repos Source code
def create_irepo_method(functions, name, repo):
    text = ""
    text += "using M2.Business.Repositories;\n"
    text += "using Microsoft.EntityFrameworkCore;\n"
    text += "using System;\n"
    text += "using System.Collections.Generic;\n"
    text += "using System.Threading.Tasks;\n"
    text += "using System.Linq;\n"
    text += "using M2.Business.Entities;\n"
    
    text += "\n"
    text += "namespace M2.Data.Repositories\n"
    text += "{\n"
    text += "   public class "+name+" : Repository<"+repo+">, I"+name+"\n"
    text += "   {\n"
    text += "       public "+name+"(M2DbContext context) : base(context) { }\n"
    text += "       private M2DbContext M2DbContext { get { return Context as M2DbContext; } }\n"

    functions = []
    for f in functions:
        text += "       public Task<N/A> " + f + "\n"
        text += "       {\n"
        text += "           throw new NotImplementedException();\n"
        text += "       }\n"
    text += "       }\n"
    text += "}\n"

    return text

fc = FilesCreator("repos3")
for repo in all_adapters_calls2:

    interface = repo.replace("Adapter","")+"Repository"
    fc.create_file(interface+".cs","",create_irepo_method(all_adapters_calls2[repo],interface,repo.replace("Adapter","")))
    
print(len(all_adapters_calls2))
