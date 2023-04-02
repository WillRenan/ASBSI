# Instruções para executar um projeto Flask

## Pré-requisitos
Certifique-se de ter instalado o Python 3 e o pip em sua máquina.

## Clonando o projeto
1. Abra o terminal e navegue até o diretório em que deseja clonar o projeto.
2. Execute um dos seguintes comandos, dependendo do método de clonagem que preferir:

   - HTTPS: `git clone https://github.com/WillRenan/ASBSI.git`
   - SSH: `git clone git@github.com:WillRenan/ASBSI.git`
   
   Certifique-se de substituir `WillRenan` pelo seu nome de usuário no GitHub, se necessário.

## Configurando o ambiente virtual
1. Navegue até o diretório do projeto clonado.
2. Execute o comando `python3 -m venv .venv` para criar um ambiente virtual Python.
3. Execute o comando `source .venv/bin/activate` para ativar o ambiente virtual.
4. Execute o comando `pip install -r requirements.txt` para instalar as dependências do projeto.

## Executando o projeto
1. Certifique-se de que o ambiente virtual está ativado.
2. Execute o comando `flask run` para iniciar o servidor Flask.
3. Abra um navegador da web e acesse o endereço `http://localhost:5000` para visualizar o projeto em execução.
