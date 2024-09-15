import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# URL de base
base_url = 'https://books.toscrape.com/catalogue/page-{}.html'

# Parcourir les 50 premières pages
book_urls = []
for page_num in tqdm(range(1, 51), desc="Gathering URLs"):
    # Construire l'URL de chaque page
    url = base_url.format(page_num)

    # Faire la requête pour chaque page
    response = requests.get(url)
    if response.status_code == 200:
        # Parse le HTML avec BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extraire les URLs des livres sur la page
        for article in soup.find_all('article', class_='product_pod'):
            # Trouver l'URL relative du livre
            link = article.find('a')['href']
            # Reconstituer l'URL complète (remplacer les chemins relatifs)
            full_link = 'https://books.toscrape.com/catalogue/' + \
                link.replace('../../../', '')
            # Ajouter l'URL à la liste
            book_urls.append(full_link)
    else:
        print(
            f"Erreur lors de la récupération de la page {page_num}, code d'état: {response.status_code}")

# Vérifier le nombre d'URL collectées
print(f"Nombre total d'URLs collectées: {len(book_urls)}")


# Parcourir les URLs de chaque livre
all_books_data = []
for url in tqdm(book_urls, desc="Extracting books data", leave=True):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        def extract_book_data(soup):
            # Remplacer ces sélecteurs par ceux correspondant au code source réel du livre
            title = soup.find('h1').text if soup.find(
                'h1') else 'Titre non trouvé'
            star_rating = soup.find('p', class_='star-rating')['class'][1] if soup.find(
                'p', class_='star-rating') else 'Note non trouvée'
            price = soup.find('p', class_='price_color').text if soup.find(
                'p', class_='price_color') else 'Prix non trouvé'
            quantity = soup.find('p', class_='instock availability').text.strip(
            ) if soup.find('p', class_='instock availability') else 'Quantité non trouvée'
            genre = soup.find('ul', class_='breadcrumb').find_all(
                'a')[2].text if soup.find('ul', class_='breadcrumb') else 'Genre non trouvé'
            description = soup.find('meta', attrs={'name': 'description'})['content'].strip(
            ) if soup.find('meta', attrs={'name': 'description'}) else 'Description non trouvée'

            return {
                'Title': title,
                'Star Rating': star_rating,
                'Price': price[1:],
                'Quantity': quantity,
                'Genre': genre,
                'Description': description
            }

        # Récupérer les données du livre
        book_data = extract_book_data(soup)
        all_books_data.append(book_data)
        print(f"Les données du livre {book_data['Title']} ont été extraites.")
    else:
        print(
            f"Erreur lors de la récupération de la page {url}. Code d'état : {response.status_code}")

# Sauvegarder les données dans un fichier CSV
df = pd.DataFrame(all_books_data)
df.to_csv('book_data.csv', index=False)
print(f"Les données de {len(all_books_data)} livres ont été enregistrées dans 'book_data.csv'.")
