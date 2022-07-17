# save_links

Save all your tabs' links under specified names and reopen them whenever you like (Currently, only for Windows OS).
Interact with this script from the command line.


## Overview
The script works by sending keystrokes to select and copy links, maximize windows, close tabs, etc. using 'pyautogui'.
The links are stored in shelve and txt files which can also be opened using the script.

## How it works
1. The script locates the browser's window using a characteristic image (e.g. the plus sign to add tabs or the close button)
2. The window is maximized.
3. The link of the first tab is selected using ctrl + L, copied using ctrl + c and saved in an array.
4. The tab is suppressed using ctrl + w.
5. The 2 previous steps are repeated until the characteristic image isn't identified.
6. The links stored in the array are saved in txt and shelve files.
7. The saved links, which were saved under a specific name, can be inspected, deleted or opened by the script.

## Installation
Download / make a local copy of save_links.py.

Download the following dependencies:

```python
import pyautogui, pyperclip
```
Now, the script can be executed from cmd using: 

```
py C:<path_to_script>\save_links.py <keyword> link_group_name
```

In addition, a faster way of running the script without typing the whole path is to:

### Create a .bat file and adding folder to PATH system environment
1. Create a `.bat` file containing:
```bat
@py C:/Users/your_user/your_folder/save_links.py %*
@pause
```
2. Name the file: `save_links.bat`.
3. In environment variables, edit Path and add `C:\Users\your_user\your_folder`
4. Now, the script can be executed from the run dialog (win + r) or cmd by only typing `save_links <keyword> 
link_group_name`.

## Setup
First, run the script without any arguments.

```cmd
save_links
```
This will create the following folders in the current working directory:
```
Directory overview:
'Save Links' > 'Images' > [Image files of plus symbol/identifier of selected browser(s)]
'Save Links' > 'Links' > 'Shelve' > [Shelve files with links]
'Save Links' > 'Links' > 'Plain Text' > [Txt files with links]
```
Now, add images of the plus sing / browser identifier to `Save links/Images`.

The images need to be of good quality (.png preferably) and the smaller they are the better. 

In addition, 2 or more images may need to be added because the identifier may have 2 tones: one
when the window is active and one when it's not. See `image_examples/` for examples.

A method of obtaining the images (of good quality) is through the use of pyautogui's [screenshot function](https://pyautogui.readthedocs.io/en/latest/screenshot.html):
```
pyautogui.screenshot('filename.png', region=(left,top, width, height))`
```

## Use
`save_links` + `keywords (e.g: save, open, show)` + `link_group_name`

### Keyword list
`help`: Displays information related to keywords and general use.

`save` + `link_group_name`: Saves links of the opened window in `link_group_name`. Closes all tabs via ctrl + w.

`open` + `link_group_name`: Opens links saved in `link_group_name` in a new window.

`append` + `link_group_name`: Appends links to `link_group_name`. Doesn't delete `link_group_name`'s past links unlike `save`.

`delete` + `link_group_name`: Deletes links saved under `link_group_name`.

`options`: displays all `link_group_name` previously saved that haven't been deleted. 

`show`: displays all `link_group_name` available, each with its associated links.

## Future Enhancement
* Improve installation and setup method
* Make the script cross-platform
  
## Contributing
I am (relatively) new to GitHub, Python, open source, and programming; this project most likely has 
several relevant mistakes. If there is something relevant that I could 
improve, please let me know as I want to keep learning; constructive feedback is appreciated :)
