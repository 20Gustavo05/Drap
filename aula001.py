# exercicio 1
with open("dna.txt", "w") as arquivo:
    arquivo.write("AATCTGCAC")

with open("dna.txt", "r") as arquivo:
    dna = arquivo.read().strip()

dna_inverso = dna[::-1]

print('Entrada: {}'.format(dna))
print('Saida: {}'.format(dna_inverso))

# exercicio 2
dna1 = str(input('Digite seu nome completo: ')).strip().capitalize()
separar = dna1.split()
unir = ''.join(separar)

print(unir)
print('Olá {}, seu nome completo tem {} letras.'.format(separar[0], len(unir)))

# exercicio 3
dna2 = str(input('Digite o nome completo do seu Pai: ')).strip().capitalize()
separar = dna2.split()
unir = '_'.join(separar)

print("Nova formatação, ('{}').".format(unir))

# exercicio 4
dna3 = str(input('Digite as 7 coisas que você mais gosta (não utilize de virgulas para separar os elementos): ')).strip()
separar = dna3.split()

print('Aqui está uma lista com as 7 coisas que você escreveu {}.'.format(separar))