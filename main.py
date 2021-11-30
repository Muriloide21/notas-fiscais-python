from os import name
import xml.etree.ElementTree as ET
import json
from re import match
import sqlite3 as sl

con = sl.connect('my-test.db')

tree = ET.parse('teste.xml')
root = tree.getroot()
namespace = match(r'\{.*\}', root.tag).group(0)

with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS NOTAS_FISCAIS (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            cnpj_or_cpf_emit TEXT,
            cnpj_or_cpf_client TEXT,
            dvenc TEXT,
            valor FLOAT
        );
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS CLIENTES (
            cnpj_or_cpf_client TEXT,
            cnpj_or_cpf_emit TEXT,
            nome TEXT,
            endereco TEXT
        );
    """)

# Iterando sobre cada nota fiscal
for nfe in root.findall(f'{namespace}NFe'):
    emit = nfe[0].find(f'{namespace}emit')
    dest = nfe[0].find(f'{namespace}dest')

    # CPF/CNPJ do fornecedor
    cpf_or_cnpj_emit = emit.find(f'{namespace}CNPJ')
    if cpf_or_cnpj_emit == None: emit.find(f'{namespace}CPF')

    cpf_or_cnpj_emit = cpf_or_cnpj_emit.text

    # CPF/CNPJ do cliente
    cpf_or_cnpj_dest = dest.find(f'{namespace}CNPJ')
    if cpf_or_cnpj_dest == None: dest.find(f'{namespace}CPF')

    cpf_or_cnpj_dest = cpf_or_cnpj_dest.text

    # Data de vencimento e valor do boleto
    cobr = (nfe[0].find(f'{namespace}cobr'))
    valor = (cobr.find(f'{namespace}fat')).find(f'{namespace}vLiq').text
    vencimento = (cobr.find(f'{namespace}dup')).find(f'{namespace}dVenc').text

    sql = 'INSERT INTO NOTAS_FISCAIS (cnpj_or_cpf_emit, cnpj_or_cpf_client, dvenc, valor) VALUES (?, ?, ?, ?)'
    data_tuple = (cpf_or_cnpj_emit, cpf_or_cnpj_dest, vencimento, float(valor))

    with con:
        con.execute(sql, data_tuple)
    

    client_name = dest.find(f'{namespace}xNome').text
    enderDest = dest.find(f'{namespace}enderDest')
    rua = enderDest.find(f'{namespace}xLgr').text
    numero = enderDest.find(f'{namespace}nro').text
    bairro = enderDest.find(f'{namespace}xBairro').text
    município = enderDest.find(f'{namespace}xMun').text

    client_address = rua + ', ' + numero + '. ' + bairro + ', ' + município + '.'
    # print(client_address)

    # Inserir na tabela de clientes (cpf/cnpj_cliente, cpf/cnpj_emit, nome, endereco)
    sql2 = 'INSERT INTO CLIENTES (cnpj_or_cpf_client, cnpj_or_cpf_emit, nome, endereco) VALUES (?, ?, ?, ?)'
    data_tuple2 = (cpf_or_cnpj_dest, cpf_or_cnpj_emit, client_name, client_address)
    
    with con:
        con.execute(sql2, data_tuple2)

# Realizando Buscas
busca = input("Qual busca você deseja realizar:\n 1 - Listar os valores/datas de vencimento dos boletos referentes a um fornecedor;\n 2 - Apresentar o nome, identificador (CPF ou CNPJ), endereço dos clientes de um fornecedor.\n")
cpf_or_cnpj = input("Insira o CPF/CNPJ em questão: ")
    
if busca == '1':
    with con:
        cur = con.cursor()
        cur.execute('SELECT valor, dVenc FROM NOTAS_FISCAIS WHERE cnpj_or_cpf_emit = ?', (cpf_or_cnpj,))
        rows = cur.fetchall()
        for row in rows:
            print(*row, sep='; ')
else:
    with con:
        cur = con.cursor()
        cur.execute('SELECT nome, cnpj_or_cpf_client, endereco FROM CLIENTES WHERE cnpj_or_cpf_emit = ?', (cpf_or_cnpj,))
        rows = cur.fetchall()
        for row in rows:
            print(*row, sep='; ')

with con:
    con.execute("DROP TABLE CLIENTES")
    con.execute("DROP TABLE NOTAS_FISCAIS")
    
#06273476000182