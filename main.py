import configparser
import os
import sys
from datetime import datetime
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.ttk import Combobox
import xmlschema
import logging


def BrowseXSDschema():
    try:
        global SchemaDir
        SchemaDir = str(filedialog.askopenfile().name)
        lblXSDschema['text'] = str(SchemaDir)
    except (TypeError, AttributeError):
        messagebox.showerror('Ошибка', 'Схема не выбрана!')
    except Exception as e:
        messagebox.showerror('Ошибка Python', 'Error:' + str(e) + str(e.args))
        logging.error(str(now) + '   ' + str(e) + ' ' + str(e.args))


def BrowseFile():
    try:
        global FileName
        FileName = str(filedialog.askopenfile().name)
        lblFilename['text'] = str(FileName)
    except (TypeError, AttributeError):
        messagebox.showerror('Ошибка', 'Файл не выбран!')
    except Exception as e:
        messagebox.showerror('Ошибка Python', 'Error:' + str(e) + str(e.args))
        logging.error(str(now) + '   ' + str(e) + ' ' + str(e.args))


def XSDCheckExec():
    ResultWindow.delete("1.0", END)
    Schema = xmlschema.XMLSchema(SchemaDir)

    try:
        if Schema.is_valid(FileName) is True:
            ResultWindow.insert("1.0", "Проверка пройдена успешно.", 'succes')
        else:
            Schema.validate(FileName)
            #ResultWindow.insert("1.0", "Проверка не пройдена!", 'warning')
    except xmlschema.XMLSchemaValidationError as err:
        #messagebox.showerror('Ошибка Python', 'Error:' + str(err) + str(err.args))
        logging.error(str(now) + '   ' + str(err) + ' ' + str(err.args))
        ResultWindow.insert("1.0",
                            'Проверка не пройдена\n' , 'warning')
        ResultWindow.insert(END, str(now) + '\n' + str(err.elem) + '\n' + str(err.reason))
    except Exception as e:
        messagebox.showerror('Ошибка Python', 'Error:' + str(e) + str(e.args))
        logging.error(str(now) + '   ' + str(e) + ' ' + str(e.args))
        ResultWindow.insert("1.0", 'Ошибка XML-файла\n' + str(now) + ' ' + str(e) + ' ' + str(e.args))




def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        app_path = os.path.dirname(sys.executable)
    elif __file__:
        app_path = os.path.dirname(__file__)
    logging.debug(str(now) + ' resource_path ' + str(app_path) + str(relative_path))
    return os.path.join(app_path, relative_path)


def get_schemas_list(path):
    try:
        for subdir, dirs, files in os.walk(path):
            for file in files:
                filepath = subdir + os.sep + file
                if filepath.endswith(".xsd"):
                    schemas_map[file] = filepath
    except Exception as e:
        messagebox.showerror('Ошибка Python', 'Error:' + str(e) + str(e.args))
        logging.error(str(now) + '   ' + str(e) + ' ' + str(e.args))

def ComboboxSelect(event):
    global SchemaDir
    SchemaDir = str(schemas_map[cbxSchema.get()])
    logging.debug(str(now) + ' ComboboxSelect ' + SchemaDir)

def default_cbx_option():
    if 'Main.xsd' in schemas_map:
        cbxSchema.set('Main.xsd')
        ComboboxSelect("<<ComboboxSelected>>")
    elif len(schemas_map) == 0:
        messagebox.showwarning('Схемы', 'Не подгружен список.Папка со схемами пуста')

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='xsd_checker.log', encoding='utf-8', level=logging.DEBUG)

    now = datetime.now()
    SchemaDir = "<Схема не выбран>"
    FileName = "<Файл не выбран>"
    schemas_map = {}

    get_schemas_list(str(resource_path("schemas")))
    schemas_map_keys = list(schemas_map.keys())

    root = Tk()
    root.title("Проверка XML-файла по XSD-схеме")
    root.geometry("950x400")

    frame_schema = LabelFrame() #(width=200, height=200)
    frame_schema.pack(padx=1, pady=1, expand=True, anchor="nw")

    lblXSDschema = Label(frame_schema, text="Выбор Cхемы:")
    lblXSDschema.pack(padx=1, pady=1, expand=True, side="left")

    cbxSchema = Combobox(frame_schema, values=schemas_map_keys, state="readonly")
    cbxSchema.pack(padx=1, pady=1, expand=True, side="left")
    cbxSchema.bind("<<ComboboxSelected>>", ComboboxSelect)

    frame_file = LabelFrame() #(width=700, height=50)
    frame_file.pack(padx=1, pady=1, expand=True, anchor="w",fill='x') #(padx=5, pady=5, expand=True)

    btnBrowseFile = Button(frame_file, text="Выберите файл", command=BrowseFile)
    btnBrowseFile.pack(padx=1, pady=1,expand=True, side="left",fill='x')

    lblFilename = Label(frame_file, text=FileName, width=200, padx=2, pady=2, bd=2, relief=RIDGE)
    lblFilename.pack(padx=1, pady=1, expand=True, side="left",fill='x')

    frame_exec = LabelFrame(width=700, height=700)
    frame_exec.pack(padx=1, pady=1, expand=True,fill='both',  anchor="s")

    btnXSDCheckExec = Button(frame_exec,height=5, width=9,text="Проверить", command=XSDCheckExec)
    btnXSDCheckExec.pack(padx=10, pady=10,expand=True, side="left")


    ResultWindow = Text(frame_exec, height=20, width=100, wrap="word")
    ResultWindow.tag_config('warning', background="yellow", foreground="red")
    ResultWindow.tag_config('succes', foreground="green")
    ResultWindow.pack(padx=10, pady=10, side="left", expand=True,fill='both')


    default_cbx_option()
    root.mainloop()
