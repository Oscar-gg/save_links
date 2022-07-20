# save_links

Save all your tabs' links under specified names and reopen them whenever you like (Currently, only for Windows OS).
Interact with this script from the command line.


## Overview
The script works by sending keystrokes to select and copy links, maximize windows, close tabs, etc. using 'pyautogui'.
The links are stored in shelve and txt files and can be opened in the default browser using the script.

https://user-images.githubusercontent.com/77394565/180081834-2951134c-99a2-4a5b-846e-56e4b3fbff6a.mp4

## How it works
1. The script locates the browser's window using a characteristic image (e.g. the plus sign to add tabs or the close button)
2. The window is maximized.
3. The link of the first tab is selected using ctrl + L, copied using ctrl + c and saved in an array.
4. The tab is suppressed using ctrl + w.
5. The 2 previous steps are repeated until the characteristic image isn't identified.
6. The links stored in the array are saved in txt and shelve files.
7. The saved links, which were saved under a specific name, can be inspected, deleted or opened by the script.

## Installation
Download / make a local copy of `save_links.py`.

Download the following dependencies:

* pyautogui 
* pyperclip

Now, the script can be executed from cmd using: 

```
py C:<path_to_script>\save_links.py <keyword> link_group_name
```
https://user-images.githubusercontent.com/77394565/180082098-bd8a3e4a-70e2-47a7-94db-26af5244cdf4.mp4

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

https://user-images.githubusercontent.com/77394565/180082944-69503f9c-06cf-4169-a5be-b5d10e8f136c.mp4

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
Now, add images of the plus sign / browser identifier to `Save links/Images`.

The images need to be of good quality (.png preferably) and the smaller they are the better. 

In addition, 2 or more images may need to be added because the identifier may have 2 tones: one
when the window is active and one when it's not. See `image_examples/` for examples.

https://user-images.githubusercontent.com/77394565/180083007-b8d4e934-b9e2-4a44-946a-dc944a78f860.mp4

A method of obtaining the images (of good quality) is through the use of pyautogui's [screenshot function](https://pyautogui.readthedocs.io/en/latest/screenshot.html):
```
pyautogui.screenshot('filename.png', region=(left,top, width, height))`
```

## Use
`save_links` + `keywords (e.g: save, open, show)` + `link_group_name`

### Keyword list
`help`: Displays information related to keywords and general use.

`save` + `link_group_name`: Saves links of the opened window in `link_group_name`. Closes all tabs via ctrl + w.

https://user-images.githubusercontent.com/77394565/180082214-4b661151-c6d4-4863-ab9b-5e5b8092e6b1.mp4

`open` + `link_group_name`: Opens links saved in `link_group_name` in a new window.

https://user-images.githubusercontent.com/77394565/180082300-c6667859-94f2-4d0c-baba-160ab08b1237.mp4

`append` + `link_group_name`: Appends links to `link_group_name`. Doesn't delete `link_group_name`'s past links unlike `save`.

https://user-images.githubusercontent.com/77394565/180082386-2b131071-638b-4cd4-9bd6-fdb7a56d924e.mp4

`delete` + `link_group_name`: Deletes links saved under `link_group_name`.

https://user-images.githubusercontent.com/77394565/180082439-8290cbf0-304c-4db5-aeca-ae17ca59b65c.mp4

`options`: displays all `link_group_name` previously saved that haven't been deleted. 

`show`: displays all `link_group_name` available, each with its associated links.

https://user-images.githubusercontent.com/77394565/180082581-c4913aa4-6c1f-4668-8fc4-2993b884125c.mp4

## Future Enhancement
* Improve installation and setup method
* Make the script cross-platform
  
## Contributing
I am (relatively) new to GitHub, Python, open source, and programming; this project most likely has 
several relevant mistakes. If there is something relevant that I could 
improve, please let me know as I want to keep learning; constructive feedback is appreciated :)
