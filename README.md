📚 Códigos das Disciplinas: Transferência de Calor e Métodos Computacionais

📝 Descrição

Este repositório contém uma coleção de códigos, trabalhos e soluções de exercícios desenvolvidos durante as disciplinas de Transferência de Calor e Métodos Computacionais do curso de Engenharia. O objetivo é servir como um portfólio acadêmico e um recurso de consulta para os algoritmos e problemas estudados.

🏛️ Contexto Acadêmico

    Universidade: ``UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE

    Curso: ``ENGENHARIA QÚIMICA

    Disciplinas: Transferência de Calor e Métodos Computacionais


📂 Estrutura do Repositório

O repositório está organizado em duas pastas principais, uma para cada disciplina. Dentro de cada pasta, os códigos são agrupados por tópicos ou listas de exercícios.

/
├── 📁 Transferencia_de_Calor/
│   ├── 01-Conducao/
│   │   ├── ex_parede_plana.py
│   │   └── ex_aleta_retangular.py
│   ├── 02-Conveccao/
│   │   └── ...
│   └── 03-Radiacao/
│       └── ...
│
├── 📁 Metodos_Computacionais/
│   ├── 01-Zeros_de_Funcoes/
│   │   ├── metodo_bisseccao.py
│   │   └── metodo_newton_raphson.py
│   ├── 02-Sistemas_Lineares/
│   │   └── metodo_gauss_seidel.py
│   └── 03-Integracao_Numerica/
│       └── ...
│


📖 Tópicos Abordados

Abaixo estão listados os principais tópicos e problemas resolvidos nos códigos deste repositório.

🔥 Transferência de Calor

    Condução:

        Condução unidimensional em regime permanente (paredes planas, cilindros, esferas).

        Sistemas com geração interna de calor.

        Análise de aletas (eficiência e efetividade).

        Condução bidimensional (métodos numéricos, fator de forma).

        Condução transiente (método da capacitância global, soluções analíticas).

    Convecção:

        Cálculo de coeficientes de convecção para escoamento interno e externo.

        Convecção natural e forçada.

        Análise de trocadores de calor (método da Média Logarítmica das Diferenças de Temperatura - MLDT e método da Efetividade-NTU).

    Radiação:

        Leis de Planck, Stefan-Boltzmann e Wien.

        Cálculo de fator de forma.

        Troca de calor por radiação entre superfícies.

    Métodos Numéricos em Transferência de Calor:

        Método das Diferenças Finitas para problemas de condução.

💻 Métodos Computacionais

    Zeros de Funções:

        Método da Bissecção.

        Método de Newton-Raphson.

        Método da Secante.

    Sistemas de Equações Lineares:

        Métodos diretos (Eliminação de Gauss).

        Métodos iterativos (Gauss-Jacobi, Gauss-Seidel).

    Interpolação e Ajuste de Curvas:

        Interpolação Polinomial (Polinômios de Lagrange e Newton).

        Regressão Linear (Método dos Mínimos Quadrados).

    Integração Numérica:

        Regra do Trapézio (simples e repetida).

        Regra de 1/3 e 3/8 de Simpson (simples e repetida).

    Solução Numérica de Equações Diferenciais Ordinárias (EDOs):

        Método de Euler.

        Métodos de Runge-Kutta de 2ª e 4ª ordem.

🛠️ Pré-requisitos e Instalação

A maioria dos códigos foi desenvolvida em Python 3. As seguintes bibliotecas são necessárias para a execução dos scripts:

    NumPy: Para cálculos numéricos e manipulação de arrays.

    Matplotlib: Para a geração de gráficos.

    SciPy: Para funções científicas e de engenharia.

Para instalar todas as dependências, você pode criar um arquivo requirements.txt e usar o pip:

    Clone o repositório:
    Bash

git clone https://github.com/seu-usuario/seu-repositorio.git

Navegue até a pasta do projeto:
Bash

cd seu-repositorio

Instale as dependências (recomendado usar um ambiente virtual):
Bash

    pip install -r requirements.txt

    (Se o arquivo requirements.txt não existir, você pode instalar as bibliotecas manualmente: pip install numpy matplotlib scipy)

🚀 Como Usar

Para executar um script específico, navegue até a pasta correspondente e execute o arquivo Python.

Exemplo:
Bash

# Navegue para a pasta de um dos métodos
cd Metodos_Computacionais/01-Zeros_de_Funcoes/

# Execute o script
python metodo_bisseccao.py

A maioria dos scripts contém exemplos de uso em seus próprios corpos ou em comentários, explicando as entradas e saídas esperadas.

🤝 Como Contribuir

Este é um repositório primariamente para fins de documentação pessoal e acadêmica. No entanto, se você encontrar algum erro, tiver uma sugestão de melhoria ou uma implementação mais eficiente, sinta-se à vontade para abrir uma Issue ou um Pull Request.

    Faça um Fork do projeto.

    Crie uma nova Branch (git checkout -b feature/sua-feature).

    Faça o Commit das suas alterações (git commit -m 'Adiciona nova feature').

    Faça o Push para a Branch (git push origin feature/sua-feature).

    Abra um Pull Request.

🧑‍💻 Autor

    Nome: ``

    GitHub: @seu-usuario

    LinkedIn: Seu Nome

⚖️ Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes. Isso significa que você é livre para usar, modificar e distribuir o código, desde que dê o devido crédito.
