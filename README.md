# Arbominer
O arbominer é uma ferramenta desenvolvida em Python como proposta de trabalho de conclusão de curso (TCC) que tem como objetivo extrair informações clínicas, epidemiológicas e genética das arboviroses dengue, zika e chikungunya. A ferramenta tem o intuito de facilitar a extração de informações em um grande volume de artigos ciêntificos, possibilitando que pesquisadores consigam extrair e analisar um maior número de informações em um menor tempo.

# Requisitos

#### Python 3.7: https://www.python.org/downloads/release/python-377/
#### DJANGO: (https://www.djangoproject.com/)
#### NLTK: (https://www.nltk.org/)
#### Textract: (https://textract.readthedocs.io/en/stable/)

# Instalação
Após a instalção do python coloque-o na variável de ambiente do seu sistema, em seguida inicie a instalação de algumas bibliotecas.

A primeira é o DJANGO, pois a ferramenta foi construida para ser WEB e ser de facil acesso aos usuários e por esse motivo foi adotado o framework DJANGO. A sua instalação é via terminal e para faze-lá é necessário rodar o seguinte comando:

#### `pip install django`

Para a leitura e conversão dos PDFs em texto foi utilizado a biblioteca textract. Para a sua instação, rode o seguinte comando: 

#### `pip install textract`

Para toda a parte de extração de informação foi utilizado a biblioteca NTLK que consiste em ser uma biblioteca para processamento de linguagem natural. Para sua instalação é necessário apenas rodar o commando: 

#### `pip install nltk`

# Run

Para rodar o projeto é necessário apenas está na pasta raiz do projeto e rodar o comando:
#### `python manage.py runserver`

