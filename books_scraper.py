
import requests
from bs4 import BeautifulSoup

# URL de base
base_url = 'https://books.toscrape.com/catalogue/page-{}.html'

# Liste pour stocker tous les URLs des livres
book_urls = []

# Parcourir les 50 premières pages
for page_num in range(1, 51):  # 1 à 50 inclus
    # Construire l'URL de chaque page
    url = base_url.format(page_num)
    
    # Faire la requête pour chaque page
    response = requests.get(url)
    
    # Vérifier si la requête est réussie
    if response.status_code == 200:
        # Parse le HTML avec BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraire les URLs des livres sur la page
        for article in soup.find_all('article', class_='product_pod'):
            # Trouver l'URL relative du livre
            link = article.find('a')['href']
            # Reconstituer l'URL complète (remplacer les chemins relatifs)
            full_link = 'https://books.toscrape.com/catalogue/' + link.replace('../../../', '')
            # Ajouter l'URL à la liste
            book_urls.append(full_link)
        
    else:
        print(f"Erreur lors de la récupération de la page {page_num}, code d'état: {response.status_code}")

# Vérifier le nombre d'URL collectées
print(f"Nombre total d'URLs collectées: {len(book_urls)}")



from bs4 import BeautifulSoup
import pandas as pd
# Variable pour vérifier si c'est la première écriture dans le fichier
first_write = True

# Parcourir les URLs de chaque livre
for url in book_urls:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        def extract_book_data(soup):
            # Remplacer ces sélecteurs par ceux correspondant au code source réel du livre
            title = soup.find('h1').text if soup.find('h1') else 'Titre non trouvé'
            star_rating = soup.find('p', class_='star-rating')['class'][1] if soup.find('p', class_='star-rating') else 'Note non trouvée'
            price = soup.find('p', class_='price_color').text if soup.find('p', class_='price_color') else 'Prix non trouvé'
            quantity = soup.find('p', class_='instock availability').text.strip() if soup.find('p', class_='instock availability') else 'Quantité non trouvée'
            genre = soup.find('ul', class_='breadcrumb').find_all('a')[2].text if soup.find('ul', class_='breadcrumb') else 'Genre non trouvé'
            description = soup.find('meta', attrs={'name':'description'})['content'].strip() if soup.find('meta', attrs={'name':'description'}) else 'Description non trouvée'

            return {
                'Title': title,
                'Star Rating': star_rating,
                'Price': price,
                'Quantity': quantity,
                'Genre': genre,
                'Description': description
            }

        # Récupérer les données du livre
        book_data = extract_book_data(soup)

        # Créer un DataFrame Pandas pour la ligne de ce livre
        df = pd.DataFrame([book_data])

        # Sauvegarder les données dans un fichier CSV
        if first_write:
            # Première écriture : créer un nouveau fichier avec l'en-tête
            df.to_csv('book_data.csv', index=False, mode='w')
            first_write = False
        else:
            # Ajout à la suite : ne pas réécrire l'en-tête
            df.to_csv('book_data.csv', index=False, mode='a', header=False)

        print(f"Les données du livre {book_data['Title']} ont été extraites et enregistrées.")
    else:
        print(f"Erreur lors de la récupération de la page {url}. Code d'état : {response.status_code}")


    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        def extract_book_data(soup):
        # Remplacer ces sélecteurs par ceux correspondant au code source réel du livre
            title = soup.find('h1').text if soup.find('h1') else 'Titre non trouvé'
            star_rating = soup.find('p', class_='star-rating')['class'][1] if soup.find('p', class_='star-rating') else 'Note non trouvée'
            price = soup.find('p', class_='price_color').text if soup.find('p', class_='price_color') else 'Prix non trouvé'
            quantity = soup.find('p', class_='instock availability').text.strip() if soup.find('p', class_='instock availability') else 'Quantité non trouvée'
            genre = soup.find('a', href=True, class_='genre').text if soup.find('a', href=True, class_='genre') else 'Genre non trouvé'
            description = soup.find('meta', attrs={'name':'description'})['content'].strip() if soup.find('meta', attrs={'name':'description'}) else 'Description non trouvée'

            return {
                'Title': title,
                'Star Rating': star_rating,
                'Price': price,
                'Quantity': quantity,
                'Genre': genre,
                'Description': description
            }

    # Récupérer les données du livre
        book_data = extract_book_data(soup)

    # Créer un DataFrame Pandas
        df = pd.DataFrame([book_data])

    # Sauvegarder les données dans un fichier Excel ou CSV
        df.to_csv('book_data.csv', index=False)  # Sauvegarder en CSV
    # print(df)

        print("Les données du livre ont été extraites et enregistrées dans un fichier.")
    else:
        print(f"Erreur lors de la récupération de la page. Code d'état : {response.status_code}")

all_books_data = []

# Parcourir les URLs de chaque livre
for url in book_urls:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        def extract_book_data(soup):
            # Remplacer ces sélecteurs par ceux correspondant au code source réel du livre
            title = soup.find('h1').text if soup.find('h1') else 'Titre non trouvé'
            star_rating = soup.find('p', class_='star-rating')['class'][1] if soup.find('p', class_='star-rating') else 'Note non trouvée'
            price = soup.find('p', class_='price_color').text if soup.find('p', class_='price_color') else 'Prix non trouvé'
            quantity = soup.find('p', class_='instock availability').text.strip() if soup.find('p', class_='instock availability') else 'Quantité non trouvée'
            genre = soup.find('ul', class_='breadcrumb').find_all('a')[2].text if soup.find('ul', class_='breadcrumb') else 'Genre non trouvé'
            description = soup.find('meta', attrs={'name':'description'})['content'].strip() if soup.find('meta', attrs={'name':'description'}) else 'Description non trouvée'

            return {
                'Title': title,
                'Star Rating': star_rating,
                'Price': price,
                'Quantity': quantity,
                'Genre': genre,
                'Description': description
            }

        # Récupérer les données du livre
        book_data = extract_book_data(soup)

        # Ajouter les données du livre à la liste
        all_books_data.append(book_data)

        print(f"Les données du livre {book_data['Title']} ont été extraites.")
    else:
        print(f"Erreur lors de la récupération de la page {url}. Code d'état : {response.status_code}")

# Créer un DataFrame Pandas unique avec toutes les données collectées
df = pd.DataFrame(all_books_data)

# Sauvegarder les données dans un fichier CSV
df.to_csv('book_data.csv', index=False)

print(f"Les données de {len(all_books_data)} livres ont été enregistrées dans 'book_data.csv'.")
