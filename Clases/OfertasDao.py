import datetime
import pyrebase


config = {

  "apiKey": "AIzaSyAXMsxrT40GRQp_Erm9BVKMjbQemUn3IC0",
  "authDomain": "telegram-99907.firebaseapp.com",
  "projectId": "telegram-99907",
  "storageBucket": "telegram-99907.appspot.com",
  "messagingSenderId": "372936121306",
  "databaseURL": "https://telegram-99907-default-rtdb.firebaseio.com/",
  "appId": "1:372936121306:web:bb2327627350a463b9fee3"

}

class FirebaseSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseSingleton, cls).__new__(cls)
            cls._instance.firebase = pyrebase.initialize_app(config)
            cls._instance.db = cls._instance.firebase.database()
        return cls._instance

    def insertar_oferta(self, data, categoria):
        
        self.db.child("ofertas/"+categoria).push(data)
    
    def buscar_oferta_id_categoria(self, id, categoria):
        ofertas = self.db.child("ofertas/"+categoria).get()
       
        if ofertas.each() is not None:
            for oferta in ofertas.each():
                oferta_info = oferta.val()
                if oferta_info.get("oferta_id") == id and oferta_info.get("categoria") == categoria:
                    #return oferta.key(), oferta_info
                    return oferta.val(),oferta.key()
        return None
    
    def buscar_ofertas_nuevas(self):
        categorias = self.db.child("ofertas").get()
        ofertas_nuevos = []

        if categorias.each() is not None:
            for categoria in categorias.each():
                
                ofertas = self.db.child("ofertas/" + categoria.key()).get()
                if ofertas.each() is not None:
                    for oferta in ofertas.each():
                        oferta_info = oferta.val()

                        if oferta_info.get("estado") == "nuevo":
                            ofertas_nuevos.append((oferta.key(), oferta_info))

        return ofertas_nuevos
    
    def buscar_ofertas_publicadas(self):
        categorias = self.db.child("ofertas").get()
        ofertas_nuevos = []

        if categorias.each() is not None:
            for categoria in categorias.each():
                
                ofertas = self.db.child("ofertas/" + categoria.key()).get()
                if ofertas.each() is not None:
                    for oferta in ofertas.each():
                        oferta_info = oferta.val()

                        if oferta_info.get("estado") == "publicado":
                            ofertas_nuevos.append((oferta.key(), oferta_info))

        return ofertas_nuevos


    def buscar_oferta_id_categoria(self, id, categoria):
        ofertas = self.db.child("ofertas/"+categoria).get()
       
        if ofertas.each() is not None:
            for oferta in ofertas.each():
                oferta_info = oferta.val()
                if oferta_info.get("oferta_id") == id and oferta_info.get("categoria") == categoria:
                    return oferta.key(), oferta_info
        return None
    
    def actualizar_estado_oferta(self,categoria, oferta_key, referencia_img, id_mensaje):
        nuevos_datos = {
            "estado": "publicado",
            "referencia_img": referencia_img,
            "id_mensaje": id_mensaje
        }

        self.db.child("ofertas").child(categoria).child(oferta_key).update(nuevos_datos)

    def actualizar_estado_agotado_oferta(self,categoria, oferta_key):
        nuevos_datos = {
            "estado": "agotado",
        }

        self.db.child("ofertas").child(categoria).child(oferta_key).update(nuevos_datos)
    
    
    def eliminar_oferta(self, oferta_key, categoria):
        ofertas = self.db.child("ofertas/" + categoria).get()

        if ofertas.each() is not None:
            for oferta in ofertas.each():
                if oferta.key() == oferta_key:
                    self.db.child("ofertas/" + categoria + "/" + oferta.key()).remove()
                    return "Oferta eliminada correctamente"

        return "La oferta no existe"
    

# Uso:
# Tu puedes crear otra instancia para acceder desde otra clase
db = FirebaseSingleton()

