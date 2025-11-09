from typing import List
from itertools import product
import pathlib

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
        """
        return {}

    def evalua_sub(self, asignacion):
        """Recibe como entrada una lista de booleanos (asignación de verdad) y
        devuelve un diccionario con las fórmulas como llaves y sus valores de
        verdad como valores. Las entradas de esta lista de booleanos
        corresponden con las variables de la fórmula original. La finalidad de
        esta función es generar los renglones de la tabla de verdad
        correspondiente.
        """
        return {}

    def tex_formula(self):
        """Devuelve la fórmula con los separadores necesarios para crear la
        tabla en LaTeX.
        """
        return ""

    def _cabecera_tabla(self):
        """Devuelve la cabecera de la tabla de verdad en formato de tabla de
        LaTeX.
        """
        return ""

    def _renglon_verdad(self, asignacion):
        """Devuelve un renglón de la tabla de verdad de la fórmula,
        en formato de tabla de LaTeX, correspondiente a la
        asignación de verdad recibida.
        """
        return ""

    def tabla_verdad(self):
        """Devuelve la tabla de verdad de la fórmula en formato LaTeX."""
        return ""

    def LaTeX(self, nombre_archivo):
        """Crea un archivo con nombre nombre_archivo.tex, que es un archivo
        mínimo en LaTeX para poder compilar la tabla de verdad asociada a la
        fórmula.
        """
        pass

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
