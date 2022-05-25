
arq = open('fat16_1sectorpercluster.img', 'rb')

fat_bs = arq.read(36)



bytes_per_sector  = int.from_bytes(fat_bs[11:13], "little")
sector_per_cluster = fat_bs[13]
num_sector_reserved = int.from_bytes(fat_bs[14:16], "little")
num_fat = fat_bs[16]
num_entries_dir = int.from_bytes(fat_bs[17:19], "little")
total_sectors = int.from_bytes(fat_bs[19:21], "little")
sector_per_fat = int.from_bytes(fat_bs[22:24], "little")

arq.seek((bytes_per_sector*num_sector_reserved))

fat = arq.read(num_fat * sector_per_fat * bytes_per_sector)

num_sector_rootDir = int((num_entries_dir *32)/bytes_per_sector)
 

rootDir = arq.read(num_sector_rootDir * bytes_per_sector)

# print(rootDir)
# print(bytes_per_sector)
# print(sector_per_cluster)
# print(num_sector_reserved)
# print(num_fat)
# print(num_entries_dir)
# print(total_sectors)
# print(sector_per_fat)
pos_in = 0
lista_arquivos = []
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
arq.close()