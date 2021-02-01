from html import escape

import arxiv
import telebot

my_bot = telebot.TeleBot('insert-token-here')


def arxiv_checker(message):
    my_bot.send_chat_action(message.chat.id, 'upload_document')
    if len(message.text.split()) > 1:
        arxiv_search(' '.join(message.text.split(' ')[1:]), message)
    else:
        return "Nothing to show, try to search smth else."


def arxiv_search(query, message):
    try:
        arxiv_search_res = arxiv.query(query, max_results=10)
        query_answer = ''
        for paper in arxiv_search_res:
            end = '…' if len(paper['summary']) > 300 else ''
            a_name = paper['authors'][0]
            if len(paper['authors']) > 5:
                a_name += ' et al'
            query_answer += \
                '• {0}. "[{1}]({2})". {3}{4}.<br>'.format(
                    a_name,
                    escape(paper['title'].replace('\n', ' ')),
                    paper['pdf_url'],
                    escape(paper['summary'][0:300].replace('\n', ' ')),
                    end)
        my_bot.reply_to(message, query_answer, parse_mode="Markdown")

    except Exception:
        pass


@my_bot.message_handler(commands=['arxiv'])
def do_arxiv_check(message):
    arxiv_checker(message)


my_bot.polling(none_stop=True, interval=0)
