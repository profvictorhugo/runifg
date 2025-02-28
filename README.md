# 🏃‍♂️ RunIFG - Sistema de Controle de Corridas de Rua 🏃‍♀️

___________

## 📌 Sobre o Projeto  

O **RunIFG** é um sistema web desenvolvido para o gerenciamento de corridas de rua promovidas pelo **Instituto Federal de Goiás (IFG) - Campus Inhumas**. O sistema permite o cadastro de eventos, inscrições de participantes, acompanhamento de resultados e emissão de certificados.  

---

## 🚀 Funcionalidades  

✅ Cadastro de corridas e eventos esportivos  
✅ Inscrição online de participantes  
✅ Gerenciamento de categorias e faixas etárias  
✅ Controle de resultados e classificação  

---

## 🛠️ Tecnologias Utilizadas  

🔹 **Front-end**: *HTML + CSS + Javascript*  
🔹 **Back-end**: *Python + Flask*  
🔹 **Banco de Dados**: *MySQL*  

---

## 📥 Como Instalar e Executar  

1️⃣ Clone este repositório:  
```bash
git clone https://github.com/profvictorhugo/RunIFG.git
```
### Configuração do Ambiente Virtual e Variáveis de Ambiente  

Para garantir um ambiente isolado e organizado para o desenvolvimento do projeto, utilizamos um ambiente virtual (`venv`) e um arquivo de variáveis de ambiente (`.env`).  

#### 1. Criando o Ambiente Virtual  

1. Certifique-se de ter o **Python** instalado no seu sistema.  
2. No terminal ou prompt de comando, navegue até o diretório do projeto:  
   ```sh
   cd /caminho/do/projeto
   ```  
3. Crie um ambiente virtual executando:  
   ```sh
   python -m venv venv
   ```  
   Isso criará uma pasta chamada `venv`, onde serão armazenadas as dependências do projeto.  

4. Ative o ambiente virtual de acordo com o seu sistema operacional:  
   - **Windows (Prompt de Comando)**:  
     ```sh
     venv\Scripts\activate
     ```
   - **Windows (PowerShell)**:  
     ```sh
     venv\Scripts\Activate.ps1
     ```
   - **MacOS/Linux**:  
     ```sh
     source venv/bin/activate
     ```

   Quando ativado, o nome do ambiente (`venv`) será exibido no início da linha de comando.  

#### 2. Instalando as Dependências  

Com o ambiente virtual ativo, instale as dependências do projeto usando:  
```sh
pip install -r requirements.txt
```  

Para verificar se todas as dependências foram instaladas corretamente, utilize:  
```sh
pip list
```  

#### 3. Criando o Arquivo `.env`  

Para armazenar configurações sensíveis e garantir a correta configuração do projeto, é necessário criar um arquivo `.env` na raiz do projeto. Esse arquivo deve conter as seguintes variáveis:  

```ini
MYSQL_HOST=
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_DB=
SECRET_KEY=
FLASK_ENV=
FLASK_RUN_HOST=
FLASK_RUN_PORT=
```

**Descrição das variáveis:**  
- **`MYSQL_HOST`**: Endereço do banco de dados MySQL.  
- **`MYSQL_USER`**: Usuário do MySQL.  
- **`MYSQL_PASSWORD`**: Senha do usuário MySQL (caso haja).  
- **`MYSQL_DB`**: Nome do banco de dados utilizado.  
- **`SECRET_KEY`**: Chave secreta usada para segurança em aplicações Flask.  
- **`FLASK_ENV`**: Define o ambiente do Flask (`development` para desenvolvimento).  
- **`FLASK_RUN_HOST`**: Endereço onde a aplicação será executada.  
- **`FLASK_RUN_PORT`**: Porta onde a aplicação será servida.  

> **Importante**: Esse arquivo não deve ser compartilhado publicamente ou versionado no Git por motivos de segurança.  

#### 4. Desativando o Ambiente Virtual (Opcional)  

Quando terminar de trabalhar no projeto, você pode desativar o ambiente virtual com:  

- **Windows (Prompt de Comando ou PowerShell)**:  
  ```sh
  deactivate
  ```
- **MacOS/Linux**:  
  ```sh
  deactivate
  ```

Seguindo esses passos, seu ambiente estará configurado corretamente e pronto para rodar o projeto. 🚀

---

## 📞 Contato e equipe

📧 E-mail: victor.lopes@ifg.edu.br

🌎 Site: ifg.edu.br

Desenvolvido com ❤️ pelo IFG - Campus Inhumas 🚀

#### Alunos envolvidos:

**Front-end**:
🔹Colocar nomes

**Back-end**:
🔹Bruna Borges

**Banco de Dados**:
🔹Bruna Borges
