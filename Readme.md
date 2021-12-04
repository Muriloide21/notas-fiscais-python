# Venha para Recomb

O desafio é desenvolver um programa que permita realizar as seguintes buscas:

1) Listar os valores e data de Vencimento dos boletos presentes em um nota fiscal conforme o CPF ou CNPJ de um fornecedor.
2) Apresentar o nome, identificador (CPF ou CNPJ), endereço dos clientes de um fornecedor.

**Escolha as tecnologias que você vai usar e tente montar uma solução completa para rodar a aplicação.**

Para enviar o resultado, basta realiazar um Fork deste repositório e abra um Pull Request, com seu nome.

É importante comentar que deve ser enviado apenas o código fonte. Não aceitaremos códigos compilados.

Por fim, o candidato deve atualizar o Readme.md com as seguintes informações:
  
 1) Documentação da solução;
 2) Lista dos diferenciais implementados

## Avaliação

O programa será avaliado levando em conta os seguintes critérios:
|Critério|	Valor|
|-------|--------|
|Legibilidade do Código 	|10|
|Organização do Código|10|
|Documentação do código 	|10|
|Documentação da solução 	|10|
|Tratamento de Erros 	|10|
|Total| 	50|

A pontuação do candidato será a soma dos valores obtidos nos critérios acima.

## Diferenciais

O candidato pode aumentar a sua pontuação na seleção implementando um ou mais dos itens abaixo:
|Item |	Pontos Ganhos|
|-----|--------------|
|Criar um serviço com o problema 	|30|
|Utilizar banco de dados 	|30|
|Implementar Clean Code 	|20|
|Implementar o padrão de programação da tecnologia escolhida 	|20|
|Qualidade de Código com SonarQube| 	15|
|Implementar testes unitários 	|15|
|Implementar testes comportamentais |	15|
|Implementar integração com Travis 	|10|
|Implementar integração com Travis + SonarQube 	|10|
|Implementar usando Docker 	|5|
|Total |	170|

A nota final do candidato será acrescido dos pontos referente ao item implementado corretamente.

## Penalizações

O candidato será desclassifiado nas seguintes situações:

1) Submeter um solução que não funcione;
2) Não cumprir os critérios presentes no seção Avaliação;
3) Plágio;

## Documentação da Solução

Escolhi utilizar a linguagem Python para realizar o desafio,
Para a parte de parsing do XML, escolhi o módulo xml.etree.ElementTree;
Aproveitando-me da linguagem, utilizei a biblioteca sqlite3 para fazer a integração com Banco de Dados.
Para abrir uma porta com o serviço escolheu-se utilizar Flask.

A ideia da solução é percorrer todas as notas fiscais contidas no XML passado como parâmetro e obter as seguintes informações de cada uma:

- CPF/CNPJ do Fornecedor;
- CPF/CNPJ do Cliente;
- Valor e Data de Vencimento dos boletos;
- Nome e Endereço dos Clientes.

Para isso, utiliza-se dos métodos *find()* e *findall()* do módulo de Element Tree e da função *match()* da biblioteca de Regular Expressions.

Uma vez obtidas as informações necessárias em cada nota fiscal, são feitas inserções nas tabelas NOTAS_FISCAIS e CLIENTES criadas no início da execução. O formato dessas tabelas pode ser visualizado na função *initiate_tables()* do módulo *database.py*.

Passada toda a fase de *parsing* solicita-se ao usuário o tipo de busca que ele deseja realizar e o CPF/CNPJ do fornecedor em questão (tudo isso na página disponibilizada com Flask). Em seguida, realiza-se uma *query* de busca (SELECT) no banco de dados para obter as informações solicitadas.

## Documentação da Solução

Lista dos diferenciais implementados:

- Criar um serviço com o problema: Flask;
- Utilizar banco de dados: sqlite3;
- Implementar Clean Code:
    - Função de parsing bem comentada ao longo das etapas para melhor entendimento do leitor;
    - Nomes das funções, variáveis, módulos e tabelas do banco inteligíveis;
    - Modularização das etapas de parsing e interação com banco de dados;
    - Generalização de funções para evitar repetições de código;
- 