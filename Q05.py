import networkx as nx
from random import choice

def change_costs_factor(ddc, c):
    
    if not isinstance(ddc, nx.DiGraph) or c not in list(ddc.nodes()): return None
    
    #Soma todos os fatores relevantes para o custo da manutenção
    custo = 1 + numero_ciclos(ddc,c) + numero_tangles(ddc,c) + numero_dependentes(ddc, c)
    return custo

#numero_dependentes calcula o numero de dependentes de uma classe especifica e retorna o custo para a manutenção.
def numero_dependentes(ddc, c):
    dependentes = []
    #Lista inicialmente os predecessores diretos (dependentes) da classe, no decorrer da execução adiciona também os indiretos
    all_predesseccors = list(ddc.predecessors(c))
    
    while all_predesseccors:
        #Escolhe aleatoriamente um dos predecessores da classe
        node = choice(all_predesseccors)
        #Adiciona na lista de dependentes desta classe
        dependentes.append(node)
        #Lista os predecessores desta classe que ja é uma predecessora da classe inicial, ou seja, os 
        #predecessores indiretos (dependentes indiretos).
        predeccessors_indiretos = list(ddc.predecessors(node))
        
        #Itera sobre os predecessores indiretos
        for predeccessor_indireto in predeccessors_indiretos:
            #Se este prede. indireto não esta ainda nas lista de dependentes e não esta na lista de 
            #all_predecessor e ele não é a propia classe inicial, significa que este predecessor não 
            #foi analisado ainda, então, adicionamos na lista all_predecessor
            if predeccessor_indireto not in dependentes and predeccessor_indireto not in all_predesseccors and predeccessor_indireto != c:
                all_predesseccors.append(predeccessor_indireto)
        #Removemos a classe analisada
        all_predesseccors.remove(node) 
        
    return len(dependentes)

#numero_ciclos calcula a quantidade de ciclos de dependencia minima que a classe participa e retorna seu custo para manutenção. 
def numero_ciclos(ddc,c):
    num_ciclos = 0
    #Lista o numero de ciclos simples que a classe participa
    ciclos = list(nx.recursive_simple_cycles(ddc))
    #Soma-se 10 para cada ciclo simples que classe participa
    for ciclo in ciclos:
        if c in ciclo:
            num_ciclos += 10
            
    return num_ciclos

#numero_tangles calcula a quantidade de tangles e retorna seu custo para a manutenção.
def numero_tangles(ddc,c):
    num_tangles = 0 
    #Lista todos os componentes fortes do grafo
    tangles = list(nx.strongly_connected_components(ddc))
    #Se a classe esta presente no componente forte e ele tem tamanho maior que 3 consideramos como um tangle
    # e soma-se 50.
    for tangle in tangles:
        if len(tangle) > 3 and c in tangle:
            num_tangles += 50
    return num_tangles