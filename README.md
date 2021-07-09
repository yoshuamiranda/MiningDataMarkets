# MiningDataMarkets
Mining Data for Emerging Markets

Descripcion:
Busqueda de informacion real de las opiniones de personas respecto a un tema en la red social de twitter asi como la prediccion con los resultados de esas opiniones para un mercadeo futuro


El proyecto se devide en varios scripts

#script.py
Este archivo toma el ultimo tweet guardado (ID) en la bd y hace una busqueda con la API de twitter con un ID mayor al recuperado asi no se repiten datos
La informacion que entrega twitter es guardado en una base de datos en MONGO y los datos relevantes que necesitamos son guardados en una base de datos MySQL

-Se limpia los textos de tweet
-Se eliminan los retweets para no tener inormacion repetida
-Se guardan los hashtags
-Se guardan los usuarios
-Se guardan la palabras de cada texto por separado
-Se guardan las cantidades de retwets o Favs que tenga un tweet

Este archivo se corre automaticamemte cada hora

#sa_spanish
Este archivo califica el texto que se ha guardado anteriormente en una escala entre 0 (negativo) y 1 (positivo)

Este archivo se corre automaticamemte cada hora

#AWSSentiment
Este archivo califica de una forma mejor las opiniones de los textos entregando 5 resultados en una escala entre 0 y 1
-Positivo entre 0 y 1
-Negativo entre 0 y 1
-Neutro entre 0 y 1
-Mezclado entre 0 y 1
-Que tipo de texto es de acuerdo a las calificaciones dadas en texto

Este archivo se corre automaticamemte cada hora

#words.py
Este archivo limpia las palabras vacias (stopwords) para no tmarlas en cuenta para nuestros analisis
