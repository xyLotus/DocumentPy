"""
This is the DocPy module made for creating HtmlDocuments in
a commandline interface environment.
It is also very handy for creating HTML Documentations.
"""

__author__ = 'Lotus'
__version__ = 0.7

# Imports
import os
import platform

# External Imports
try:
    from bs4 import BeautifulSoup
except ImportError as e:
    print('Error while trying to import external libary.')
    print('Traceback:\n', e)
    exit()

# Figuring out platform [os] & checking compatiblity
platform = platform.system()
if not platform in ['Windows', 'Linux']:
    print('Youre using a platform that is not compatible with this program.')
    print('Compatible platforms: Windows, Linux.')
    exit()

clear_commands = {'Windows': 'cls', 'Linux': 'clear'}
clear_command = clear_commands[platform]

# Setting title for commandline if platform is Win
if platform == 'Windows':
    os.system('title Commandline Interface Environment')

# Create Back-up File
if not os.path.isfile(f'{os.getcwd()}/backup.html'):
    with open('backup.html', 'w'):
        pass

# Global Functions
def call_method(cls: object, function: str, args: list):
    """ Calls method from given class, with given arguments """
    getattr(cls, function)(args)

def error(txt: str):
    """ Outputs string in error format. """
    print(f'[ERROR] - ({txt})')

def get_prettify(src: str) -> str:
    """ Function returning the prettified version of the given file [@param = file]"""
    try:
        prettify_obj = BeautifulSoup(src, 'html.parser')
        return prettify_obj.prettify()
    except Exception as e:
        print(f'Error while trying to prettify src')
        print(f'Traceback:\n{e}')
        exit()

# Classes
class Document:
    """ Document class responsible for assigning mandatory doc vars. """
    title = ''
    lang = ''
    author = ''
    charset = ''
    content = ''
    css_file = ''
    body_content = ''
    background = ''
    nextline = False


doc = Document()

# Global Function (includes mandatory object to work [doc | @Document])
def append_content(additional_content: str):
    """ Appends the content (@file = htmldoc, @tag = <body>). """
    doc.content += additional_content + '\n'


class FileStream:
    """ FileStream Class responsible for file handling. """
    def __init__(self):
        #====FileDataVars====#
        self.open_bool = False
        self.new_bool = False
        self.file = ''
        self.file_str = ''
        #====================#

        #===FileContentVar===#
        cwd = os.getcwd()
        try:
            with open(f'{cwd}/skeleton.html', 'r') as f:
                self.skeleton = f.read()
        except Exception as e:
            # Error Stacktraceback & Exit
            error(e)
            exit()
        #====================#

    def write(self, text):
        """ Write to file. """
        with open(self.file, 'a') as f:
            f.write(text)

    def init_skeleton(self):
        """ Method that writes skeleton to given file. """
        with open(self.file, 'w') as f:
            f.write(self.skeleton)
        
    def get_content(self, file_name: str):
        """ Gets the whole content of a given file. """
        with open(file_name, 'r') as f:
            return f.read()

    def backup(self):
        """ backs up the current htmldoc content in backup.html """
        with open('backup.html', 'w') as f:
            content_inst = self.file_str.format(
                                    title = doc.title, 
                                    lang = doc.lang, 
                                    char = doc.charset, 
                                    author = doc.author, 
                                    content = doc.content )

            soup = BeautifulSoup(content_inst, 'html.parser')
            f.write(soup.prettify())

    @staticmethod
    def insert_line(src: list, line: str, pos: int) -> list:
        """ Inserts line @pos in src [list]. """
        src = src[:pos] + [line] + src[pos:]
        return src

    def insert_content_tag(self, content: str, search_kw: str) -> bool:
        """ Method that inserts {content} before the </body> tag, if {content} is non existent. """
        content_tag = '  {content}'
        str_instance = content.splitlines()
        line_count = 0
        for line in str_instance:
            if not content_tag in line:
                if search_kw in line:
                    str_instance = self.insert_line(
                                        src = str_instance, 
                                        line = content_tag, 
                                        pos = line_count )

                self.file_str = ''
                for line in str_instance:
                    self.file_str += line + '\n'

                with open(self.file, 'w') as f:
                    f.write(self.file_str)
            else:
                return
            line_count += 1

    def update_doc(self, content: str, fin_seq: bool = False):
        """ Method that updates htmldoc with prettified HTML and inserted {config}. """
        pretty_content = get_prettify(content)

        if not fin_seq:
            self.insert_content_tag(pretty_content, ' </body>')
            reformated_content = self.file_str
        else:
            reformated_content = content
        
        with open(self.file, 'w') as f:
            f.write(get_prettify(reformated_content))


