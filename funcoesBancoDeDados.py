import mysql.connector
from datetime import datetime
import copy

mydb = mysql.connector.connect( host="localhost", user="root", password="almoxarifado", database='almoxarifado' )
mycursor = mydb.cursor()

# funcionarios = ['leandro','caina','gabriel','carlao','carlosm','valter',
#                 'francinaldo', 'jailson', 'juliedson', 'vinicius sm',
#                 'antunes','joselito','douglas','kevin','osvaldo','zaqueu',
#                 'alessandro','ronaldo','eduardo','julia',]
# funcionarios.sort()
# funcionariosdb = []


class Debug:
    def __init__(self):
        self.debug = False


def exe(querry, save=False):

    mycursor.execute(querry)
    debug   =  Debug()
    result  =  mycursor.fetchall()
    if debug.debug :
        print('exe foi executada com o parametro: ' + querry)
        print('e o resultado foi: '+str(result))
    if save:
        mydb.commit()
        if debug.debug :
            print("commit")
    return result

################# preenche o funcionariodb com o que estiver no banco de dados

def fimDaRecorrencia(obj):
    """essa função deve ser usada sempre que uma função de interação recorrente for usada e não houver uma interação de recorrencia subsequente"""
    
    obj.enviaParaRespostaGUI("fim da interação ",nomesColunas  =  [])
    obj.comandControler[1]     = copy.deepcopy([False,None,{}])
    
def atualizaVariavelFuncionarios(obj):

    debug  =  Debug()
    var  =  []
    for x in exe('select nome, funcao from funcionarios'):
        var.append([str(x[0]),str(x[1])])
    obj.funcionariosdb = var
    if debug.debug :
        print('self.funcionariosdb: ',obj.funcionariosdb)

def printObj(obj):
    
    if obj.FromGUI:
        respostaGUI  =  'funcionario atual: '  +  obj.funcionarioAtual  +  """
"""+     'modo atual: ' +  obj.modoAtual  +  """
"""
        obj.enviaParaRespostaGUI(  respostaGUI  ,  nomesColunas  =  []  )
    else:
        print('funcionario atual: ',obj.funcionarioAtual,'\n\n')
        print('modo atual:',obj.modoAtual,'\n\n')
        if input("deseja o historico de comandos?(s/n)\n ").lower() == 's':
            if len(obj.historicoDeComandos)  >  0:
                print('historico é: \n\n')
                for comando in obj.historicoDeComandos:
                    print(comando)    
            else:
                print('sem comandos no histórico')    
    
def validezDoIdentificador(identificador):
    if identificador.isnumeric():
        return True
    else:
        return False





def inputTratada(string=''):
    ####### essa função não será usada quando executando pela GUI!!!!!!!!!!

    stringInicial = input(string).lower()
    palavrasNaoTratadas = stringInicial.split(' ')
    palavras=[]
    for word in palavrasNaoTratadas:
        if word == '':
            pass
        elif word[0].isdigit():
            quant=''
            while word[0].isdigit():
                quant += word[0]
                word=word[1:]
                
            for x in range(int(quant)):
                palavras.append(word)
        else:
            palavras.append(word)

    return palavras



def dictToList(dicionario):
    lista  =  []
    for key in dicionario:
        lista.append([str(key),str(dicionario[key])])
    return lista

def printBonito(  arg  , obj , espacamento = 2  ,  antes  =  []  ,  depois  =  []  ) :
    
    if type(arg)  ==  dict:
        arg  =  dictToList(arg)

    if len(arg)  ==  0  :
        print("\n\n registro vazio em printBonito \n\n")
        
    elif type(arg) in [list,tuple]:
        for linha in arg:
            for index in range(len(linha)):
                linha[index]  =  str(linha[index])
        
        print('o argumento inicial da print bonitos é:',arg)
        listaDeTamanhosMaximosPorColuna=[]
        for x in range(len(arg[0])):                                    # para cada coluna
            listaDeTamanhosMaximosPorColuna.append(0)                   # reserva o espaço para a informação daquela coluna
            for linha in arg:                                           # para cada linha dentro da coluna especificada
                palavra  =  str(linha[x])                                   # transforma em string a palavra referente à coluna dentro dessa linha
                if len(palavra)  >  listaDeTamanhosMaximosPorColuna[x]:     # se ela for maior do que o máximo ja analizado para aquela coluna vai alterar esse máximo
                    listaDeTamanhosMaximosPorColuna[x]  =  len(palavra)

        novaLista  =  []
        
        for linha in arg:                                                                                            #para cada linha
            novaLista.append([])                                                                                     # reserva o espaço em novaLista para armazenar as informações
            for indexDaPalavra in range(len(linha)):                                                                 # para cada index percorrendo a quantidade de palavras da linha
                tamanhoMaxAtual = listaDeTamanhosMaximosPorColuna[indexDaPalavra]
                palavraAtual    = str(linha[indexDaPalavra])
                

                
                quantDeEspacos = tamanhoMaxAtual - len(palavraAtual) + espacamento
