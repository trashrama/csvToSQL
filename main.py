import csv_to_sql

# aqui não tem jeito, tem que testar a encodificação mesmo
# testa latin1, se sair bugado põe utf-8
meuCsv = csv_to_sql.Csv('202301_Cadastro.csv', 'latin-1', colunas=['NOME', 'cpf'])
meuCsv.gravarTabela()

meuCsv.gravarInserts(qtde=None, porLetra='A-S')

