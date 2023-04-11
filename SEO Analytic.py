from bs4 import BeautifulSoup
import requests
import nltk
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')

#Bibliografía:
#https://www.danielherediamejias.com/guide-seo-onpage-scraping-python/
#https://neilpatel.com/blog/seo-errors-ecommerce-websites/
#https://www.josebernalte.com/las-10-reglas-seo/
#https://nestrategia.com/mejorar-posicionamiento-seo/
#https://rockcontent.com/es/blog/que-es-seo/#:~:text=Se%20trata%20del%20conjunto%20de,de%20las%20marcas%20en%20Internet

# URL del sitio web
url = input("Ingrese el enlace de su página web: ")

# Verificar conectividad de red
try:
    response = requests.get(url, timeout=5)
except requests.ConnectionError:
    print("Error de conexión")
    exit(1)
except requests.Timeout:
    print("Tiempo de espera agotado")
    exit(1)

# Verificar que el servidor esté en línea y accesible
if response.status_code != 200:
    print("El servidor no está en línea o no se puede acceder a él")
    exit(1)
content = response.content

# Crear objeto BeautifulSoup con el contenido obtenido
soup = BeautifulSoup(content, "html.parser")

# Obtener el idioma principal de la página (si lo tiene)
html_language = None
html_tag = soup.find('html')

#Definir Array buenas y malas prácticas
buenasPracticas = []
malasPracticas = []
totalPractica = 0

# Detectar Keywords
keyword_usadas = 0
bod = soup.find('body').text
# Convertir el texto a minúsculas y tokenizarlo
palabras_a_minusuculas = [i.lower() for i in word_tokenize(bod)]
swe = nltk.corpus.stopwords.words('spanish')
swi = nltk.corpus.stopwords.words('english')
swf = nltk.corpus.stopwords.words('french')
swg = nltk.corpus.stopwords.words('german')
swp = nltk.corpus.stopwords.words('portuguese')
swr = nltk.corpus.stopwords.words('russian')
conectores = swe + swi + swf + swg + swp + swr

lemmatizer = nltk.stem.WordNetLemmatizer()
palabras = [lemmatizer.lemmatize(p) for p in palabras_a_minusuculas if p.isalpha() and p not in conectores]

# Obtener las palabras clave más comunes 
for i in palabras_a_minusuculas:
    if i not in conectores and i.isalpha():
        palabras.append(i)

if palabras == 0:
    malasPracticas.append({"Titulo":"Keywords: ", "Valor" : "No", "Descripcion" : "No hay keywords detectadas."})

else:
    totalPractica += 1
    buenasPracticas.append({"Titulo":"Keywords: ", "Valor" : "Si", "Descripcion" : "Hay keywords detectadas."})   
    palabras_claves = nltk.FreqDist(palabras)
    keywords = [p[0] for p in palabras_claves.most_common(10) if p[1] > 1 and len(p[0]) > 2]

# Metodo para comparar Keywords con texto
def palabras_coincidentes(array, texto):
    for palabra in array:
        if palabra in texto:    
            return True
    return False  

# Obtener el título de la página
title = soup.title.text.strip()


title_split = title.lower().split()
title_coincidencias = palabras_coincidentes(keywords, title_split)
title_bool = title_coincidencias
if title_coincidencias:
    title_bool = True 
    keyword_usadas +=1
    totalPractica
    
    
else:
    title_key ="No hay Keyword en Meta Title"
    title_bool = False


# Mostrar el título de la página y la cantidad de letras que tiene
if (len(title) >65 and len(title)<30 ):
    buenasPracticas.append({"Titulo": f"Title: {title}.", "Valor":f"({len(title)} carácteres)", "Descripcion" : "El título se encuentra configurado. El largo debe ser entre 30 y 65 caracteres."})
else:
    malasPracticas.append({"Titulo": f"Title: {title}.", "Valor":f"({len(title)} carácteres)", "Descripcion" : "El título no cumple con la configuración. El largo debe ser entre 30 y 65 caracteres."})

# Extraer la descripción
description_key =""

description_tag = soup.find("meta", attrs={"name": "description"})
if description_tag:
    description = description_tag.get("content")
    description_length = len(description)
    buenasPracticas.append({"Titulo":"Meta Descripción: ", "Valor": f"{description_length}" " carácteres", "Descripcion":"La página cuenta con la configuración de la descripción."})
    totalPractica +=1
    description_split = description.lower().split()
    description_coincidencias = palabras_coincidentes(keywords, description_split)
    description_bool = description_coincidencias
    if description_coincidencias:
        keyword_usadas +=1
        
    else:
        description_key ="No hay Keyword en Meta Name Description"
