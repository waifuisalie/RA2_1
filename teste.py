class AnalisadorSintaticoLL1:
    def __init__(self):
        self.gramatica = {}
        self.first = {}
        self.follow = {}
        self.tabela_ll1 = {}
        self.terminais = set()
        self.nao_terminais = set()

    def construirGramatica(self):
        """
        Função obrigatória: Define gramática, calcula FIRST/FOLLOW e constrói tabela LL(1)
        """
        # Definir gramática corrigida (sem MEM em AFTER_NUM)
        self.gramatica = {
            'PROGRAM': [['LINHA', 'PROGRAM_PRIME']],
            'PROGRAM_PRIME': [['LINHA', 'PROGRAM_PRIME'], ['EPSILON']],
            'LINHA': [['LPAREN', 'CONTENT', 'RPAREN']],
            'CONTENT': [
                ['NUMBER', 'AFTER_NUM'],
                ['IDENTIFIER', 'AFTER_ID'],
                ['LPAREN', 'EXPR', 'RPAREN', 'AFTER_EXPR'],
                ['FOR', 'FOR_STRUCT'],
                ['WHILE', 'WHILE_STRUCT'],
                ['IFELSE', 'IF_STRUCT']  # ← ALTERAÇÃO: IFELSE inicia estrutura
            ],
            'AFTER_NUM': [
                ['NUMBER', 'OPERATOR'],
                ['IDENTIFIER'],
                ['RES']
            ],
            'AFTER_ID': [
                ['NUMBER', 'OPERATOR'],
                ['IDENTIFIER', 'OPERATOR'],
                ['LPAREN', 'EXPR', 'RPAREN', 'OPERATOR'],
                ['EPSILON']
            ],
            'AFTER_EXPR': [
                ['NUMBER', 'OPERATOR'],
                ['IDENTIFIER', 'OPERATOR'],
                ['LPAREN', 'EXPR', 'RPAREN', 'OPERATOR']
            ],
            'EXPR': [
                ['NUMBER', 'AFTER_NUM'],
                ['IDENTIFIER', 'AFTER_ID'],
                ['LPAREN', 'EXPR', 'RPAREN', 'AFTER_EXPR']
            ],
            'OPERATOR': [['ARITH_OP'], ['REL_OP'], ['LOGIC_OP']],
            'ARITH_OP': [['PLUS'], ['MINUS'], ['MULT'], ['DIV'], ['MOD'], ['POW']],  # ← ALTERAÇÃO: apenas DIV
            'REL_OP': [['GT'], ['LT'], ['EQ'], ['NEQ'], ['GTE'], ['LTE']],
            'LOGIC_OP': [['AND'], ['OR'], ['NOT']],
            'FOR_STRUCT': [['NUMBER', 'NUMBER', 'IDENTIFIER', 'LINHA']],
            'WHILE_STRUCT': [['LPAREN', 'EXPR', 'RPAREN', 'LINHA']],
            'IF_STRUCT': [['LPAREN', 'EXPR', 'RPAREN', 'LINHA', 'LINHA']]  # ← ALTERAÇÃO: sem ELSE separado
        }

        # Identificar terminais e não-terminais
        self._identificarSimbolos()

        # Calcular conjuntos FIRST
        self._calcularFirst()

        # Calcular conjuntos FOLLOW
        self._calcularFollow()

        # Construir tabela LL(1)
        self._construirTabelaLL1()

        # Validar se é LL(1) (sem conflitos)
        conflitos = self._validarLL1()

        return {
            'gramatica': self.gramatica,
            'first': self.first,
            'follow': self.follow,
            'tabela_ll1': self.tabela_ll1,
            'eh_ll1': len(conflitos) == 0,
            'conflitos': conflitos
        }

    def _identificarSimbolos(self):
        """Identifica terminais e não-terminais da gramática"""
        self.nao_terminais = set(self.gramatica.keys())

        for producoes in self.gramatica.values():
            for producao in producoes:
                for simbolo in producao:
                    if simbolo != 'EPSILON' and simbolo not in self.nao_terminais:
                        self.terminais.add(simbolo)

        # Adicionar $ (fim de cadeia)
        self.terminais.add('$')

    def _calcularFirst(self):
        """Calcula conjuntos FIRST para todos os símbolos"""
        # Inicializar FIRST para terminais
        for terminal in self.terminais:
            self.first[terminal] = {terminal}

        # Inicializar FIRST para não-terminais
        for nao_terminal in self.nao_terminais:
            self.first[nao_terminal] = set()

        # FIRST(EPSILON) = {EPSILON}
        self.first['EPSILON'] = {'EPSILON'}

        # Iterar até não haver mudanças
        mudou = True
        while mudou:
            mudou = False
            for nao_terminal, producoes in self.gramatica.items():
                for producao in producoes:
                    first_producao = self._firstProducao(producao)
                    tamanho_antes = len(self.first[nao_terminal])
                    self.first[nao_terminal] |= first_producao
                    if len(self.first[nao_terminal]) > tamanho_antes:
                        mudou = True

    def _firstProducao(self, producao):
        """Calcula FIRST de uma produção específica"""
        resultado = set()

        for simbolo in producao:
            first_simbolo = self.first.get(simbolo, {simbolo})
            resultado |= first_simbolo - {'EPSILON'}

            # Se não deriva epsilon, parar
            if 'EPSILON' not in first_simbolo:
                break
        else:
            # Todos derivam epsilon
            resultado.add('EPSILON')

        return resultado

    def _calcularFollow(self):
        """Calcula conjuntos FOLLOW para não-terminais"""
        # Inicializar FOLLOW
        for nao_terminal in self.nao_terminais:
            self.follow[nao_terminal] = set()

        # FOLLOW(símbolo inicial) contém $
        self.follow['PROGRAM'] = {'$'}

        # Iterar até não haver mudanças
        mudou = True
        while mudou:
            mudou = False
            for nao_terminal, producoes in self.gramatica.items():
                for producao in producoes:
                    for i, simbolo in enumerate(producao):
                        if simbolo in self.nao_terminais:
                            # Calcular FIRST do resto da produção
                            resto = producao[i+1:]
                            first_resto = self._firstProducao(resto) if resto else {'EPSILON'}

                            tamanho_antes = len(self.follow[simbolo])

                            # Adicionar FIRST(resto) - {EPSILON}
                            self.follow[simbolo] |= first_resto - {'EPSILON'}

                            # Se EPSILON em FIRST(resto), adicionar FOLLOW(nao_terminal)
                            if 'EPSILON' in first_resto:
                                self.follow[simbolo] |= self.follow[nao_terminal]

                            if len(self.follow[simbolo]) > tamanho_antes:
                                mudou = True

    def _construirTabelaLL1(self):
        """Constrói tabela de parsing LL(1)"""
        # Inicializar tabela vazia
        for nao_terminal in self.nao_terminais:
            self.tabela_ll1[nao_terminal] = {}

        # Preencher tabela
        for nao_terminal, producoes in self.gramatica.items():
            for producao in producoes:
                # Calcular FIRST da produção
                first_producao = self._firstProducao(producao)

                # Para cada terminal em FIRST
                for terminal in first_producao - {'EPSILON'}:
                    if terminal in self.tabela_ll1[nao_terminal]:
                        # Conflito detectado!
                        print(f"⚠️ CONFLITO em [{nao_terminal}, {terminal}]")
                    self.tabela_ll1[nao_terminal][terminal] = producao

                # Se EPSILON em FIRST, adicionar para FOLLOW
                if 'EPSILON' in first_producao:
                    for terminal in self.follow[nao_terminal]:
                        if terminal in self.tabela_ll1[nao_terminal]:
                            # Conflito detectado!
                            print(f"⚠️ CONFLITO em [{nao_terminal}, {terminal}]")
                        self.tabela_ll1[nao_terminal][terminal] = producao

    def _validarLL1(self):
        """Valida se gramática é LL(1) (sem conflitos)"""
        conflitos = []

        for nao_terminal in self.nao_terminais:
            producoes = self.gramatica[nao_terminal]

            if len(producoes) > 1:
                # Verificar se FIRST são disjuntos
                for i, prod1 in enumerate(producoes):
                    first1 = self._firstProducao(prod1)

                    for j, prod2 in enumerate(producoes[i+1:], i+1):
                        first2 = self._firstProducao(prod2)

                        intersecao = (first1 - {'EPSILON'}) & (first2 - {'EPSILON'})
                        if intersecao:
                            conflitos.append({
                                'nao_terminal': nao_terminal,
                                'tipo': 'FIRST-FIRST',
                                'producoes': [prod1, prod2],
                                'conflito': intersecao
                            })

                        # Verificar conflito FIRST-FOLLOW
                        if 'EPSILON' in first1:
                            intersecao_follow = (first2 - {'EPSILON'}) & self.follow[nao_terminal]
                            if intersecao_follow:
                                conflitos.append({
                                    'nao_terminal': nao_terminal,
                                    'tipo': 'FIRST-FOLLOW',
                                    'producoes': [prod1, prod2],
                                    'conflito': intersecao_follow
                                })

        return conflitos

    def parsear(self, tokens, tabela_ll1):
        """
        Função obrigatória: Parser descendente recursivo LL(1)

        Args:
            tokens: Lista de tokens da entrada
            tabela_ll1: Tabela LL(1) construída

        Returns:
            Dict com derivação ou erro sintático
        """
        # Adicionar $ ao final dos tokens
        tokens_com_fim = tokens + ['$']

        # Pilha de análise (começa com $ e símbolo inicial)
        pilha = ['$', 'PROGRAM']

        # Índice do token atual
        indice = 0

        # Derivação (histórico de passos)
        derivacao = []

        print("\n=== INICIANDO PARSING ===")
        print(f"Entrada: {' '.join(tokens_com_fim)}\n")

        while pilha:
            topo = pilha[-1]
            token_atual = tokens_com_fim[indice]

            print(f"Pilha: {' '.join(reversed(pilha))}")
            print(f"Token atual: {token_atual}")

            # Caso 1: Topo é terminal
            if topo in self.terminais or topo == '$':
                if topo == token_atual:
                    print(f"✓ Match: {topo}\n")
                    pilha.pop()
                    indice += 1
                    derivacao.append(f"Match terminal: {topo}")
                else:
                    erro = f"❌ ERRO SINTÁTICO: Esperado '{topo}', encontrado '{token_atual}'"
                    print(erro)
                    return {
                        'sucesso': False,
                        'erro': erro,
                        'derivacao': derivacao
                    }

            # Caso 2: Topo é não-terminal
            elif topo in self.nao_terminais:
                if token_atual in tabela_ll1.get(topo, {}):
                    producao = tabela_ll1[topo][token_atual]
                    print(f"Aplicar: {topo} → {' '.join(producao)}\n")

                    pilha.pop()

                    # Empilhar produção (ordem reversa)
                    if producao != ['EPSILON']:
                        for simbolo in reversed(producao):
                            pilha.append(simbolo)

                    derivacao.append(f"{topo} → {' '.join(producao)}")
                else:
                    erro = f"❌ ERRO SINTÁTICO: Nenhuma regra para [{topo}, {token_atual}]"
                    print(erro)
                    return {
                        'sucesso': False,
                        'erro': erro,
                        'derivacao': derivacao
                    }

            # Caso 3: EPSILON
            elif topo == 'EPSILON':
                print(f"✓ Derivar epsilon\n")
                pilha.pop()
                derivacao.append("Derivar ε")

            else:
                erro = f"❌ ERRO: Símbolo desconhecido '{topo}'"
                print(erro)
                return {
                    'sucesso': False,
                    'erro': erro,
                    'derivacao': derivacao
                }

        print("=== PARSING CONCLUÍDO COM SUCESSO ===\n")
        return {
            'sucesso': True,
            'derivacao': derivacao
        }


