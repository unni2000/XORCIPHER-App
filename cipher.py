import curses
import ctypes
import string
import functools, io, itertools, os, re, sys
import platform
import timeit
#8)Have no global variables (except functions).

def compare(text,key2):
  library_path="xorcipher"
  ntv_fnct=load_cipher_lib(library_path)
  msg=(ctypes.c_int8*10)()
  key1=(ctypes.c_int8*4)()
  buf=(ctypes.c_int8*len(text))()
  msg=bytes(text.encode('cp437'))
  key1=bytes(key2.encode('cp437'))
  ntv_fnct(msg, key1, buf, len(text), len(key2))
  message=bytes(text.encode('CP437'))#byte sequence
  key=bytes(key2.encode('CP437'))#byte sequence
  cypher = cipher(message,key)
  if(bytes(buf).decode('cp437')==cypher.decode('cp437')):
    return True
  else:
    return False

#Driver Program
#run_gui(background)
#Takes the background (sometimes called stdser) object as a parameter and runs the program. It should be runnable using the curses.wrapper() function. This function should not return anything.

def run_gui(background):
  try:
    c ="h"
    #2) Initialize default text and key2 values
    text = "This is a haiku; it is not too long I think; but you may disagree"
    key2 = "But there's one sound that no one knows... What does the Fox say?"
    status = "Application started successfully."
    inputt = "input area"
    option = 0
    a=""
    b=""
    while 1:
      #1)Display welcome message and menu
      welcome = "Welcome to the XOR-Cipher App!"
      options =" [F] Read text from a local File\n  [I] Read text from user Input prompt\n  [R] Apply Rust cipher to this text\n  [P] Apply Python cipher to this text\n  [V] Verify cipher results match\n  [K] Change Key used for ciphers\n  [B] Run Benchmarks on text (100000x)\n  [Q] Quit the Application"
      curses.curs_set(0)
      curses.noecho()
      background.clear()
      background.keypad(False)
      #4)Show status message (left-aligned) on last line
      background.addstr(25,1,"Status: "+status)
      background.refresh()
      #7)Use a 25x80 (row/column) layout 
      box0 = curses.newwin(25, 80,0,0)
      box0.addstr(1,40-len(welcome)//2,welcome)
      box1 = curses.newwin(10, 40,2,20)
      box1.addstr(1,1, options)
      box2 = curses.newwin(4,76,12,2)
      #3)Show current text and key values under menu
      box2.addstr(1,1," TEXT ["+str(text)[:65].lstrip("b'").rstrip("'")+"]")
      box2.addstr(2,1," KEY  ["+key2.lstrip("b'").rstrip("'")+"]")
      
      box0.box()
      box1.box()
      box2.box()
      
      background.refresh()
      box0.refresh()
      box1.refresh()
      box2.refresh()
      
      status = "Application started successfully."
      if(text==a):
        text=b
        a=""
        option=0
        box2.refresh()  
      
      
      
      if(option in [1,2,6]):
        curses.echo()
        background.keypad(True)
        #1)Start on 18th row, 2nd column and be 6 x 78
        box3 = curses.newwin(6,78,18,1)
        #2)Display prompt, centered, on 2nd row
        box3.addstr(1,40-len(inputt)//2,inputt)
        #3)Display box, centered, under prompt, size 3x68
        box4 = curses.newwin(3,68,20,6)
        box3.box()
        box4.box()
        box3.refresh()
        box4.refresh()
        #4)Allow entry of 65 characters on one line only
        #Reading Strings from the User whenever a string is read from the user, the same dialog structure should be used (Figure 2).
        s = background.getstr(21,7,65)
        curses.noecho()
        #Terminate on entry of the ENTER / linefeed
        background.keypad(False)
        if(option == 1):
          x=str(s).lstrip("b'").rstrip("'").strip()
          if(x==""):
            text = "This is a ; it is not too long I think; but you may disagree"
            status="File load cancelled."
          else:
            try:
              #5)Trim resulting whitespace at beginning / end         
              text = str(file_open(s)).strip()
              status = "File contents loaded successfully."
            except:
              x=str(s).lstrip("b'").rstrip("'")
              status = "ERROR: COULD NOT LOAD FILE: "+x+"."
          c = "h"
          option = 0
        elif(option == 2):
          x=str(s).lstrip("b'").rstrip("'").strip()
          if(x==""):
            text = "This is a haiku; it is not too long I think; but you may disagree"
            status = "Cancelled user input of text (empty string)."
          else:
            #Trim resulting whitespace at beginning / end
            text = x.strip()
            status = "New text loaded into memory from user input."
          c = "h"
          option = 0

        elif(option == 6):
          x=str(s).lstrip("b'").rstrip("'").strip()
          if(x==""):
            key2 = "But there's one sound that no one knows... What does the Fox say?"
            status = "Cancelled user input of key (empty string)."
            background.refresh()
            background.addstr(25,1,"Status: "+status)
            background.clrtoeol()
            background.refresh()
          else:
            key2 = str(s).strip()
            status = "New key loaded into memory from user input."
        
          c = "h"
          option = 0
        
      elif(option == 7):
        box5 = curses.newwin(6,78,18,1)
        box5.addstr(1,28,"Running Benchmarks....")
        box5.box()
        box5.refresh()
        library_path="xorcipher"
        ntv_fnct=load_cipher_lib(library_path)
        msg=(ctypes.c_int8*10)()
        key1=(ctypes.c_int8*4)()
        buf=(ctypes.c_int8*len(text))()
        a = timeit.default_timer()
        background.refresh()
        status = "Applied Rust cipher."
        background.addstr(25,1,"Status: "+status)
        background.clrtoeol()
        background.refresh()
        for i in range(100000):
          msg=(ctypes.c_int8*10)()
          key1=(ctypes.c_int8*4)()
          buf=(ctypes.c_int8*len(text))()
          msg=bytes(text.encode('cp437'))
          key1=bytes(key2.encode('cp437'))
          ntv_fnct(msg, key1, buf, len(text), len(key2))
        b = timeit.default_timer()
        background.refresh()
        status = "Applied Python cipher."
        background.addstr(25,1,"Status: "+status)
        background.clrtoeol()
        background.refresh()
        for j in range(100000):
          message=bytes(text.encode('CP437'))#byte sequence
          key=bytes(key2.encode('CP437'))#byte sequence
          cypher = cipher(message,key)
        c = timeit.default_timer()
        a=b-a
        b=c-b
        background.refresh()
        box5.addstr(1,28,"Results from Benchmark")
        background.clrtoeol()
        box5.addstr(2,28,"----------------------")
        background.clrtoeol()
        background.refresh()
        time1=float("{:.3f}".format(a))
        time2=float("{:.3f}".format(b))
        box5.addstr(3,28,"Rust Cipher:   0"+str(time1).lstrip('-')+"s")
        box5.addstr(4,28,"Python Cipher: 0"+str(time2).lstrip('-')+"s")
        background.clrtoeol()
        #The status should be updated upon completion
        status = "Benchmark results displayed.     "
        background.addstr(25,1,"Status: "+status)
        background.refresh()
        box5.box()
        box5.refresh()
        #5)Detect single-character input for menu
        c = background.getch()
        status = "Application started successfully"
        c = "h"
        option=0
       
      else:
        #5)Detect single-character input for menu
        c = background.getch()
      #6)Accept upper and lowercase input variants
      if(c==ord('Q') or c==ord('q')):
        break
      elif(c==ord('F') or c==ord('f')):
        inputt = "Enter file to load below, then press [ENTER]"
        option = 1
      elif(c==ord('I') or c==ord('i')):
        inputt = "Enter new text below, then press [ENTER]"
        option = 2
      elif(c==ord('R') or c==ord('r')):
        b=text
        background.refresh()
        status = "Applied Rust cipher."
        background.addstr(25,1,"Status: "+status)
        background.clrtoeol()
        background.refresh()
        library_path="xorcipher"
        ntv_fnct=load_cipher_lib(library_path)
        msg=(ctypes.c_int8*10)()
        key1=(ctypes.c_int8*4)()
        buf=(ctypes.c_int8*len(text))()
        #7)All texted should be manipulated as CP437
        msg=bytes(text.encode('cp437'))
        key1=bytes(key2.encode('cp437'))
        ntv_fnct(msg, key1, buf, len(text), len(key2))
        ctrl_translation = str.maketrans(bytes(range(0,32)).decode("CP437"),"�☺☻♥♦♣♠•◘○◙♂♀♪♫☼►◄↕‼¶§▬↨↑↓→←∟↔▲▼")
        text = bytes(buf).decode('CP437').translate(ctrl_translation)
        a=text
      elif(c==ord('P') or c==ord('p')):
        #7)All texted should be manipulated as CP437
        b=text
        background.refresh()
        status = "Applied Python cipher."
        background.addstr(25,1,"Status: "+status)
        background.clrtoeol()
        background.refresh()
        message=bytes(text.encode('CP437'))#byte sequence
        key=bytes(key2.encode('CP437'))#byte sequence
        cypher = cipher(message,key)
        ctrl_translation = str.maketrans(bytes(range(0,32)).decode("CP437"),"�☺☻♥♦♣♠•◘○◙♂♀♪♫☼►◄↕‼¶§▬↨↑↓→←∟↔▲▼")
        text = cypher.decode('CP437').translate(ctrl_translation)
        a=text
      elif(c==ord('K') or c==ord('k')):
        inputt = "Enter new key and then press [ENTER]"
        option = 6
      elif(c==ord('B') or c==ord('b')):
        option = 7
      elif(c==ord('V') or c==ord('v')):
        ver = compare(text,key2)
        if(ver):
          background.addstr(25,1,"Status: Cipher match verified!")
          #9)The status should be updated upon completion
          status = "Cipher match verified!"
        else:
          background.addstr(25,1,"Status: Warnning: ciphers do not match!")
          #9)The status should be updated upon completion
          status = "Warnning: ciphers do not match!"
        background.refresh()
      elif(str(c)=='10'):
        #10)If an empty string is entered, this should be considered a cancellation action by the user.
        text = "This is a haiku; it is not too long I think; but you may disagree"
        key2 = "But there's one sound that no one knows... What does the Fox say?"
        option = 0
      elif(str(c) not in ["\n","h"]):
        #9)The status should be updated upon completion
        status = "ERROR: Invalid menu selection!"
        option = 0
  finally:
    curses.endwin()
    print("Thanks for using XOR-Cipher App; See you next time!")

def file_open(fname):
  file = open(fname,"r")
  content = file.read()
  file.close()
  return content

'''cipher (message, key)
Executes the Python cipher described earlier. It should accept two byte sequences and return a ciphered byte
sequence. It should not change the data stored in message or key.
'''
def cipher(message,key):
  keylen = len(key)
  ciphertext = bytearray(len(message))
  for pos, b in enumerate(message):
    operand: byte = key[pos % keylen]
    ciphertext[pos] = byte = b ^ operand
  return bytes(ciphertext)

'''load_cipher_lib(library_path)
Loads the cipher shared library at library_path, set its method parameters, and return the library object.'''  
def load_cipher_lib(library_path):
  # chooselibrary name
  lib=library_path

  # system system specific library name

  sys_lib='lib%s.so'%lib

  # try to load native library from various locations
  # (current directory, python file directory, system path...)
  ntv_lib=None
  
  path=os.path.join(os.path.curdir, sys_lib)
  try:
    ntv_lib=ctypes.CDLL(path)
    #break
  except:
    pass
  if ntv_lib is None:
    sys.stderr.write('cannot load library %s\n'%lib)
    sys.exit(1)

  # try to find native function
  fnct_name='cipher'
  ntv_fnct=None
  try:
    ntv_fnct=ntv_lib[fnct_name]
  except:
    pass
  if ntv_fnct is None:
    sys.stderr.write('cannot find function %s in library %s\n'%
                    (fnct_name, lib))
    sys.exit(1)

  # function prototype
  ntv_fnct.restype=None # no return value
  ntv_fnct.argtypes=[ctypes.c_void_p, # msg
                    ctypes.c_void_p, # key
                    ctypes.c_void_p, # buf
                    ctypes.c_size_t, # msg_len
                    ctypes.c_size_t] # key_len

  return ntv_fnct

#9)Run the application if invoked directly – and only run the application when so invoked.
curses.wrapper(run_gui)