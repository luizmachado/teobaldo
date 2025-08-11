# Teobaldo - Assistente de Mobilidade Urbana com IA

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg)](https://nextjs.org/)
[![LangChain](https://img.shields.io/badge/LangChain-blueviolet.svg)](https://www.langchain.com/)

**Teobaldo** é um assistente de conversação avançado projetado para simplificar a mobilidade urbana. Construído com uma arquitetura moderna, o projeto integra um agente de IA com múltiplos serviços para fornecer uma experiência de planejamento de rotas inteligente e contextual.

O principal objetivo deste projeto é demonstrar habilidades técnicas em desenvolvimento full-stack, com foco em:
* **Backend Robusto com IA:** Utilização de Python, FastAPI e LangGraph para criar um agente autônomo e com memória.
* **Frontend Moderno e Reativo:** Interface de chat construída com Next.js e TypeScript para uma ótima experiência de usuário.
* **Integração de APIs:** Conexão com serviços externos como Google Maps e APIs de previsão do tempo.
* **Sistema de Memória Adaptativa:** Capacidade do agente de aprender e reter as preferências do usuário para personalizar interações futuras.

## 🎞️ Demonstração

[![Demonstração do Teobaldo](https://s14.gifyu.com/images/bNlw1.gif)](https://gifyu.com/image/bNlw1)


## ✨ Recursos Principais

* **Planejamento de Rota e Visualização:** Consulte a API do Google Maps para obter direções detalhadas e exiba um mapa interativo diretamente na interface de chat.
* **Previsão do Tempo no Destino:** O agente pode verificar a previsão do tempo para o local de destino e informar o usuário.
* **Busca por Parceiros na Rota:** Encontre estabelecimentos conveniados (restaurantes, postos, etc.) ao longo do trajeto planejado.
* **Memória Adaptativa:**
    * **Curto Prazo:** O agente mantém o contexto da conversa atual, permitindo interações fluidas e de acompanhamento.
    * **Longo Prazo:** O sistema extrai e armazena preferências do usuário (ex: "prefiro rotas com menos pedágios", "gosto de parar em postos da rede X") em um banco de dados vetorial (ChromaDB), usando-as para personalizar futuras recomendações.
* **Interface de Chat Intuitiva:** Frontend limpo e responsivo com componentes de alta qualidade, incluindo indicadores de digitação e rolagem automática.
* **Autenticação Segura:** Sistema de login para proteger as conversas e preferências de cada usuário.

## 🏗️ Arquitetura e Design do Sistema

O projeto é dividido em um frontend (cliente) e um backend (servidor), que se comunicam via uma API REST. O coração do backend é um agente de IA construído com **LangGraph**.

### Fluxo do Agente de IA

O fluxo de raciocínio do agente é orquestrado por um grafo de estados (`StateGraph`), garantindo um processo de decisão modular e robusto.

1.  **Entrada do Usuário:** Uma nova mensagem é recebida pela API do FastAPI.
2.  **Recuperação de Memória de Longo Prazo (`retrieve_long_term_memory`):** O agente primeiro consulta o ChromaDB para buscar preferências passadas do usuário que sejam relevantes para a consulta atual.
3.  **Chamada ao Modelo (`call_model`):** A mensagem do usuário, o histórico da conversa (memória de curto prazo) e as preferências recuperadas são formatadas em um prompt e enviadas ao LLM (Gemini). O modelo então decide se deve responder diretamente ou usar uma ferramenta.
4.  **Decisão Condicional (`should_continue`):** O grafo verifica se a resposta do LLM contém uma chamada de ferramenta.
    * **Se SIM ➞ `call_tools`:** A função correspondente à ferramenta (ex: `get_route_and_polyline`, `get_weather_forecast`) é executada. O resultado (ex: a URL do mapa, a previsão do tempo) é adicionado ao estado do agente. O fluxo então retorna ao passo 3 (`call_model`) para que o LLM processe o resultado da ferramenta.
    * **Se NÃO ➞ `update_memory`:** A resposta final está pronta.
5.  **Atualização da Memória de Longo Prazo (`update_long_term_memory`):** Antes de finalizar, o agente analisa toda a conversa para extrair novas preferências do usuário. Se algo relevante for encontrado, é salvo no ChromaDB para uso futuro.
6.  **Fim (`END`):** A resposta final é enviada ao usuário.

### Estrutura de Estado (`AgentState`)

O estado é passado entre os nós do grafo e contém todas as informações necessárias para a execução, incluindo o histórico de mensagens, ID do usuário, informações da rota e o contexto recuperado da memória.

## 🛠️ Tech Stack

| Área | Tecnologias Utilizadas |
| --- | --- |
| **Backend** | **Python**, **FastAPI**, **LangChain**, **LangGraph**, **Gemini (Google AI)**, **ChromaDB**, **Ollama**, **AioSQLite** |
| **Frontend** | **Next.js**, **React**, **TypeScript**, **Tailwind CSS**, **Shadcn/ui**, **Lucide React** |
| **Autenticação** | **JWT** (JSON Web Tokens) |
| **Banco de Dados** | **SQLite** (para checkpoints de conversas), **JSON** (para dados de usuários/parceiros) |

## 📁 Estrutura do Projeto

A estrutura do projeto foi organizada para separar claramente as responsabilidades entre backend, frontend e dados.

```
.
├── src
│   ├── app/                      # Lógica principal do backend (FastAPI)
│   │   ├── agent/                # Módulos do agente de IA com LangGraph
│   │   │   ├── graph.py          # Definição do grafo do agente
│   │   │   ├── nodes.py          # Nós de lógica do agente (chamada ao LLM, tools, memória)
│   │   │   └── state.py          # Definição do estado do agente
│   │   ├── api/v1/               # Endpoints da API
│   │   │   └── chat.py           # Endpoint para o chat
│   │   ├── models/               # Modelos de LLM (Gemini, Ollama)
│   │   └── tools/                # Ferramentas disponíveis para o agente
│   │       ├── maps_tools.py     # Ferramenta de rota do Google Maps
│   │       ├── partner_tools.py  # Ferramenta de busca de parceiros
│   │       └── weather_tools.py  # Ferramenta de previsão do tempo
│   ├── data/                     # Dados da aplicação
│   │   ├── conversations.sqlite  # Banco de dados para memória de curto prazo
│   │   └── vector_store/         # Banco de dados vetorial para memória de longo prazo
│   └── frontend/                 # Aplicação frontend em Next.js
│       └── src/
│           ├── app/              # Páginas e layouts do Next.js
│           │   └── (app)/chat/
│           │       └── page.tsx  # Página principal do chat
│           ├── components/
│           │   ├── chat/         # Componentes React específicos do chat
│           │   │   ├── ChatInterface.tsx # Componente principal que gerencia o estado do chat
│           │   │   ├── MessageBubble.tsx # Renderiza cada bolha de mensagem (inclusive o mapa)
│           │   │   └── MessageList.tsx   # Lista as mensagens
│           │   └── ui/           # Componentes de UI reutilizáveis (Shadcn)
│           └── lib/
│               └── types.ts      # Definições de tipos TypeScript
└── ...

```


## 🚀 Como Executar Localmente

### Pré-requisitos

* Python 3.9+
* Node.js 18+ e npm
* Ollama (para embeddings de memória de longo prazo)
* Uma chave de API do Google Maps

### 1. Clonar o Repositório

```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio
```

### 2. Configurar o Backend

a. Navegue até a pasta do projeto e crie um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

b. Instale as dependências Python:

```bash
pip install -r requirements.txt
```

c. Configure as variáveis de ambiente. Crie um arquivo `.env` na raiz do projeto e adicione suas chaves:

```
GOOGLE_MAPS_API_KEY="SUA_CHAVE_AQUI"
GEMINI_API_KEY="SUA_CHAVE_AQUI"
```

d. Inicie o servidor backend com Uvicorn:

```bash
uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Configurar o Frontend

a. Em um novo terminal, navegue até a pasta do frontend:

```bash
cd src/frontend
```

b. Instale as dependências NPM:

```bash
npm install
```

c. Inicie o servidor de desenvolvimento do Next.js:

```bash
npm run dev
```

### 4. Acessar a Aplicação

Abra seu navegador e acesse `http://localhost:3000`. Você deverá ver a interface de login do Teobaldo.

## 🌟 Possíveis Melhorias Futuras

* **Streaming de Respostas:** Implementar streaming de tokens do LLM para o frontend para uma resposta mais rápida e dinâmica.
* **WebSockets:** Substituir a comunicação HTTP por WebSockets para uma comunicação bidirecional em tempo real.
* **Testes Automatizados:** Adicionar testes unitários e de integração para garantir a estabilidade do código.
* **Expansão de Ferramentas:** Adicionar novas ferramentas, como reserva de restaurantes ou compra de passagens.

## 📧 Contato

Luiz Augusto Machado da Silva – luizmachado.to@gmail.com

Link do Projeto: `https://github.com/seu-usuario/seu-repositorio`
