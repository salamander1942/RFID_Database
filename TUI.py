from tag_database_lib import Tag, TagDatabase  # Import your Tag and TagDatabase classes
import RPi.GPIO as GPIO
from mfrc522 import MFRC522

GPIO.setmode(GPIO.BCM)
mfrc522 = MFRC522()

class TUI_RFID():
    #scan for rfid tags
    
    def scan():
        while True:
            status, tag_type = mfrc522.MFRC522_Request(mfrc522.PICC_REQIDL)
            if status == mfrc522.MI_OK:
                print()
                print('----')
                print()
                print("Card detected!")

                # Get the UID of the card
                status, uid = mfrc522.MFRC522_Anticoll()
            
                if status == mfrc522.MI_OK:
                    print("UID: {}".format(uid))
                
                    # Print UID in hexadecimal format
                    uid_str = ''.join([hex(byte)[2:].zfill(2) for byte in uid])
                    print("UID in Hex: {}".format(uid_str)) 
                    db.update_time(uid_str)
                    return uid_str;break
            else:
                # No card detected
               pass
    
  
if __name__=='__main__':
    
    def extra_dic_add(UID,mode):
        dic = {}
        print()
        n = int(input("How many items do you want to add to the dictionary? "))
        
        
        for _ in range(n):
            print('\n'+'-'*10+'\n')
            keys = input("Enter key: ")
            value = input("Enter value: ")
            dic[keys] = value
        db.append_tag(UID, mode,**dic)
        
    def extra_dic_remove(UID,mode):
        print('\n'+'-'*10+'\n')
        e = input('enter the item to be removed')
        db.append_tag(UID,mode,e)
        
    print('\n'+'-'*10+'\n')
    print('would you like to load a seperate database y/n')
    i = input()
    if i ==('yes' or 'y'):
        j = input("input filepath")
        db = TagDatabase(j)

    else:
        db = TagDatabase()
    db.load_data()

    while True:
        print('\n'+'-'*10+'\n')

        a = input('Would you like to scan for RFID tags? yes or no')
    
        if a ==('yes' or 'y'):
            c = TUI_RFID.scan()
            if db.display_tag_info(c) == True:
                print()
                print('-'*10)
                print()
                print('If you would like to edit this tag enter 1')
                print('if you would like to delete this tag enter 2')
                print('if you would like to do nothing to this tag enter anything else')
                b = input()
                
                if b == '1':
                    print()
                    print('----------')
                    print()
                    print('1: Change the tag name')
                    print('2: Add to the "extra" list')
                    print('3: Replace the "extra" list')
                    print('4: remove item from the "extra" list extra, item')
                    print()
                    d = int(input())
                    
                    if d == 2 or 3:
                        extra_dic_add(c,d)

                    if d == 4:
                        extra_dic_remove(c,d)
                    
                elif b == '2':
                    db.delete_tag(c)
                    print('\n'+'-'*10,+'\n')
                    print('deleted tag')
                    
                else:
                    print()
                    print('----------')
                    print()
                    print('did nothing')
                    pass
                
            else:
                print()
                print('----------')
                print()
                print('if you would like to add this tag to the database enter 1')
                print('if you do not want to add this tag enter anything else')
                
                d = input()
                
                if d == '1':
                    db.add_or_update_tag(c)
                    print()
                    print('----------')
                    print()
                    print('added tag')
                else:
                    print()
                    print('----------')
                    print()
                    print('did not add tag')
                    pass
        else:
            print()
            print('-'*10)
            print()
            print('if you would like to list database enter 1')
            print('if you would like to add a new tag enter 2')
            print('if you would like to delete a tag enter 3')
            
            e = int(input())
            
            if e == 1:
                db.list_all_tags()        
            elif e == 2:
                print('\n'+'-'*10+'\n')
                print('enter a tag UID')
                f = input()
                if db.is_valid_uid(f) == True:
                    db.add_or_update_tag(f)
                    print('\n'+'-'*10+'\n')
                    print('what would you like to name your tag? (if no input skips this step')
                    g = input()
                    if g != None:
                        db.append_tag(f,1,g)
                    print('\n','-'*10,'\n')
                    print('would you like to add anything extra to your tag? yes/no')
                    h = input()
                    if h == 'yes' or 'y':
                        extra_dic_add(f,2)
                        print('/n'+'-'*10+'\n')
                        print('added extra')
                    
                else:
                    print('\n'+'-'*10+'\n')
                    print(f"{f} is not a valid tag UID")
            elif e == 3:
                print('\n'+'-'*10,'\n')
                print('enter UID to be deleted')
                f = input()
                if db.is_valid_uid(f) == True:
                    db.delete_tag(f)
                    print('\n'+'-'*10,+'\n')
                    print('deleted tag')
                else:
                    print('\n'+'-'*10,+'\n')
                    print(f"{f} is not a valid tag")

            else:
                print(f"{e} is not a valid character")

            
                    
