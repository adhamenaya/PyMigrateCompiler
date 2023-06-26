from Parser import Parser
text = "adham enaya"
text2 = ""
pos = 0

p = Parser()
text = p.read_file_as_one_line("old_files\\address.txt")

while pos < len(text):
    text2 += text[pos]
    pos = pos+1

print(text)
print("--------------")
print(text2)

