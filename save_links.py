#! python3

# Description: script that performs 2 main actions: saves the tabs' links of an opened window in
# shelve and text documents, and opens the stored links on the default browser, by controlling
# the mouse and keyboard. The links are stored under specific names given by the user, which can
# be inspected or deleted.

# Link manager by Oscar-gg [Github]

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
    """Constructs message in case a link group name is reused.

    :param shelve_file: file containing all link group information
    :param link_group: name of link group.
    :return: String containing information of the overwritten link group.
    """
    message = "'" + link_group + "'" + " has been previously used to save links." + '\n'
    message += "The new links will be saved and the previous ones erased." + '\n' * 2
    message += "Links erased:" + '\n' * 2
    message += link_group_to_str(shelve_file, link_group)

    return message


def select_window():
    """Selects and maximizes the corresponding window.
    :return:
    """

    update_image_paths()

    if len(active_image_paths) == 0:
        print('ERROR, no plus sign identified.')
        return

    try:
        location = pyautogui.locateCenterOnScreen(IMAGE_PREFIX + '\\' + active_image_paths[0], grayscale=True)
        pyautogui.click(location.x + 15, location.y)
    except FileNotFoundError:
        print("Unexpected error at select_window() function.")
        return

    time.sleep(sleep_time())
    pyautogui.hotkey('win', 'up')
    pyautogui.hotkey('ctrl', '1')
    center_move()


def update_image_paths(region=(0, 0) + pyautogui.size()):
    """Searches for plus signs in the screen. Adds the corresponding names of the identified plus signs to a list.

    :param region: the region of the screen to search the image. (left, top, width, height)
    :return: None, updates global variable
    """
    global active_image_paths

    # grayscale: reduces execution time, but also accuracy.
    # region: reduces execution time and search area.

    for image in os.listdir(IMAGE_PREFIX):
        if image in active_image_paths:
            continue
        if pyautogui.locateOnScreen(IMAGE_PREFIX + '\\' + image, grayscale=True, region=region):
            active_image_paths.append(image)
            break


