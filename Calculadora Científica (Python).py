import tkinter as tk
from tkinter import ttk, messagebox
import math
import re

class CalculadoraCientifica:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Científica")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        
        # Variáveis
        self.expressao = ""
        self.resultado_var = tk.StringVar()
        self.resultado_var.set("0")
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Criar interface
        self.criar_interface()
        
    def configurar_estilo(self):
        """Configura o estilo da calculadora"""
        self.root.configure(bg='#2c3e50')
        
    def criar_interface(self):
        """Cria a interface da calculadora"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Display
        display_frame = tk.Frame(main_frame, bg='#34495e', relief='sunken', bd=2)
        display_frame.pack(fill='x', pady=(0, 10))
        
        self.display = tk.Entry(
            display_frame,
            textvariable=self.resultado_var,
            font=('Arial', 20, 'bold'),
            justify='right',
            state='readonly',
            bg='#ecf0f1',
            fg='#2c3e50',
            relief='flat',
            bd=10
        )
        self.display.pack(fill='x', padx=5, pady=5)
        
        # Frame dos botões
        buttons_frame = tk.Frame(main_frame, bg='#2c3e50')
        buttons_frame.pack(expand=True, fill='both')
        
        # Definir botões
        self.criar_botoes(buttons_frame)
        
    def criar_botoes(self, parent):
        """Cria todos os botões da calculadora"""
        # Configuração dos botões
        botoes = [
            # Linha 1 - Funções científicas
            [('sin', '#e74c3c'), ('cos', '#e74c3c'), ('tan', '#e74c3c'), ('log', '#e74c3c'), ('ln', '#e74c3c')],
            # Linha 2 - Mais funções científicas
            [('√', '#e74c3c'), ('x²', '#e74c3c'), ('xʸ', '#e74c3c'), ('π', '#e74c3c'), ('e', '#e74c3c')],
            # Linha 3 - Controles
            [('(', '#95a5a6'), (')', '#95a5a6'), ('C', '#e67e22'), ('⌫', '#e67e22'), ('÷', '#3498db')],
            # Linha 4 - Números e operações
            [('7', '#ecf0f1'), ('8', '#ecf0f1'), ('9', '#ecf0f1'), ('×', '#3498db'), ('1/x', '#e74c3c')],
            # Linha 5
            [('4', '#ecf0f1'), ('5', '#ecf0f1'), ('6', '#ecf0f1'), ('-', '#3498db'), ('±', '#95a5a6')],
            # Linha 6
            [('1', '#ecf0f1'), ('2', '#ecf0f1'), ('3', '#ecf0f1'), ('+', '#3498db'), ('=', '#27ae60')],
            # Linha 7
            [('0', '#ecf0f1'), ('.', '#ecf0f1'), ('', ''), ('', ''), ('', '')]
        ]
        
        for i, linha in enumerate(botoes):
            for j, (texto, cor) in enumerate(linha):
                if texto:  # Se o texto não estiver vazio
                    if texto == '0':
                        # Botão 0 ocupa duas colunas
                        btn = self.criar_botao(parent, texto, cor, i, j, columnspan=2)
                    elif texto == '=':
                        # Botão = ocupa duas linhas
                        btn = self.criar_botao(parent, texto, cor, i-1, j, rowspan=2)
                    else:
                        btn = self.criar_botao(parent, texto, cor, i, j)
    
    def criar_botao(self, parent, texto, cor, linha, coluna, rowspan=1, columnspan=1):
        """Cria um botão individual"""
        # Cor do texto baseada na cor de fundo
        if cor == '#ecf0f1':  # Números
            text_color = '#2c3e50'
        else:
            text_color = 'white'
            
        btn = tk.Button(
            parent,
            text=texto,
            font=('Arial', 12, 'bold'),
            bg=cor,
            fg=text_color,
            relief='raised',
            bd=2,
            command=lambda t=texto: self.processar_clique(t)
        )
        
        btn.grid(
            row=linha, 
            column=coluna, 
            rowspan=rowspan, 
            columnspan=columnspan,
            sticky='nsew', 
            padx=2, 
            pady=2
        )
        
        # Configurar peso das linhas e colunas
        parent.grid_rowconfigure(linha, weight=1)
        parent.grid_columnconfigure(coluna, weight=1)
        
        return btn
    
    def processar_clique(self, valor):
        """Processa o clique nos botões"""
        try:
            if valor == 'C':
                self.limpar()
            elif valor == '⌫':
                self.apagar()
            elif valor == '=':
                self.calcular()
            elif valor in ['sin', 'cos', 'tan', 'log', 'ln', '√']:
                self.adicionar_funcao(valor)
            elif valor == 'π':
                self.adicionar_constante('π')
            elif valor == 'e':
                self.adicionar_constante('e')
            elif valor == 'x²':
                self.adicionar_operador('**2')
            elif valor == 'xʸ':
                self.adicionar_operador('**')
            elif valor == '1/x':
                self.adicionar_funcao('1/')
            elif valor == '±':
                self.trocar_sinal()
            elif valor == '×':
                self.adicionar_operador('*')
            elif valor == '÷':
                self.adicionar_operador('/')
            else:
                self.adicionar_valor(valor)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no processamento: {str(e)}")
    
    def limpar(self):
        """Limpa a expressão"""
        self.expressao = ""
        self.resultado_var.set("0")
    
    def apagar(self):
        """Apaga o último caractere"""
        if self.expressao:
            self.expressao = self.expressao[:-1]
            self.resultado_var.set(self.expressao if self.expressao else "0")
    
    def adicionar_valor(self, valor):
        """Adiciona um valor à expressão"""
        self.expressao += str(valor)
        self.resultado_var.set(self.expressao)
    
    def adicionar_operador(self, operador):
        """Adiciona um operador à expressão"""
        if self.expressao and self.expressao[-1] not in ['+', '-', '*', '/', '**']:
            self.expressao += operador
            self.resultado_var.set(self.expressao)
    
    def adicionar_funcao(self, funcao):
        """Adiciona uma função à expressão"""
        if funcao == '1/':
            self.expressao += '1/('
        else:
            self.expressao += f'{funcao}('
        self.resultado_var.set(self.expressao)
    
    def adicionar_constante(self, constante):
        """Adiciona uma constante à expressão"""
        if constante == 'π':
            self.expressao += str(math.pi)
        elif constante == 'e':
            self.expressao += str(math.e)
        self.resultado_var.set(self.expressao)
    
    def trocar_sinal(self):
        """Troca o sinal do último número"""
        if self.expressao:
            # Encontrar o último número
            match = re.search(r'(\d+\.?\d*)$', self.expressao)
            if match:
                numero = match.group(1)
                inicio = match.start()
                if inicio > 0 and self.expressao[inicio-1] == '-':
                    # Remove o sinal negativo
                    self.expressao = self.expressao[:inicio-1] + numero
                else:
                    # Adiciona o sinal negativo
                    self.expressao = self.expressao[:inicio] + '-' + numero
                self.resultado_var.set(self.expressao)
    
    def calcular(self):
        """Calcula o resultado da expressão"""
        try:
            if not self.expressao:
                return
            
            # Substituir funções por equivalentes em Python
            expressao_python = self.expressao
            expressao_python = expressao_python.replace('sin(', 'math.sin(math.radians(')
            expressao_python = expressao_python.replace('cos(', 'math.cos(math.radians(')
            expressao_python = expressao_python.replace('tan(', 'math.tan(math.radians(')
            expressao_python = expressao_python.replace('log(', 'math.log10(')
            expressao_python = expressao_python.replace('ln(', 'math.log(')
            expressao_python = expressao_python.replace('√(', 'math.sqrt(')
            
            # Contar parênteses para funções trigonométricas
            for func in ['sin', 'cos', 'tan']:
                count = expressao_python.count(f'math.{func}(math.radians(')
                expressao_python += ')' * count
            
            # Avaliar a expressão
            resultado = eval(expressao_python)
            
            # Formatar o resultado
            if isinstance(resultado, float):
                if resultado.is_integer():
                    resultado = int(resultado)
                else:
                    resultado = round(resultado, 10)
            
            self.resultado_var.set(str(resultado))
            self.expressao = str(resultado)
            
        except ZeroDivisionError:
            messagebox.showerror("Erro", "Divisão por zero!")
            self.limpar()
        except ValueError as e:
            messagebox.showerror("Erro", f"Erro matemático: {str(e)}")
            self.limpar()
        except Exception as e:
            messagebox.showerror("Erro", f"Expressão inválida: {str(e)}")
            self.limpar()

def main():
    """Função principal"""
    root = tk.Tk()
    app = CalculadoraCientifica(root)
    
    # Centralizar a janela
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
