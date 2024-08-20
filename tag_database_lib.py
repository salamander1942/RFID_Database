import os
import pickle
import time

class Tag:
    def __init__(self, UID, name, last_scan_time,extra=None):
        self.UID = UID
        self.name = name
        self.last_scan_time = last_scan_time
        self.extra = extra if extra is not None else {}

    def to_dict(self):
        return {
            'UID': self.UID,
            'name': self.name,
            'last_scan_time': self.last_scan_time,
            'extra': self.extra
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['UID'],
            data['name'],
            data['last_scan_time'],
            data.get('extra', {})
        )

class TagDatabase:
    def __init__(self, filename='/home/fraser/TagData.txt'):
        self.filename = filename
        self.tags = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'rb') as f:
                    self.tags = pickle.load(f)
            except EOFError:
                print()
                print('----')
                print("File is empty. Starting with an empty database.")
                self.tags = {}
            except pickle.UnpicklingError:
                print()
                print('----')
                print("Error unpickling file. Starting with an empty database.")
                self.tags = {}
            except Exception as e:
                print()
                print('----')
                print(f"An error occurred while loading data: {e}")
                self.tags = {}
            

    def save_data(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.tags, f)


    def add_or_update_tag(self, tag_UID):
        if tag_UID in self.tags:
            print()
            print('----')
            print(f"Tag {tag_UID} already exists.")
        else:
            print()
            print('----')
            print(f"Adding new tag: {tag_UID}")
            # Create a default Tag object with minimal data
            tag = Tag(tag_UID, name='', last_scan_time='',extra={})
            self.tags[tag_UID] = tag.to_dict()
            self.save_data()

   
    def append_tag(self, tag_UID, mode, *args, **kawrgs):
        if tag_UID in self.tags:
            tag_data = self.get_tag(tag_UID)
        
            if mode == 1:
            # Change the tag's name
                tag_data['name'] = args[0]
            
            elif mode == 2:
                for key, value in kawrgs.items():
                    tag_data['extra'][key] = value
            
            elif mode == 3:
            # Replace 'extra' with a new list
                tag_data['extra'] = {}
                for key, value in kawrgs.items():
                    tag_data['extra'][key] = value
                    self.save_data()
                
            elif mode == 4:
            # Remove an item from the "extra" list
                if args and args[0] in tag_data['extra']:
                    del tag_data['extra'][args[0]]
                else:
                    print()
                    print('----')
                    print("Error: Item to remove not found in 'extra'.")
            
            else:
                print()
                print('----')
                print('Invalid mode. Modes are:')
                print('1: Change the tag name')
                print('2: Add to the "extra" list')
                print('3: Replace the "extra" list')
                print('4: remove item from the "extra" list extra, item')
        # Save the updated data
    
        else:
            print('Invalid tag UID')
        self.save_data()


    def get_tag(self, tag_UID):
        return self.tags.get(tag_UID, None)

    def display_tag_info(self, tag_UID):
        tag_data = self.get_tag(tag_UID)
        if tag_data:
            print(f"Tag ID: {tag_data['UID']}")
            print(f"Tag Name: {tag_data['name']}")
            print(f"Last Scanned: {tag_data['last_scan_time']}")
            print(f"Extra Information: {tag_data.get('extra', 'None')}")
            return True
        else:
            print(f"Tag with ID {tag_UID} not found.")
            return False

    def list_all_tags(self):
        if self.tags:
            for tag_UID, tag_data in self.tags.items():
                print()
                print('-'*10)
                print()
                print(f"Tag ID: {tag_UID}")
                print(f"Tag Name: {tag_data['name']}")
                print(f"Last Scanned: {tag_data['last_scan_time']}")
                print(f"Extra Information: {tag_data.get('extra', 'None')}")
        else:
            print()
            print('-'*10)
            print()
            print('No tags found')

    def delete_tag(self, tag_UID):
        print()
        print('-'*10)
        print()
        if tag_UID in self.tags:
            del self.tags[tag_UID]
            self.save_data()
            print(f"Tag with ID {tag_UID} has been deleted.")
        else:
            print(f"Tag with ID {tag_UID} not found.")
            
    def update_time(self, tag_UID):
        if tag_UID in self.tags:
            tag_data = self.get_tag(tag_UID)
            tag_data['last_scan_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            self.save_data()
        else:
            print('Tag not found')
            
    def is_valid_uid(self,UID):
        if len(UID) != 10:
            return False  
        try:
            int(UID,16)
            return True
        except ValueError:
            return False
            

if __name__ == '__main__':
    db = TagDatabase()
    db.add_or_update_tag('cc82c321ac')
    db.list_all_tags()
    x = 'cc82c321ac'
    db.update_time(x)
    db.list_all_tags()
    db.update_time('cc82c321ac')
    db.list_all_tags()


            
        




    

            
        
