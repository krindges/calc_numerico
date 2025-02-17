import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

# Título do app
st.title("📌 Método da Bissecção para Encontrar Raízes")

# Entrada da função pelo usuário
st.subheader("Digite a função f(x):")
func_str = st.text_input("Exemplo: x**3 - 5*x + 2", "x**3 - 5*x + 2")

# Definir variável simbólica
x = sp.symbols('x')

try:
    # Converter string para expressão simbólica
    func_expr = sp.sympify(func_str)

    # Converter para função NumPy
    f_lambdified = sp.lambdify(x, func_expr, "numpy")

    # Criar gráfico da função
    st.subheader("📈 Gráfico da Função")
    fig, ax = plt.subplots(figsize=(6, 4))
    
    x_vals = np.linspace(-10, 10, 400)
    y_vals = f_lambdified(x_vals)
    
    ax.axhline(0, color='black', linewidth=1)  # Linha horizontal
    ax.axvline(0, color='black', linewidth=1)  # Linha vertical
    ax.plot(x_vals, y_vals, label=f"f(x) = {func_expr}")
    ax.legend()
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid()

    st.pyplot(fig)  # Exibir gráfico no Streamlit

    # Entrada do intervalo [a, b]
    st.subheader("⚙️ Escolha o Intervalo para a Bissecção")
    a = st.number_input("Digite o valor de a:", value=0.0, step=0.1)
    b = st.number_input("Digite o valor de b:", value=2.0, step=0.1)

    # Botão para calcular a raiz
    if st.button("🔍 Encontrar Raiz"):
        # Verificar se o intervalo contém uma raiz
        if f_lambdified(a) * f_lambdified(b) >= 0:
            st.error("O intervalo [a, b] não contém uma raiz válida. Escolha outro intervalo.")
        else:
            # Método da Bissecção
            tol = 1e-6  # Precisão
            max_iter = 100  # Número máximo de iterações
            iteracoes = 0
            while (b - a) / 2 > tol and iteracoes < max_iter:
                c = (a + b) / 2  # Ponto médio
                if f_lambdified(c) == 0:
                    break  # Encontrou a raiz exata
                elif f_lambdified(a) * f_lambdified(c) < 0:
                    b = c  # Nova extremidade direita
                else:
                    a = c  # Nova extremidade esquerda
                iteracoes += 1

            raiz = (a + b) / 2  # Aproximação final
            st.success(f"✅ Raiz encontrada: {raiz:.6f} em {iteracoes} iterações.")
except Exception as e:
    st.error(f"Erro ao processar a função: {e}")
