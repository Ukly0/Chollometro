import datetime
import OfertasDao as OfertasDao
import re

class Oferta:
    def __init__(self, titulo, link_afiliado, precio_original, precio, img, 
                 oferta_id, producto_id, categoria, porcentaje = None):
        
        self.oferta_key = ""
        self.titulo = titulo
        self.link_afiliado = link_afiliado
        self.precio_original = precio_original
        self.precio = precio
        self.img = img
        self.oferta_id = oferta_id
        self.producto_id = producto_id
        self.categoria = categoria
        self.fecha = datetime.datetime.now().strftime("%Y-%m-%d")
        self.estado = "nuevo"
        self.referencia_img = ""
        self.id_mensaje = ""

        if porcentaje is None and precio_original != 0:
            self.porcentaje = self.porcentaje_rebajado()
        else:
            self.porcentaje = porcentaje

    def buscar_existe(self,db):
        oferta = db.buscar_oferta_id_categoria(self.oferta_id, self.categoria)
        return bool(oferta)
    
    def insertar_oferta(self, db):
        data = {

            "titulo": self.titulo,
            "link_afiliado": self.link_afiliado,
            "precio_original": self.precio_original,
            "precio": self.precio,
            "img": self.img,
            "oferta_id": self.oferta_id,
            "producto_id": self.producto_id,
            "fecha": self.fecha,
            "estado": self.estado,
            "categoria": self.categoria,
            "porcentaje": self.porcentaje,
            "referencia_img": self.referencia_img 
        }   

        if not self.buscar_existe(db):
            db.insertar_oferta(data, self.categoria)
        else: 
            print("\t*EXISTE*")

    def porcentaje_rebajado(self):

       
        self.precio = self.precio.replace(",",".")
        self.precio = re.sub(r'[^\d.]', '', self.precio)
        
        try:      
            self.precio = float(self.precio)
        except ValueError:
            print("Error: El valor ingresado no es un número válido.")
            
        if self.precio_original != "0":
            print(self.precio_original)
            self.precio_original = self.precio_original.replace(",",".")
            self.precio_original = re.sub(r'[^\d.]', '', self.precio_original)
            self.precio_original = float(self.precio_original)
            diferencia = self.precio_original - self.precio
            
            return round((diferencia / self.precio_original) * 100)

        else:
            return 0
        
    def obtener_ofertas_nuevas(db):
        return db.buscar_ofertas_nuevas()
    
    def actualizar_estado(self,db):
        return db.actualizar_estado_oferta(self.categoria,self.oferta_key, self.referencia_img, self.id_mensaje)
    
    def toString(self):
        print(f"+ Titulo: {self.titulo} \n+ Link: {self.link_afiliado} \n+ Id_Producto: {self.producto_id} \n+ Precio Anterior: {self.precio_original} \n+ Precio: {self.precio} \n+ Categoria: {self.categoria}")

    
