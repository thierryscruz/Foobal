# Sistema de Seleção de Time de Futebol

Um sistema completo para sortear times de futebol de forma balanceada, desenvolvido com Flask (backend) e React (frontend).

## Funcionalidades

### ✅ Principais Recursos
- **Campo de Data**: Seleção da data da sessão de futebol
- **Cadastro de Jogadores**: Até 20 jogadores com nome e nível de habilidade
- **Níveis de Habilidade**: 3 níveis (1 = Melhor, 2 = Intermediário, 3 = Iniciante)
- **Algoritmo de Balanceamento Inteligente**:
  - Prioriza os 12 primeiros jogadores da lista
  - Garante que jogadores nível 1 nunca fiquem no mesmo time
  - Distribui equilibradamente os níveis 2 e 3
  - Jogadores extras vão para a reserva
- **Tema Claro/Escuro**: Alternância entre temas visuais
- **Interface Responsiva**: Funciona em desktop e mobile

### 🎯 Regras do Algoritmo
1. **Times de 6 jogadores cada** (total de 12 jogadores ativos)
2. **Níveis 1 nunca no mesmo time**:
   - 2 níveis 1: um para cada time
   - 3 níveis 1: 2 para um time, 1 para outro
   - 4+ níveis 1: distribuição equilibrada
3. **Balanceamento automático** dos níveis 2 e 3
4. **Priorização dos 12 primeiros** da lista
5. **Sistema de reservas** para jogadores extras

## Instalação e Execução

### Pré-requisitos
- Python 3.11+
- Node.js 20+
- npm ou pnpm

### Passo a Passo

1. **Clone ou baixe o projeto**
   ```bash
   # Se baixado como ZIP, extraia para uma pasta
   cd futebol-system
   ```

2. **Configure o ambiente virtual Python**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências Python**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o servidor**
   ```bash
   python src/main.py
   ```

5. **Acesse o sistema**
   - Abra seu navegador em: `http://localhost:5000`

## Como Usar

### 1. Configuração Inicial
- **Data**: Selecione a data da sessão (padrão: data atual)
- **Tema**: Use o botão no canto superior direito para alternar entre claro/escuro

### 2. Cadastro de Jogadores
- Preencha os nomes dos jogadores (mínimo 12 para sortear)
- Selecione o nível de cada jogador:
  - **Nível 1**: Jogadores mais habilidosos
  - **Nível 2**: Jogadores intermediários  
  - **Nível 3**: Jogadores iniciantes

### 3. Sorteio
- Clique em **"Sortear Times"** para gerar os times
- O resultado mostrará:
  - **Time A** (azul) e **Time B** (vermelho)
  - Distribuição de níveis por time
  - **Reservas** (se houver mais de 12 jogadores)

### 4. Funcionalidades Extras
- **Limpar**: Remove todos os dados e recomeça
- **Novo Sorteio**: Pode sortear novamente com os mesmos jogadores

## Estrutura do Projeto

```
futebol-system/
├── src/
│   ├── models/
│   │   ├── user.py          # Modelo de usuário (template)
│   │   └── futebol.py       # Modelo de dados do futebol
│   ├── routes/
│   │   ├── user.py          # Rotas de usuário (template)
│   │   └── futebol.py       # Rotas do sistema de futebol
│   ├── static/              # Frontend React compilado
│   ├── database/
│   │   └── app.db          # Banco SQLite
│   └── main.py             # Servidor Flask principal
├── venv/                   # Ambiente virtual Python
├── requirements.txt        # Dependências Python
└── README.md              # Esta documentação
```

## API Endpoints

### Sorteio Rápido
- **POST** `/api/futebol/sortear-rapido`
- Sorteia times sem salvar no banco
- Body: `{"jogadores": [{"nome": "João", "nivel": 1}, ...]}`

### Sessões (Opcional)
- **GET** `/api/futebol/sessoes` - Listar sessões salvas
- **POST** `/api/futebol/sessoes` - Criar nova sessão
- **GET** `/api/futebol/sessoes/{id}` - Obter sessão específica
- **PUT** `/api/futebol/sessoes/{id}` - Atualizar sessão
- **POST** `/api/futebol/sessoes/{id}/sortear` - Sortear times de uma sessão

## Tecnologias Utilizadas

### Backend
- **Flask**: Framework web Python
- **SQLAlchemy**: ORM para banco de dados
- **Flask-CORS**: Suporte a CORS
- **SQLite**: Banco de dados

### Frontend
- **React**: Biblioteca JavaScript
- **Tailwind CSS**: Framework CSS
- **shadcn/ui**: Componentes UI
- **Lucide Icons**: Ícones
- **Vite**: Build tool

## Personalização

### Alterando Regras do Algoritmo
Edite o arquivo `src/routes/futebol.py`, função `algoritmo_balanceamento()`:

```python
def algoritmo_balanceamento(jogadores):
    # Modifique as regras aqui
    # Exemplo: alterar tamanho dos times
    # if len(time_a) < 5 and len(time_b) < 5:  # Times de 5
```

### Modificando a Interface
O frontend está compilado em `src/static/`. Para modificar:
1. Edite os arquivos em `../futebol-frontend/src/`
2. Execute `npm run build` na pasta do frontend
3. Copie os arquivos de `dist/` para `src/static/`

## Solução de Problemas

### Erro "Necessário pelo menos 12 jogadores"
- Certifique-se de preencher pelo menos 12 nomes de jogadores
- Verifique se não há campos vazios nos primeiros 12

### Erro de CORS
- Verifique se o Flask-CORS está instalado: `pip install flask-cors`
- Reinicie o servidor Flask

### Interface não carrega
- Verifique se os arquivos estão em `src/static/`
- Acesse `http://localhost:5000` (não `127.0.0.1`)

### Banco de dados
- O banco SQLite é criado automaticamente em `src/database/app.db`
- Para resetar: delete o arquivo `app.db` e reinicie o servidor

## Suporte

Para dúvidas ou problemas:
1. Verifique se seguiu todos os passos de instalação
2. Confirme que as dependências foram instaladas corretamente
3. Teste em um navegador atualizado (Chrome, Firefox, Safari)

## Licença

Este projeto foi desenvolvido como sistema personalizado para seleção de times de futebol.

