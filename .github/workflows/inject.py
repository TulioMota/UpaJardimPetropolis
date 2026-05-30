"""
inject.py — executado pelo GitHub Actions durante o deploy.
Substitui os placeholders do index.html pelas credenciais reais,
que vêm das variáveis de ambiente (GitHub Secrets).
Este arquivo NÃO contém nenhuma credencial.
"""
import os
import sys

url = os.environ.get('SUPABASE_URL', '').strip()
key = os.environ.get('SUPABASE_ANON_KEY', '').strip()

if not url:
    print('ERRO: variável SUPABASE_URL está vazia.', file=sys.stderr)
    sys.exit(1)

if not key:
    print('ERRO: variável SUPABASE_ANON_KEY está vazia.', file=sys.stderr)
    sys.exit(1)

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

if '__SUPABASE_URL__' not in content:
    print('ERRO: placeholder __SUPABASE_URL__ não encontrado no index.html.', file=sys.stderr)
    sys.exit(1)

if '__SUPABASE_ANON_KEY__' not in content:
    print('ERRO: placeholder __SUPABASE_ANON_KEY__ não encontrado no index.html.', file=sys.stderr)
    sys.exit(1)

content = content.replace('__SUPABASE_URL__', url)
content = content.replace('__SUPABASE_ANON_KEY__', key)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Substituição concluída com sucesso.')
