from StringBuilder import StringBuilder
class Class:
    access = ""
    name = ""
    regions = []
    enums = []
    consts = []
    declars = []

    def __init__(self):
        pass

    def __init__(self, name, access):
        self.name = name
        self.access = access
        
    def add_region(self, r):
        self.regions.append(r)

    def add_enums(self, enums):
        self.enums.append(enums)

    def set_consts(self, consts):
        self.consts = consts

    def set_declars(self, declars):
        self.declars = declars

    def print(self):
        print("-Class: "+ self.access+" "+ self.name)

        for e in self.enums:
            e.print()

        print("###Consts: ")
        for c in self.consts:
            c.print()

        print("###Declars: ")
        for d in self.declars:
            d.print()
            
        for r in self.regions:
            r.print()

        
                
class Region:
    name = ""
    functions = []

    def __init__(self, name):
        self.name = name
        self.functions = []
    def addFunction(self, f):
        self.functions.append(f)

    def print(self):
        print("###Region: "+ self.name)
        for f in self.functions:
            if f is not None:
                f.print()

class Function:
    name = ""
    body = ""
    _input = []
    _return = None
    def __init__(self, name):
        self.name = name
    def setInput(self, _input):
        self._input = _input
    def setReturn(self, _return):
        self._return = _return
    def set_body(self, body):
        self.body = body

    def print(self):
        print("-----Function: "+ self.name)
        print("------Input: ")
        for p in self._input:
            p.print()
        print("------Return: "+self._return)
        
class FunParam:
    name = ""
    _type = ""
    nullable = False
    
    def __init__(self, name, _type, nullable):
        self.name = name
        self._type = _type
        self.nullable = nullable

    def print(self):
        print("------"+self.name+","+self._type+","+self.nullable)

class Enums:
    name = ""
    values = []

    def __init__(self, name, values):
        self.name = name
        self.values = values

    def print(self):
        print("###Enums: "+self.name)
        sb = []
        for k,v in self.values:
            sb.append(k+","+v)
        s = ":".join(sb)
        print("-----"+s)
        
class Const:
    name = ""
    _type = ""
    default = ""

    def __init__(self, name, _type, default):
        self.name = name
        self._type = _type
        self.default = default

    def print(self):
        print("-----"+self.name+":"+self._type+"="+self.default)

class Declar:
    name = ""
    _type = ""
    default = ""

    def __init__(self, name, _type, default):
        self.name = name
        self._type = _type
        self.default = default

    def print(self):
        print("-----"+self.name+":"+self._type+"="+self.default)
        
