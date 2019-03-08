import matplotlib.pyplot as plt

names = ['Aproximado', 'Certo', 'Errado']
values = [12, 13, 4]

plt.ylabel('# Respostas por categoria')
plt.bar(names, values)
plt.show()