import pandas as pd

class Csv:
    @staticmethod
    def __nehNumero(string):
        ret = None
        try:
            ret = float(string) if '.' in string else int(string)
            return False
        except:
            return True

    # função besta, só pra arredondar o tamanho
    @staticmethod
    def __arredondar(numero):

        if numero < 50:
            return 50
        if numero > 50 and numero < 100:
            return 100
        else:
            return 500

    @staticmethod
    def __limpar_arquivo(locacao_txt):
        f = open(locacao_txt, 'w')
        f.write("")
        f.close()
        return locacao_txt
    @staticmethod
    def __pegarNome(locacao):

        temp = locacao.split('.')[0].strip()
        nome = []
        i = len(temp)-1

        while(temp[i].isalpha()):
            nome.append(temp[i])
            i -= 1
        nome.reverse()

        return ''.join(nome).strip().upper()

    def definirCSV(self, locacao_csv, enc):
        print('3% - Definindo codificação')
        # temp = None
        # falhou = False
        # for enc in self.possiveisEncodings:
        #     temp = pd.read_csv(locacao_csv, sep=None, encoding=enc, engine='python')
        #     lista = temp.values.tolist()
        #     for sublista in lista:
        #         if not falhou:
        #             for item in sublista:
        #                 if not falhou and isinstance(item, str):
        #                     for letra in item:
        #                         if not letra.isalnum() and letra != ' ':
        #                             falhou = True
        #                             print(f'5% {enc} falhou! Tentando a próxima')
        #                             break
        temp = pd.read_csv(locacao_csv, sep=None, encoding=enc, engine='python')
        return temp




    def __init__(self, locacao_csv, enc):
        self.csv = self.definirCSV(locacao_csv, enc)
        self.nome_tab = self.__pegarNome(locacao_csv)
        self.csv_lista = []
        self.podeNull = []
        self.tratar()
    def tratar(self):
        print("7% - Trocando NaN's por NULL")

        #retirando da lista os sigilosos
        self.csv_lista = [sublista for sublista in list(self.csv.values.tolist()) if sublista[0] != -11]

        for i in range(len(self.csv_lista)):
            for y in range(len(self.csv_lista[i])):
                if pd.isna((self.csv_lista[i])[y]):
                    (self.csv_lista[i])[y] = 'NULL'
                    self.podeNull.append(y)
                elif (self.csv_lista[i])[y] == '':
                    self.podeNull.append(y)

        print("50% - Alterações de NaN finalizadas")

    def gravarTabela(self):

        f = open(self.__limpar_arquivo('tables.sql'), 'a')
        f.writelines(f"CREATE TABLE {self.nome_tab} (\n")

        for i, item in enumerate(list(self.csv.columns.values.tolist())):
            # tem que fazer um if pra datas
            if 'data' in item.casefold():
                f.write(f'{item} DATE')
            else:
                tamanho = 0
                ehInt = False
                for sub in self.csv_lista:
                    if isinstance(sub[i], str) or '*' in str(sub[i]):
                        if len(sub[i]) > tamanho:
                            tamanho = len(sub[i])
                    else:
                        if isinstance(sub[i], int):
                            ehInt = not ehInt
                        break
                if tamanho == 0:
                    f.write(f'{item} {"INT" if ehInt == True else "FLOAT"}')
                else:

                    f.write(f'{item} VARCHAR({self.__arredondar(tamanho)})')

            if (i == 0):
                f.write(" PRIMARY KEY NOT NULL")
            else:
                if not (i in self.podeNull):
                    f.write(' NOT NULL')

            if (i != len(list(self.csv.columns.values.tolist()))-1):
                f.writelines(',\n')
        f.writelines(");")
        f.close()
        print("70% - Gravação de Tabela concluída")

    def gravarInserts(self, qtde = None, porLetra = ''):

        verifica = False if qtde is None and porLetra == '' else True
        porLetra = porLetra.strip()

        if qtde is None:
            qtde = len(self.csv_lista)
        else:
            if qtde > len(self.csv_lista) or qtde <= 0:
                print(f"ERRO: - A quantidade disponível em {self.nome_tab} é {len(self.csv_lista)} entradas")
                return None

        if (len(porLetra) != 3 and len(porLetra) != 1 and len(porLetra) != 0) or (not porLetra.isalpha() and porLetra != '' and '-' not in porLetra):
            print('ERRO: - Digite uma letra de A a Z no parâmetro "porLetra"')
            return

        if len(porLetra) == 3:
            listaLetras = porLetra.split('-')

        file = open(self.__limpar_arquivo("inserts.sql"), "a")
        file.write(f'INSERT INTO {self.nome_tab} VALUES ')

        counter = 0
        for y, sublista in enumerate(self.csv_lista):

                if verifica:
                    if counter == qtde:
                        file.close()
                        print("100% - Gravação de Inserts concluída")
                        return

                        #Isso aqui é tipo:
                        #'a' < 'b' - True, por que A <- B <- C e etc...
                        #Então ele vai verificar todas as letras até chegar na que você quer.

                    match(len(porLetra)):
                        case 3:
                            t1 = listaLetras[0].upper()
                            t2 = listaLetras[1].upper()
                            t3 = sublista[1][0].upper()


                            if t3 < t1 < t2:
                                continue
                            elif t1 < t2 < t3:
                                file.close()
                                print("100% - Gravação de Inserts concluída")
                                return

                        case _:
                            t1 = sublista[1][0].upper()
                            t2 = porLetra.upper()
                            if t1 < t2:
                                continue
                            elif t1 > t2:
                                file.close()
                                print("100% - Gravação de Inserts concluída")
                                return


                file.write('(')
                for i in range(len(sublista)):

                    if isinstance(sublista[i], str) and sublista[i] != 'NULL' and self.__nehNumero(sublista[i]):
                        if i == len(sublista) - 1:
                            file.write(f"'{sublista[i]}'")
                        else:
                            file.write(f"'{sublista[i]}', ")
                    else:
                        if i == len(sublista) - 1:
                            file.write(f"{sublista[i]}")
                        else:
                            file.write(f"{sublista[i]}, ")
                file.write(')')
                file.write(';\n') if y == qtde else file.write(",\n")
                counter +=1

        file.close()
        print("100% - Gravação de Inserts concluída")


if __name__ == '__main__':
    meuCsv = Csv('202301_Cadastro.csv', 'latin-1')
    meuCsv.gravarTabela()

    """

    """
    meuCsv.gravarInserts(qtde=14, porLetra='A-D')