file_stream = FileStream()

class Commands:
    """ Commands class responsible for storing methods, that will get reflected. [See: C# Reflection] """
    def __init__(self):
        self.auto_coloring = True
        self.next_line = True
        self.auto_color = 'black'
    
    #====PrivateFunctions====#
    def _construct_txt(self, src: str, param_index: int) -> list:
        """ Constructs inner text of given tag [@param = src]. """
        tag_text = ''
        index_count = 0
        if self.auto_coloring:
            for arg in src[param_index:]:
                if index_count == len(src[param_index:])-1:
                    tag_text += arg
                else:
                    tag_text += arg + ' '
                index_count += 1
        else:
            self.auto_color = 'black'
            for arg in src[param_index:]:
                if index_count == len(src[param_index:])-1:
                    tag_text += arg
                else:
                    tag_text += arg + ' '
                index_count += 1

                tag_text += arg

        return [tag_text, self.auto_color]
    #======================#

    #====FileCommands====#
    def open(self, args):
        """ Method that opens the given file. """
        if not file_stream.new_bool:
            file_stream.open_bool = True

        doc.content = ''

        cwd = os.getcwd()
        if os.path.isfile(f'{cwd}/{args[0]}'):
            file_stream.file = args[0]

            with open(file_stream.file, 'r') as f:
                file_stream.file_str = f.read()
            
            file_stream.insert_content_tag(file_stream.file_str, '  </body>')
        else:
            error(f'Couldnt find [{args[0]}]')
            exit()
        
        print(f'Opened [{args[0]}]!')

    def new(self, args):
        """ Method that creates a new file. """
        file_stream.new_bool = True
        cwd = os.getcwd()
        if not os.path.isfile(f'{cwd}/{args[0]}'):
            print(f'Creating [{args[0]}]...')

            file_stream.file = args[0]
            with open(args[0], 'w'):
                pass
            
            file_stream.init_skeleton()
            self.open(args = [args[0]])
        else:
            error(f'File [{args[0]}] already exists.')

    def reload(self, args, fin_seq: bool = False):
        """ Method that reloads current htmldoc with the new given elements. """
        if fin_seq:
            print(r'File will be finalized, {content} tag removed.')
            print('You can start editing the file again by using the "open [file_name]" command (Y/N)')
        else:
            print('Warning: You will not be able to change your changes later on.')
            print('Are you sure that you want to save these changes? (Y/N)')
        answer = input('           -> ')
        if answer.upper() in ['Y', '', ' ']:
            print('Saving changes...')
            if file_stream.open_bool:
                content_instance = file_stream.file_str.format(content = doc.content)
                
                file_stream.update_doc(content_instance, fin_seq)
            else:
                content_instance = file_stream.file_str.format(
                                    title = doc.title, 
                                    lang = doc.lang, 
                                    char = doc.charset, 
                                    author = doc.author, 
                                    content = doc.content )

                file_stream.update_doc(content_instance, fin_seq)

                print(f'Updated [{file_stream.file}]!')
        elif answer.upper() == 'N':
            print('Changes not saved.')
        doc.content = ''
    #====================#

    #========Misc========#
    def out(self, args):
        """ CMD Output. """
        index_count = 0
        for arg in args:
            if not index_count == len(args)-1:
                print(arg, end=' ')
            else:
                print(arg)
            index_count += 1

    def cls(self, args):
        """ Method that clears the commandline interface. """
        os.system(clear_command)
    
    def exit(self, args):
        """ Method that exits the program. """
        self.finish('')
        exit()
    
    def getfile(self, args):
        """ Method that outputs the current file. [See: @FileStream] """
        if len(file_stream.file) > 0:
            print('Current Working File: ', file_stream.file)
        else:
            print('Current Working File: NONE')
        file_stream.backup()
    #====================#

    #====HTMLDocInfo====#
    def title(self, args):
        """ Sets title for htmldoc. """
        doc.title = args[0]
        file_stream.backup()
        print('Set title to [', doc.title, ']')
    
    def charset(self, args):
        """ Sets charset for htmldoc. """
        doc.charset = args[0]
        file_stream.backup()
        print('Set charset to [', doc.charset, ']')

    def author(self, args):
        """ Sets author for htmldoc. """
        doc.author = args[0]
        file_stream.backup()
        print('Set author to [', doc.author, ']')

    def lang(self, args):
        """ Sets language for htmldoc. """
        doc.lang = args[0]
        file_stream.backup()
        print('Set lang to [', doc.lang, ']')
    #====================#

    #====FileEditing====#
    def finish(self, args):
        """ Upon calling this command the {content} tag will not be inserted & exit seq. """
        self.reload(args = '', fin_seq = True)

    def nextline(self, args):
        r""" Command responsible for either inserting a \n at end of a </tag> or not. """
        pass

    def background(self, args):
        """ Command that sets background color in htmldoc. """
        doc.background = args[0]
        print('Set background to [', doc.background, ']')

    def delete(self, args):
        """ Command that deletes everything in content. """
        print('Are you sure that you want to delete all of the <body> content? (Y/N)')
        answer = input('')
        if answer.upper() == 'Y':
            print('<body> content cleared!')
            doc.content = ''
        elif answer.upper() == 'N':
            print('<body> content not cleared.')

    def coloring(self, args):
        """ Command that auto-colors the given htmldoc element to the given color. """
        if args[0].upper() in ['TRUE', 'ON']:
            self.auto_coloring = True
            print('Auto-Coloring: On')
        elif args[0].upper() == ['FALSE', 'OFF']:
            self.auto_coloring = False
            print('Auto-Coloring: Off')
        elif args[0] == '':
            print(self.auto_color)
        else:
            self.auto_color = args[0]       
            print('Set auto-coloring to: [', args[0], ']')
            
    def code(self, args):
        """ Creates code tag with given content. """
        # Command Info: (NOTE -> zero-indexed)
        # Arg1 = CodeTagContent
        c_code, color_str = self._construct_txt(src = args, param_index = 0)
        
        code_content = f'<code style="color:{color_str}";>{c_code}</code>'
        append_content(code_content)
        file_stream.backup()

        print(f'Created HTML Document Element [{code_content}]')

    
    def header(self, args):
        """ Creates given header with given size in htmldoc. """
        # Command Info: (NOTE -> zero-indexed)
        # Arg1 = HeaderSize (index), Arg2 = Header Text
        h_text, color_str = self._construct_txt(src = args, param_index = 1)

        header_info = f'<h{args[0]} style="color:{color_str}";>{h_text}</h{args[0]}>'
        append_content(header_info)
        file_stream.backup()

        print(f'Created HTML Document Element [{header_info}]')

    def paragraph(self, args):
        """ Creates a new paragraph with the given text. """
        # Command Info: (NOTE -> zero-indexed)
        # Arg1 = Paragraph Text
        p_text, color_str = self._construct_txt(src = args, param_index = 0)

        paragraph_str = f'<p style="color:{color_str}">{p_text}</p>'
        append_content(paragraph_str)
        file_stream.backup()
        
        print(f'Created HTML Document Element [{paragraph_str}]')
    #=================#

    #===CommandAlternatives===#
    def fin(self, args):
        """ Upon calling this command the {content} tag will not be inserted & exit seq. """
        # NOTE -> This is a alternative version of the finish method
        self.reload(args = '', fin_seq = True)
    def c(self, args):
        """ Creates code tag with given content. """
        # Command Info: (NOTE -> zero-indexed)
        # Arg1 = CodeTagContent
        # NOTE -> This is a alternative version of the code method
        c_text, color_str = self._construct_txt(src = args, param_index = 0)
        
        code_content = f'<code style="color:{color_str}";>{c_text}</code>'
        append_content(code_content)
        file_stream.backup()

        print(f'Created HTML Document Element [{code_content}]')

    def h(self, args):
        """ Creates given header with given size in htmldoc. """
        # Command Info: (NOTE -> zero-indexed)
        # Arg1 = HeaderSize (index), Arg2 = Header Text
        # NOTE -> This is a alternative command [@method = header]
        h_text, color_str = self._construct_txt(src = args, param_index = 1)

        header_info = f'<h{args[0]} style="color:{color_str}";>{h_text}</h{args[0]}>'
        append_content(header_info)
        file_stream.backup()

        print(f'Created HTML Document Element [{header_info}]')

    def p(self, args):
        """ Creates a new paragraph with the given text. """
        # Command Info: (NOTE -> zero-indexed)
        # Arg1 = Paragraph Text
        # NOTE -> This is a alternative command [@method = paragraph]
        p_text, color_str = self._construct_txt(src = args, param_index = 0)

        paragraph_str = f'<p style="color:{color_str}">{p_text}</p>'
        append_content(paragraph_str)
        file_stream.backup()
        
        print(f'Created HTML Document Element [{paragraph_str}]')

    def ac(self, args):
        """ Command that auto-colors the given htmldoc element to the given color. """
        # NOTE -> This is a alternative command [@method = coloring]
        if args[0].upper() in ['TRUE', 'ON']:
            self.auto_coloring = True
            print('Auto-Coloring: On')
        elif args[0].upper() == ['FALSE', 'OFF']:
            self.auto_coloring = False
            print('Auto-Coloring: Off')
        elif args[0] == '':
            print(self.auto_color)
        else:
            self.auto_color = args[0]       
            print('Set auto-coloring to: [', args[0], ']')
    
    def bg(self, args):
        """ Command that sets background color in htmldoc. """
        # NOTE -> This is a alternative version of the background method
        doc.background = args[0]
        print(f'Set background to [{doc.background}]')
    #=========================#