##                print('a quantidade de espaços calculada atual é: ',quantDeEspacos)
                
                if len(palavraAtual) > tamanhoMaxAtual:
                    print('algo muito errado está acontecendo a palavra é maior que o tamanho maximo calculado \n\n\n\n')
                    print('indexDaPalavra é: ',indexDaPalavra)
                    print('a linha é: ',linha)
                    print('a palavra atual é: ',palavraAtual)
                    print('tamanho da novaLista é:', len(novaLista))

                palavra  =  str(palavraAtual) + quantDeEspacos*' '
                novaLista[-1].append(palavra)
                
        segundaEmDiante = False
        for listaLinha in novaLista:
            linha=""
            for palavra in listaLinha:
                linha+=palavra
            if all( palavra == '' for palavra in linha.split(' ')):
                if(not segundaEmDiante):
                    segundaEmDiante = True
                else:
                    a = input('-->')
            print(linha)
    else:
        resposta = f'o tipo {type(arg)} não consigo lidar , o objeto é: {str(arg)}'
        obj.enviaParaRespostaGUI(resposta,nomesColunas  =  [] )
        print(resposta)
        


def dictToSortedDict(dictionaire):
    temp  =  list(dictionaire.keys())
    temp.sort()
    sortedDic={temp[x]:dictionaire[y] for x,y in enumerate(temp)}
    return sortedDic

def mostraListaDeSiglasEEquips(obj):
    obj.ferEquipdb = dictToSortedDict(obj.ferEquipdb)
    listaFerEquipdb = []
    for x in obj.ferEquipdb:
        listaFerEquipdb.append(  [  x  ,  obj.ferEquipdb[x]  ]  )
    if obj.FromGUI:
        obj.enviaParaRespostaGUI(listaFerEquipdb,nomesColunas=['sigla','equipamento'])
    else:
        printBonito(obj.ferEquipdb,obj)


def ShowComands(obj):
    """lista de comandos diponíveis"""
    info  =  []
    print('o comando controler é: ',obj.comandControler)
##    print('o tipo do comando controler é:',type(obj.comandControler))
##    print('o tipo do primeiro elemento do comand controler é: ',type(obj.comandControler[0]))
    for key in obj.comandControler.keys():
        linhaTratada = []
        linhaTratada.append(key)
        linhaTratada.append(obj.comandControler[key][1].__doc__)
        info.append(linhaTratada)
        
    print('a info que é injetada na resposta para GUI do showcomands é: ',info)    
    obj.enviaParaRespostaGUI(info, nomesColunas  =  ['comandos','explicações'])    

    

                       
                       
                    
                       
                    
                    
                
def checaEquip(equip,estado=[],periodo=[]):
    """funcao para verificar o equipamento específico(exemplo 'mr3" ou um tipo
    específico de equipamento( exemplo 'mt') e listar todos, alem de se estao
    dentro ou fora do almoxarifado com quem, data e horário de saida e de entrada

    variavel "estado" receberá:

    'f' se estiver procurando FORA   do almoxarifado
    'd' se estiver procurando DENTRO do almoxarifado
    [] se for independente do estado do equipamento.

    variavel "periodo" receberá o numero de dias a serem olhados incluindo o atual para trás
    
    """
    UltimoRegistro = ''
    querry = """select * from  registrodesaidasdeequips
                where
                Ferramenta like '""" + equip + "%'" 
    if estado:
        if estado    ==  'f':                            # 'f' significa fora do almoxarifado nesse caso
            querry   +=  ' and DataRetorno is null '
        elif estado  ==  'd':                          # 'd' significa dentro do almoxarifado 
            querry   +=  ' and DataRetorno is not null '

    result  =  exe(querry)
    return result######################################################################### essa função ainda não esta implementada



def checaRegistroEquip(equip):
    querry  =  f"""select * from listaDeFerramentas
            where
            tipoENumero = '{equip}'"""
    a  =  exe(querry)
    return a
    

def recebeFuncionarioDaGUI(palavras,obj):
    pass

def recorenteNomeFuncionarioNovo(obj,resposta):
    nome = copy.copy((resposta))
    print('o nome que entrou na funcao recorrente aqui foi:  ', nome)
    if nome!= '' and nome in obj.funcionariosdb  :
        obj.enviaParaRespostaGUI(f" o funcionario {nome} ja está registrado",nomesColunas=[])
    else:
            
        obj.enviaParaRespostaGUI( "profissao?  "  ,  nomesColunas  =  []  )
        obj.setaFuncaoRecorrente(recorrenteProfissaoFuncionarioNovo)
        obj.comandControler[1]  =  obj.comandControler[1][:-1]       ############## essa linha deleta a resposta da função anterior   ######
        obj.comandControler[1][2]['nome']  =  nome

def recorrenteProfissaoFuncionarioNovo(obj,resposta):
    nome = obj.comandControler[1][2]['nome']
    profissao = resposta
    querry  =  f"insert into funcionarios (nome, funcao) values ('{nome}' , '{profissao}' )"
##    if debug.debug:
##        print('a querry é: ' + querry)
    exe(  querry  ,  save  =  True  )
        # mydb.commit()
    obj.atualizaVariavelFuncionarios()
    fimDaRecorrencia(obj)
    

##    obj.enviaParaRespostaGUI( pergunta  ,  nomesColunas  =  []  )
##    obj.comandControler[1][1]  =  recorrenteSeEstaEntreOsSuspeitos
##    obj.comandControler[1]  =  obj.comandControler[1][:-1]
def registraFuncionarioNovo(obj):
    debug  =  Debug()
    if obj.FromGUI:
        obj.setaFuncaoRecorrente(recorenteNomeFuncionarioNovo)
##        obj.comandControler[1].append('')
        obj.enviaParaRespostaGUI("nome usual: ",nomesColunas  =  []  )
        