else:
    malasPracticas.append({"Titulo":"Meta Descripción: ", "Valor":"0", "Descripcion":"La página no cuenta con la configuración de la descripción."})
    description_bool = False

# Contar la cantidad de encabezados <h1>
h1_count = len(soup.find_all("h1"))
if h1_count == 1:
    buenasPracticas.append({"Titulo":"Encabezado H1: ", "Valor": f"{h1_count} encontrado(s)", "Descripcion":"El sitio cuenta con una correcta configuración de encabezados H1."})
    totalPractica += 1
else:
    malasPracticas.append({"Titulo":"Encabezado H1: ", "Valor": f"{h1_count} encontrado(s)", "Descripcion":"La cantidad de encabezados <h1> debe ser 1."})
    
if h1_count:
    h1_split = soup.find("h1").text.lower().split()
    h1_coincidencias = palabras_coincidentes(keywords, h1_split)
    h1_bool = h1_coincidencias
    if h1_coincidencias:    
        keyword_usadas +=1
        
        h1_bool = True
    else:
        h1_key ="No hay Keyword en H1"
        h1_bool = True
else:
    h1_key = "No hay elemento H1 en la página"
    h1_bool = False

# Entrega de informacion de Keywords
if keyword_usadas == 3:
    buenasPracticas.append({"Titulo":"Configuración Keywords: ", "Valor":"", "Descripcion":"Existe una configuración de Keywords correcta."})
    buenasPracticas += 1
else:
    malasPracticas.append({"Titulo":"Configuración Keywords: ", "Valor":"", "Descripcion":"No hay una configuración de Keywords optima (Revisar Title,Description o H1)."})
    # if title_bool == False:
    #     malasPracticas.append(title_key)
    # if description_bool == False:
    #     malasPracticas.append(description_key)
    # if h1_bool == False:
    #     malasPracticas.append(h1_key)

#Buscar las img de los html
images = [[a["src"], a.get("alt", "")] if "src" in a.attrs else [None, a.get("alt", "")] for a in soup.find_all('img')]

# Contar la cantidad de imágenes con atributo TITLE
title_images = soup.find_all("img", attrs={"title": True})
title_images_count = len(title_images)

# Contar la cantidad de imágenes con atributo o etiqueta ALT dentro de las imágenes con atributo TITLE
alt_title_images = [img for img in title_images if img.has_attr("alt")]
alt_title_images_count = len(alt_title_images)

# Contar la cantidad de imágenes sin atributo o etiqueta ALT ni atributo TITLE
no_attr_images_count = len([img for img in images if img[1] == ""])
no_attr_title_images_count = len([img for img in images if img[1] == "" and img[0] in [i["src"] for i in title_images]])

# Calcular la cantidad de imágenes que tienen al menos un atributo
at_least_one_attr_count = len(soup.find_all("img", alt=True)) + len(soup.find_all("img", title=True)) + alt_title_images_count

# Imprimir los resultados obtenidos en una sola línea
total_images_count = len(soup.find_all("img"))
imagenes_title = total_images_count-alt_title_images_count
if alt_title_images_count and no_attr_images_count and no_attr_title_images_count == 0:
    #malasPracticas.append(f"Imágenes: {total_images_count}\nAlgunas Imágenes no cuentan con atributo o etiqueta ALT ({no_attr_images_count} de {total_images_count}) y atributo TITLE ({no_attr_title_images_count} de {total_images_count})")
    buenasPracticas.append({"Titulo":"Imágenes: ", "Valor":f"{total_images_count}", "Descripcion":"Las imagenes cuentan con todos sus atributos definidos."})
else:
    totalPractica +=1 
    malasPracticas.append({"Titulo":"Imágenes: ", "Valor":f"{total_images_count}", "Descripcion":f"Algunas Imágenes no cuentan con atributo o etiqueta ALT ({no_attr_images_count} de {total_images_count}) y atributo TITLE ({imagenes_title} de {total_images_count}."})
    # buenasPracticas.append(f"Imágenes: {total_images_count}\nLas imagenes cuentan con todos sus atributos definidos.")

