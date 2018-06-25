from tabelas import Pessoa, db, Produto, Pedidos, Cardapio, Empresa, PedidoProduto

lista_de_tabelas = [ Pessoa, Produto, Pedidos, Cardapio, Empresa, PedidoProduto ]

db.connect()
db.create_tables(lista_de_tabelas)

#usu = Pessoa()
#usu.usuario = "teste"
#usu.senha = "123"
#usu.email = "uashduiashdu"
#usu.foto_url = "uashduiashd"
#usu.frase = "teste"
#usu.cidade = "ashduihasd"
#usu.bairro = "iuashduhas"
#usu.rua = "iuashduihas"
#usu.numero = "3212"
#usu.save()

#emp = Empresa()

#emp.nome = "empresa x"
#emp.cnpj = "654654564"
#emp.foto_url = "iuahsdu"
#emp.save()