#    else:
#
#        funcionario  =  input("nome usual: ")
#    
#        if funcionario in obj.funcionariosdb  :
#            print(f" o funcionario {funcionario} ja está registrado")
#        else:
#            if obj.FromGUI:
#                funcao  =  'funcao vinda da GUI'             ############################################
#            else:
#                funcao  =  input('funcao: ')
#
#            querry  =  f"insert into funcionarios (nome, funcao) values ('{funcionario}' , '{funcao}' )"
#            if debug.debug:
#                print('a querry é: ' + querry)
#            exe(  querry  ,  save  =  True  )
#            # mydb.commit()
#        obj.atualizaVariavelFuncionarios()
#        if debug.debug:
#            print("consegui executar ela")
#    #return func
    
def registraFaltaDeNumeracao(palavraSemNumero):
    
    '''essa função vai registrar a ocorrencia de falta de numeração para aquele tipo de ferramenta
        e vai perguntar quantas sem numero eu estimo'''
    quant  =  input(f'quantas {palavraSemNumero} você estima que tem atualmente? ')
    # if FromGUI:
        # a='falta implementar essa porra'    #######################################
    # else:
    print(f"falta implementar essa parte espertão")

    
def registraSaida(obj):
    """
    essa função ainda precisa verificar se a
    sigla existe e
    se o equipamento ja é cadastrado e
    se não for solucionar isso,
    obs:
    numero diferente  não é tão problemático quanto
    sigla porem quero pergunta de verificação para ambos 
"""
    debug        =  Debug()
    funcionario  =  obj.funcionarioAtual
    equips       =  obj.listaEquipAtual
    usoExterno   =  obj.usoExterno
    if debug.debug:
        
        print('estou no registraSaida')
        print('funcionario é: ' , funcionario)
        print('equip é: ' , equips)

    if usoExterno:
        respostaUsoExterno = "uso externo ativado nesta saida "
        if obj.FromGUI  :
            obj.enviaParaRespostaGUI(  respostaUsoExterno  ,  colunas  =  []  )
        
        print(respostaUsoExterno)
        
    for fer in equips:
        nomeFer        =  fer['nome']
        identificador  =  fer['identificador']
        if debug.debug:
            print(f'ferramenta:{nomeFer} \n identificador: {identificador}')
                    
        
        if validezDoIdentificador(identificador):
            
            quantQueNaoVoltou  =  exe(f'''select count(*) from registroDeSaidasDeEquips
                                        where
                                        Ferramenta    = '{nomeFer}' and
                                        DataRetorno   is null       and
                                        identificador = '{identificador}'
                            ''')[0][0]
            if quantQueNaoVoltou  ==  1  :

                funcionarioDoRegistroNaoFeito  =  exe(f'''select funcionario from registroDeSaidasDeEquips
            where
            Ferramenta     = '{nomeFer}'       and
            DataRetorno    is null             and
            identificador  = '{identificador}'
            ''')[0][0]
                exe(f"""update registroDeSaidasDeEquips set
            DataRetorno    = current_date(),
            HorarioRetorno = current_time()   
            where
            Ferramenta     = '{nomeFer}'                        and
            Funcionario    = '{funcionarioDoRegistroNaoFeito}'  and
            DataRetorno    is null                              and
            identificador  = '{identificador}'
            """)
                resposta  =   f'a ferramenta não tinha registro de retorno, estava com {funcionarioDoRegistroNaoFeito}'
                if obj.FromGUI  :
                    obj.enviaParaRespostaGUI(  resposta  ,  nomesColunas  =  []  )
                
                print(resposta)

            if quantQueNaoVoltou > 1:
                resposta=f'multiplos registros da ferramenta:{nomeFer} sem retorno, obs: deveria ser unico'
                if obj.FromGUI:
                    obj.enviaParaRespostaGUI(  resposta  ,  nomescolunas  =  []  )
                else:
                    print(resposta)
        
            
        querry1  =  f'''insert into registroDeSaidasDeEquips
                             (Ferramenta,Funcionario,DataSaida,HorarioSaida,usoExterno, identificador) values
                             ( '{nomeFer}' ,'{funcionario}' ,current_date(), current_time() ,{usoExterno}, '{identificador}' ) '''
        if debug.debug:
            print('defini a querry')
            ##    try:
            print('vou tentar executar a querry1 = '  +  querry1)
        exe(querry1)
        resposta  =  f"""{nomeFer+'-'+identificador} saiu com {funcionario}"""
        if obj.FromGUI:
            obj.enviaParaRespostaGUI(resposta,nomesColunas=[])
        else:
            print(resposta)   ### aviso de saida da ferramenta

        if debug.debug:
            print(' consegui executar a querry1')
        
        registroDeComando                   =  {}
        registroDeComando['funcionario']    =  obj.funcionarioAtual
        registroDeComando['modo']           =  obj.modoAtual
        registroDeComando['equip']          =  nomeFer
        registroDeComando['identificador']  =  identificador
        obj.historicoDeComandos.append(registroDeComando)


###############################   interação recorrente com a GUI precisa ser implementada para poder ter isso aqui     ################################################################################
        if usoExterno:
            if obj.FromGUI:
                continuar = 'essa aqui tem que vir da GUI' ############
            else:
                continuar  =  input('continuar com usoExterno? (s/n)')
            if continuar  !=  's':
                obj.usoExterno  =  False
######################################################################################################################################################################
    obj.listaEquipAtual  =  list([])
    if debug.debug:
        if obj.FromGUI:
            obj.enviaParaRespostaGUI(resposta)
        print(resposta)
    mydb.commit()     
        
                
        ## aqui falta fazer essa querry registrar o id do ultimo registro
    ##    querry2= f"""update listaDeFerramentas set responsavelAtual ='{funcionario}'
    ##    where tipoENumero = '{equip}'""" 
    ##    print('a segunda querry é: ' +querry2)
    ##    exe(querry2)
    ##    print("consegui executar a querry2")
    ##    except:
    ##        print('deu erro nessa porrra')

    
