-- Cria a tabela onde o robô guarda o histórico de preços.
-- Rode este código uma única vez no SQL Editor do Supabase.

create table if not exists precos (
  id           bigint generated always as identity primary key,
  produto_nome text          not null,
  produto_url  text          not null,
  preco        numeric(10,2) not null,
  coletado_em  timestamptz   not null default now()
);

-- Deixa mais rápida a busca pelo último preço de cada produto (usada no passo d).
create index if not exists precos_url_data_idx on precos (produto_url, coletado_em desc);

-- Segurança: bloqueia o acesso público à tabela.
-- O robô usa a chave secreta (secret key), que continua tendo acesso.
alter table precos enable row level security;
