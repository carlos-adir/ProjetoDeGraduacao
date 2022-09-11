# Poisson

Nesta pasta contém os códigos e resultados obtidos rodando em paralelo.
Para tratamento de dados, temos os códigos escritos em python.

### Códigos em C

```
poisson2D_ksp.c
poisson3D_ksp.c
```

### Resultados obtidos

Foram rodadas diversas vezes e temos diversas pastas, que na ordem que foram feitas são

* ```results_2022-07-04-11-02```
* ```results_2022-07-07-09-48```
* ```results_eder_2022-07-10-17-20```
* ```results_2022-07-16-20-03```
* ```results_googlecloud8-2022-07-24```
* ```results-e2standard8-12-08-2022```
* ```results-e2standard8-16-08-2022```
* ```results-e2memory8-22-08-2022```
* ```results-e2memory8-23-08-2022```
* ```results-e2memory8-26-08-2022```




### Códigos em python

A decisão de fazer códigos em ```python``` se deve principalmente à sua simplicidade para abrir arquivos, fazer a leitura usando ```re```(Regular expressions) e mostrar os gráficos de forma mais fácil.
As bibliotecas usadas são:

* ```re``` - Leitura dos arquivos
* ```numpy``` - Operações com vetores
* ```matplotlib``` - Mostrar gráficos
* ```compmec.nurbs``` - Utilizar Splines

Os arquivos que usamos são

* ```show_results.py``` - Principal. Contém varias ```main``` e plota os resultados lidos
* ```read_data_from_files.py``` - Contém as funções que leem os arquivos de resultados.
* ```removenonusefulfiles.py``` - Usado no ```makefile``` para deletar os arquivos que deram erro. Frequentemente por causa de falta de memória ou porque o processo foi cancelado apertando ```Ctrl+C```
* ```plot_theoriccurves.py``` - Plota apenas os gráficos teóricos, sem precisar dos arquivos base
* ```renamefolder.py``` - Renomeia a pasta de ```results``` para ```results-ano-mes-dia-hora-minuto```. O objetivo inicial era rodar o ```makefile``` várias vezes seguidas sem se preocupar com a sobreescrita de arquivos, visto que a cada fim de calculo, a pasta seria renomeada.

### Como rodar

A maneira mais simples é digitar ```make``` no terminal.
Tomará bastante tempo.

Para modificar os parâmetros, vá dentro do arquivo ```makefile```, onde há configurações quanto ao tamanho da malha.
