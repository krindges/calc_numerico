import streamlit as st
import numpy as np
import sympy as sp
import plotly.graph_objects as go

# Título do app
st.title("📌 Zeros de função: Método da Bissecção")

# Entrada da função pelo usuário
st.subheader("Digite a função f(x):")
func_str = st.text_input("Exemplo: x**3 - 5*x + 2", "x**3 - 5*x + 2")

# Intervalo para o gráfico
x1 = st.number_input("Exemplo: -3", value=-3.0, step=0.1, format="%.1f")
x2 = st.number_input("Exemplo: 3", value=3.0, step=0.1, format="%.1f")

# Definir variável simbólica
x = sp.symbols('x')

try:
    # Converter string para expressão simbólica
    func_expr = sp.sympify(func_str)

    # Converter para função NumPy
    f_lambdified = sp.lambdify(x, func_expr, "numpy")

    # Criar gráfico da função com Plotly
    st.subheader("📈 Gráfico da Função")

    # Gerar pontos da função
    x_vals = np.linspace(x1, x2, 400)
    y_vals = f_lambdified(x_vals)

    # Criar o gráfico interativo
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f"f(x) = {func_expr}"))

    # Adicionar linha horizontal e vertical no eixo 0
    fig.add_shape(type="line", x0=x1, x1=x2, y0=0, y1=0, line=dict(color="black", width=1))
    fig.add_shape(type="line", x0=0, x1=0, y0=min(y_vals), y1=max(y_vals), line=dict(color="black", width=1))

    # Layout do gráfico
    fig.update_layout(
        title="Gráfico da Função",
        xaxis_title="x",
        yaxis_title="f(x)",
        template="plotly_white",
        showlegend=True
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Entrada do intervalo [a, b]
    st.subheader("⚙️ Escolha o Intervalo para a Bissecção")
    a = st.number_input("Digite o valor de a:", value=0.0, step=0.1, format="%.1f")
    b = st.number_input("Digite o valor de b:", value=2.0, step=0.1, format="%.1f")
    tol = st.number_input("Precisão (tolerância):", value=1.0e-6, step=1.0e-7, format="%.2e")
    max_iter = st.number_input("Número máximo de iterações:", value=100, step=1)

    # Botão para calcular a raiz
    if st.button("🔍 Encontrar Raiz"):
        # Verificar se o intervalo contém uma raiz
        if f_lambdified(a) * f_lambdified(b) >= 0:
            st.error("O intervalo [a, b] não contém uma raiz válida. Escolha outro intervalo.")
        else:
            # Método da Bissecção
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
