def comeco():
    # arq = open('fat16_1sectorpercluster.img', 'rb')
    arq = open('fat16_4sectorpercluster.img', 'rb')

    fat_bs = arq.read(36)
    global bytes_per_sector, sector_per_cluster, num_sector_reserved, num_fat, num_entries_dir, total_sectors, sector_per_fat, fat, rootDir, dados

    bytes_per_sector  = int.from_bytes(fat_bs[11:13], "little")
    sector_per_cluster = fat_bs[13]
    num_sector_reserved = int.from_bytes(fat_bs[14:16], "little")
    num_fat = fat_bs[16]
    num_entries_dir = int.from_bytes(fat_bs[17:19], "little")
    total_sectors = int.from_bytes(fat_bs[19:21], "little")
    sector_per_fat = int.from_bytes(fat_bs[22:24], "little")

    arq.seek((bytes_per_sector*num_sector_reserved))
    # pega conteudo da fat
    fat = arq.read(num_fat * sector_per_fat * bytes_per_sector)

    num_sector_rootDir = int((num_entries_dir *32)/bytes_per_sector)
    
    # pega conteudo do rootDir
    rootDir = arq.read(num_sector_rootDir * bytes_per_sector)

    # print(rootDir)
    # print(bytes_per_sector)
    # print(sector_per_cluster)
    # print(num_sector_reserved)
    # print(num_fat)
    # print(num_entries_dir)
    # print(total_sectors)
    # print(sector_per_fat)
    inicio_dados = arq.tell()

    num_final = arq.seek(0,2)
    arq.seek(inicio_dados,0)

    dados = arq.read(num_final - inicio_dados)
    verifica_arquivo(0,arq, rootDir, 0)
 

    

    arq.close()
def mostrar_conteudo(arq, conteudo_arq, flag):
    global fat
    # pega o conteudo dos clusters na fat
    print(f"conteudoarq: {conteudo_arq}")
    first_cluster = conteudo_arq[4]
    entradaFirst_cluster = int.from_bytes(fat[first_cluster*2:first_cluster*2+2], "little")
    lista_cluster = []
    lista_cluster.append(first_cluster)

    while entradaFirst_cluster < 65528:
        lista_cluster.append(entradaFirst_cluster)
        entradaFirst_cluster = int.from_bytes(fat[entradaFirst_cluster*2:entradaFirst_cluster*2+2], "little")

    print(f"listacluster: {lista_cluster}")
    
    conteudo = ''

    
    
    # print(dados)
    for cluster in lista_cluster:
        
        if conteudo_arq[2] == 'arquivo':
            if flag == 0:
                ini_dados = ((cluster-2)*sector_per_cluster*bytes_per_sector) - 2*sector_per_cluster*bytes_per_sector
                final_dados = ((cluster-1)*sector_per_cluster*bytes_per_sector)- 2*sector_per_cluster*bytes_per_sector
            else: 
                ini_dados = ((cluster-2)*sector_per_cluster*bytes_per_sector) 
                final_dados = ((cluster-1)*sector_per_cluster*bytes_per_sector)
                print(f"inidados:{ini_dados}")
            byte_cluster = dados[ini_dados:final_dados]
            conteudo = conteudo + byte_cluster.decode("utf-8")
            print(f"conteudo {conteudo}")
            
        # se diretorio
        else: 
            ini_dados = ((cluster-2)*sector_per_cluster*bytes_per_sector)
            print(ini_dados)
            verifica_arquivo(ini_dados, arq, dados,1)
      

def verifica_arquivo(pos_in, arq, rootDir, flag):
    global dados
    lista_arquivos = []
    # veirifica o tipo de arquivo e se tem algo
    print(pos_in)
    while(rootDir[pos_in] != 0):
        list_inter = []
        if rootDir[pos_in] == 229 or rootDir[pos_in+11] == 15:
            pos_in +=32
            continue
        elif rootDir[pos_in+11] == 16:
            tipo = "diretorio"
            
        elif rootDir[pos_in+11] == 32:
            # arquivo
            tipo = "arquivo"
    
        if rootDir[pos_in + 8] == 32:
            extensao = ' '
        else:
            extensao = rootDir[pos_in + 8:pos_in + 11].decode("utf-8")
        nome = rootDir[pos_in:pos_in + 8].decode("utf-8")
        tamanho_arquivo = int.from_bytes(rootDir[pos_in + 28:pos_in + 32], "little")
        first_cluster = int.from_bytes(rootDir[pos_in + 26:pos_in + 28], "little")
        
        list_inter = [nome, extensao, tipo, tamanho_arquivo, first_cluster]
        pos_in +=32
        lista_arquivos.append(list_inter)

    print(lista_arquivos)
    aux = 0
    for arquivo in lista_arquivos:
        print(f"{aux} - Nome: {arquivo[0]} | Extensao: {arquivo[1]} | Tipo: {arquivo[2]} | Tamanho: {arquivo[3]} | First_cluster: {arquivo[4]}")
        aux +=1

    resp = int(input("Insira o numero do arquivo que deseja visualizar: \n"))
    mostrar_conteudo(arq, lista_arquivos[resp], flag)
if __name__ == '__main__':
    comeco()