@echo "This procedure installs the required packages of the project"
cd ..
call ./venv/Scripts/activate
pip install -r requirements
pause