# Identificar enlaces internos
internal_links = [[a.get_text(), a["href"], "nofollow" if "nofollow" in str(a) else "follow", "title" in a.attrs] for a in soup.find_all('a', href=True) if url in a["href"] or a["href"].startswith("/")]
number_internal_links = len(internal_links)
links_with_title_count = sum(1 for link in internal_links if link[3])
if number_internal_links==links_with_title_count:
    buenasPracticas.append({"Titulo":"Links internos: ", "Valor":f"{number_internal_links}", "Descripcion":f"Todos los links cuentan con el atributo TITLE ({links_with_title_count} de {number_internal_links})."})
else:
    malasPracticas.append({"Titulo":"Links internos: ", "Valor":f"{number_internal_links}", "Descripcion":f"Algunos links no cuentan con el atributo TITLE ({links_with_title_count} de {number_internal_links})."})

# Identificar enlaces externos
external_links = [[a.get_text(), a["href"], "nofollow"] if "nofollow" in str(a) else [a.get_text(), a["href"], "follow"] for a in soup.find_all('a', href=True) if url not in a["href"] and not a["href"].startswith("/")]
number_external_links = len(external_links)
if number_external_links > 0:
    buenasPracticas.append({"Titulo":"Links externos: ", "Valor":f"{number_external_links}", "Descripcion" : f"Existen {number_external_links} links a otras entidades fuera de la organización"})
    totalPractica += 1
else:
    malasPracticas.append({"Titulo":"Links externos: ", "Valor": "0", "Descripcion" : "No existen links a otras entidades fuera de la organización"})

# Contar la cantidad de enlaces rotos
broken_links_count = 0
for link in soup.find_all("a"):
    if link.has_attr("href"):
        try:
            response = requests.get(link["href"])
            if response.status_code >= 400:
                broken_links_count += 1
        except:
            broken_links_count += 1
if broken_links_count != 0:
    malasPracticas.append({"Titulo" : "Links Rotos: ", "Valor" : f"{broken_links_count}", "Descripcion" : f"Existen {broken_links_count} links que no están definidos."})
else:
    totalPractica += 1
    buenasPracticas.append({"Titulo" : "Links Rotos: ", "Valor" :  f"{broken_links_count}", "Descripcion" : "Todos los links están definidos."})

# Contar la cantidad total de enlaces
total_links_count = len(soup.find_all("a"))

# Verificar si hay redireccionamiento 301
redirection = False
if response.history:
    for resp in response.history:
        if resp.status_code == 301:
            redirection = True
            totalPractica +=1
            buenasPracticas.append({"Titulo" : "Redireccionamiento 301: ", "Valor" : "Si", "Descripcion" :  "La página tiene redireccionamiento 301"})
        else:
            malasPracticas.append({"Titulo" : "Redireccionamiento 301: ", "Valor" :  "No",  "Descripcion" : "La página no tiene redireccionamiento 301"})

# Verificar si hay canonicalización
canonicalization = False
if soup.find("link", attrs={"rel": "canonical"}):
    canonicalization = True
    totalPractica +=1
    buenasPracticas.append({"Titulo" : "Canonicalización: ", "Valor" : f"{url}", "Descripcion" : "La página tiene la etiqueta CANONICAL."})
else:
    malasPracticas.append({"Titulo" : "Canonicalización: ", "Valor" :  f"{url}", "Descripcion" : "La página no tiene la etiqueta CANONICAL."})

# Verificar si hay robots.txt
robots = False
response = requests.get(url + "/robots.txt")
if response.status_code == 200:
    robots = True
    totalPractica +=1
    buenasPracticas.append({"Titulo" : "Robots: ", "Valor" : "Si", "Descripcion" : "La página tiene un archivo Robots.txt"})
else:
    malasPracticas.append({"Titulo" : "Robots: ", "Valor" : "No", "Descripcion" : "La página no tiene un archivo Robots.txt"})

# Verificar si hay sitemap.xml
sitemap = False
response = requests.get(url + "/sitemap.xml")
if response.status_code == 200:
    sitemap = True
    totalPractica +=1
    buenasPracticas.append({"Titulo" : "Sitemap: ", "Valor" : "Si", "Descripcion" : "La página tiene un archivo sitemap.xml"})
else:
    malasPracticas.append({"Titulo" : "Sitemap: ", "Valor" : "No", "Descripcion" : "La página no tiene un archivo sitemap.xml"})

# # Obtener el tiempo de carga de la página
# load_time = response.elapsed.total_seconds()
# print("El tiempo de carga de la página es de: ", load_time, "segundos.")

