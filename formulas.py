 #Universidad Nacional Autónoma de México
 #Facultad de Ciencias
 #Licenciatura en Ciencias de la Computación
 #Estructuras Discretas 
 #Practica7  - Tablas de verdad y LaTeX
 #Escrito por: Hernandez Vazquez Diego y Bruno Bernardo Soto Lugo
from typing import List
from itertools import product
import pathlib
from pathlib import Path #para la función LaTeX 

Asignacion = List[bool]


class Formula:
    """Clase para representar fórmulas booleanas."""
    def __init__(self, izquierda, conectivo=None, derecha=None):
        """Constructor para la clase. En el caso de las variables, izquierda es
        el identificador de la variable, el cual debe ser un entero, y los
        demás argumentos deben ser None. El atributo conectivo debe ser un
        string, 'C'(onjunción), 'D'(isyunción), 'I'(mplicación), 'N'(egación) o
        'B'(icondicional). Para cualquier fórmula que no sea una variable, el
        atributo izquierda debe ser una fórmula, y para las fórmulas con
        conectivo distinto a 'N', el atributo derecho también tiene que ser una
        fórmula.

        """
        conectivos = ['C', 'D', 'I', 'B', 'N']

        # variables
        if conectivo is None:
            if not isinstance(izquierda, int) and izquierda < 0:
                raise TypeError("Las variables deben ser números naturales.")
        # fórmulas
        else:
            if conectivo not in conectivos:
                raise ValueError(f"El conectivo {conectivo} es incorrecto.")
            if not isinstance(izquierda, Formula):
                raise TypeError(f"{izquierda} no es de tipo fórmula.")
            # negación unaria
            if conectivo == 'N' and derecha is not None:
                raise TypeError(
                    "No debe existir una fórmula derecha en la negación."
                )
            # conectivos binarios
            if conectivo != 'N' and not isinstance(derecha, Formula):
                raise TypeError(f"{derecha} no es de tipo fórmula.")
        self.izquierda = izquierda
        self.conectivo = conectivo
        self.derecha = derecha

#-----------------------------FUNCIONES PRÁCTICA 1------------------------------

    def __repr__(self):
        """Representación en cadena, legible para humanos, de las fórmulas."""
        return ""

    def lista_variables(self):
        """Devuelve la lista de todas las variables de una fórmula en orden."""
        return []

    def mayor_variable(self):
        """Devuelve la variable más grande que ocurre en una fórmula."""
        return 0

    def numero_conectivos(self):
        """Devuelve el número de conectivos que ocurren en la fórmula."""
        return 0

    def _evalua_aux(self, asignacion: Asignacion, variables: List[int]):
        """Función auxiliar para evaluar una fórmula. Recibe una lista de
        booleanos (una asignación de verdad), y una lista con los números de
        las variables correspondientes.
        Eg. _evalua_aux([0, 1, 1], [1, 2, 5]) corresponde a:
        x1 = 0
        x2 = 1
        x5 = 1
        """
        return False

    def evalua(self, asignacion: Asignacion):
        """Devuelve el valor de verdad de la fórmula bajo una
        asignación dada, que recibe como entrada en la forma
        de una lista de booleanos.
        """
        return False

    def aplana(self):
        """Devuelve una lista con la versión aplanada del árbol
        de sintáxis de la fórmula en preorden.
        """
        return []

    def aplana_sin_variables(self):
        """Devuelve una lista con la versión aplananada del
        árbol de sintaxis de la fórmula, sin las hojas.
        """
        return []

