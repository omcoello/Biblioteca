import funciones as fn
from datetime import date, timedelta

stuDict = fn.getLoginDict("estudiantes.txt")
admDict = fn.getLoginDict("administradores.txt")
bookDict = fn.getBookDict()
loanDict = fn.getLoanDict()
print(loanDict)

# Log in de usuarios
userLoged = ""
while userLoged == "":
    userInput = input("Ingrese su usuario: ")
    passwordInput = input("Ingrese su contrasenia: ")
    userLoged = fn.validateUser(userInput, passwordInput, stuDict, admDict)


# Variables para actualizar unicamente las tablas modificadas en la sesion
loanUpdate = False
bookUpdate = False
newLoans = []

# Manejando las acciones segun el tipo de usuario
userType, userId = userLoged[0], userLoged[1]
option = ""
if userType == "admin":
    while option != "3":
        fn.printAdminMenu()
        option = input("Ingrese una opcion del menu: ")
        if option == "1":
            code = input("Ingrese el codigo del libro a consultar: ")
            if code in bookDict.keys():
                print("Detalles del libro con codigo", code)
                print("Titulo:", bookDict[code]["titulo"])
                print("Autor:", bookDict[code]["autor"])
                print("Cantidad:", bookDict[code]["cantidad"])
            else:
                print("No existe un libro con el codigo ingresado.")
            print()
        elif option == "2":
            print("Ingrese los datos del libro a registrar.")
            code = input("Ingrese el codigo: ")
            title = input("Ingrese el titulo: ")
            author = input("Ingrese el autor: ")
            quantity = input("Ingrese la cantidad: ")
            if code in bookDict.keys():
                bookDict[code]["cantidad"] += int(quantity)
                print("El libro ya esta registrado. Se anadio " +
                      str(quantity) + " unidades al inventario")
            else:
                bookDict[code] = dict()
                bookDict[code]["titulo"] = title
                bookDict[code]["autor"] = author
                bookDict[code]["cantidad"] = int(quantity)
                print("Libro registrado exitosamente.")
            bookUpdate = True
            print()
elif userType == "student":
    while option != "3":
        fn.printStudentMenu()
        option = input("Ingrese una opcion del menu: ")
        if option == "1":
            print("Catalogo de libros disponibles:")
            availableBooks = fn.getAvailableBooks(userId, loanDict, bookDict)
            print("Si desea prestar un libro, digite su respectivo codigo. ")
            print("En caso de no realizar ningun prestamo, digite la letra \"n\". ")
            confirmation = input("Respuesta: ")
            if confirmation.strip() != "n":
                if confirmation in availableBooks and bookDict[confirmation]["cantidad"] > 0:
                    bookDict[confirmation]["cantidad"] -= 1
                    lastConfirmation = input(
                        "¿Esta seguro de realizar este prestamo? S/N \n")
                    if lastConfirmation.upper() == "S":
                        code = fn.generateRandomLoanId(loanDict)
                        loanDict[code] = dict()
                        loanDict[code]["libro"] = confirmation
                        loanDict[code]["estudiante"] = userId
                        loanDict[code]["fechaPrestamo"] = date.today()
                        loanDict[code]["fechaDevolucion"] = date.today() + \
                            timedelta(30)
                        print("Prestamo exitoso.")
                        newLoans.append(str(code)+","+ userId+","+ confirmation+","+
                                        date.today().strftime('%Y-%m-%d')+","+(date.today() + timedelta(30)).strftime('%Y-%m-%d'))
                        print(str(code)+","+ userId+","+ confirmation+","+
                                        date.today().strftime('%Y-%m-%d')+","+(date.today() + timedelta(30)).strftime('%Y-%m-%d'))
                        loanUpdate = True
                    else:
                        bookDict[confirmation]["cantidad"] += 1
                        print("Deshaciendo prestamo...")
                else:
                    print("No existe el libro con el codigo ingresado")
            print()
        elif option == "2":
            print("Prestamos activos: ")
            for key, data in loanDict.items():
                if userId == data["estudiante"]:
                    print("Titulo:", bookDict[data["libro"]]["titulo"])
                    print("Autor:", bookDict[data["libro"]]["autor"])
                    print("Fecha prestamo:",
                          data["fechaPrestamo"])
                    print("Fecha devolucion:",
                          data["fechaDevolucion"], "\n")
            print()

# Actualizar archivos modificados

if loanUpdate:
    file = open("prestamos.txt", "a")
    if len(list(loanDict.keys())) == 0:
        file.write("codigo,estudiante,libro,fechaPrestamo,fechaDevolucion\n")
    for loan in newLoans:        
        file.write(loan+"\n")
if bookUpdate:
    file = open("libros.txt", "w")
    file.write("codigo,titulo,autor,cantidad" + "\n")
    print("diccionario antes de update", bookDict)
    for k, v in bookDict.items():
        print("clave:",k, "valor:",v)
        file.write(str(k) + "," + v["titulo"] + "," + v["autor"] + "," + str(v["cantidad"]) + "\n")
