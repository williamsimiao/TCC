# Uma aplicação para perguntas e respostas no domínio de Inteligência Computacional
## Usage
* Clone the project
* Obtein an telegram token follwing (theses steps)[https://core.telegram.org/bots#4-how-are-bots-different-from-humans] 
* Crie um arquivo 'config.ini' na pasta 'bot' e adicione seu token
```
[DEFAULT]
token={SEUTOKENGIGANTEAQUI}
```
* conda create -n YOURENV python=3.6 anaconda
* source activate TELEGRAM
* pip install python-telegram-bot==10.1.0
* pip install allennlp
* cd question_answering
* wget "https://s3-us-west-2.amazonaws.com/allennlp/models/bidaf-model-2017.09.15-charpad.tar.gz"
* wget "https://s3-us-west-2.amazonaws.com/allennlp/models/ner-model-2018.04.26.tar.gz"
* cd ..
* python bot/bot.py
* Make a question about the domain of Computacional Inteligence