def center_move():
    """Moves the cursor to the center of the screen.
    :return:
    """
    a, b = pyautogui.size()
    pyautogui.moveTo(a // 2, b // 2)


def get_links():
    """Collects links using browser hotkeys.

    :return: Array containing tabs' links.
    """

    links = []

    update_image_paths(region_func())

    time.sleep(sleep_time())

    global active_plus_sign

    for image in active_image_paths:
        if pyautogui.locateOnScreen(IMAGE_PREFIX + '\\' + image, grayscale=True, region=region_func()):
            active_plus_sign = image  # Once the window is selected, the active plus sign can be identified.
            break

    if not active_plus_sign:
        print("Error, no active plus sign identified")
        return

    try:
        for _ in range(20):
            a = 1
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(sleep_time())
            pyautogui.hotkey('ctrl', 'c')
            links.append(pyperclip.paste())
            time.sleep(sleep_time())
            pyautogui.hotkey('ctrl', 'w')
            if pyautogui.locateOnScreen(IMAGE_PREFIX + '\\' + active_plus_sign, grayscale=True, region=region_func()):
                a = 0

            if a == 1:
                break
    except KeyboardInterrupt:
        # Exception commonly triggered because of ctrl + c hotkey.
        return links

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
    time.sleep(sleep_time())
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


def check_args(arguments):
    """Function that checks if the arguments are valid. Displays general and help information.

    :param arguments:list of arguments retrieved from command line.
    :return: None
    """
    if arguments[1] == 'help':
        help_function()
        sys.exit("Program aborted, help info displayed.\n")
    if arguments[1] == 'options':
        show_options()
        sys.exit("Program aborted, options displayed.\n")
    if arguments[1] == 'show':
        show_detailed_options()
        sys.exit("Program aborted, detailed options displayed.\n")
    if len(arguments) != 3:
        print('Error:', str(len(arguments)), 'arguments introduced.')
        sys.exit('Program aborted, incorrect amount of arguments.')
    if arguments[1] != 'save' and arguments[1] != 'append' and arguments[1] != 'open' \
            and arguments[1] != 'delete':
        print('Error:', arguments[1], 'is not a valid argument.')
        dramatic_close_message()
        sys.exit('\n\nProgram aborted.')


def exec_time(initial_time, function='function'):
    """Prints the execution time of a function.

    :param initial_time: The time in seconds since the epoch before function execution.
    :param function: the name of the function, helps for debugging and tracking specific functions.
    :return:
    """
    print('Execution time of', function + ':', time.time() - initial_time, 'seconds', '\n')


def help_function():
    """Help section that displays information related to keywords and general use.
    """
    print('Link manager by Oscar-gg\n')
    print('The purpose of this program is to store the links of an opened window in order to'
          ' open them when indicated through the arguments.')
    print('Only tested for chrome and, in case you want to save the links of a window, it should be opened'
          ' and visible.')
    print('Only works with Windows OS, and the hotkeys of the browser (ctrl #, ctrl l, ctrl w, etc) '
          'should be active')
    print('The arguments are received from the run dialog or the command line.\n')
    print("WARNING: If the terminal blocks the plus sign of the chrome window, the script won't work.")
    print('The format expected for the arguments is the following:')
    print("name.py open/save/append/options/help/show/delete link_group_name", end='\n\n')
    print('If there are more or less arguments, the program will throw an error.')
    print('The save method erases the previously stored links under the specific reused link group name.', end="\n\n")
    print("For more information check the project's github at: [...]")


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
    """Shows the available options, each with its links stored.
        :return:
    """
    shelve_file = shelve.open(SHELVE_FILE_PATH)
    for key in shelve_file.keys():
        print(link_group_to_str(shelve_file, key))
    shelve_file.close()


def link_group_to_str(shelve_file, link_group):
    """Returns string with the links saved under a specific link group name.

    :param shelve_file: file containing all link group information
    :param link_group: name of link group.
    :return: String containing individual links of a link group.
    """
    try:
        string = 'Name: ' + link_group + '\n'
        for link in shelve_file[link_group]:
            string += link + "\n"
        string += '\n'
        return string
    except TypeError:
        return "Link group to str: TypeError with link group " + link_group


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
        print('WARNING: Add images of the plus sign/identifier of your browser in ' + "Save Links\\Images.")
        print("Else, the script will not work.")


def region_func():
    """Returns the region to search the web browser icon in.

    :return: 4 integer tuple of (left, top, width, height)
    """
    width, height = pyautogui.size()
    return 0, 0, width, height/8


def sleep_time():
    """Used to modify the duration of most time.sleep() statements.

    :return: 0.2
    """
    return 0.2


# -Start of execution
# Format: name.py open/save/append/options/help/show/delete link_group_name

# Directory overview:
# 'Save Links' > 'Images' > [Image files of plus symbol of selected browser(s)]
# 'Save Links' > 'Links' > 'Shelve' > [Shelve files with links]
# 'Save Links' > 'Links' > 'Plain Text' > [Txt files with links]

setup()

argument_list = sys.argv

# Global Variables
SHELVE_FILE_PATH = r'Save Links\Links\Shelve\links_shelve'
TXT_FILE_PATH = r'Save Links\Links\Plain Text'
IMAGE_PREFIX = r'Save Links\Images'

# Usually, the plus sign has 2 tones: one when the window is active and one when it's not.
# To distinguish the inactive from the active, this variable is used.
active_plus_sign = ''

active_image_paths = []

if len(argument_list) < 2:
    sys.exit('Invalid argument list.')

check_args(argument_list)

if argument_list[1] == 'save':
    save_links(argument_list[2])
elif argument_list[1] == 'open':
    open_links(argument_list[2])
elif argument_list[1] == 'append':
    append_links(argument_list[2])
elif argument_list[1] == 'delete':
    delete_links(argument_list[2])
