## [Cloning HeartstopperTimer to your local directory][100]
Navigate to where you want to clone HeartstopperTimer. Note that cloning *will* create a "HeartstopperTimer" folder itself.

```
$ git clone https://github.com/syntaxvoid/HeartstopperTimer.git
```

## [Using the application][101]
Open a command prompt with administrator access and navigate to HeartstopperTimer. Then run
```
python HeartstopperTimer.py
```
A GUI window should open up. Now you can get started! If it doesn't work right away, check out the troubleshooting section below.

__**or just click the `HeartstopperTimer.exe` executable :D**__


---
---
---

# [Contributing your own code][103]
If you want to make your own contributions, clone the repo to your profile, make some changes, then submit a pull request.


## [Building into a .EXE][999]

Make sure you have pyinstaller installed. Type `pyinstaller` in any command prompt; if you see a help message then it's installed. If you need to install pyinstaller, run
```
$ pip install pyinstaller
```

Then change directory to wherever main.py is located and run the included **`ToExe.bat`** batch file.
```
$ cd HeartstopperTimer
$ ToExe.bat
```
Say yes to any prompts, but the only one might be asking if you want to overwrite the data in `dist\main`. 

Now run `HeartstopperTimer\dist\main\HeartstopperTimer.exe` and let the stoppers begin!

## [Troubleshooting][102]

<table>
  <tbody>
    <tr>
      <th align="center">Error Message</th>
      <th align="center">Solution</th>
    </tr>
    <tr>
      <td>ModuleNotFoundError: No module named PIL</td>
      <td>Run "python -m pip install pillow"</td>
    </tr>
    <tr>
      <td>ModuleNotFoundError: No module named win32gui</td>
      <td>Run "python -m pip install pypiwin32"</td>
    </tr>
    <tr>
    <td>'pyinstaller' is not recognized as an internal or external command,
operable program or batch file.</td>
    <td>Ensure you have pyinstaller installed. See build section above. If you're positive that you've installed pyinstaller and still see the error, then you'll need to find the pyinstaller script. Twp popular places for it to install to is at "C:\Users\{YOUR_USERNAME}\AppData\Roaming\Python\Python38\Scripts" and "C:\Users\{YOUR_USERNAME}\Anaconda3\Scripts\</td>
    </tr>
    <tr>
      <td>Anything else?</td>
      <td><a href="https://github.com/SyntaxVoid/HeartstopperTimer/issues/new">Submit an issue here</a>, providing as much detail as possible. </td>
    </tr>
  </tbody>
</table>


# Remember to [submit any issues][1]!


[1]: https://github.com/SyntaxVoid/HeartstopperTimer/issues/new

[100]: https://github.com/SyntaxVoid/HeartstopperTimer#cloning-heartstoppertimer-to-your-local-directory
[101]: https://github.com/SyntaxVoid/HeartstopperTimer#using-the-application
[102]: https://github.com/SyntaxVoid/HeartstopperTimer#troubleshooting
[103]: https://github.com/SyntaxVoid/HeartstopperTimer#contributing-your-own-code
[999]: https://github.com/SyntaxVoid/HeartstopperTimer#building-into-a-exe