class Parser:
    pos = 0
    global text
    def next_char(self):        
        if(not self.eof()):
            return self.text[self.pos]

    
    def run(self, text0):
        self.text = text0

        imports = self.find_imports()

        self.parse_extras()        
        access = self.parse_access_modifier()
        name = self.parseClass()
        _class = Class(name, access)
        
        regions = []

        while True:  
            regionName = self.parseRegion()
            region = Region(regionName)
            print("***"+regionName)
            while True:
                # Find enums
                if regionName == "Enums":
                    name, values = self.find_enums()
                    _class.add_enums(Enums(name, values))
                    self.consume_white_space()
                elif regionName == "Entity Constants":
                    consts = self.find_const()
                    _class.set_consts(consts)
                    self.consume_white_space()
                elif regionName == "Table Adapter Declarations":
                    declars = self.find_adapter_declarations()
                    _class.set_declars(declars)
                    self.consume_white_space()
                elif regionName == "Table Adapter Properties":
                    self.consume_char()
                    self.consume_white_space()
                else:
                    self.consume_white_space()
                    self.parse_extras()
                    
                    f = self.parse_function_signature()

                    funBodyParsed, body = self.parse_function_body()
                    print(body)
                    if f is not None:
                        f.set_body(body)
                    
                    region.addFunction(f)
                    self.consume_white_space()

                
                if self.next_char()=="#":
                    break
            if regionName not in ("Enums", "Entity Constants"):
                _class.add_region(region)
            self.parse_end_region()
            print("3333333333333333")
            if self.start_with("End Class"):
                break
                
        self.parseEndClass()
        #_class.print()
        return _class
        

    def start_with(self, prefix):
        return self.text[self.pos:].lstrip().startswith(prefix) == True

    def eof(self):
        return self.pos >= len(self.text)

    def consume_char(self):
        if self.pos < len(self.text):
            ch = self.text[self.pos]
            self.pos = self.pos + 1
            return ch
        else:
            return None
        
    def consume_white_space(self):
        while(not self.eof() and self.is_white_space(self.text[self.pos])):
            ch = self.consume_char()

    def is_white_space(self, ch):
        return ch == " "

    #runner
    def consume_while(self):
        sb = ""
        while(not self.eof()):
            sb = sb + str(self.consume_char())

        return str(sb)

    def parse_access_modifier(self):
        sb = ""
        if(self.start_with("Public")):
            while(True):
                self.consume_white_space()
                sb = sb + self.consume_char()
                if sb == "Public":
                    return str(sb)
                
        elif(self.start_with("Private")):
            while(True):
                self.consume_white_space()
                sb = sb + self.consume_char()
                if sb == "Private":
                    return str(sb)

    def parse_extras(self):
        self.consume_white_space()
        if self.start_with("<"):
            x = self.consume_char()
            while True:
                self.consume_char()
                if self.next_char()==">":
                    self.consume_char() #remove the > char
                    self.consume_white_space()
                    if self.next_char() == "_":
                        self.consume_char() #remove the _ char
                    break
                
    def parseClass(self):
        className = ""
        self.consume_white_space()
        if(self.start_with("Class")):
            while(True):
                self.consume_white_space()
                self.find_keyword("Class")
                className = self.find_element()
                self.consume_white_space()
                if(self.next_char()=="#" or self.next_char()==" "):
                    break
        return className
                
    def parseEndClass(self):
        
        sb = ""
        c = 0
        self.consume_white_space()
        if(self.start_with("End Class")):
            while(True):
                self.consume_white_space()
                ch = self.consume_char()
                sb = sb + ch
                if str(sb) == "End Class":
                    return True
                else:
                    return False
                
    def parseRegion(self):
        regionName = ""
        self.consume_white_space()
        if(self.start_with("#Region")):
            self.consume_white_space()
            self.find_keyword("#Region")
            regionName = self.find_element_withQ()
            
            #remove white space in between
            #regionName = self.create_camel_case(regionName)
            
        return regionName

    def create_camel_case(self, name):
        name2 = name.title()
        name2 = name2.replace(" ","")
        return name2
            
    
    def parseClass(self):
        className = ""
        self.consume_white_space()
        if(self.start_with("Class")):
            self.consume_white_space()
            self.find_keyword("Class")
            className = self.find_element()
            self.consume_white_space()
   
        return className
    def parse_end_region(self):
        
        sb = ""
        c = 0
        self.consume_white_space()
        if(self.start_with("#End Region")):
            self.consume_white_space()
            while(True):
                ch = self.consume_char()
                sb = sb + ch
                if str(sb) == "#End Region":
                    return True
            return False

    def parse_function_signature(self):
        self.consume_white_space()
        public = self.parse_access_modifier()
        
        self.consume_white_space()
        sbF = "" #Fucntion keyword
        sbN = "" #Fucntion name
        
        if(self.start_with("Function")):
            while(True):
                self.consume_white_space()
                ch = ""
                if sbF == "Function":
                    if self.next_char() != "(":
                        ch = self.consume_char()
                        sbN = sbN + ch
                    else:
                        pi,pr = self.parse_function_input()
                        f = Function(sbN)
                        f.setInput(pi)
                        f.setReturn(pr)
                        return f             
                else:
                    ch = self.consume_char()
                    sbF = sbF + ch
 
    def parse_function_body(self):
        sbBody = ""
        while(True):
            if self.start_with("End Function"):
                self.consume_white_space()
                end = self.find_keyword("End")
                fucntion = self.find_keyword("Function")
                sbBody = sbBody.replace("     ","\n")
                return True, sbBody
            else:
                ch = self.consume_char()
                sbBody = sbBody + ch
        return False, ""
         
    def curr(self):
        print(self.text[self.pos:])

    def parse_function_input(self):
        self.consume_white_space()
        params = []

        sbByV = ""          # ByValue keyword
        sbParamName = ""    # param name
        sbAs = ""           # As keyword
        sbParamType = ""    # param type
        ch = ""
        nameComplete = False
        
        if(self.start_with("(")):
            ch = self.consume_char() #remove (
            if self.next_char()!=")":
                while(True):
                    self.consume_white_space()
                    if self.start_with("ByVal"):
                        self.find_keyword("ByVal")
                    elif self.start_with("ByRef"):
                        self.find_keyword("ByRef")
                    p,ch = self.find_param_pair()
                    params.append(p)
                    
                    if ch == ")":
                        break
                    
            self.consume_char() # to remove the ) char
            self.find_keyword("As")
            returnParam = self.find_element()
            
        return params, returnParam

    def get_nullable_param(self):
        
        self.consume_white_space()
        
        self.find_keyword("Nullable")
        self.consume_char() #remove (
        self.find_keyword("Of")
        _type = self.find_element()
        self.consume_char() #remove )
        print("###############################################"+_type+"##")
        return _type
        
    def find_param_pair(self):
        
        findType = False
        sbParamName = ""
        sbParamType = ""
        is_null = False
        self.consume_white_space()
        while(True):
            sbParamName = self.find_element()
            self.find_keyword("As")
            self.consume_white_space()
            if 1 == 1:
                if self.start_with("Nullable"):
                    sbParamType = self.get_nullable_param()
                    is_null = True
                else:
                    sbParamType = self.find_element()
                    is_null = False
            else:
                sbParamType = self.find_element()

            if self.next_char() in [" ", ",", ")"]:
                ch = self.consume_char()
                break
                
        return FunParam(str(sbParamName),str(sbParamType),is_null), ch

    def find_keyword(self,keyword,case_sensetive=True):
        sb = ""
        self.consume_white_space()
        while(True):
            ch = self.consume_char()
            sb = sb + str(ch)
            if self.next_char() in [" ", ",", ")", "("]:
                break
        if str(sb) == keyword:
            return True
        else:
            return False
        
    def find_element(self):
        sb = ""
        ch = ""
        self.consume_white_space()
        while(True):
            ch = self.consume_char()
            sb = sb + str(ch)
            if self.next_char() in [" ", ",", ")", "#"] or self.eof():
                #self.consume_char()
                break
        return str(sb)

    def find_element_withQ(self):
        sb = ""
        ch = ""
        countQ=0
        self.consume_white_space()
        while(True):
            ch = self.consume_char()
            if ch !="\"":
                sb = sb + str(ch)
            else:
                countQ = countQ + 1
            if countQ == 2:
                break
            
        return str(sb)

    def find_imports(self):
        imports_list = []
        while self.start_with("Imports"):
            imports = self.find_keyword("Imports")
            lib = self.find_element()
            imports_list.append(lib)
            self.consume_white_space()
        return imports_list

    def find_enums(self):
        self.find_keyword("Public")
        self.find_keyword("Enum")
        enum_name = self.find_element()
        values = []
        while True:
            key = self.find_element()
            self.find_keyword("=")
            value = self.find_element()
            values.append((key, value))
            self.consume_white_space()
            if self.start_with("End Enum"):
                self.find_keyword("End")
                self.find_keyword("Enum")
                break

        return enum_name, values

    def find_const(self):
        self.consume_white_space()
        consts = []

        while self.next_char()!= "#":
            self.find_keyword("Public")
            self.find_keyword("Const")
            name = self.find_element()
            self.find_keyword("As")
            _type = self.find_element()
            self.find_keyword("=")
            default = self.find_element_withQ()
            consts.append(Const(name, _type, default))
            self.consume_white_space()
            
        return consts

    def find_adapter_declarations(self):
        self.consume_white_space()
        declars = []
        while self.next_char()!= "#":
            self.find_keyword("Public")
            name = self.find_element()
            self.find_keyword("As")
            _type = self.find_element()
            self.find_keyword("=")
            default = self.find_element()
            declars.append(Declar(name, _type, default))
            self.consume_white_space()
            
        return declars

#### Read file
    def read_file_as_one_line(self,file_name):
        lines = []
        f = open(file_name,"r",encoding='UTF-8')

        while True:
            line = f.readline()
            # ignore the comment line early
            if line.find("'")!=-1:
                continue
            if not line:
                break
            else:
                #lines.append(line.lstrip().replace("\n",""))
                lines.append(line.lstrip().replace("\n","     "))
        
        return self.convert(lines)

    def convert(self, lst):
        return ' '.join(lst)
