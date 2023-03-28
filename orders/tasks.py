# from datetime import datetime
# from urllib.request import urlopen
#
# from bs4 import BeautifulSoup
#
from celery import shared_task
from django.core.mail import send_mail
from django.http import BadHeaderError, HttpResponse

# from quote.models import Author, Quote
#
# import requests
from core import settings


# Helping function: Checking the connection to the site:
# @shared_task
# def check_connection(url):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         return response
#     except requests.HTTPError as e:
#         raise e
#     except Exception as e:
#         raise e


# The main function
# @shared_task
# def author_quote():
#     page = 1
#     count_5 = 0
#     while True:
#         # https://quotes.toscrape.com/page/1/   -- the first page of the site
#         url = f"https://quotes.toscrape.com/page/{page}/"
#         if not check_connection(url):  # Helping function: Checking the connection to the site
#             return
#         try:
#             raw = urlopen(url).read()
#             original = raw.decode('utf-8')
#             replacement = original.replace('\u201c', '').replace('\u201d', '').replace('\u2019', "")
#             soup = BeautifulSoup(replacement, features='html.parser',)
#             if not soup('span', class_="text",):
#                 email_end()  # Helping function: Sends email when all quotes are in DataBase
#                 return
#             quotes = soup.findAll('div', class_="quote",)
#             quote_list = []
#             for q in quotes:
#                 text = q.find('span', class_="text",).text
#                 name_author = q.find('small', class_="author",).text.split()
#                 semi_link = q.find("a")['href']
#                 url_author = f"http://quotes.toscrape.com{ semi_link}/"
#                 quote = author_data(url_author)  # Helping function: Parsing authors page
#                 quote['text'] = text
#                 quote['first_name'] = name_author[0]
#                 quote['last_name'] = " ".join(name_author[1:])
#                 quote_list.append(quote)
#             count_5 = save_5(quote_list, count_5)  # Helping function: Saving 5 quotes from one page
#             if count_5 == 5:
#                 break  # Stops after saving 5 quotes per one work
#             page += 1

    #     except Exception as e:
    #         raise e
    # return


# Helping function: Parsing authors page
# @shared_task
# def author_data(url_author):
#     check_connection(url_author)
#     try:
#         raw_author = urlopen(url_author).read()
#         original = raw_author.decode('utf-8')
#         replacement = original.replace('\u201c', '').replace('\u201d', '').replace('\u2019', '').replace(
#             '&#34;', '"').replace('\\', '').replace('\n    ', '').replace('&#39;', '')
#
#         soup = BeautifulSoup(replacement, features='html.parser',)
#         authors = soup.findAll('div', class_="author-details", )
#         for a in authors:
#             date_of_birth_wrong = a.find('span', class_="author-born-date",).text
#             date_of_birth = datetime.strptime(date_of_birth_wrong, '%B %d, %Y')
#             place_of_birth = a.find("span", class_="author-born-location",).text
#             quote = {
#                 "now": str(datetime.now()),
#                 'date_of_birth': date_of_birth,
#                 'place_of_birth': place_of_birth,
#             }
#             return quote
#     except Exception as e:
#         raise e
#
#
# # Helping function: Saving 5 quotes from one page
# # @shared_task
# def save_5(quote_list, count_5):
#     for q in quote_list:
#         try:
#             author = Author.objects.get(first_name=q['first_name'], last_name=q['last_name'],
#                                         date_of_birth=q['date_of_birth'], place_of_birth=q['place_of_birth'])
#         except Author.DoesNotExist:
#             author = Author.objects.create(
#                 first_name=q['first_name'],
#                 last_name=q['last_name'],
#                 date_of_birth=q['date_of_birth'],
#                 place_of_birth=q['place_of_birth'],
#             )
#         pk = author.id
#
#         try:
#             Quote.objects.get(text=q['text'],)
#         except Quote.DoesNotExist:
#             Quote.objects.create(
#                 title=" ".join(q['text'].split()[:4]) + "...",
#                 author=Author.objects.get(pk=pk),
#                 text=q['text'],
#             )
#             count_5 += 1
#             if count_5 == 5:
#                 return count_5  # Stop main function after saving 5 quotes per one work
#     return count_5  # The main function gives another page or sends email


# # Helping function: Sends email when all quotes are in DataBase
# @shared_task
# def email_end():
#     send_mail(
#         f"BookShop.",
#         "Цитаты закончились...",
#         "admin@admin.com",
#         ["admin@admin.com"],
#         fail_silently=False,
#     )
#     return


@shared_task
def send_mail_temp(subject, message, user_email=None):
    email_to = [settings.EMAIL_HOST_USER, user_email]
    if user_email is None:
        email_to = [settings.EMAIL_HOST_USER]
    try:
        send_mail(
            subject=f"{subject}",
            message=f"{message}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=email_to,
            fail_silently=False,
        )
    except BadHeaderError:
        return HttpResponse("Invalid header found.")
