# 📚 BookWise Backend API

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-FCA121?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

## 🌟 Sobre o Projeto

**BookWise Backend** é uma API REST robusta e escalável desenvolvida para gerenciar uma plataforma de e-commerce de livros. Este projeto oferece funcionalidades completas para autenticação de usuários, gerenciamento de catálogo de livros, processamento de compras e muito mais.

### 🔗 Frontend Repository

Este projeto funciona em conjunto com o **BookWise Frontend**:
- 🎨 **Frontend Repository**: [bookwise-frontend](https://github.com/mantovaniandre/bookwise-frontend)
- 🚀 **Tecnologias Frontend**: Angular, TypeScript

## ⚡ Principais Funcionalidades

- 🔐 **Autenticação JWT**: Sistema seguro de login e registro
- 📚 **Gerenciamento de Livros**: CRUD completo para catálogo de livros
- 👤 **Perfis de Usuário**: Criação e edição de perfis
- 🛒 **Sistema de Compras**: Processamento de pedidos e histórico
- 🔍 **Busca Avançada**: Pesquisa por título, autor, categoria
- 💳 **Processamento de Pagamento**: Integração com cartões de crédito
- 📝 **Sistema de Comentários**: Avaliações e reviews de livros

## 🛠 Tecnologias Utilizadas

- **Framework**: Flask (Python)
- **Autenticação**: Flask-JWT-Extended
- **Banco de Dados**: MySQL com SQLAlchemy ORM
- **Criptografia**: Bcrypt para hash de senhas
- **CORS**: Flask-CORS para requisições cross-origin
- **Timezone**: PyTZ para manipulação de fusos horários

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- Python 3.8+
- MySQL 5.7+ ou MySQL 8.0+
- pip (gerenciador de pacotes Python)

## 🚀 Instalação e Configuração

### 1. Clone o repositório
```bash
git clone https://github.com/mantovaniandre/bookwise-backend.git
cd bookwise-backend/bookwise-backend
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r app/requirements.txt
```

### 4. Configure o banco de dados
```sql
-- Conecte-se ao MySQL e crie o banco de dados
CREATE DATABASE bookwise;
```

### 5. Configure as variáveis de ambiente
Edite o arquivo `app/configuration/database.py` com suas credenciais:

```python
# Exemplo de configuração do banco de dados
DATABASE_URL = "mysql+pymysql://username:password@localhost/bookwise"
```

### 6. Execute a aplicação
```bash
cd app
python main.py
```

A API estará disponível em: `http://localhost:5000`

## 📚 Documentação da API

### Autenticação
- `POST /login` - Login do usuário

### Usuários
- `POST /createUser` - Criar novo usuário
- `PUT /updateUser` - Atualizar perfil (requer autenticação)
- `DELETE /deleteUser` - Deletar usuário (requer autenticação)
- `GET /profileUser` - Obter perfil do usuário (requer autenticação)

### Livros
- `GET /getAllBooks` - Listar todos os livros
- `GET /getBookById/<id>` - Obter livro por ID
- `PUT /createBook` - Criar novo livro (requer autenticação)
- `PUT /updateBookById/<id>` - Atualizar livro (requer autenticação)
- `DELETE /deleteBookById/<id>` - Deletar livro (requer autenticação)
- `GET /searchBooks?option=<option>&term=<term>` - Buscar livros

### Compras
- `POST /createPurchase` - Processar compra (requer autenticação)
- `GET /getPurchase` - Histórico de compras (requer autenticação)

### Exemplo de Requisição

```bash
# Login
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Obter todos os livros
curl -X GET http://localhost:5000/getAllBooks
```

## 🏗 Arquitetura do Projeto

```
app/
├── configuration/          # Configurações da aplicação
│   ├── database.py        # Configuração do banco de dados
│   └── secret_key.py      # Chaves secretas JWT
├── controller/            # Controllers/Routes
│   ├── book.py           # Rotas de livros
│   ├── login.py          # Rota de autenticação
│   ├── purchase.py       # Rotas de compras
│   └── user.py           # Rotas de usuários
├── model/                # Modelos do banco de dados
│   ├── book.py
│   ├── user.py
│   ├── purchase.py
│   └── ...
├── service/              # Lógica de negócios
├── util/                 # Utilitários e responses
├── migration/            # Migrações e dados iniciais
└── main.py              # Ponto de entrada da aplicação
```

## 🧪 Testando a API

### Usando curl
```bash
# Teste básico de conectividade
curl http://localhost:5000/getAllBooks

# Criar usuário
curl -X POST http://localhost:5000/createUser \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao@example.com",
    "password": "123456"
  }'
```

### Usando Postman
1. Importe a coleção de endpoints
2. Configure o ambiente com `baseUrl = http://localhost:5000`
3. Teste os endpoints conforme a documentação

## 🔒 Segurança

- ✅ Autenticação JWT
- ✅ Hash de senhas com Bcrypt
- ✅ Validação de entrada
- ✅ CORS configurado
- ✅ Sanitização de dados

## 🚀 Deploy

### Usando Docker (Recomendado)
```dockerfile
# Exemplo de Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY app/requirements.txt .
RUN pip install -r requirements.txt

COPY app/ .
EXPOSE 5000

CMD ["python", "main.py"]
```

### Deploy em Produção
1. Configure variáveis de ambiente
2. Use um servidor WSGI (Gunicorn)
3. Configure proxy reverso (Nginx)
4. Implemente SSL/HTTPS

## 🤝 Contribuindo

1. Faça o fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Contato

**André Mantovani** - Desenvolvedor Full Stack

- 💼 [LinkedIn](https://linkedin.com/in/mantovaniandre)
- 📧 Email: andreluizdiasmantovani@gmail.com
- 🌐 Site: https://amantovani.netlify.app/
- 🐙 GitHub: [@mantovaniandre](https://github.com/mantovaniandre)

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela no repositório!**

### 🔗 Projetos Relacionados
- [BookWise Frontend](https://github.com/mantovaniandre/bookwise-frontend) - Interface Angular/TypeScript
- [Outros projetos no meu perfil](https://github.com/mantovaniandre)

---
*Desenvolvido com ❤️ por [André Mantovani](https://github.com/mantovaniandre)*