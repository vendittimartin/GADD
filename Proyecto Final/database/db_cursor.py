from database.database import connect_to_db

def insert_image(image_obj):
    connection, cursor = connect_to_db()

    if connection and cursor:
        try:
            insert_query = '''
                INSERT INTO Image (vector, name)
                VALUES (%s, %s)
            '''
            cursor.execute(insert_query, (image_obj.vector, image_obj.name))

            connection.commit()
            print('Image insertada correctamente.')

        except Exception as e:
            print('Error al agregar Image:', e)

        finally:
            cursor.close()
            connection.close()
    else:
        print('Error al conectar a la base de datos.')

def get_similar_images(quantity_images, image_obj):
    connection, cursor = connect_to_db()

    if connection and cursor:
        try:
            insert_query = '''
                SELECT GET_SIMILAR_IMAGES(quantity, vector)
                VALUES (%s, %s)
            '''
            cursor.execute(insert_query, (quantity_images, image_obj.vector))

            connection.commit()

        except Exception as e:
            print('Error consultar imagenes similares:', e)

        finally:
            cursor.close()
            connection.close()
    else:
        print('Error al conectar a la base de datos.')
