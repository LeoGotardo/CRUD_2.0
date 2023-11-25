from pymongo import MongoClient


class Model:
    def __init__(self):
        # Configuração de conexão com o MongoDB
        self.root = "LeoGotardo"
        self.password = "GUDP6TDvj9vdzGEH"
        self.CONNECTION_STRING = f"mongodb+srv://{self.root}:{self.password}@cluster0.gcolnp2.mongodb.net/"
        self.client = MongoClient(self.CONNECTION_STRING)
        self.bd = self.client["Belle"]
        self.Login = self.bd["Logins"]

        # Lista para armazenar mensagens de erro
        self.error = []

        # Debug: exibe o conteúdo da coleção 'user_shopping_list'
        print(self.client['user_shopping_list'])


    def cad(self, login, Password):
        # Adiciona um novo usuário à coleção 'Logins'
        User = {
            "login": login,
            "Password": Password
        }
        self.Login.insert_one(User)

        return id  # Retorna o ID do usuário (não está implementado corretamente)


    def verifyLogin(self, login):
        # Verifica se um login específico existe na coleção 'Logins'
        has = self.has(login)

        if has != {}:
            return True
        else:
            return False


    def valid(self, login, password):
        # Verifica se um login e senha são válidos
        if self.verifyLogin(login, "Login") == False:
            self.validPass(password)


    def has(self, Name):
        # Retorna uma lista de todos os logins na coleção 'Logins'
        every = self.Login.find({"login": Name})
        self.logins = []

        for result in every:
            self.logins.append(result["login"])
        return self.logins


    def credencialADD(self, login, password, passwordCondirm):
        # Adiciona credenciais se válidas, caso contrário, retorna uma mensagem de erro
        if self.credencialValid(login, password, passwordCondirm) == True:
            if self.validPass(login, password) == False:
                self.cad(login, password)
                return "Valid Cadaster"
            else:
                self.error.append("Login already exists.")
                return self.error
        else:
            return self.error


    def credencialValid(self, login, password, passwordConfirm):
        # Verifica se as credenciais são válidas
        if self.loginValid(login) == True:
            if self.passValid(password, passwordConfirm) == True:
                validPass = True
                return validPass
            else:
                self.error.append("Invalid Password")
                return False
        else:
            self.error.append("Invalid Login")
            return False


    def verify(self, login, password):
        # Verifica se um login e senha são válidos e retorna o ID do usuário
        if self.verifyLogin(login) == True:
            if self.validPass(login, password) == True:
                ret = self.findID(login, password)

                valid = ret[0]
                ret.append(None)
                
                if valid == True:
                    return ret
            else:
                self.error.append("Invalid Password")
                
                ret[0] = False
                ret[1] = None
                ret.append(self.error)
                
                return ret
        else:
            self.error.append("Invalid Login")
            
            ret[0] = False
            ret[1] = None
            ret.append(self.error)

            return ret



    def loginValid(self, login):
        # Verifica se um login é válido
        if self.verifyLogin(login) == True or login != "":
            return True
        else:
            return False


    def passValid(self, password, passwordConfirm):
        # Verifica se uma senha é válida
        if password == passwordConfirm:
            return True
        elif password == "" or passwordConfirm == "":
            return False
        else:
            self.error.append("Invalid Password")


    def validPass(self, login, password):
        # Verifica se um login e senha são válidos
        login = self.Login.find({"login": login},{ "$and": {"Password": password}})
        
        if login != {}:
            return True
        else:
            return False 


    def edit(self, id, paramter):
        # Atualiza informações de um usuário na coleção 'Logins'
        self.Login.update_one({})


    def findID(self, login, password):
        # Encontra o ID de um usuário com base no login
        ret = [None]

        id = self.Login.find({"login": login},{ "$and": {"Password": password}})

        for result in id:
            ret.append(result["_id"])


        if id != {}:
            ret[0] = True
        else:
            ret[0] = False

        return ret


    def erase(self, id):
        # Exclui um usuário com base no ID
        self.Login.delete_one({id})


if __name__ == "__main__":
    # Instância um objeto Model para testar a classe
    model = Model()
