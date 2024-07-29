import barcode # type: ignore
import os
import subprocess
import sys
from PIL import Image # type: ignore
from PIL import ImageDraw # type: ignore
from PIL import ImageFont # type: ignore
from barcode.writer import ImageWriter # type: ignore
from datetime import datetime
import argparse

global fpath
version="1.1.4"

def resource_path(relative_path)->str:
    #print(f"RElpath{relative_path}")
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def install(package):#depr, valido per test su console
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
def create_barcode(data, filename,codifica)->str:
    print(f"Genero barcode per {data} su {filename} con codifica {codifica}")
    wlog(f"Genero barcode per {data} su {filename} con codifica {codifica}")
    # Scegliere il formato del codice a barre (es. 'code128', 'ean13', ecc.)
    options = {
        'module_width': 0.3,  # Larghezza di ogni singola unità del barcode
        'module_height': 10,
        'quiet_zone': 0,
        'font_size': 10,
        'text_distance': 1,
        'background': 'white',
        'foreground': 'black',
        'write_text': False,  # Disabilita il testo
    }
    if codifica=='code39':
        barcode_class = barcode.get_barcode_class('code39')
    elif codifica=='ean13':
        barcode_class = barcode.get_barcode_class('ean13')
    else:
        barcode_class = barcode.get_barcode_class('code128')
    ean = barcode_class(data, writer=ImageWriter())

    data=data.replace("/","_")
    
    filename=resource_path(os.path.join(filename,data))

    # Salva l'immagine del barcode
    fullname = ean.save(filename, options)
    
    return fullname

def wlog(msg:str,create=False):
    global fpath
    #file_dir = os.path.dirname(os.path.realpath('__file__'))
    #print(file_dir)
    logpath=resource_path(os.path.join(_path,"log.txt"))
    #print(f"APRO FILE IN {logpath}")
    if not create: 
        #print("Non creo")
        f = open(logpath, "a")
    else:
        #print("Creo")
        f = open(logpath, "w")
    f.write('\n'+str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))+'\t'+msg+'\n')
    f.close()
    
def check_lib():
    wlog("INIT")
    try:
        import barcode # type: ignore
        wlog(">>>> Barcode ok")
    except ModuleNotFoundError:
        wlog("Barcode non presente")
        install("python-barcode pillow")
    try:
        import PIL  # type: ignore
        wlog(">>>> PIL  ok")
    except ModuleNotFoundError:
        wlog("Barcode non presente")
        install("PIL ")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Data=dato da barcodizzare, path=path dove salvare,filename=nome file')
    parser.add_argument('data', type=str,
                    help='data')
    parser.add_argument('path', type=str,
                    help='path',default=os.path.join(os.environ['USERPROFILE'],"Desktop"))
    parser.add_argument('filename', type=str,nargs='?',
                    help='filename',default='BarcodeGen')
    parser.add_argument('-codifica', type=str,
                help='codifica del barcode',default='code128')
   
    args = parser.parse_args()
    data=args.data
    codifica=args.codifica

    filename=args.filename
    _path=resource_path(os.path.join(f'{args.path}',filename,data))
    _path=_path.replace("/","_")
    print(f"PATH = {_path}") 
    print(f"DATA TO BARCODIZE = {data}")
    print(f"CODIFICA ={codifica}")
    print(f"FILENAME= {filename}")

   # _path=os.path.join(os.environ['USERPROFILE'],"Desktop","barcodegenerated","img")
    if not os.path.exists(_path):
        #print("PATH NON ESISTE DEVO CREARLA")
        os.makedirs(_path)
        wlog(f"--- Version {version} ---",True) 
        wlog(f"Creo percorso: {_path}") 
    else:
        wlog(f"--- Version {version} ---",True) 
        
   
    print(f"Cambio dir in {_path}")   
    os.chdir(_path)   
    print(os.listdir())
    #print(f"QUI HO {_path}")
    
    fpath=_path
    #print(f"FPATH é {fpath}")
    #self.font_path = 'arial.ttf'
    #os.chdir(path)
    
    #check_lib() #se non da eseguibile
    
    wlog("Inizializzazione")
    print(f"DIR SAVE: {_path}")
    if codifica=='ean13' and len(data)<13:
        print("ERRORE")
        wlog("Il codice deve essere >= di 13 caratteri per il formato ean13")
        sys.exit()
    else:    
        filepath = create_barcode(data, _path,codifica)
        print(f"Codice a barre salvato come: {filepath}")
        wlog(f"Codice a barre salvato come: {filepath}")

    #input("premi per uscire")

