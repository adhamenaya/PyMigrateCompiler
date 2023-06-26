from io import StringIO ## for Python 3

class StringBuilder:
     _file_str = None

     def __init__(self):
         self._file_str = StringIO()

     def append(self, str):
         self._file_str.write(str)

     def __str__(self):
         return self._file_str.getvalue()
