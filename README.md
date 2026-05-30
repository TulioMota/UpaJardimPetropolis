# UpaJardimPetropolis
Trabalho academico


# 🏘️ Jardim Petrópolis — Consulta de Equipe

Aplicação pública para consultar a qual equipe um endereço pertence no Jardim Petrópolis, Betim - MG.

**Stack:** HTML + Supabase (PostgreSQL + RLS) + GitHub Pages

---

## 📁 Estrutura do Projeto

```
jardim-petropolis/
├── index.html            ← aplicação completa (single-page)
├── supabase-setup.sql    ← script SQL para configurar o banco
├── _headers              ← headers HTTP de segurança (GitHub Pages via Cloudflare)
└── README.md
```

---

## 🚀 Passo a Passo para Deploy

### 1. Configurar o Supabase

1. Acesse [supabase.com](https://supabase.com) e crie um projeto
2. No Dashboard → **SQL Editor** → **New Query**
3. Cole o conteúdo de `supabase-setup.sql` e execute
4. Verifique em **Table Editor** se a tabela `enderecos` foi criada
5. Verifique em **Authentication → Policies** se as políticas RLS estão ativas

#### Pegar as credenciais:
- Dashboard → **Project Settings** → **API**
- Copie a **URL do projeto** (`https://xxxx.supabase.co`)
- Copie a **anon / public key** ⚠️ nunca a `service_role`

### 2. Configurar o `index.html`

Edite as linhas no início do `<script>`:

```js
const SUPABASE_URL      = 'https://SEU-PROJETO.supabase.co';
const SUPABASE_ANON_KEY = 'SUA-ANON-KEY-AQUI';
```

> A `anon key` é segura para o frontend. A proteção real vem do RLS.
> **Jamais coloque a `service_role` key em código público.**

### 3. Atualizar a Content Security Policy

No `<head>` do `index.html`, substitua `SEU-PROJETO` pela URL real:

```html
connect-src 'self' https://SEU-PROJETO.supabase.co;
```

### 4. Publicar no GitHub Pages

```bash
git init
git add .
git commit -m "chore: deploy inicial"
git remote add origin https://github.com/seu-usuario/jardim-petropolis.git
git push -u origin main
```

No repositório GitHub:
- **Settings** → **Pages**
- Source: `Deploy from a branch`
- Branch: `main` / `/(root)`
- Salvar → aguardar ~1 min → site publicado

### 5. Popular o banco de dados

Use o **Table Editor** do Supabase ou importe um CSV:

```sql
INSERT INTO public.enderecos (nome_rua, numero, equipe) VALUES
  ('Rua das Rosas', 100, 'Equipe Verde'),
  ('Rua das Rosas', 102, 'Equipe Verde'),
  ('Rua das Palmeiras', 50, 'Equipe Azul');
```

> Ou exporte sua planilha como CSV e use **Table Editor → Import CSV**.

---

## 🔒 Arquitetura de Segurança

### Por que a anon key no frontend é segura?

A `anon key` é **projetada para ser pública**. Ela só autentica o projeto, não dá permissões. As permissões reais vêm exclusivamente do **Row Level Security (RLS)**.

### Camadas de proteção implementadas

| Camada | Medida |
|--------|--------|
| **Banco** | RLS ativo — anon só pode `SELECT` |
| **Banco** | Funções RPC com `SECURITY DEFINER` e validação interna |
| **Banco** | `LIMIT 1` nas queries — sem enumeração em massa |
| **Banco** | `LIMIT 50` no autocomplete |
| **Banco** | Constraints de dados (`CHECK`) na tabela |
| **Frontend** | Rate limiting client-side (10 consultas/min) |
| **Frontend** | Sanitização de inputs antes de qualquer query |
| **Frontend** | `maxlength` e validação de tipo nos campos |
| **Frontend** | Mensagens de erro genéricas — sem vazar detalhes técnicos |
| **HTTP** | CSP, X-Frame-Options, HSTS, X-Content-Type-Options |
| **CDN** | Hash de integridade (SRI) no script do Supabase |

### O que o usuário anônimo NÃO pode fazer

- ❌ INSERT, UPDATE, DELETE na tabela
- ❌ Listar todos os endereços de uma vez
- ❌ Acessar o campo `id` ou `created_at`
- ❌ Executar queries arbitrárias
- ❌ Chamar a `service_role`

### Verificar RLS no Supabase

```sql
-- Execute no SQL Editor para confirmar que anon não consegue escrever:
SET role anon;
INSERT INTO public.enderecos (nome_rua, numero, equipe)
VALUES ('Teste', 1, 'Fraude');
-- Deve retornar: ERROR: new row violates row-level security policy
RESET role;
```

---

## 🎨 Personalizar as Cores das Equipes

No `index.html`, localize o objeto `EQUIPE_CORES` e adicione ou edite:

```js
const EQUIPE_CORES = {
  'equipe verde':    { bg: '#22c55e', text: '#fff' },
  'equipe azul':     { bg: '#3b82f6', text: '#fff' },
  'equipe vermelha': { bg: '#ef4444', text: '#fff' },
  'equipe amarela':  { bg: '#f59e0b', text: '#1a1714' },
  // Adicione novas equipes aqui...
  _default:          { bg: '#4f8ef7', text: '#fff' }, // fallback
};
```

> A chave é o **nome da equipe em minúsculo** exatamente como está no banco.

---

## 📊 Estrutura da Tabela

```sql
enderecos (
  id         BIGSERIAL PRIMARY KEY,
  nome_rua   TEXT NOT NULL,
  numero     INTEGER NOT NULL,
  equipe     TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE (nome_rua, numero)
)
```

---

## ⚠️ Checklist antes de publicar

- [ ] `SUPABASE_URL` e `SUPABASE_ANON_KEY` atualizados no `index.html`
- [ ] CSP atualizada com a URL real do Supabase
- [ ] Script SQL executado no Supabase
- [ ] RLS confirmado ativo (Dashboard → Auth → Policies)
- [ ] Dados reais inseridos na tabela `enderecos`
- [ ] Testou consulta válida → retorna equipe correta
- [ ] Testou consulta inválida → retorna "não encontrado"
- [ ] `service_role` key **nunca** commitada no repositório
- [ ] `.gitignore` não inclui credenciais acidentais

---

## 🔧 Comandos úteis (Supabase CLI)

```bash
# Instalar
npm install -g supabase

# Login
supabase login

# Ver tabelas
supabase db diff

# Push de migration local
supabase db push
```
