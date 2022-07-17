#save_links

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
7. The saved links, which were saved under a specific name, can be inspected, deleted or opened.

## Installation
Download / make a local copy of save_links.py.

Download the following dependencies:

```python
import pyautogui, pyperclip
```
Now, the script can be executed from cmd using: 

```
py C:<path_to_script>\save_links.py <save/delete/etc> link_group_name
```

In addition, a faster way of running the script without typing the whole path is to:

### Create a .bat file and adding folder to PATH system environment
1. Create a `.bat` file containing:
```bat
@py C:/Users/your_user/your_folder/save_links.py %*
@pause
```
2. In environment variables, edit Path and add `C:\Users\your_user\your_folder`
3. Now, the script can be executed from the run dialog (win + r) or cmd by only typing `save_links <save/delete/etc> 
link_group_name`.

## Setup


```cmd

```
## Use

## Project Glossary

## Future Enhancement


