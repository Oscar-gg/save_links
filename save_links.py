#! python3

# Description: script that makes 2 main actions. First, it saves the links of the opened window in
# shelve and text documents. Then the other action is opening the stored links when asked.

# imports
import os
import pyautogui
import sys
import shelve
import pyperclip
import time
import webbrowser


# Function that saves the links of the open window.
def save_links(class_name):
    os.chdir(r'Save Links')
    shelve_file = shelve.open(r'Class Links\Shelve\Links de Clases')
    text_file = open('Class Links\\Plain Text\\' + class_name + '.txt', 'w')
    select_window()
    links = get_links()
    shelve_file[class_name] = links
    for link in links:
        text_file.write(link + "\n")
    shelve_file.close()
    text_file.close()


# Function that selects and maximizes the corresponding window.
def select_window():
    a = 0

    #TODO: for loop that iterates through all images in given directory, instead of hard coding the names
    try:

        location = pyautogui.locateCenterOnScreen(r'Images\plus.png')
        pyautogui.click(location.x + 15, location.y)
    except:
        try:
            location = pyautogui.locateCenterOnScreen(r'Images\plus2.png')
            pyautogui.click(location.x + 15, location.y)
        except:
            try:
                location = pyautogui.locateCenterOnScreen(r'Images\plus3.png')
                pyautogui.click(location.x + 15, location.y)
            except:
                try:
                    location = pyautogui.locateCenterOnScreen(r'Images\plus4.png')
                    pyautogui.click(location.x + 15, location.y)
                except:
                    print('ERROR, no plus sign identified.')
                    a = 1
    if a == 0:
        time.sleep(.2)
        pyautogui.hotkey('win', 'up')
        pyautogui.hotkey('ctrl', '1')
        center_move()


# Function that moves the mouse to the center of the screen.
def center_move():
    a, b = pyautogui.size()
    pyautogui.moveTo(a // 2, b // 2)


# Function that collects the links.
def get_links():
    links = []
    try:
        for _ in range(20):
            a = 0
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'c')
            links.append(pyperclip.paste())
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'w')
            # TODO: for loop that iterates through all images in given directory, instead of hard coding the names
            location = pyautogui.locateCenterOnScreen(r'Images\plus2.png')
            try:
                pyautogui.moveTo(location.x / 2, location.y / 2)
            except:
                try:
                    location = pyautogui.locateCenterOnScreen(r'Images\plus4.png')
                    pyautogui.moveTo(location.x / 2, location.y / 2)
                except:
                    a = 1
            center_move()
            if a == 1:
                break
            center_move()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        return links
    return links


def open_links(class_name):
    """Opens saved links in a new window.

    :param class_name: The name of the group of links to open
    :return:
    """
    if not valid_name(class_name):
        sys.exit("Error: class name doesn't exist.")

    os.chdir(r'Save Links\Class Links\Shelve')
    shelve_retrieve = shelve.open('Links de Clases')

    webbrowser.open(shelve_retrieve[class_name][0], new=1)
    time.sleep(0.2)
    pyautogui.hotkey('win', 'up')
    for x in range(1, len(shelve_retrieve[class_name])):
        webbrowser.open(shelve_retrieve[class_name][x])
    shelve_retrieve.close()


def valid_name(link_group_name):
    """Validates that data is saved under the specified name.

    :param link_group_name: The name to check.
    :return: True if name found, false if not found.
    """
    os.chdir(r'Save Links\Class Links\Shelve')
    shelve_retrieve = shelve.open('Links de Clases')
    exists = 0

    if link_group_name in list(shelve_retrieve.keys()):
        exists = 1

    shelve_retrieve.close()
    return exists


# Function that appends the links
def append_links(class_name):
    os.chdir(r'Save Links')
    shelve_file = shelve.open(r'Class Links\Shelve\Links de Clases')
    if class_name not in list(shelve_file.keys()):
        shelve_file.close()
        sys.exit("Error: class name doesn't exist.")
    text_file = open('Class Links\\Plain Text\\' + class_name + '.txt', 'a')
    temp_list = shelve_file[class_name]
    select_window()
    to_append = get_links()
    for link in to_append:
        temp_list.append(link)
        text_file.write(link + "\n")
    shelve_file[class_name] = temp_list
    shelve_file.close()
    text_file.close()


