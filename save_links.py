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


def save_links(new_link_group):
    """Saves links of the opened window. Closes all tabs via ctrl + w.
    :param new_link_group: The name selected for the group of links.
    :return:
    """
    shelve_file = shelve.open(SHELVE_FILE_PATH)
    text_file = open(TXT_FILE_PATH + '\\' + new_link_group + '.txt', 'w')

    end_message = 'Links saved successfully'

    if valid_name(new_link_group):
        end_message = past_links(shelve_file, new_link_group)

    select_window()
    links = get_links()
    shelve_file[new_link_group] = links
    for link in links:
        text_file.write(link + "\n")
    shelve_file.close()
    text_file.close()

    print(end_message)


def past_links(shelve_file, link_group):
    message = "'" + link_group + "'" + " has been previously used to save links." + '\n'
    message += "The new links will be saved and the previous ones erased." + '\n' * 2
    message += "Links erased:" + '\n' * 2
    message += link_group_to_str(shelve_file, link_group)

    return message


def select_window():
    """Selects and maximizes the corresponding window.
    :return:
    """
    a = 0

    os.chdir('Save Links')

    # TODO: for loop that iterates through all images in given directory, instead of hard coding the names
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

    os.chdir('..')  # Returns to initial cwd


def center_move():
    """Moves the cursor to the center of the screen.
    :return:
    """
    a, b = pyautogui.size()
    pyautogui.moveTo(a // 2, b // 2)


def get_links():
    """Collects links using browser hotkeys.
    :return:
    """
    links = []
    os.chdir('Save Links')
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

    os.chdir('..')  # Returns to initial cwd
    return links


def open_links(link_group):
    """Opens saved links in a new window.

    :param link_group: The name of the group of links to open.
    :return:
    """
    if not valid_name(link_group):
        sys.exit("Error: Group of links doesn't exist.")

    shelve_retrieve = shelve.open(SHELVE_FILE_PATH)
    webbrowser.open(shelve_retrieve[link_group][0], new=1)
    time.sleep(0.2)
    pyautogui.hotkey('win', 'up')
    for x in range(1, len(shelve_retrieve[link_group])):
        webbrowser.open(shelve_retrieve[link_group][x])
    shelve_retrieve.close()


def valid_name(link_group_name):
    """Validates that there is data saved under the specified name.

    :param link_group_name: The name to check.
    :return: True if name found, false if not found.
    """
    shelve_retrieve = shelve.open(SHELVE_FILE_PATH)
    exists = 0

    if link_group_name in shelve_retrieve.keys():
        exists = 1

    shelve_retrieve.close()
    return exists


def append_links(link_group):
    """Appends links to previously saved file

    :param link_group: The name of the group of links to append links to.
    :return:
    """

    if not valid_name(link_group):
        sys.exit("Error: Link group doesn't exist.")

    shelve_file = shelve.open(SHELVE_FILE_PATH)
    text_file = open(TXT_FILE_PATH + '\\' + link_group + '.txt', 'a')

    temp_list = shelve_file[link_group]
    select_window()
    to_append = get_links()
    for link in to_append:
        temp_list.append(link)
        text_file.write(link + "\n")
    shelve_file[link_group] = temp_list
    shelve_file.close()
    text_file.close()


def delete_links(link_group):
    """Deletes the links saved under the specified name from the txt and shelve file.

    :param link_group: The name of the group of links to delete.
    :return:
    """
    if not valid_name(link_group):
        sys.exit("Error: Link group doesn't exist.")

    if os.path.exists(TXT_FILE_PATH + "\\" + link_group + ".txt"):
        os.remove(TXT_FILE_PATH + "\\" + link_group + ".txt")
    else:
        print("Error: txt file of specified group of links not found")

    shelve_file = shelve.open(SHELVE_FILE_PATH)

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


def show_options():
    """Shows the available options to open, delete, or append.
    :return:
    """
    shelve_file = shelve.open(SHELVE_FILE_PATH)
    print('Available options:\n')
    for key in shelve_file.keys():
        print(key)
    shelve_file.close()
    print('\n')


def show_detailed_options():
    shelve_file = shelve.open(SHELVE_FILE_PATH)
    for key in shelve_file.keys():
        print(link_group_to_str(shelve_file, key))
    shelve_file.close()


def link_group_to_str(shelve_file, link_group):
    string = 'Name: ' + link_group + '\n'
    for link in shelve_file[link_group]:
        string += link + "\n"
    string += '\n'
    return string


def dramatic_close_message():
    print('Invalid argument introduced.')
    print('Program closing in ', end='')
    for x in range(5, 0, -1):
        print(x, end=' ', flush=True)
        time.sleep(1)


def setup():
    """Creates the folders used by the program for the first time. Gives messages related to setup.
    """
    print('Your current working directory (where files are saved): ' + os.getcwd(), '\n')

    if not os.path.isdir('Save Links'):
        os.mkdir('Save Links')  # Folder that contains files used by the script.
    if not os.path.isdir('Save Links\\Images'):
        os.mkdir('Save Links\\Images')  # Folder to save images of plus signs.
    if not os.path.isdir('Save Links\\Links'):
        os.mkdir('Save Links\\Links')  # Contains the files with links.
    if not os.path.isdir('Save Links\\Links\\Shelve'):
        os.mkdir('Save Links\\Links\\Shelve')  # Shelve files with links.
    if not os.path.isdir('Save Links\\Links\\Plain Text'):
        os.mkdir('Save Links\\Links\\Plain Text')  # Plain files w/links.
    if len(os.listdir(r'Save Links\Images')) == 0:
        print('WARNING: Add images of the plus sign of your browser in ' + "Save Links\\Images. Else, the script "
                                                                           "will not work.")


# Main thread
# Format: name.py open/save/append/options/help/show/delete link_group_name

# Directory overview:
# 'Save Links' > 'Images' > [Image files of plus symbol of selected browser(s)]
# 'Save Links' > 'Links' > 'Shelve' > [Shelve files with links]
# 'Save Links' > 'Links' > 'Plain Text' > [Txt files with links]

setup()

argument_list = sys.argv

SHELVE_FILE_PATH = r'Save Links\Links\Shelve\links_shelve'

TXT_FILE_PATH = r'Save Links\Links\Plain Text'

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
