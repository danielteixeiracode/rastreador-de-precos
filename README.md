# Rastreador de Preços

Robô em Python que, todo dia à meia-noite, visita páginas de produtos em lojas online,
lê o preço, guarda um histórico no banco de dados e envia um e-mail quando o preço cai.

## Como funciona

1. Lê a lista de produtos no arquivo `produtos.json`.
2. Abre a página de cada produto e extrai o preço.
3. Busca no Supabase (PostgreSQL) o último preço guardado.
4. Grava o preço de hoje.
5. Se o preço caiu, envia um e-mail pelo Gmail.

## Tecnologias

- **Python**: a linguagem do robô.
- **Supabase**: banco de dados PostgreSQL na nuvem, onde fica o histórico de preços.
- **Gmail** (senha de app): envio dos alertas.
- **GitHub Actions**: roda o robô automaticamente todos os dias.

## Estrutura de pastas

```
Rastreador de Precos/
├── .github/workflows/
│   └── rastreador.yml   # agendamento diário no GitHub Actions
├── main.py              # ponto de partida: é o arquivo que você executa
├── produtos.json        # lista de produtos a acompanhar
├── requirements.txt     # bibliotecas Python necessárias
├── .env.example         # modelo das senhas/chaves (sem valores reais)
├── .env                 # suas senhas/chaves reais (NÃO vai para o GitHub)
├── .gitignore           # arquivos que o Git deve ignorar
├── rastreador/          # o código do robô, dividido por assunto
│   ├── config.py        # lê o produtos.json e o .env
│   ├── preco.py         # baixa a página e encontra o preço
│   ├── banco.py         # grava e busca preços no Supabase
│   ├── comparacao.py    # decide se o preço caiu, subiu ou ficou igual
│   └── notificacao.py   # monta e envia o e-mail de alerta pelo Gmail
├── testar_email.py      # envia um e-mail de exemplo para testar o Gmail
├── sql/
│   └── criar_tabela.sql # código que cria a tabela no Supabase
└── tests/               # testes automáticos
    ├── test_banco.py
    ├── test_comparacao.py
    ├── test_config.py
    ├── test_notificacao.py
    └── test_preco.py
```

## Como a comparação funciona

Para cada produto, o robô:

1. lê o preço de hoje na página;
2. busca no banco o **último** preço guardado daquele produto (ordenando por
   `coletado_em`, do mais novo para o mais antigo, e pegando só o primeiro);
3. grava o preço de hoje;
4. compara os dois e mostra o resultado:

| Situação                         | O que aparece na tela                          |
|----------------------------------|------------------------------------------------|
| Nenhum preço anterior no banco   | `R$ 38,40 (primeira leitura, nada para comparar)` |
| Preço menor que o anterior       | `R$ 35,00 — CAIU! (antes: R$ 38,40)`            |
| Preço maior que o anterior       | `R$ 40,00 — subiu (antes: R$ 38,40)`            |
| Preço igual                      | `R$ 38,40 — sem mudança`                        |

A busca acontece **antes** de gravar; senão o robô compararia o preço de hoje com ele mesmo.

Quando o preço **cai**, o robô envia um e-mail de alerta com o preço antigo, o novo,
a economia e o link do produto.

## Configurando o Gmail (uma única vez)

O robô envia o e-mail pelo Gmail usando uma **senha de app** — uma senha de 16 letras
criada só para ele, diferente da sua senha normal.

