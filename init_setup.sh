echo [$(date)]: "START"
echo [$(date)]: "creating env with python version 3.8"
conda create --prefix ./NLP-SQLenv python==3.8 -y
echo [$(date)]: "activating the environment"
source activate ./NLP-SQLenv
echo [$(date)]: "installing the dev requirements"
pip install -r requirements.txt
echo [$(date)]: "NOW RUNNIG app.py"
python app.py
echo [$(date)]: "ALL COMMANDS COMPLETED!!!"