# Verificar si hay una página de error 404 personalizada
error_404 = False
response = requests.get(url + "/404")
if response.status_code == 404:
    error_404 = True
    totalPractica +=1
    buenasPracticas.append({"Titulo" : "Error 404: ", "Valor" : "Si", "Descripcion" : "La página tiene una página de error 404 personalizada"})
else:
    malasPracticas.append({"Titulo" : "Error 404: ", "Valor" : "No", "Descripcion" : "La página no tiene una página de error 404 personalizada"})

# Obtener el idioma principal de la página (si lo tiene)
html_language = html_tag['lang']
if html_language:
    totalPractica +=1
    buenasPracticas.append({"Titulo" : "Idioma: ", "Valor" : f"{ html_language}" , "Descripcion" : "Haz especificado el idioma de tu sitio web"})
else:
    malasPracticas.append({"Titulo" : "Idioma: ", "Valor" : "No encontrado", "Descripcion" : f"No haz especificado el idioma de tu sitio web"})

# Verificar si la página tiene optimización móvil
viewport = soup.find("meta", attrs={"name": "viewport"})
if viewport:
    totalPractica += 1
    buenasPracticas.append({"Titulo" : "Optimización Movil: ", "Valor" : "Si", "Descripcion" : f"La página tiene optimización móvil"})
else:
    malasPracticas.append({"Titulo" : "Optimización Movil: ", "Valor" : "No", "Descripcion" : f"La página no tiene optimización móvil"})
    
# Verificar si la página es compatible con dispositivos móviles
# mobile_compatible = soup.find("meta", attrs={"name": "mobileoptimized"})
# if mobile_compatible:
#     totalPractica += 1
#     buenasPracticas.append("Compatibilidad Movil: Si\nLa página es compatible con dispositivos móviles")
# else:
#     malasPracticas.append("Compatibilidad Movil: No\nLa página no es compatible con dispositivos móviles")

# Analizar el HTML en busca del código de seguimiento de Google Analytics
def has_google_analytics(content):
    soup = BeautifulSoup(content, 'html.parser')
    for link in soup.find_all('link'):
        if 'rel' in link.attrs and 'href' in link.attrs and 'preconnect' in link.attrs['rel']:
            if 'google-analytics.com' in link.attrs['href']:
                return True
    return False

if has_google_analytics(content):
    totalPractica +=1
    buenasPracticas.append({"Titulo" : "Google™ Analytics: ", "Valor" : "Si", "Descripcion" : "El seguimiento de Google™ Analytics está presente en la página."})
else:
    malasPracticas.append({"Titulo" : "Google™ Analytics: ", "Valor" : "No", "Descripcion" : "El seguimiento de Google™ Analytics no está presente en la página."})

# Obtener el método de codificación de la página
charset = soup.meta.get("charset")
if charset:
    totalPractica +=1
    buenasPracticas.append({"Titulo" :"Códificación: ", "Valor" : f"{charset}", "Descripcion" : "La codificación idioma/carácteres está especificada"})
else:
    malasPracticas.append({"Titulo" :"Códificación: ", "Valor" : "No encontrado", "Descripcion" : "La codificación idioma/carácteres no está especificada"})

# Verificar si la página tiene certificado SSL
if url.startswith("https://"):
    totalPractica +=1
    buenasPracticas.append({"Titulo" :"Certificado ssl: ", "Valor" : "Si", "Descripcion" : "La página cuenta con un certificado SSL"})
else:
    ssl_cert = response.headers.get("Strict-Transport-Security")
    if ssl_cert:
        totalPractica +=1
        buenasPracticas.append({"Titulo" :"Certificado ssl: ", "Valor" : "Si", "Descripcion" : "La página cuenta con un certificado SSL"})
    else:
        malasPracticas.append({"Titulo" :"Certificado ssl: ", "Valor" : "No", "Descripcion" : "La página no cuenta con un certificado SSL"})

promedio = (totalPractica / 15)*10

print("")

if promedio.is_integer():
    promedio = int(promedio)
    print("Tienes un promedio de optimización de: {:.0f}/10".format(promedio))
else:
    print("Tienes un promedio de optimización de: {:.1f}/10".format(promedio))

print("\nBuenas prácticas:\n")
for item in buenasPracticas:
    print(item)

print("\nMalas prácticas: \n")
for item in malasPracticas:
    print(item)

print("\nKeywords encontradas: \n")

print(keywords)