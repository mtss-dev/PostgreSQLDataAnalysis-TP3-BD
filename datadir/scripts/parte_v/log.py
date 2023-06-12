import re

# Lê o conteúdo do arquivo de log
with open('log.txt', 'r') as file:
    log_content = file.read()

# Encontra todos os números que aparecem depois de 'Thread_n' usando uma expressão regular
pattern = r'Thread_\d+:\s(\d+)'
matches = re.findall(pattern, log_content)

# Converte os números em inteiros e os ordena em ordem crescente
numbers = [int(match) for match in matches]
numbers.sort()
unique_numbers = list(set(numbers))

# Imprime os números em ordem crescente
expected_numbers = list(range(1, 201))
for i in range(0, 200):
    if(i+1 == numbers[i]):
        print(f"EM POSICAO {i+1}, {numbers[i]}")
    else:
        print(f"OUT OUT OUT: {i+1}, {numbers[i]}")