#-----------------------------FUNCIONES PRÁCTICA 2------------------------------

    def _evalua_sub_aux(self, asignacion: Asignacion, variables: List[int],
                        resultado: dict['Formula', bool]):
        """Función auxiliar para evaluar a la fórmula y todas sus subfórmulas.
        Recibe como entrada una lista de booleanos (asignación de verdad), una
        lista con las variables en las que ocurren las variables, y una lista
        de las subfórmulas de la fórmula. Resultado asocia a cada subfórmula
        su valor de verdad bajo la asignación, como los diccionarios son
        mutables pueden devolverlo o simplemente modificarlo en su función.

        Se sacaria una variable donde busco su posición y saco su valor de asignacion. 
        Guardo el resultado[self] = valor.
        - Si es una negación evalúo la subfórmula izquierda, luego calculo el valor de la subfórmula.
        - Si es un conectivo evalúo recursivamente izquierda y derecha, luego calculo el valor según el conectivo y lo guardo.
        """
        # Caso hoja: variable
        if self.conectivo is None:
            # busco la posición de la variable (número) en la lista de variables
            pos = None
            for i, num in enumerate(variables):
                if num == self.izquierda:
                    pos = i
                    break
            if pos is None:
                # esto no debería pasar si lista_variables() está bien
                raise ValueError("La variable no está en la lista de variables.")
            valor = asignacion[pos]
            if self not in resultado:
                resultado[self] = valor
            return

        # Caso negación: evaluo la subfórmula izquierda primero
        if self.conectivo == 'N':
            self.izquierda._evalua_sub_aux(asignacion, variables, resultado)
            # calculo mi valor a partir del valor de la subfórmula
            val_sub = resultado[self.izquierda]
            val = not val_sub
            if self not in resultado:
                resultado[self] = val
            return

        # Caso binario: evaluo ambas ramas primero
        self.izquierda._evalua_sub_aux(asignacion, variables, resultado)
        self.derecha._evalua_sub_aux(asignacion, variables, resultado)

        left_val = resultado[self.izquierda]
        right_val = resultado[self.derecha]

        # calculo según el conectivo (como principiante lo hago con ifs)
        if self.conectivo == 'C':   # conjunción
            val = left_val and right_val
        elif self.conectivo == 'D': # disyunción
            val = left_val or right_val
        elif self.conectivo == 'I': # implicación (¬A ∨ B)
            val = (not left_val) or right_val
        elif self.conectivo == 'B': # bicondicional
            val = (left_val and right_val) or (not left_val and not right_val)
        else:
            # no debería llegar aquí por las comprobaciones del constructor
            raise ValueError(f"Conectivo desconocido: {self.conectivo}")

        if self not in resultado:
            resultado[self] = val
        return
    
    def evalua_sub(self, asignacion):
        """Recibe como entrada una lista de booleanos (asignación de verdad) y
        devuelve un diccionario con las fórmulas como llaves y sus valores de
        verdad como valores. Las entradas de esta lista de booleanos
        corresponden con las variables de la fórmula original. La finalidad de
        esta función es generar los renglones de la tabla de verdad
        correspondiente.
        """
         # obtengo la lista de variables (en el orden esperado por 'asignacion')
        variables = self.lista_variables()
        resultado: dict['Formula', bool] = {}
        # llamo a la función recursiva que va llenando el diccionario
        self._evalua_sub_aux(asignacion, variables, resultado)
        return resultado

    def tex_formula(self):
        """Devuelve la fórmula con los separadores necesarios para crear la
        tabla en LaTeX.
        Solo hay 3 casoscposibles: variable, negación, binario.
        - Caso variable: retorno x_{n}
        - Caso negación: pongo la posición izquierda vacía y el operador \lnot
        - Caso binario: obtengo las dos partes recursivamente y las uno
           con el símbolo correspondiente. 

        """
        # Caso variable: retorno x_{n}
        if self.conectivo is None:
            return f'x_{{{self.izquierda}}}'

        # Caso negación: pongo la posición izquierda vacía y el operador \lnot
        if self.conectivo == 'N':
            sub_tex = self.izquierda.tex_formula()
            return f'( & \\lnot & {sub_tex})'

        # Caso binario: obtengo las dos partes recursivamente y las uno
        left_tex = self.izquierda.tex_formula()
        right_tex = self.derecha.tex_formula()

        # mapeo de conectivos en latec
        if self.conectivo == 'C':
            simbolo = r'\land'
        elif self.conectivo == 'D':
            simbolo = r'\lor'
        elif self.conectivo == 'I':
            simbolo = r'\to'
        elif self.conectivo == 'B':
            simbolo = r'\leftrightarrow'
        else:
            # esto no debería pasar por las comprobaciones del constructor
            raise ValueError(f"Conectivo desconocido: {self.conectivo}")

        return f'({left_tex} & {simbolo} & {right_tex})'

    def _cabecera_tabla(self):
        """Devuelve la cabecera de la tabla de verdad en formato de tabla de
        LaTeX.
        
        Hacemos listas pequeñas para entender bien cómo queda la cadena final. 
        """ 
        # obtengo la lista de variables:
        vars_list = self.lista_variables()

        # se construye las partes para las variables,
        partes = []
        for n in vars_list:
            partes.append(f'x_{{{n}}}')

        # fórmula completa en TeX
        formula_tex = self.tex_formula()

        # si hay variables, las junto y añado la fórmula
        if partes:
            header = '  ' + ' & '.join(partes) + ' & ' + formula_tex + ' \\\\\n'
        else:
            header = '  ' + formula_tex + ' \\\\\n'

        return header
        


    def _renglon_verdad(self, asignacion):
        """Devuelve un renglón de la tabla de verdad de la fórmula,
        en formato de tabla de LaTeX, correspondiente a la
        asignación de verdad recibida.
        """
        # Convertir True/False a '1'/'0'
        vars_order = self.lista_variables()
        valores_vars = []
        for i in range(len(vars_order)):
            valores_vars.append('1' if asignacion[i] else '0')

        inicio = '  ' + ' & '.join(valores_vars)

        # representación TeX de la fórmula completa
        cuerpo_tex = self.tex_formula()

        evals = self.evalua_sub(asignacion)

        # subfórmulas internas en orden
        subs = self.aplana_sin_variables()

        # se reemplaza cada subfórmula por su valor de verdad
        for sub in subs:
            tex_sub = sub.tex_formula()
            val = '1' if evals.get(sub, False) else '0'
            if sub is self:
                reemplazo = r'\mathbf{' + val + r'}'
            else:
                reemplazo = val
            # se reemplaza la primera ocurrencia de la representación TeX de la subfórmula
            # por el valor.
            try:
                cuerpo_tex = cuerpo_tex.replace(tex_sub, reemplazo, 1)
            except Exception:
                pass

        # se borran las apariciones de variables dentro del cuerpo TeX para mantener
        # las columnas vacías
        for n in vars_order:
            cuerpo_tex = cuerpo_tex.replace(f'x_{{{n}}}', '')

        # se construye el renglón final 
        renglon = inicio + ' & ' + cuerpo_tex + ' \\\\\n'

        return renglon


    def tabla_verdad(self):
        """Devuelve la tabla de verdad de la fórmula en formato LaTeX."""
        return ""

    def LaTeX(self, nombre_archivo):
        """Crea un archivo con nombre nombre_archivo.tex, que es un archivo
        mínimo en LaTeX para poder compilar la tabla de verdad asociada a la
        fórmula.
        """
        # Crear el archivo .tex
        p = Path(nombre_archivo)
        if p.suffix != ".tex":
            # Si no, pues se lo pongo
            p = p.with_suffix(".tex")

        # Ahora saco la lista de variables y la fórmula en versión LaTeX
        vars_list = self.lista_variables()
        formula_tex = self.tex_formula()   # aquí salen los &

        # Cuento cuántas variables hay
        num_vars = len(vars_list)

        # Número de columnas de la fórmula
        formula_cols = formula_tex.count("&") + 1

        # Construyo las columnas
        cols_vars = ""
        for _ in range(num_vars):
            cols_vars += "c"

        cols_formula = ""
        for _ in range(formula_cols):
            cols_formula += "c "

        # Junto todo
        array_spec = cols_vars + "|" + cols_formula

        # Ahora hago una lista donde voy metiendo cada línea
        lines = []
        lines.append(r"\documentclass{article}")
        lines.append(r"\usepackage{adjustbox}")
        lines.append(r"\begin{document}")
        lines.append(r"\[")
        lines.append(r"\begin{adjustbox}{max width=\textwidth, array=" + array_spec + r"} \\")

        # Cabecera
        cab = self._cabecera_tabla()
        for ln in cab.splitlines():
            lines.append(ln)

        # Línea horizontal
        lines.append(r"\hline")

        # Ahora necesito todas las combinaciones de valores
        from itertools import product  # importar aquí para no molestar en otras funciones
        if num_vars == 0:
            assignments = [()]
        else:
            assignments = list(product([True, False], repeat=num_vars))

        # Uso la función de renglón
        for asign in assignments:
            reng = self._renglon_verdad(asign)
            for ln in reng.splitlines():
                lines.append(ln)

        # Final del entorno
        lines.append(r"\end{adjustbox}")
        lines.append(r"\]")
        lines.append(r"\end{document}")

        # Se escribe el archivo .tex 
        f = open(str(p), "w", encoding="utf-8")
        f.write("\n".join(lines) + "\n")
        f.close()

# x1 = Formula(1)
# x2 = Formula(2)
# x3 = Formula(3)

# f1 = Formula(x1, 'C', x2)
# f2 = Formula(x3, 'N')
# f3 = Formula(f1,'D',f2)
# f4 = Formula(f1, 'B', f3)
# f5 = Formula(f1, 'I', f4)
# print(f3.tabla_verdad())
# f5.LaTeX("ejemplo")
