import random as rd

def getLoginDict(fileName):
    file = open(fileName, "r")
    file.readline()
    d = dict()
    for line in file:
        id, user, password = line.strip().split(",")
        d[id] = dict()
        d[id]["user"] = user
        d[id]["password"] = password
    return d


def getBookDict():
    file = open("libros.txt", "r")
    file.readline()
    d = dict()
    for line in file:
        codigo, titulo, autor, cantidad = line.strip().split(",")
        d[codigo] = dict()
        d[codigo]["titulo"] = titulo
        d[codigo]["autor"] = autor
        d[codigo]["cantidad"] = int(cantidad)
    return d


def getLoanDict():
    file = open("prestamos.txt", "r")
    file.readline()
    d = dict()
    for line in file:
        codigo, estudiante, libro, fechaPrestamo, fechaDevolucion = line.strip().split(",")
        d[codigo] = dict()
        d[codigo]["libro"] = libro
        d[codigo]["estudiante"] = estudiante
        d[codigo]["fechaPrestamo"] = fechaPrestamo
        d[codigo]["fechaDevolucion"] = fechaDevolucion
    return d


def printAdminMenu():
    print("*** MENU ADMINISTRADOR ***")
    print("1. Consultar Libro por codigo")
    print("2. Insertar Libro")
    print("3. Salir")


def printStudentMenu():
    print("*** MENU ESTUDIANTE ***")
    print("1. Ver catalogo de libros disponibles")
    print("2. Ver prestamos activos")
    print("3. Salir")


def validateUser(u, p, stuDict, admDict):
    for key, data in admDict.items():
        if data["user"] == u and data["password"] == p:
            return ("admin", key)
    for key, data in stuDict.items():
        if data["user"] == u and data["password"] == p:
            return ("student", key)
    return ""


def getAvailableBooks(id, loans, books):
    studentLoans = []
    availableLoans = []
    for data in loans.values():
        if id == data["estudiante"]:
            studentLoans.append(data["libro"])
    for code in books.keys():
        if code not in studentLoans:
            print("Codigo:", code, end=" - ")
            print("Titulo:", books[code]["titulo"], end=" - ")
            print("Autor:", books[code]["autor"], end=" - ")
            print("Cantidad:", books[code]["cantidad"])
            availableLoans.append(code)
    return availableLoans


def generateRandomLoanId(loans):
    randomLoan = rd.randrange(1, 1000)
    while randomLoan in loans.keys():
        randomLoan = rd.randrange(1, 1000)
    return randomLoan