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

Depois que rodar o sistema o link para acessar a página de pesquisa é:

#### `http://127.0.0.1:8000/textmining/`

Por padrão o DJANGO trabalha na porta 8000.

Acessando o link, será exibita a seguint página:
![Tela inicial do arbominer](https://github.com/arbominer/static/image/arbominer_inicial.png)

Um dos parâmetros de pesquisa da ferramente é o vírus que permitirá a pesquisa em um dois arbovírus, sendo eles a Dengue, Zika e Chikungunya. Porém o vírus da dengue pode ser pesquisado através de seus sorotipos 1, 2, 3 e 4.

O segundo parâmetro é o tipo de análise que deverá ser feita nos artigos que estão armazenados no repositório, existem apenas dois tipos de análise sendo elas a análise estatística e análise semântica.
A análise estatística permite retornar quantos termos pesquisados existem no artigo, como pode ver na imagem a seguir. 
![Tela de resultado da análise estatística](https://github.com/arbominer/static/image/arbominer_analise_estatistica.png)

Já a análise semântica iirá retornar frases que tenham alguma algum dos termos pesquisados em seu escopo, como pode-se ver na imagem a seguir
![Tela de resultado da análise semântica](https://github.com/arbominer/static/image/arbominer_analise_semantica.png)

O terceiro parâmetro da pesquisa é um campo para adicionar tags que irá aceitar apenas palavras, caso não seja informado nenhuma palavra para a pesquisa a ferramenta irá fazer a pesquisa com algumas palavras previamente definida em seu código.

Os resultados da pesquisa é armazenado em uma tabela com 4 colunas, elas permitiram observar que tipo de virus foi pesquisado, o nome do arquivo (caso clicar no nome, o arquivo será aberto para análise manual), o link do arquivo para o pubmed e os resultados retornados da pesquisa estatística ou semântica.