def recorrenteSeEstaEntreOsSuspeitos(obj,resposta):
    suspeitos  =  obj.comandControler[1][2]['suspeitos']
    nomeFer    =  obj.comandControler[1][2]['nomeFer']
    identificador  = obj.comandControler[1][2]['identificador']
    print(' a resposta recebida na função recorrenteSeEstaEntreOsSuspeitos é ',resposta)
##    try:
    posicaoDoDono  =  int(resposta)
    print('consegui converter a resposta em int')

                                
    if posicaoDoDono in range(len(suspeitos)): ## aqui foi identificado o dono da ferramenta sem identificação única
        donoIdentificado  =  list(suspeitos.keys())[posicaoDoDono]
        IdDonoReal        =  suspeitos[donoIdentificado][0]
        querryDosDonos    =  f""" update registroDeSaidasDeEquips set  dataRetorno = current_date(),  horarioRetorno = current_time()
                                         where
                                         id = {IdDonoReal}
                                          """
        exe(querryDosDonos)
    ################################# interação recorrente com a GUI precisa ser implementada aqui     ########################################################                

        obj.enviaParaRespostaGUI(f"""{nomeFer+'-'+identificador} de {donoIdentificado} retornou"""  ,  nomesColunas  =  []  )

    ################################# interação recorrente com a GUI precisa ser implementada aqui     ########################################################                
        registroDeComando                   =  {}
        registroDeComando['funcionario']    =  donoIdentificado
        registroDeComando['modo']           =  obj.modoAtual
        registroDeComando['equip']          =  nomeFer
        registroDeComando['identificador']  =  'sn'
        registroDeComando['querry']         =  querryDosDonos
                            
        obj.historicoDeComandos.append(registroDeComando)        

    else:
##        obj.enviaParaRespostaGUI('posicao do dono desconhecida',nomesColunas=[])         ########### apenas provisório isso aqui, ja que a proxima resposta fala quase o mesmo   ######
                            
        donoReal       =  'desconhecido'
        querrySemDono  =  f"""insert into registroDeSaidasDeEquips
                                    (Funcionario,Ferramenta,Dataretorno,HorarioRetorno, identificador)
                                    values ('{donoReal}', '{nomeFer}' , current_date(),Current_time(), '{identificador}'  )   """
        exe(querrySemDono)

        obj.enviaParaRespostaGUI(f"""{nomeFer+'-'+identificador} de dono {donoReal} retornou """,nomesColunas=[])

        registroDeComando                  =  {
                'funcionario'   :  donoReal,
                'modo'          :  obj.modoAtual,
                'equip'         :  nomeFer,
                'identificador' :  'sn',
                'querry'        :  querrySemDono,
                }
            
        obj.historicoDeComandos.append(registroDeComando)
    fimDaRecorrencia(obj)
##    except:
##        obj.comandControler[1]  =  obj.comandControler[1][:-1]  ####################   essa linha apenas limpa a resposta de recorrência
##         ############################################################################   que ja estava escrita para poder usar a nova resposta sem problemas
##        print('o programa precisa que a resposta para a pergunta feita seja um numero, caso contrário não fará nada')

def RecorrenteSeEFuncionarioAtual(obj,resposta):
    print('a variavel resposta que chegou na recorrência é: '  ,  resposta  )
    ################## parte de tratamento da string 'resposta' #############################
    suspeitos      =  obj.comandControler[1][2]['suspeitos']
    nomeFer        =  obj.comandControler[1][2]['nomeFer']
    identificador  = obj.comandControler[1][2]['identificador']

    resp  =  resposta.split(' ')
    palavraCorreta  =  ''
    for palavra in resp:
        if palavra:
            palavraCorreta  =  palavra.lower()
            break
    ########################################################################################
        
    if palavraCorreta  ==  's':
        if obj.funcionarioAtual  !=  'desconhecido':
            querry3  =  f""" update registroDeSaidasDeEquips set  DataRetorno = current_date(),  HorarioRetorno = current_time()
                         where
                         id = '{suspeitos[obj.funcionarioAtual][0]}'                        
                         """

            exe(querry3)
            resposta  =  f""" {nomeFer+'-'+identificador} de {obj.funcionarioAtual} retornou"""
            if obj.FromGUI:
                obj.enviaParaRespostaGUI(resposta,nomesColunas = [] )
            else:
                print(resposta)
                        
            registroDeComando                   =  {}
            registroDeComando['funcionario']    =  obj.funcionarioAtual
            registroDeComando['modo']           =  obj.modoAtual
            registroDeComando['equip']          =  nomeFer
            registroDeComando['identificador']  =  identificador
            registroDeComando['querry']         =  querry3
            obj.historicoDeComandos.append(registroDeComando)
            fimDaRecorrencia(obj)
    else:
        pergunta  =  """qual deles é o dono? \n'"""

        for indice , func in enumerate(list(obj.comandControler[1][2]['suspeitos'].keys())):
            pergunta   +=  func + f'({indice}) , '
        pergunta       +=  '\n digite -1 se for desconhecido, digite o numero entre parentezis se for um deles \n'  
        
        obj.enviaParaRespostaGUI( pergunta  ,  nomesColunas  =  []  )
        obj.comandControler[1][1]  =  recorrenteSeEstaEntreOsSuspeitos
        obj.comandControler[1]  =  obj.comandControler[1][:-1]  ####################   essa linha apenas limpa a resposta de recorrência
        ############################################################################   que ja estava escrita para poder usar a nova resposta sem problemas
         
        
