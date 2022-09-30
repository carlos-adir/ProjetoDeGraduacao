# Projeto de Gradução

Este trabalho foi desenvolvido como o Trabalho e Conclusão de Curso (TCC) da Engenharia Mecânica na Universidade de Brasília.
O relatório deste trabalho pode ser acesso através do link: 

### Do que se trata?

O tema do trabalho, **Programação Paralela para Resolução de Equações Diferenciais Parciais pelo Método de Diferenças Finitas**
faz implementação em C utilizando o PETSc da solução MDF da equação de Poisson.
Então, lançamos diversos calculos e analisamos os resultados.
O resumo do trabalho é dado por:

> A programação paralela hoje é uma das alternativas usadas para aumentar a velocidade de cálculo em face do previsível fim da lei de Moore.
> Bibliotecas de alto nível, como o PETSc utilizado por este trabalho, fornece ferramentas que diminuem a necessidade de programadores paralelos experientes para desenvolver algoritmos eficientes.
> Neste trabalho, usamos o PETSc com a linguagem C para implementar a solução numérica 2D e 3D da Equação de Poisson usando o Método das Diferenças Finitas em uma malha estruturada.
> Foram efetuados cálculos utilizando máquinas do Google Cloud com até 8 processadores, com malhas de até 125 milhões de pontos e analisamos o código utilizando métricas como Lei de Amdahl e de Karp-Flatt.
> Os resultados 2D obtidos indicaram uma eficiência próxima de 1.
> Já para o 3D, a comunicação entre os processadores consumiu cerca de 20% do tempo total limitando a aceleração.
> Foi observado em ambos casos o fenômeno de aceleração superlinear para valores específicos de tamanho da malha.


### Como usar?

Os códigos foram testados utilizando o Ubuntu (Linux) a no google cloud através de SSH.
Assim, primeiro instalamos

```
cd ~
mkdir Git
cd Git
git clone https://github.com/carlos-adir/ProjetoDeGraduacao
cd ProjetoDeGraduacao
make
```

**PS:**
* Foi testado em apenas ambiente Linux. Não se sabe se em windows e mac o comando é o mesmo
* No GoogleColab, fazendo ```cd ~``` direciona à pasta ```/root``` e não ```/home/```. Desta forma, dentro do ```makefile``` é necessário trocar ```HOME_DIR?=${shell cd ~ && pwd}``` para ```HOME_DIR?="/content/"``` 

E então para rodar um código, tem um ```makefile``` dentro da pasta ```Poisson``` que já lança o calculo para diversos

```
cd Poisson
make
```

### Dicas

* Se utilizar o Google Cloud por SSH, é interessante lançar o calculo e fechar a janela (para o computador não ficar preso). Para fazer isso, instale o ```screen``` e o execute antes de lançar o cálculo:

> ```
> sudo apt-get install screen
> screen
> cd Poisson
> make
> ```
> 
> Então ```Press Ctrl+A Ctrl+D``` e pode fechar a janela do SSH.
> Para retormar o trabalho, acesse novamente por SSH e digite
> 
> ```
> screen -r
> ```
> 
> Informação retirada do  [stackoverflow](https://stackoverflow.com/questions/48221807/google-cloud-instance-terminate-after-close-browser)

### Contato

Envie-me email a ```carlos.adir.leite@gmail.com``` com a tag ```[UnB][PG] - Assunto```
