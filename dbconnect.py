import pymysql

def connection():
    conn = pymysql.connect(host="us-cdbr-iron-east-01.cleardb.net",
                           user='b83454456f00ac',
                           passwd='e2d78b2c',
                           db = 'heroku_581ae41f7902ee4')
    c = conn.cursor()

    return c,conn




# def criar_table_ask ():
#     try:
#         c, conn = connection()
#         print()
#         with warnings.catch_warnings():
#             warnings.simplefilter('ignore')
#             c.execute(f"DROP TABLE IF EXISTS ask ")
#             c.execute(f""" CREATE TABLE ask (
#                         `idask` INT NOT NULL AUTO_INCREMENT ,
#                         `iduser` INT ,
# open_domingo VARCHAR(600) DEFAULT '' not null,
# open_Segunda VARCHAR(600) DEFAULT '' not null,
# open_Terça VARCHAR(600) DEFAULT '' not null,
# open_Quarta VARCHAR(600) DEFAULT '' not null,
# open_Quinta VARCHAR(600) DEFAULT '' not null,
# open_Sexta VARCHAR(600) DEFAULT '' not null,
# open_Sabado VARCHAR(600) DEFAULT '' not null,
# close_domingo VARCHAR(600) DEFAULT '' not null,
# close_Segunda VARCHAR(600) DEFAULT '' not null,
# close_Terça VARCHAR(600) DEFAULT '' not null,
# close_Quarta VARCHAR(600) DEFAULT '' not null,
# close_Quinta VARCHAR(600) DEFAULT '' not null,
# close_Sexta VARCHAR(600) DEFAULT '' not null,
# close_Sabado VARCHAR(600) DEFAULT '' not null,
# dinheiro VARCHAR(600) DEFAULT '' not null,
# multibanco VARCHAR(600) DEFAULT '' not null,
# cheque VARCHAR(600) DEFAULT '' not null,
# paypal VARCHAR(600) DEFAULT '' not null,
# boleto VARCHAR(600) DEFAULT '' not null,
# criptomoedas VARCHAR(600) DEFAULT '' not null,
# outros VARCHAR(600) DEFAULT '' not null,
# delivery VARCHAR(600) DEFAULT '' not null,
# desconto VARCHAR(600) DEFAULT '' not null,
#
#                          PRIMARY KEY(`idask`))
#                         ENGINE = InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin""")
#
#             conn.commit()
#         print('TABELA-ASK CRIADA COM SUCESSOO')
#
#     except Exception as e:
#         print(f' ERROR:       {str(e)}')
#         return (str(e))
# def criar_table_fotos ():
#     try:
#         c, conn = connection()
#         print()
#         with warnings.catch_warnings():
#             warnings.simplefilter('ignore')
#             c.execute(f"DROP TABLE IF EXISTS FOTOS ")
#             c.execute(f""" CREATE TABLE FOTOS (
#                         `idfoto` INT NOT NULL AUTO_INCREMENT ,
#                         `iduser` INT ,
#                         `foto` VARCHAR(450)  NULL , PRIMARY KEY(`idfoto`))
#                         ENGINE = InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin""")
#
#             conn.commit()
#         print('TABELA-FOTOS CRIADA COM SUCESSOO')

    # except Exception as e:
    #     print(f' ERROR:       {str(e)}')
    #     return (str(e))