def registraEntrada(obj):
    """
    essa função apenas faz o registro de entrada, ainda falta implementar a
    verificação da existência do
    registro de saida e do
    registro da sigla e do 
    registro na lista de ferramentas
    alem de controlar se de fato ela consegu7u achar o registro e modificá-lo
"""
##    tempo = datetime.now()
##    data,hora= str(tempo.date()),str(tempo.time()).split('.')[0]
    ## essa parte verifica a existência de registro de saida sem retorno
    
    debug  =  Debug()
    
    equips  =  obj.listaEquipAtual
    if equips:            
        for fer in equips:
            nomeFer        =  fer['nome']
            identificador  =  fer['identificador']
            if validezDoIdentificador(identificador):
                
                registroDeSaidaAtivo  =  exe(f"""select count(*) from registroDeSaidasDeEquips
                                       where
                                       Ferramenta    = '{nomeFer}'        and
                                       identificador = '{identificador}'  and
                                       DataRetorno is null """)[0][0]

                if registroDeSaidaAtivo  ==  0:
                    resposta=f"'{fer}' se encontra sem registro de saida atual por isso não farei o registro de entrada"
                    if obj.FromGUI:
                        obj.enviaParaRespostaGUI(resposta,nomesColunas=[])
                    print(resposta)

                else :
                    
                    querry1  =  f"""update registroDeSaidasDeEquips set  dataRetorno = current_date(),  horarioRetorno = current_time()
                     where
                     Ferramenta     = '{nomeFer}'       and
                     identificador  = '{identificador}' and
                     DataRetorno    is null             and
                     HorarioRetorno is null
                     """
                    if debug.debug:
                        print('vou atualizar a tabela registroDeSaidasDeEquips com a querry: ' + querry1)
                    
                    exe(querry1)
                    resposta  =  f"""{nomeFer+'-'+identificador} retornou """
                    if obj.FromGUI:
                        obj.enviaParaRespostaGUI(resposta,nomesColunas=[])
                    
                    print(resposta)
                    
                    registroDeComando  =  {}
                    registroDeComando['funcionario']    =  obj.funcionarioAtual
                    registroDeComando['modo']           =  obj.modoAtual
                    registroDeComando['equip']          =  nomeFer
                    registroDeComando['identificador']  =  identificador
                    registroDeComando['querry']         =  querry1
                    obj.historicoDeComandos.append(registroDeComando)

            else:
                querry2  =  f"""select Funcionario, id  from registroDeSaidasDeEquips
                            where
                            Ferramenta     = '{nomeFer}'       and
                            (
                            identificador is null or
                            identificador  = '' or
                            identificador  = 'sn'
                            )
                            and
                            DataRetorno is null
                            order by
                            DataSaida desc"""
                
                funcionariosComEssaFerramenta  =  exe(querry2)
                suspeitos  =  {}

                for func in funcionariosComEssaFerramenta:
                    suspeitos[func[0]]  =  [].copy()
                for otherfunc in funcionariosComEssaFerramenta:
                    suspeitos[otherfunc[0]].append(otherfunc[1])

                    
                    ##################################################################################################################################3
                if obj.FromGUI :
                    obj.setaFuncaoRecorrente(RecorrenteSeEFuncionarioAtual)
##                    obj.comandControler[1][0] = True             ###################### preciso setar isso sempre que for a primeira vez que usa função recorrente
##                    obj.comandControler[1][1] = RecorrenteSeEFuncionarioAtual       ################referenciei a função de recorrencia
                    obj.comandControler[1][2]['suspeitos']      =  copy.deepcopy(suspeitos)                ################aqui enviarei todas as variáveis necesárias para a próxima função da recorrência
                    obj.comandControler[1][2]['nomeFer']        =  nomeFer
                    obj.comandControler[1][2]['identificador']  =  identificador  
                    obj.enviaParaRespostaGUI(f"a ferramenta é de {obj.funcionarioAtual} (s/n)"  ,  nomesColunas  =  []  )


                    
                else:
