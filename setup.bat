@echo off
echo upgrade pip .......
python -m pip install --upgrade pip > nul
echo done
echo(
echo Install Virtualenv Lib.......
pip install virtualenv > nul
echo done
echo(
echo Create .env.......
python -m venv .env > nul
echo done
echo(
echo Activate .env.......
call .env\Scripts\activate > nul
echo done
echo(
echo upgrade pip .env.......
python -m pip install --upgrade pip > nul
echo done
echo(
echo Install requirements.txt in .env.......
pip install -r requirements.txt > nul
echo done
echo(
echo create shortucut.......
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%cd%\Multipole.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%cd%\run.bat" >> CreateShortcut.vbs
echo oLink.WorkingDirectory  = "%cd%" >> CreateShortcut.vbs
echo oLink.IconLocation = "%cd%\icon.ico" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs  
cscript CreateShortcut.vbs > nul
del CreateShortcut.vbs > nul
echo done
echo(
echo Hit any key to exit....
pause>nul
Exit /b