# ========== TESTES ==========

if __name__ == "__main__":
    # Criar analisador
    analisador = AnalisadorSintaticoLL1()

    # Construir gramática e verificar se é LL(1)
    print("=" * 60)
    print("CONSTRUINDO GRAMÁTICA E CALCULANDO FIRST/FOLLOW")
    print("=" * 60)

    resultado = analisador.construirGramatica()

    # Exibir FIRST
    print("\n📊 CONJUNTOS FIRST:")
    for simbolo, first_set in sorted(analisador.first.items()):
        if simbolo in analisador.nao_terminais:
            print(f"  FIRST({simbolo}) = {{{', '.join(sorted(first_set))}}}")

    # Exibir FOLLOW
    print("\n📊 CONJUNTOS FOLLOW:")
    for simbolo, follow_set in sorted(analisador.follow.items()):
        print(f"  FOLLOW({simbolo}) = {{{', '.join(sorted(follow_set))}}}")

    # Verificar se é LL(1)
    print("\n" + "=" * 60)
    if resultado['eh_ll1']:
        print("✅ A GRAMÁTICA É LL(1)! (Sem conflitos)")
    else:
        print("❌ A GRAMÁTICA NÃO É LL(1)!")
        print("\nConflitos encontrados:")
        for conflito in resultado['conflitos']:
            print(f"  • {conflito['tipo']} em {conflito['nao_terminal']}")
            print(f"    Conflito: {conflito['conflito']}")
    print("=" * 60)

    # TESTES DE PARSING
    print("\n\n" + "=" * 60)
    print("TESTES DE PARSING")
    print("=" * 60)

    testes = [
        {
            'nome': 'Teste 1: Operação simples (5 3 +)',
            'tokens': ['LPAREN', 'NUMBER', 'NUMBER', 'PLUS', 'RPAREN']
        },
        {
            'nome': 'Teste 2: Armazenamento (10 X)',
            'tokens': ['LPAREN', 'NUMBER', 'IDENTIFIER', 'RPAREN']
        },
        {
            'nome': 'Teste 3: Leitura de variável (X)',
            'tokens': ['LPAREN', 'IDENTIFIER', 'RPAREN']
        },
        {
            'nome': 'Teste 4: Resultado anterior (2 RES)',
            'tokens': ['LPAREN', 'NUMBER', 'RES', 'RPAREN']
        }
    ]

    for teste in testes:
        print(f"\n\n{'=' * 60}")
        print(teste['nome'])
        print('=' * 60)

        resultado_parse = analisador.parsear(
            teste['tokens'],
            analisador.tabela_ll1
        )

        if resultado_parse['sucesso']:
            print("✅ Parsing bem-sucedido!")
        else:
            print(f"❌ {resultado_parse['erro']}")