################################# interação recorrente com a GUI precisa ser implementada aqui     ########################################################                
                    if obj.funcionarioAtual  !=  'desconhecido' and input(f'a ferramenta é de {obj.funcionarioAtual} (s/n)').lower() == 's':
                        querry3  =  f""" update registroDeSaidasDeEquips set  DataRetorno = current_date(),  HorarioRetorno = current_time()
                         where
                         id = '{suspeitos[obj.funcionarioAtual][0]}'                        
                         """

                        exe(querry3)
                        resposta  =  f""" {nomeFer+'-'+identificador} de {obj.funcionarioAtual} retornou"""

                        print(resposta)
                        
                        registroDeComando                   =  {}
                        registroDeComando['funcionario']    =  obj.funcionarioAtual
                        registroDeComando['modo']           =  obj.modoAtual
                        registroDeComando['equip']          =  nomeFer
                        registroDeComando['identificador']  =  identificador
                        registroDeComando['querry']         =  querry3
                        obj.historicoDeComandos.append(registroDeComando)
    ################################# interação recorrente com a GUI precisa ser implementada aqui     ########################################################                
                        
                    else:
                        pergunta  =  """qual deles é o dono? \n\n '"""
                        for indice, func in enumerate(list(suspeitos.keys())):
                            pergunta   +=  func + f'({indice}) , '
                        pergunta       +=  ' \n\n digite -1 se for desconhecido, digite o numero entre parentezis se for um deles \n'  

                        posicaoDoDono  =  int(input(pergunta))

                                
                        if posicaoDoDono in range(len(suspeitos)): ## aqui foi identificado o dono da ferramenta sem identificação única
                            donoIdentificado  =  list(suspeitos.keys())[posicaoDoDono]
                            IdDonoReal        =  suspeitos[donoIdentificado][0]
                            querryDosDonos    =  f""" update registroDeSaidasDeEquips set  dataRetorno = current_date(),  horarioRetorno = current_time()
                                         where
                                         id = {IdDonoReal}
                                          """
                            exe(querryDosDonos)
    ################################# interação recorrente com a GUI precisa ser implementada aqui     ########################################################                

                            print(f"""{nomeFer+'-'+identificador} de {donoIdentificado} retornou""")

    ################################# interação recorrente com a GUI precisa ser implementada aqui     ########################################################                
                            registroDeComando                   =  {}
                            registroDeComando['funcionario']    =  donoIdentificado
                            registroDeComando['modo']           =  obj.modoAtual
                            registroDeComando['equip']          =  nomeFer
                            registroDeComando['identificador']  =  'sn'
                            registroDeComando['querry']         =  querryDosDonos
                            
                            obj.historicoDeComandos.append(registroDeComando)        

                        else:
                            print('posicao do dono desconhecida')
                            
                            donoReal       =  'desconhecido'
                            querrySemDono  =  f"""insert into registroDeSaidasDeEquips
                                    (Funcionario,Ferramenta,Dataretorno,HorarioRetorno, identificador)
                                    values ('{donoReal}', '{nomeFer}' , current_date(),Current_time(), '{identificador}'  )   """
                            exe(querrySemDono)

                            print(f"""{nomeFer+'-'+identificador} de dono {donoReal} retornou """)

                            registroDeComando                  =  {}
                            registroDeComando['funcionario']   =  donoReal
                            registroDeComando['modo']          =  obj.modoAtual
                            registroDeComando['equip']         =  nomeFer
                            registroDeComando['identificador'] =  'sn'
                            registroDeComando['querry']        =  querrySemDono
                            obj.historicoDeComandos.append(registroDeComando)
                            
                                
                            
    else:
        resposta  =  "tentaram executar a funcao de registrar entrada sem nenhum equipamento para entrar"
        if obj.FromGUI:
            obj.enviaParaRespostaGUI(resposta,nomesColunas=[])
        else:
            print(resposta)
    obj.listaEquipAtual  =  list([])
    if debug.debug:
        print('limpei a lista de Equips atual , veja: ', obj.listaEquipAtual)
    mydb.commit()
    

def mostraFuncionarios(obj  =  '' ):
    """mostra uma lista de funcionarios"""
    listaDeFuncionarios  =  []
    funcionarios  =  exe('select nome from funcionarios')
    funcionarios  =  list(funcionarios)
    funcionarios.sort()
    funcionariosParaGUI=[]
    for x in funcionarios:
        listaDeFuncionarios.append(x[0])
        if not obj.FromGUI:
            print(x[0])
        else:
            funcionariosParaGUI.append(x)
    if obj.FromGUI:
        obj.enviaParaRespostaGUI( funcionariosParaGUI,nomesColunas=['funcionario'] )
    
    ##################### preciso implementar aqui o envio da listaDeFuncionarios para a GUI
    
def commit(obj):
    mydb.commit()

def registraNovaFerramenta(obj):
    equips  =  obj.listaEquipAtual
    for equip in equips:
        if obj.checaRegistroFerramenta(equip):
            resposta=f"'{equip}' ja está registrada"
            if obj.FromGUI:
                obj.enviaParaRespostaGUI(resposta,nomesColunas=[])
            print(resposta)
        else:    
            a  =  f"insert into siglasENomesDeEquips (abreviaturaDeEquipamento) values ('{equip}') "
            exe(a)
            if obj.FromGUI:
                obj.enviaParaRespostaGUI(f""" {equip} foi registrada """,nomesColunas=[])
    mydb.commit()

def checaRegistroFerramentaERegistra(siglaSemNumero):
    quant  =  exe(f""" select count(*) from siglasENomesDeEquips
                where
                abreviaturaDeEquipamento = '{siglaSemNumero}' """)[0][0]
    if quant > 0 :
        print('equipamento ja registrado')
        return True
    else:
        return False

def pendenciasFuncionario(obj):
    
    funcionario   =  obj.funcionarioAtual
    equipsAtuais  =  exe(f"""select id,Ferramenta, identificador, DataSaida, HorarioSaida from registroDeSaidasDeEquips
                       where
                       funcionario ='{funcionario}' and
                       DataRetorno is null
                       and DataSaida < current_date()
                       order by
                       DataSaida desc """)
    if len(equipsAtuais)  >  0 :
        if obj.FromGUI:
            obj.enviaParaRespostaGUI(equipsAtuais,nomesColunas  =  [  'Ferramenta' , 'identificador' , 'DataSaida' , 'HorarioSaida'  ], identificador = True  )
        else:
            resposta = f"\n\n{funcionario} está com:\n "
            printBonito(trataRegistro(equipsAtuais,obj),obj)
    else:
        resposta = f"{funcionario} nao se encontra com equipamentos atualmente\n"
        if obj.FromGUI:
            obj.enviaParaRespostaGUI(resposta,nomesColunas=[])
        
        print(resposta)