1. Ative a verificação em duas etapas em
   [myaccount.google.com/signinoptions/twosv](https://myaccount.google.com/signinoptions/twosv).
2. Crie a senha de app em
   [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   (nome: `Rastreador de Precos`) e copie a senha exibida.
3. Preencha no `.env`:

   ```
   GMAIL_USUARIO=email.que.envia@gmail.com
   GMAIL_SENHA_APP=abcdefghijklmnop
   EMAIL_DESTINO=email.que.recebe@gmail.com
   ```

4. Teste o envio (não mexe no banco):

   ```powershell
   python testar_email.py
   ```

## Configurando o Supabase (uma única vez)

1. Crie uma conta gratuita em [supabase.com](https://supabase.com) e crie um projeto novo.
2. No menu lateral do projeto, abra o **SQL Editor**, cole o conteúdo de
   [`sql/criar_tabela.sql`](sql/criar_tabela.sql) e clique em **Run**.
   Isso cria a tabela `precos`:

   | coluna         | o que guarda                         |
   |----------------|--------------------------------------|
   | `id`           | número de identificação da linha     |
   | `produto_nome` | nome do produto                      |
   | `produto_url`  | endereço da página do produto        |
   | `preco`        | preço lido (ex.: 38.40)              |
   | `coletado_em`  | data e hora da leitura (automático)  |

3. Copie a **URL do projeto** e a **chave secreta** (*secret key*) para o arquivo `.env`:

   ```
   SUPABASE_URL=https://xxxxxxxx.supabase.co
   SUPABASE_KEY=sb_secret_xxxxxxxx
   ```

A tabela tem *Row Level Security* ativado: ninguém consegue ler ou alterar os dados
pela internet sem a chave secreta, que fica só no `.env`.

## Como o preço é encontrado

O robô baixa o HTML da página (com a biblioteca `requests`) e procura, com a biblioteca
`BeautifulSoup`, uma etiqueta `<meta>` que informa o preço. Muitas lojas usam essas
etiquetas para mostrar o preço no Google, por exemplo:

```html
<meta itemprop="price" content="38.40" />
```

O robô tenta, nesta ordem: `itemprop="price"` (padrão schema.org),
`property="product:price:amount"` e `property="og:price:amount"` (padrão Open Graph).
Se a página de uma loja nova não tiver nenhuma delas, o robô mostra o erro
"Não encontrei o preço na página." e segue para o próximo produto.

Os preços são guardados como `Decimal` (e não `float`), porque o `Decimal` faz contas
com dinheiro sem erros de arredondamento.

## Como rodar no seu computador (Windows)

Abra o terminal na pasta do projeto e rode:

```powershell
# 1. Criar o ambiente virtual (só na primeira vez)
python -m venv .venv

# 2. Ativar o ambiente virtual (toda vez que abrir um terminal novo)
.venv\Scripts\Activate.ps1

# 3. Instalar as bibliotecas (na primeira vez e quando o requirements.txt mudar)
pip install -r requirements.txt

# 4. Criar seu arquivo de senhas a partir do modelo (só na primeira vez)
copy .env.example .env

# 5. Rodar o robô
python main.py
# Saída esperada:
#   Verificando 1 produto(s)...
#   - Meditações - Marco Aurélio: R$ 38,40 — sem mudança

# 6. Rodar os testes
python -m pytest
```

> Se o passo 2 der erro de "execução de scripts desabilitada", rode uma vez:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e responda `S`.

## Como acompanhar um produto novo

Abra o `produtos.json` e acrescente um item na lista, separado por vírgula:

```json
[
  {
    "nome": "Meditações - Marco Aurélio",
    "url": "https://www.livrariascuritiba.com.br/marco-aurelio---meditacoes-lv472246/p"
  },
  {
    "nome": "Outro produto",
    "url": "https://..."
  }
]
```

## Execução automática (GitHub Actions)

O arquivo [`.github/workflows/rastreador.yml`](.github/workflows/rastreador.yml) faz o
GitHub rodar o robô **todo dia às 03:00 UTC (meia-noite em Brasília)**, na nuvem, mesmo
com o computador desligado. A cada execução ele instala as bibliotecas, roda os testes
e depois o robô.

Como o `.env` não vai para o GitHub, as senhas ficam guardadas nos **Secrets** do
repositório. Para cadastrá-las: no repositório, **Settings → Secrets and variables →
Actions → New repository secret**, criando um secret para cada variável:

`SUPABASE_URL`, `SUPABASE_KEY`, `GMAIL_USUARIO`, `GMAIL_SENHA_APP`, `EMAIL_DESTINO`

Para rodar na hora, sem esperar a meia-noite: aba **Actions → Rastreador de Preços →
Run workflow**. Se algum produto der erro, a execução fica marcada com ❌ e o GitHub
avisa por e-mail.

> Observação: em repositórios sem nenhuma alteração por 60 dias, o GitHub pausa os
> agendamentos. Para reativar, basta clicar em **Enable workflow** na aba Actions.

## Segurança

Senhas e chaves ficam **somente** no arquivo `.env`, que está no `.gitignore` e por isso
nunca é enviado ao GitHub. O arquivo `.env.example` mostra quais variáveis são necessárias,
mas sem os valores.
