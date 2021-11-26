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
            cnpj_or_cpf_client TEXT NOT NULL PRIMARY KEY,
            cnpj_or_cpf_emit TEXT
            nome TEXT,
            endereco TEXT,
        );
    """)

input = input("Insira o CPF/CNPJ em questão: ")

# Iterando sobre cada nota fiscal
for nfe in root.findall(f'{namespace}NFe'):
    emit = nfe[0].find(f'{namespace}emit')

    # CPF/CNPJ do fornecedor
    cpf_or_cnpj = emit.find(f'{namespace}CNPJ')
    if cpf_or_cnpj == None: emit.find(f'{namespace}CPF')

    cpf_or_cnpj = cpf_or_cnpj.text

    # Data de vencimento e valor do boleto
    cobr = (nfe[0].find(f'{namespace}cobr'))
    valor = (cobr.find(f'{namespace}fat')).find(f'{namespace}vLiq').text
    vencimento = (cobr.find(f'{namespace}dup')).find(f'{namespace}dVenc').text

    sql = 'INSERT INTO NOTAS_FISCAIS (cnpj_or_cpf_emit, cnpj_or_cpf_client, dvenc, valor) VALUES (?, ?, ?, ?)'
    data_tuple = (name, cpf_or_cnpj, vencimento, float(valor))

    with con:
        con.execute(sql, data_tuple)

    #TODO
    # Inserir na tabela de clientes (cpf/cnpj_cliente, cpf/cnpj_emit, nome, endereco)

    #TODO
    # Dado um CPF/CNPJ de um fornecedor, realizar os 2 tipos de buscas utilizando as TABLES


#06273476000182