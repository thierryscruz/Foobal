# 🚀 Início Rápido - Sistema de Seleção de Time

## Para Começar Agora

### 1. Executar o Sistema
```bash
cd futebol-system
source venv/bin/activate
python src/main.py
```

### 2. Abrir no Navegador
- Acesse: `http://localhost:5000`

### 3. Usar o Sistema
1. **Preencha pelo menos 12 jogadores** com seus nomes
2. **Selecione os níveis** de cada jogador (1, 2 ou 3)
3. **Clique em "Sortear Times"**
4. **Veja o resultado** com os times balanceados

## Dicas Importantes

### ✅ Para Funcionar Bem
- **Mínimo 12 jogadores** preenchidos
- **Nível 1** = Melhor jogador
- **Nível 3** = Jogador iniciante
- **Primeiros 12 da lista** têm prioridade

### 🎯 Algoritmo Inteligente
- **Níveis 1 nunca ficam juntos** no mesmo time
- **Distribui equilibradamente** níveis 2 e 3
- **Times de 6 jogadores** cada
- **Sobra vai para reserva**

### 🎨 Recursos Extras
- **Botão lua/sol** = Tema claro/escuro
- **Campo de data** = Organizar por sessão
- **Botão Limpar** = Recomeçar tudo

## Exemplo de Uso

```
Jogadores preenchidos:
1. João Silva (Nível 1)      ← Melhor jogador
2. Maria Santos (Nível 2)    ← Intermediário  
3. Pedro Costa (Nível 2)     ← Intermediário
4. Ana Lima (Nível 3)        ← Iniciante
... (até 12 jogadores)

Resultado do Sorteio:
🔵 Time A: João, Maria, Ana... (6 jogadores)
🔴 Time B: Pedro, Carlos, Lucia... (6 jogadores)
🪑 Reservas: (se houver mais de 12)
```

## Se Algo Der Errado

### Erro "Necessário 12 jogadores"
- Conte quantos nomes você preencheu
- Deve ter exatamente 12 ou mais

### Não aparece resultado
- Verifique se clicou em "Sortear Times"
- Recarregue a página (F5)

### Interface estranha
- Teste em Chrome ou Firefox
- Limpe o cache do navegador

---

**Pronto! Agora é só usar e sortear seus times! ⚽**