def equipamentosHojeDeFuncionario(obj):

    """equipamentos do funcionario hoje"""
    
    equipsJaDevolvidosHoje  =  exe(f""" select id,  Ferramenta, identificador , HorarioSaida, HorarioRetorno from registroDeSaidasDeEquips
        where
        funcionario ='{obj.funcionarioAtual}' and
        DataSaida = current_date()""")
    
    if len(equipsJaDevolvidosHoje)>0:

        resposta  =  'lista de equips que ele pegou e devolveu hoje:\n'

        if obj.FromGUI:
            obj.enviaParaRespostaGUI( equipsJaDevolvidosHoje,nomesColunas  =  [ 'Ferramenta' , 'identificador' , 'HorarioSaida' , 'HorarioRetorno']  ,  identificador  =  True  )

        else:
            print()
            printBonito(trataRegistro(equipsJaDevolvidosHoje,obj))       #############  aqui usa o trataRegistro
    else:
        resposta  =  '\nnão há equipamento devolvido por ele hoje\n'

        if obj.FromGUI:
            obj.enviaParaRespostaGUI(resposta,nomesColunas = [] )

        else:
            print(resposta)

##    pendenciasFuncionario(obj)

    
def historicoFerramenta(obj):

    """historico da ferramenta atual """
    
    Ferramentas  =  obj.listaEquipAtual
    palavraSemNumero,identificador  =  Ferramentas[0]['nome'],Ferramentas[0]['identificador']
    
########################################################### interação reccorente para implementar na GUI ################################################3
    if len(Ferramentas)  >  0 :
                
        for ferramenta in Ferramentas:
                
            historico  =  exe(f"""select  id,  Funcionario, DataSaida, HorarioSaida, DataRetorno, HorarioRetorno  from registroDeSaidasDeEquips
                      where
                      Ferramenta='{palavraSemNumero}' and
                      identificador = '{identificador}'
                      order by
                  DataSaida desc limit 60""")
            if obj.FromGUI:
                obj.enviaParaRespostaGUI( historico , nomesColunas  =  [  'Funcionario'  ,  'DataSaida' ,  'HorarioSaida' ,  'DataRetorno'  ,  'HorarioRetorno'  ] , identificador = True )
            else:
                input(f"{palavraSemNumero,identificador} -->")
                printBonito(historico)
##        else:
##            string  =  'de qual delas vc quer saber?  '
##    
##            for ferramenta in Ferramentas:
##                string  +=  f"  {ferramenta}  "
##            fer  =  input(string)
##        if fer in obj.FerEquipdb:
##            obj.listaEquipAtual  =  [fer]
##            historicoFerramenta(obj)
##        else:
##            resposta=f'{fer} não é uma ferramenta cadastrada'
##            if obj.FromGUI:
##                obj.enviaParaRespostaGUI(resposta,nomesColunas=[])
##            print(resposta)
            
##    elif len(Ferramentas)  ==  1 :
##        print(Ferramentas)
##        
##        historico  =  exe(f"""select DataSaida, HorarioSaida, DataRetorno, HorarioRetorno, Funcionario from registroDeSaidasDeEquips
##                      where
##                      Ferramenta='{palavraSemNumero}' and
##                      identificador = '{identificador}'
##                      order by
##                      DataSaida desc limit 60""")
##        resposta= f"os ultimos registros de {palavraSemNumero+identificador} são:"
##        if obj.FromGUI:
##            obj.enviaParaRespostaGUI(historico,nomesColunas=[])
##        
##        print(resposta)
        

    else:
        resposta= 'funcao de procurar histórico foi executada com a listaEquipAtual vazia'
        if obj.FromGUI:
            obj.enviaParaRespostaGUI(resposta,nomesColunas=[])
        print(resposta)
        
    obj.RegistraELimpaListaEquipAtual()

def retornaObjParaValoresIniciais(obj):
    debug=Debug()
    modoAntigo           = obj.modoAtual
    equipsAntigos        = obj.listaEquipAtual.copy()
    funcionarioAntigo    = obj.funcionarioAtual
    obj.modoAtual        = ''
    obj.listaEquipAtual  = [].copy()
    obj.funcionarioAtual = ''
    if debug.debug:
        resposta  =  f""" funcionario foi de {funcionarioAntigo} para {obj.funcionarioAtual} \n
modo foi de {modoAntigo} para {obj.modoAtual} \n
lista de equipamentos foi de {equipsAntigos} para {obj.listaEquipAtual}
            
        """
        if obj.FromGUI:
            obj.enviaParaRespostaGUI(resposta,nomesColunas=[])
        print(resposta)
    
def modoSaida(obj):
    obj.modoAtual  =  'saida'
    resposta='modo saida ativado'
    if obj.FromGUI:
        obj.enviaParaRespostaGUI(resposta,nomesColunas=[])
    else:
        print(resposta)

def modoEntrada(obj):
    obj.modoAtual  =  'entrada'
    resposta = 'modo entrada ativado'
    if obj.FromGUI:
        obj.enviaParaRespostaGUI(resposta,nomesColunas=[])
    else:
        print(resposta)

def usoExterno(obj):
    obj.usoForaDaObra()
    resposta = f"uso externo : {obj.usoExterno}"
    if obj.FromGUI:
        obj.enviaParaRespostaGUI(resposta,nomesColunas=[])
    print(resposta)
    
