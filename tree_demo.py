from tree_design import (TreeBuilder, InvalidBuildOperation)

# Demonstrando o uso de TreeBuilder. Ele vai criar uma árvore mock para o teste
# das demais funcionalidades ser feito.

dataset = ["datapoint_1", "datapoint_2", "datapoint_3"]

new_builder = TreeBuilder(dataset)

# Averiguando o estado atual do builder, após inicialização
print(f"Estado do builder recem-inicializado é do tipo {type(new_builder._state)}")

# Averiguando que o comportamento é de acordo com o estado atual
try:
    new_builder.start_prune()
except InvalidBuildOperation as e:
    print(f"Builder lançou uma exception por tentar executar uma operação inválida para o estado dele: {e}")
print("")


new_builder.start_split()


# Averiguando o novo estado do builder
print("")
print(f"Depois de executar a operação, verificando novo estado do builder: {type(new_builder._state)}")

# Averiguando que o comportamento é de acordo com o estado atual
try:
    new_builder.start_split()
except InvalidBuildOperation as e:
    print(f"Builder lançou uma exception por tentar executar uma operação inválida para o estado dele: {e}")
print("")


new_builder.start_prune()

# Averiguando o último estado do builder
print("")
print(f"Depois de executar a operação, verificando o novo estado do builder: {type(new_builder._state)}")

# Averiguando que nenhuma operação para mexer na árvore é válida agora
try:
    new_builder.start_prune()
except InvalidBuildOperation as e:
    print(f"Builder lançou uma exception por tentar executar uma operação inválida para o estado dele: {e}")

try:
    new_builder.start_split()
except InvalidBuildOperation as e:
    print(f"Builder lançou uma exception por tentar executar uma operação inválida para o estado dele: {e}")
#print(treeRoot)
