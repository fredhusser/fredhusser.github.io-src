mkdir venv
virtualenv venv

cd venv/Scripts/
activate.bat
cd ..
cd ..

easy_install http://www.voidspace.org.uk/python/pycrypto-2.6.1/pycrypto-2.6.1.win32-py2.7.exe
pip install -r requirements.txt