cmds = Commands()


class Commandline:
    """ Commandline Interface Environment Class. """
    def __init__(self):
        self.prefix: str = '-$'
        
    def run(self):
        """ Method that runs the (runtime) endless cmd loop. """
        no_check_func = [
                        'cls', 
                        'new', 
                        'open', 
                        'getfile', 
                        'out', 
                        'exit', 
                        'coloring', 
                        'c',
                        'nextline']
        
        no_nextline_funcs = ['cls']
        
        while 1:
            raw_cmd = input(f'{self.prefix} ').split()
            if not len(raw_cmd) == 0:
                base_cmd = raw_cmd[0]
                cmd_args = raw_cmd[1:]
                try:
                    if base_cmd in no_check_func:
                        call_method(cmds, base_cmd, cmd_args)
                        if cmds.next_line:
                            if not base_cmd in no_nextline_funcs:
                                print()
                    else:
                        if len(file_stream.file) == 0:
                            error('FileStream file attribute is not defined')
                            print('| -> Create A File: "new file_name" - Open A File: "open file_name"')
                        else:
                            call_method(cmds, base_cmd, cmd_args)
                            if cmds.next_line:
                                if not base_cmd in no_nextline_funcs:
                                    print()
                except AttributeError as e:
                    print('Error -> ', e)
                    error(f'Command [{base_cmd}] could not be found')
                except IndexError as e:
                    print(e)
                    error(f'Command [{base_cmd}] requires more than the [{len(cmd_args)}] given arguments')

# Commandline init
cmdl = Commandline()
cmdl.run()
