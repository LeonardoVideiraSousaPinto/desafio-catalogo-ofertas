Guia de Execução do Projeto
Bem-vindo(a)! Este README fornece um passo a passo para testar o projeto localmente.

Requisitos
	Docker versão 27.4.0 ou superior
	Python versão 3.12.6 ou superior

Passo 1: Subir o Docker com Docker Compose
	Abra o PowerShell.
	Navegue até o diretório onde o arquivo docker-compose.yml está salvo:
		cd 'C:\caminho\para\seu\diretorio\Docker SQL Server'
	Execute o comando para subir os containers:
		docker-compose up -d

Passo 2: Instalar o virtualenv
	No PowerShell, execute o seguinte comando para instalar o virtualenv:
		pip install virtualenv

Passo 3: Criar um Ambiente Virtual
	Crie o ambiente virtual com o comando:
		python -m venv .venv

Passo 4: Ativar o Ambiente Virtual e Instalar Dependências
	Ative o ambiente virtual com:
		.venv\Scripts\Activate
	Instale as dependências necessárias do projeto com:
		pip install -r C:\caminho\para\seu\diretorio\requirements.txt

Passo 5: Executar o Robô de Scraping
	Navegue até o diretório onde o script do robô de scraping está localizado:
		cd 'C:\caminho\para\seu\diretorio\Robo Scraper'
	Execute o robô de scraping com:
		python scraper.py

Passo 6: Subir a Aplicação Django
	Navegue até o diretório do projeto Django:
		cd 'C:\caminho\para\seu\diretorio\DjangoApp'
	Execute o servidor Django com:
		python manage.py runserver

Passo 7: Acesse o Site
	Abra o navegador e acesse o site através do seguinte link:
		http://127.0.0.1:8000/