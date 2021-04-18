import requests, bs4

BASE_URL = "https://www.tudogostoso.com.br"

user_input = input("Digite o que deseja pesquisar: ")

class Recipe:
    link = BASE_URL
    img = ''
    category = ''
    title = ''
    author = ''

def main():
    recipes = get_data_from_other_pages()
    for i in range(len(recipes)):
      print('{} - {}'.format((i+1), recipes[i].title))

def get_url(page):
    research = user_input.replace(" ", "+")
    url = BASE_URL + "/busca?page={}&q={}".format(page, research)
    return url

def get_input():
    return input("Digite o que deseja pesquisar: ")
    
def get_str_without_spaces(string):
    return string.rstrip().lstrip()
    
def get_html(page):
    url = get_url(page)
    result = requests.get(url)
    tree = bs4.BeautifulSoup(result.text, features="html.parser" )
    html = tree.prettify()
    return bs4.BeautifulSoup(html, features="html.parser")

def find_recipes(page):
    html = get_html(page)
    return html.select('.recipe-card a')
    
def get_data(page):
    recipes_list = []
    
    for item in find_recipes(page):
        item_link = BASE_URL + item.get('href')
        item_img = item.select('.image')
        item_category = item.select('.category span')
        item_title = item.select('.title')
        item_author = item.select('.user span')
        recipe = Recipe()
        
        recipe.link = item_link
        recipe.img  = item_img[0].get('src')
        recipe.category = get_str_without_spaces(item_category[0].get_text())
        recipe.title = get_str_without_spaces(item_title[0].get_text())
        recipe_author = get_str_without_spaces(item_author[0].get_text())
        
        recipes_list.append(recipe)
        
    del recipes_list[-5:]
     
    return recipes_list
    

def get_num_pages():
    html = get_html(1)
    total_results = html.select('.num')[0]
    num_recipes = get_num_of_string(total_results.text)
    page = 1
    
    if num_recipes > 1005:
        page = int(1005/15)
    elif (num_recipes%20 > 0):
        page = int(num_recipes/15) + 1
    
    return page

def get_num_of_string(string):
    new_string = ""
    for i in string:
        if i.isdigit():
            new_string = new_string + i
    return int(new_string)
    
def get_data_from_other_pages():
    recipes = []
    for i in range(get_num_pages()):
        recipes.extend(get_data(i+1))
        print("Page: {}".format(i+1))
    return recipes

main()