def trataRegistro(registros, obj):
    """
    esta função agrupa pelo valor da primeira coluna, que tem que ser funcionarios, em relação aos outros,

    a segunda e terceira coluna tem que ser ferramenta e identificador respectivamente,

    os outros dados podem ser qualquer quantidade em qualquer ordem

    """

    debug=Debug()
    funcionarios     = [].copy()
    registroTratado  = [].copy()
    for registro in registros:
        
        funcionario    =  registro[0]
        ferramenta     =  obj.ferEquipdb[registro[1]] + '-' +registro[2]
        dados          =  registro[3:]

        
        if funcionario not in funcionarios:
            
            funcionarios.append(funcionario)
            registroTratado.append([].copy())
            for reg in range(len(registros[0])-1):
                registroTratado[-1].append(' ')
            
            registroTratado.append([funcionario])
        else:
            registroTratado.append([len(funcionario)*' '])
            
        registroTratado[-1].append(ferramenta)
        for dado in dados:
            registroTratado[-1].append(dado)         
    if debug.debug:
        if obj.FromGUI:
            pass ################### preciso implementar aqui
        else:
            print('aqui esta a lista tratada dentro da função equips fora hoje: ',registroTratado )
    return registroTratado


def equipsforaHoje(obj):
    registros        =  exe("select  id,  Funcionario, Ferramenta,identificador, HorarioSaida from registroDeSaidasDeEquips where DataSaida= current_date() and DataRetorno  is null")
    if len(registros)  >  0  :
            
        registroTratado  = trataRegistro(  registros  ,  obj  ) 
        if obj.FromGUI:
            obj.enviaParaRespostaGUI(registroTratado,nomesColunas  =  [  'funcionario'  ,  'ferramenta'  ,  'horarioSaida'  ]  ,  identificador  =  True  )
        else:
            printBonito(  registroTratado  ,  obj  )
    else:
        if obj.FromGUI  :
            obj.enviaParaRespostaGUI(  'nenhum equipamento de hoje fora no momento'  ,  nomesColunas  =  []  )
def histHoje(obj):
    
    registro =  exe("select id, Funcionario, Ferramenta, identificador, HorarioSaida, HorarioRetorno from registroDeSaidasDeEquips where DataSaida = current_date()")
    registroTratado  =  trataRegistro(registro,obj)
    antes = '\no historico hoje é: \n\n'
    if obj.FromGUI:
        obj.enviaParaRespostaGUI(  registroTratado  ,  nomesColunas  =  [  'Funcionario'  ,  'Ferramenta'  ,  'HorarioSaida'  ,  'HorarioRetorno'  ] ,  antes  =  antes,identificador = True )
    else: 
        print(antes)
        printBonito(registroTratado)

def limpaRegistros(obj):
    
    querry = f"delete from registroDeSaidasDeEquips "
    
    if obj.dataInicio and not obj.dataFim:
        querry += f" where data >= {str(obj.dataInicio)}"
        
    elif not obj.dataInicio and obj.dataFim:
        querry += f" where data <= {str(obj.dataFim)}"

        
    exe(querry)

def separaFerramentaDeIdentificador(obj,palavra):
    palavraSemNumero  =  ''
    identificador     =  ''

    if palavra[-2:]    ==  'sn':
        
        identificador  =   'sn'
        palavraSemNumero  =  palavra[:-2]
        
        if palavraSemNumero in obj.ferEquipdb:
            print(f'a ferramenta {obj.ferEquipdb[palavraSemNumero]}({palavraSemNumero}) se encontra sem numero\n')
            registraFaltaDeNumeracao(palavraSemNumero)
        else:
            obj.possiveisEquipsParaRegistrar.append(palavraSemNumero)
            obj.verificarPossiveisEquips  =  True
    else:    
        for char in palavra:
            if not char.isdigit() and char  !=  '-' :
                palavraSemNumero  +=  char
            else:
                identificador     +=  char
                if char == '-':
                    palavraSemNumero+=str(identificador[:-1])
                    identificador = ''

    if identificador  == '' :
        identificador = 'sn'

    if palavraSemNumero == 'ch':
        palavraSemNumero +=  str(identificador)
        identificador     =  'sn'

    return [palavraSemNumero,identificador]

def analizaStringDeFerramenta(obj, palavra):
##    palavraSemNumero  =  ''
##    identificador     =  ''
##
##    if palavra[-2:]    ==  'sn':
##        
##        identificador  =   'sn'
##        palavraSemNumero  =  palavra[:-2]
##        
##        if palavraSemNumero in obj.ferEquipdb:
##            print(f'a ferramenta {obj.ferEquipdb[palavraSemNumero]}({palavraSemNumero}) se encontra sem numero\n')
##            registraFaltaDeNumeracao(palavraSemNumero)
##        else:
##            obj.possiveisEquipsParaRegistrar.append(palavraSemNumero)
##            obj.verificarPossiveisEquips  =  True
##    else:    
##        for char in palavra:
##            if not char.isdigit() and char  !=  '-' :
##                palavraSemNumero  +=  char
##            else:
##                identificador     +=  char
##                if char == '-':
##                    palavraSemNumero+=str(identificador[:-1])
##                    identificador = ''
##    if identificador  == '' :
##        identificador = 'sn'
##
##    if palavraSemNumero == 'ch':
##            palavraSemNumero +=  str(identificador)
##            identificador     =  'sn'
    debug  =  Debug()
    palavraSemNumero, identificador  =  separaFerramentaDeIdentificador(obj,palavra)
    
    if palavraSemNumero  in  obj.ferEquipdb:        
        obj.atualizaFerramentaAtual(  palavraSemNumero  ,  str(  identificador  )  )
        if debug.debug :
            print(f"{palavraSemNumero}-{identificador} foi posta nos equipamentos atuais")
                    
    else:
        obj.possiveisEquipsParaRegistrar.append(palavraSemNumero)
        obj.verificarPossiveisEquips  =  True


def cancelaRegistro(obj):
    print('falta implementar o cancelamento de registro')