def delete_links(link_group):
    """Deletes the links saved under the specified name from the txt and shelve file.

    :param link_group: The name of the group of links to delete.
    :return:
    """

    if not valid_name(link_group):
        sys.exit("Error: class name doesn't exist.")

    if os.path.exists("Save Links\\Class Links\\Plain Text\\" + link_group + ".txt"):
        os.remove("Save Links\\Class Links\\Plain Text\\" + link_group + ".txt")
    else:
        print("Error, txt file of specified group of links not found")

    os.chdir(r'Save Links\Class Links\Shelve')

    shelve_file = shelve.open('Links de Clases')

    try:
        links_deleted = shelve_file.pop(link_group)
        print('Link group deleted successfully' + '\n')
        print('Details of deleted links:', end='\n')
        print('Name/key:', link_group, '\n')
        print('Links erased:')

        for link in links_deleted:
            print(link)
    except KeyError:
        print("Error, Key not found")
    finally:
        shelve_file.close()


def check_args(list):
    """Function that checks if the arguments are correct.

    :param list:list of arguments retrieved from command line.
    :return: status code interpreted by main thread.
    """
    if list[1] == 'help':
        return help_function()
    if list[1] == 'options':
        return 3
    if list[1] == 'show':
        return 5
    if len(list) != 3:
        print('Error:', str(len(list)), 'arguments introduced.')
        return 2
    if list[1] != 'save' and list[1] != 'append' and list[1] != 'open' \
            and list[1] != 'delete':
        print('Error:', list[1], 'is not a valid argument.')
        return 4
    return 0


# Help section that displays information related to keywords and general use.
def help_function():
    print('Program made by Oscar Arreola\n')
    print('The purpose of this program is to store the links of an opened window in order to'
          ' open them when indicated through the arguments.')
    print('Only works for chrome and, in case you want to save the links of a window, it should be opened'
          ' and visible.')
    print('The arguments are received from the run dialog or the command line.\n')
    print("WARNING: If the terminal blocks the plus sign of the chrome window, the script won't work.")
    print('The format expected for the arguments is the following:')
    print("name.py open/save/append/options/help/show/delete link_group_name", end='\n\n')
    print('If there are more or less arguments, the program will throw an error.')
    # TODO: explain what each command does.
    print('The save method erases the previous stored links.', end="\n\n")
    return 1


# Shows the available options to open or delete.
def show_options():
    os.chdir(r'Save Links\Class Links\Shelve')
    shelve_file = shelve.open('Links de Clases')
    print('Available options:\n')
    for key in list(shelve_file.keys()):
        print(key)
    shelve_file.close()
    print('\n')
    return 0


def show_detailed_options():
    os.chdir(r'Save Links\Class Links\Shelve')
    shelve_file = shelve.open('Links de Clases')
    for key in list(shelve_file.keys()):
        print('Clase:', key)
        for link in shelve_file[key]:
            print(link)
        print('\n')
    shelve_file.close()


def dramatic_close_message():
    print('Invalid argument introduced.')
    print('Program closing in ', end='')
    for x in range(5, 0, -1):
        print(x, end=' ', flush=True)
        time.sleep(1)


def setup():
    """Creates the folders used by the program for the first time.

    """
    if not os.path.isdir('Save Links'):
        os.mkdir('Save Links')  # Folder that contains files used by the script.
    if not os.path.isdir('Save Links\\Images'):
        os.mkdir('Save Links\\Images')  # Folder to save images of plus signs.
    if not os.path.isdir('Save Links\\Class Links'):
        os.mkdir('Save Links\\Class Links')  # Contains the files with links.
    if not os.path.isdir('Save Links\\Class Links\\Shelve'):
        os.mkdir('Save Links\\Class Links\\Shelve')  # Shelve files with links.
    if not os.path.isdir('Save Links\\Class Links\\Plain Text'):
        os.mkdir('Save Links\\Class Links\\Plain Text')  # Plain files w/links.


# Main thread
# Format: name.py open/save/append/options/help/show/delete className
setup()

argument_list = sys.argv

if len(argument_list) < 2:
    sys.exit('Invalid argument list.')

status = check_args(argument_list)

if status == 1:
    sys.exit("Program aborted, help info displayed.\n")
elif status == 2:
    sys.exit('Program aborted, incorrect amount of arguments.')
elif status == 3:
    show_options()
    sys.exit("Program aborted, options displayed.\n")
elif status == 5:
    show_detailed_options()
    sys.exit("Program aborted, detailed options displayed.\n")
elif status == 4:
    dramatic_close_message()
    sys.exit('\n\nProgram aborted.')

if argument_list[1] == 'save':
    save_links(argument_list[2])
elif argument_list[1] == 'open':
    open_links(argument_list[2])
elif argument_list[1] == 'append':
    append_links(argument_list[2])
elif argument_list[1] == 'delete':
    delete_links(argument_list[2])
