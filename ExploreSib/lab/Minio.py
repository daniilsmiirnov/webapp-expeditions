from minio import Minio


client = Minio(endpoint="localhost:9000",   # адрес сервера
               access_key='danial',          # логин админа
               secret_key='danial1233',       # пароль админа
               secure=False)                # опциональный параметр, отвечающий за вкл/выкл защищенное TLS соединение


