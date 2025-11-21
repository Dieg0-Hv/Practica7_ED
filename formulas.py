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
        # Si no hay algun conectivo, entonces significa que es una variable proposicional,
        # Segun el constructor, en este caso self.izquierda almacena el numero de la variable.
        # Asi, se regresa un string "xn".
        if self.conectivo is None:
            return f"x{self.izquierda}"
        # Si el conectivo es N, entonces es una negacion.
        # De esta forma, se hace una llamada recursiva para obtener su representacion, se añaden
        # parentesis y se agrega el simbolo de negacion 
        elif self.conectivo == 'N':
            return f"(¬{repr(self.izquierda)})"
        else:
            # Se realizan varios casos dependiendo del conectivo, para saber que simbolo se usara.
            # Luego, se hacen dos llamadas recursivas para obtener las representaciones de
            # izquierda y derecha, para poner el simbolo en medio.
            simbolo = ''
            if self.conectivo == 'C':
                simbolo = '∧'
            if self.conectivo == 'D':
                simbolo = '∨'
            if self.conectivo == 'I':
                simbolo = '→'
            if self.conectivo == 'B':
                simbolo = '↔'
            return f"({repr(self.izquierda)} {simbolo} {repr(self.derecha)})"

    def lista_variables(self):
        """Devuelve la lista de todas las variables de una fórmula en orden.
         Si la fórmula es una variable, regreso una lista con ese número.
         Si es una negación, regreso la lista de la subfórmula
         Si es un conectivo binario, obtengo las listas de izquierda y derecha y las mezclo con merge ascendente y evita duplicados.
        """
        def merge(a: List[int], b: List[int]) -> List[int]:
            # si alguna está vacía, regreso el caso base
            if not a:
                return b[:]
            if not b:
                return a[:]
            # comparo las cabezas
            if a[0] == b[0]:
                # si son iguales, incluyo una sola vez y avanzo en ambas
                return [a[0]] + merge(a[1:], b[1:])
            elif a[0] < b[0]:
                return [a[0]] + merge(a[1:], b)
            else:  # b[0] < a[0]
                return [b[0]] + merge(a, b[1:])

        # Caso hoja: variable
        if self.conectivo is None:
            return [self.izquierda]

        # Caso negación: solo la subfórmula izquierda
        if self.conectivo == 'N':
            return self.izquierda.lista_variables()

        # Caso binario: obtengo listas de ambas ramas y las mezclo
        izquierda_vars = self.izquierda.lista_variables()
        derecha_vars = self.derecha.lista_variables()
        return merge(izquierda_vars, derecha_vars)

    def mayor_variable(self):
        """
        Devuelve la variable de mayor número que aparece en la fórmula.
        - Si la fórmula es una variable, regreso ese número.
        - Si la fórmula es una negación, solo reviso la parte izquierda.
        - Si la fórmula tiene dos lados, comparo recursivamente ambos lados.
        """
        # Caso 1: la fórmula es una variable
        if self.conectivo is None:
            return self.izquierda
        # Caso 2: negación del lado izquierdo
        if self.conectivo == 'N':
            return self.izquierda.mayor_variable()
        # Caso 3: busco la mayor variable de cada lado recursivamente
        mayor_izq = self.izquierda.mayor_variable()
        mayor_der = self.derecha.mayor_variable()
        # Comparo las dos 
        if mayor_izq >= mayor_der:
            return mayor_izq
        else:
            return mayor_der

    def numero_conectivos(self):
        """Devuelve el número de conectivos que ocurren en la fórmula.
        - Si la fórmula es una variable, no hay conectivos -> 0.
        - Si la fórmula es una negación, cuento 1 por la negación y llamo recursivamente a la parte izquierda.
        - Si la fórmula tiene un conectivo binario, cuento 1 por ese conectivo y llamo recursivamente a izquierda y derecha y sumo los resultados.
        """
        # Caso variable:
        if self.conectivo is None:
            return 0
        # Caso negación:
        if self.conectivo == 'N':
            # cuento 1 por la negación y sumo lo que devuelva 
            return 1 + self.izquierda.numero_conectivos()
        # Caso binario:
        return 1 + self.izquierda.numero_conectivos() + self.derecha.numero_conectivos()

    def _evalua_aux(self, asignacion: Asignacion, posiciones: List[int]):
        """Función auxiliar para evaluar una fórmula. Recibe una lista de
        booleanos (una asignación de verdad), y una lista con los números de
        las variables correspondientes.
        Eg. _evalua_aux([False, True, True], [1, 2, 5]) corresponde a:
        x1 = False
        x2 = True
        x5 = True
        """
        # Funcion auxiliar que realiza la logica recursiva.
        # De igual forma, si no hay conectivo, llegamos a una variable proposicional. Asi, izquierda almacena
        # un entero que es el numero de variable proposicional.
        # Luego, busca en que posicion esta el numero dentro de la lista "posiciones", y regresa su asignacion
        # en ese indice.
        if self.conectivo is None:
            return asignacion[posiciones.index(self.izquierda)]
        # Si el conector es una negacion, entonces se realiza una llamada recursiva para saber el valor de verdad
        # del elemento izquierda, para posteriormente negarlo con not.
        elif self.conectivo == 'N':
            return not self.izquierda._evalua_aux(asignacion, posiciones)
        else:
            # Se definen variables izq y der para simplificar el proceso de asignacion de verdad.
            # Para ambas variables se realizan llamadas recursivas para obtener a grandes rasgos los valores
            # de las formulas o variables que esten a la izquierda y derecha del conectivo.
            # Se regresa un valor de verdad final de la formula.
            izq = self.izquierda._evalua_aux(asignacion, posiciones)
            der = self.derecha._evalua_aux(asignacion, posiciones)

            if self.conectivo == 'C':
                # Conjuncion (And)
                return izq and der
            elif self.conectivo == 'D':
                # Disyuncion (Or)
                return izq or der
            elif self.conectivo == 'I':
                # Implicacion, utilizando la equivalencia P->Q == !P o Q
                return (not izq) or der
            elif self.conectivo == 'B':
                # Bicondicional, sabiendo que solo regresa true cuando P == V y Q == V o P == F y Q == F, o sea,
                # son iguales.
                # De otra forma, se pueden unir con And las implicaciones de P->Q y Q->P.
                return izq == der

    def evalua(self, asignacion: Asignacion):
        """Devuelve el valor de verdad de la fórmula bajo una asignación dada,
        que recibe como entrada en la forma de una lista de booleanos.
        """
        # Se realiza una llama a la funcion lista_variables definida previamente para obtener una lista
        # ordenada de cada numero de variable proposicional.
        posiciones = self.lista_variables()
        # Asi, se manda a la funcion auxiliar la lista de posiciones con su respectiva asignacion de verdad.
        return self._evalua_aux(asignacion, posiciones)

    def aplana(self):
        """Devuelve una lista con la versión aplanada (inorden) del árbol de
        sintáxis de la fórmula.
        - Si la fórmula es una variable, regreso una lista con ella misma.
        - Si es una negación, primero aplano la subfórmula izquierda y luego pongo la negación (la raíz) al final.
        - Si es un conectivo binario, aplano izquierda, pongo la raíz, y luego aplano derecha; todo concatenado. 
        """
        # Caso base: Una hoja
        if self.conectivo is None:
            return [self]
        # Caso negación 
        if self.conectivo == 'N':
            return self.izquierda.aplana() + [self]
        # Caso binario:
        return self.izquierda.aplana() + [self] + self.derecha.aplana()


    def aplana_sin_variables(self):
        """Devuelve una lista con la versión aplananada del árbol de sintaxis de la fórmula, sin las hojas.
        - Si la fórmula es una variable hoja, devuelvo [] porque no quiero variables.
        - Si la fórmula es una negación, primero aplanamos la subfórmula izquierda  y luego añadimos la negación. 
        - Si la fórmula es un conectivo binario, aplanamos izquierda, luego
          añadimos la raíz y luego aplanamos derecha.
        - Hago concatenaciones de listas manualmente porque quiero practicar recursión y ver paso a paso cómo se arma la lista final.
        """
        # Caso base: Una hoja
        if self.conectivo is None:
            return []

        # Caso negación: aplanar izquierda y añadir la negación
        if self.conectivo == 'N':
            return self.izquierda.aplana_sin_variables() + [self]

        # Caso binario:  aplanar izquierda, añadir la raíz y aplanar derecha
        return self.izquierda.aplana_sin_variables() + [self] + self.derecha.aplana_sin_variables()

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
        - Caso negación: pongo la posición izquierda vacía y el operador \\lnot
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
        # Inicializamos la cadena con dos espacios vacios
        cadena = "  "
        # Obtenemos los resultados y las subformulas con los metodos ya definidos para evaluar posteriormente
        resultados = self.evalua_sub(asignacion)
        subformulas = self.aplana_sin_variables()
        # Iteramos sobre las asignaciones que se proporcionan y los concatenamos a la cadena.
        # Se añade 1 si es True y 0 en otro caso, junto con un espacio, un & y otro espacio.
        # Esta iteracion añade la parte de las variables proposicionales.
        for val in asignacion:
            cadena += f"{1 if val else 0} & "
        # Iteramos ahora sobre las subformulas
        for subformula in subformulas:
            # Evaluamos para saber si pondremos un 0 o un 1
            aux = f"{1 if resultados[subformula] else 0}"
            # Si esa subformula es la formula principal, o sea, el valor final del renglon, lo ponemos en negritas.
            if subformula is self:
                cadena += f"& \\mathbf{{{aux}}} & "
            # De cualquier manera, concatenamos un &, un espacio, el valor 1 o 0, un espacio, un & y otro espacio.
            else:
                cadena += f"& {aux} & "
        # Regresamos el renglon final, añadiendo un salto de linea de LaTeX y uno de Python.
        return cadena + "\\\\\n"

    # Metodo auxiliar para el metodo tabla_verdad(). Proporciona el numero de c's que tendra la tabla.
    # Ejemplo: ...,array=cc|ccc}
    def _num_espacios(self):
        # Si es una variable proposicional, cuenta como una c
        if self.conectivo is None:
            return 1
        # Si es una negacion, se añaden dos c y se hace llamada recursiva para la formula o variable de la izquierda.
        elif self.conectivo == 'N':
            return 2 + self.izquierda._num_espacios()
        # En otro caso (conectivos), se añade una c y se hacen llamadas recursivas en la izquierda y derecha
        else:
            return 1 + self.izquierda._num_espacios() + self.derecha._num_espacios()

    def tabla_verdad(self):
        """Devuelve la tabla de verdad de la fórmula en formato LaTeX."""
        # Obtenemos el numero de variables (longitud de la lista de variables)
        # Se utilizaran para el numero de c's que tendra la parte de variables de la tabla
        num_variables = len(self.lista_variables())
        # Obtenemos el numero de c's de la formula utilizando un metodo auxiliar
        num_c = self._num_espacios()
        # Concatenamos el inicio de la tabla, incluyendo los calculos para el numero de c's
        tabla = f"\\begin{{adjustbox}}{{max width=\\textwidth ,array={'c'*num_variables}|{'c'*num_c}}} \\\\\n"
        # Concatenamos la cabecera
        tabla += self._cabecera_tabla()
        # Nueva linea, LaTeX y python
        tabla += "\\hline" + "\n"
        # Generamos todos los valores que pueden tomar las variables
        for asignacion in product([False, True], repeat=num_variables):
            # Concatenamos cada renglon considerando los valores posibles de las variables
            tabla += self._renglon_verdad(list(asignacion))
        # Final
        tabla += "\\end{adjustbox}"
        # Regresamos la tabla
        return tabla

    def LaTeX(self, nombre_archivo):
        """Crea un archivo con nombre nombre_archivo.tex, que es un archivo
        mínimo en LaTeX para poder compilar la tabla de verdad asociada a la
        fórmula.
        """
        # Creamos un string con la plantilla que utilizara el documento LaTeX. En medio,
        # insertamos la tabla con el metodo necesario.
        contenido = f"""\\documentclass{{article}}
        
\\usepackage{{adjustbox}}

\\begin{{document}}
        
\\[
{self.tabla_verdad()}
\\]
        
\\end{{document}}"""
        # Utilizamos la libreria pathlib para escribir la cadena "contenido" en un archivo.
        path = pathlib.Path(nombre_archivo)
        path.write_text(contenido, encoding='utf-8')

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
