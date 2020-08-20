def handler(event, context):
    import random
    facts_list = ['Сахар вызывает отложение жира.', 'Сахар создаёт чувство ложного голода.', 'Сахар способствует старению.', 'Сахар вызывает привыкание.', 'Сахар лишает организм витаминов группы B.', 'Сахар воздействует на сердце.', 'Сахар является возбудителем нервной системы.', 'Сахар вымывает кальций из организма.', 'Сахар снижает силу имунной системы в 17 раз.']
    random.shuffle(facts_list)
    headlines = []
    base = {
        'Напитки': {
            'Соки': {
                'Виноградный сок': 15,
                'Яблочный сок': 11,
                'Персиковый сок': 13,
                'Грушевый сок': 12,
                'Апельсиновый сок': 9,
                'Гранатовый сок': 8,
                'Вишнёвый сок': 8,
                'Морковный сок': 5,
                'Томатный сок': 4
            },
            'Компот': 22,
            'Кока-кола': 14,
            'Квас': 5,
            'Холодный чай': 11,
            'Коктейль': 15,
            'Алкоголь': {
                'Ром': 35,
                'Портвейн': 16,
                'Вино': 8,
                'Ликёр': 8
            }
        },
        'Фрукты': {
            'Банан': 20,
            'Яблоко': 13,
            'Виноград': 20,
            'Клубника': 8,
        },
        'Быстрые завтраки': {
            'Хлопья': 12,
            'Мюсли': 24
        },
        'Молочная продукция': {
            'Мороженое': 22,
            'Сладкий йогурт': 18
        },
        'Сладости': {
            'Мёд': 82,
            'Овсяное печенье': 25,
            'Карамель': 66,
            'Мороженое': 22,
            'Конфета': 50,
            'Леденец': 85,
            'Шоколад': {
                'Белый шоколад': 59,
                'Молочный шоколад': 52,
                'Тёмный шоколад (45%-59% какао)': 48,
                'Тёмный шоколад (60%-69% какао)': 37,
                'Тёмный шоколад (70%-85% какао)': 24
            }
        }
    }
    """
    Entry-point for Serverless Function.
    :param event: request payload.
    :param context: information about current execution context.
    :return: response to be serialized as JSON.
    """

    if event['session']['new']:
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {"question": "Любишь сладкое?", "facts": facts_list},
            'response': {
                'text': 'Привет! Любишь ли ты сладкое?',
                'buttons': [{'title': suggest, 'hide': True} for suggest in ["Да", "Нет"]],
                'end_session': 'false'
            },
        }

    if event['state']['session']['question'] == 'Любишь сладкое?':
        question = 'Знаете ли вы?'
        if event['request']['original_utterance'].lower() == 'да':
            text = 'О, я тоже сладкоежка, как и вы! Знаете ли вы, что сахар в больших количествах наносит вред организму?'
        elif event['request']['original_utterance'].lower() == 'нет':
            text = 'Ого, вы - редкость в наше время! Честно говоря, я как раз сладкоежка. Знаете ли вы, что сахар в больших количествах наносит вред организму?'
        elif event['request']['original_utterance'].lower() in ['помощь', 'что ты умеешь'] or 'умеешь' in event['request']['original_utterance'].lower():
            text = 'Я могу посчитать количество съеденного вами сахара, а также рассказать о его вреде. Давайте ещё раз: вы любите сладкое?'
            question = 'Любишь сладкое?'
        else:
            text = 'Простите, я не поняла вас, но я быстро учусь! Давайте ещё раз: вы любите сладкое?'
            question = 'Любишь сладкое?'
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {"question": question, "facts": facts_list},
            'response': {
                'text': text,
                'buttons': [{'title': suggest, 'hide': True} for suggest in ["Да", "Нет"]],
                'end_session': 'false'
            },
        }

    elif event['state']['session']['question'] == 'Знаете ли вы?':
        question = 'Следите ли?'
        if event['request']['original_utterance'].lower() == 'да':
            text = 'Вы - большой молодец, поскольку знание - сила! Раз вы знаете о вреде, то, наверное, следите за ежедневным потреблением сахара?'
        elif event['request']['original_utterance'].lower() == 'нет':
            question = 'Факты'
            text = 'Это не есть хорошо, поскольку необходимо сахар - большой вредитель нашему здоровью. Хотите узнать факты о вреде сахара?'
        elif event['request']['original_utterance'].lower() in ['помощь', 'что ты умеешь'] or 'умеешь' in event['request']['original_utterance'].lower():
            text = 'Я могу посчитать количество съеденного вами сахара, а также рассказать о его вреде. Давайте ещё раз: знаете ли вы, что сахар в больших количествах наносит вред организму?'
            question = 'Знаете ли вы?'
        else:
            text = 'Простите, я не поняла вас, но я быстро учусь! Давайте ещё раз: знаете ли вы, что сахар в больших количествах наносит вред организму?'
            question = 'Знаете ли вы?'
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {"question": question, "facts": facts_list},
            'response': {
                'text': text,
                'buttons': [{'title': suggest, 'hide': True} for suggest in ["Да", "Нет"]],
                'end_session': 'false'
            },
        }

    elif (event['state']['session']['question'] == 'Факты' and event['request']['original_utterance'].lower() != 'проверка') or event['request']['original_utterance'].lower() == 'факты':
        question = 'Факты'
        replies = ['Следующий факт', 'Стоп']
        if event['request']['original_utterance'].lower() in ['следующий факт', 'да'] or 'факт' in event['request']['original_utterance'].lower():
            text = event['state']['session']['facts'][0]
            if len(event['state']['session']['facts']) == 1:
                text += ' Будем честны: существует ещё немало вредных воздействий сахара на организм. Как насчёт того, чтобы посчитать количество употреблённого вами сахара за сегодня?'
                replies = ['Да', 'Нет']
                question = 'Проверка'
        elif event['request']['original_utterance'].lower() in ['стоп', 'нет']:
            text = 'Хорошо. Как насчёт того, чтобы посчитать количество употреблённого вами сахара за сегодня?'
            replies = ['Да', 'Нет']
            question = 'Проверка'
        elif event['request']['original_utterance'].lower() in ['помощь', 'что ты умеешь'] or 'умеешь' in event['request']['original_utterance'].lower():
            text = 'Я могу посчитать количество съеденного вами сахара, а также рассказать о его вреде. Что вы хотите: услышать факты или посчитать количество сахара?'
            replies = ['Факты', 'Проверка']
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {"question": question, "facts": event['state']['session']['facts'][1:], "history_list": []},
            'response': {
                'text': text,
                'buttons': [{'title': suggest, 'hide': True} for suggest in replies],
                'end_session': 'false'
            },
        }

    elif event['state']['session']['question'] == 'Следите ли?':
        question = 'Проверка'
        if event['request']['original_utterance'].lower() == 'да':
            text = 'Это замечательно! Надеюсь, у вас всё под контролем. Не хотите ли проверить ваш текущий уровень сахара?'
        elif event['request']['original_utterance'].lower() == 'нет':
            text = 'Сегодняшний день - повод начать следить за потреблением сладкого. Не хотите ли проверить ваш текущий уровень сахара?'
        elif event['request']['original_utterance'].lower() in ['помощь', 'что ты умеешь'] or 'умеешь' in event['request']['original_utterance'].lower():
            text = 'Я могу посчитать количество съеденного вами сахара, а также рассказать о его вреде. Давайте ещё раз: следите ли вы за ежедневным потреблением сахара?'
            question = 'Следите ли?'
        else:
            text = 'Простите, я не поняла вас, но я быстро учусь! Давайте ещё раз: следите ли вы за ежедневным потреблением сахара?'
            question = 'Следите ли?'
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {"question": question, "facts": facts_list, "history_list": []},
            'response': {
                'text': text,
                'buttons': [{'title': suggest, 'hide': True} for suggest in ["Да", "Нет"]],
                'end_session': 'false'
            },
        }

    elif (event['state']['session']['question'] == 'Проверка' and "all_sum" not in event['state']['session']) or (event['state']['session']['question'] == 'Всё') or (event['request']['original_utterance'].lower() == 'проверка'):
        replies = list(base.keys())
        question = 'Проверка'
        flag = 'false'
        if event['request']['original_utterance'].lower() in ['да', 'проверка']:
            text = 'Назовите категорию продукта, который вы сегодня съели.'
        elif event['request']['original_utterance'].lower() in ['нет', 'хватит']:
            text = 'Ну, не хотите - как хотите.'
            question = 'Молчанка'
            flag = 'true'
        elif event['request']['original_utterance'].lower() in ['помощь', 'что ты умеешь'] or 'умеешь' in event['request']['original_utterance'].lower():
            text = 'Я могу посчитать количество съеденного вами сахара, а также рассказать о его вреде. Что вы хотите: услышать факты или посчитать количество сахара?'
            replies = ['Факты', 'Проверка']
        else:
            text = 'Простите, я не поняла вас, но я быстро учусь! Если вы хотите проверить ваш текущий уровень сахара, то назовите категорию продукта, если не хотите - скажите: "Нет" или "Хватит"'
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {"question": question, "all_sum": 0, "way": base, "history": {}, "facts": facts_list, "history_list": []},
            'response': {
                'text': text,
                'buttons': [{'title': suggest, 'hide': True} for suggest in replies],
                'end_session': flag
            },
        }

    elif event['state']['session']['question'] == 'Проверка':
        question = 'Проверка'
        replies = list(base.keys())
        replies.append('Стоп')
        replies.append('Назад')
        replies.append('Сброс')
        replies.append('Хватит')
        now_history = event['state']['session']['history']
        history_list = event['state']['session']['history_list']
        ways = event['state']['session']['way']
        text = 'Уточните продукт. Если ошиблись с текущим продуктом - скажите "Назад". Если хотите удалить предыдущий продукт - скажите "Сброс".'
        answer = 0
        if event['request']['original_utterance'] in ways:
            if type(event['state']['session']['way'][event['request']['original_utterance']]) == float or type(
                    event['state']['session']['way'][event['request']['original_utterance']]) == int:
                answer = event['state']['session']['way'][event['request']['original_utterance']]
                replies = ['100', '250', '500', '750', '1000']
                now_history = event['state']['session']['history']
                text = 'Внесён продукт %s. Сколько грамм или миллилитров этого продукта было употреблено?' % (event['request']['original_utterance'].lower())
                ways = event['request']['original_utterance'] + '@' + str(answer)
                if event['request']['original_utterance'] not in now_history:
                    now_history[event['request']['original_utterance']] = 0
                return {
                    'version': event['version'],
                    'session': event['session'],
                    'session_state': {"question": question, "all_sum": event['state']['session']['all_sum'],
                                      "way": ways, "history": now_history, "facts": facts_list, "history_list": history_list},
                    'response': {
                        'text': text,
                        'buttons': [{'title': suggest, 'hide': True} for suggest in replies],
                        'end_session': 'false'
                    },
                }
            else:
                replies = event['state']['session']['way'][event['request']['original_utterance']]
                ways = replies.copy()
                replies = list(replies.keys())
                replies.append('Стоп')
                replies.append('Назад')
                replies.append('Сброс')
                replies.append('Хватит')
        elif event['request']['original_utterance'].lower() == 'хватит':
            return {
                'version': event['version'],
                'session': event['session'],
                'session_state': {"question": 'Молчанка', "all_sum": event['state']['session']['all_sum'], "way": ways,
                                  "history": now_history, "facts": facts_list, "history_list": history_list},
                'response': {
                    'text': 'Поняла',
                    #'buttons': [{'title': suggest, 'hide': True} for suggest in replies],
                    'end_session': 'true'
                },
            }
        elif event['request']['original_utterance'].lower() == 'стоп':
            text = 'Хорошо. Вы мужчина или женщина?'
            question = 'МЖ'
            replies = ['Мужчина', 'Женщина']
        elif event['request']['original_utterance'].lower() == 'назад':
            text = 'Назовите категорию продукта, который вы сегодня съели.'
            try:
                if '@' in ways:
                    now_history.pop(ways.split('@')[:-1][0])
            except:
                pass
            replies = list(base.keys())
            replies.append('Стоп')
            replies.append('Назад')
            replies.append('Сброс')
            replies.append('Хватит')
            ways = base.copy()
        elif event['request']['original_utterance'].lower() == 'сброс':
            if len(history_list) > 0:
                delete_product = history_list.pop()
                now_history[delete_product[0]] -= delete_product[1]
                if now_history[delete_product[0]] == 0:
                    now_history.pop(delete_product[0])
                    text = 'Удалён продукт %s.' % (delete_product[0].lower())
                else:
                    text = 'Удалён продукт %s в размере %s.' % (delete_product[0], str(delete_product[1]))
            else:
                text = 'Вы удалили все продукты. '
            text += ' Назовите категорию продукта, который вы сегодня съели.'
            replies = list(base.keys())
            replies.append('Стоп')
            replies.append('Назад')
            replies.append('Сброс')
            replies.append('Хватит')
            ways = base.copy()
        elif event['request']['original_utterance'].lower() in ['помощь', 'что ты умеешь'] or 'умеешь' in event['request']['original_utterance'].lower():
            text = 'Я могу посчитать количество съеденного вами сахара, а также рассказать о его вреде. Что вы хотите: услышать факты или посчитать количество сахара?'
            replies = ['Факты', 'Проверка']
            try:
                if '@' in ways:
                    now_history.pop(ways.split('@')[:-1][0])
            except:
                pass
        else:
            try:
                x = float(event['request']['original_utterance'])
            except:
                if type(ways) == dict:
                    replies = list(event['state']['session']['way'].keys())
                    replies.append('Стоп')
                    replies.append('Назад')
                    replies.append('Сброс')
                    replies.append('Хватит')
                    text = 'Такого продукта я не знаю.'
                else:
                    replies = ['100', '250', '500', '1000']
                    text = 'Введите корректное количество продукта.'
            else:
                replies = list(base.keys())
                replies.append('Стоп')
                replies.append('Назад')
                replies.append('Сброс')
                replies.append('Хватит')
                product = event['state']['session']['way'].split('@')[:-1][0]
                now_history = event['state']['session']['history']
                ways = base.copy()
                text = 'Внесён продукт %s, употреблённый в объёме %s мл или г. Давайте считать дальше. Назовите категорию продукта. Если всё внесено - скажите "Стоп". Если надоело - скажите "Хватит". Ошиблись с продуктом - скажите "Сброс".' % (product.lower(), event['request']['original_utterance'])
                history_list.append([product, round(float(event['request']['original_utterance']) / 100 * float(event['state']['session']['way'].split('@')[-1]))])
                if product not in now_history:
                    now_history[product] = round(float(event['request']['original_utterance']) / 100 * float(event['state']['session']['way'].split('@')[-1]))
                else:
                    now_history[product] += round(float(event['request']['original_utterance']) / 100 * float(event['state']['session']['way'].split('@')[-1]))

        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {"question": question, "all_sum": event['state']['session']['all_sum'], "way": ways, "history": now_history, "facts": facts_list, "history_list": history_list},
            'response': {
                'text': text,
                'buttons': [{'title': suggest, 'hide': True} for suggest in replies],
                'end_session': 'false'
            },
        }

    elif event['state']['session']['question'] == 'МЖ':
        question = 'Всё'
        if event['request']['original_utterance'].lower() == 'мужчина':
            norm = 60
            text = 'Итак, максимально допустимой дневной дозой для вас является 60 граммов сахара в день, оптимальное количество - 30 грамм. Вы употребили %s грамм сахара.' % (sum(event['state']['session']['history'].values()))
        elif event['request']['original_utterance'].lower() == 'женщина':
            text = 'Итак, максимально допустимой дневной дозой для вас является 50 граммов сахара в день, оптимальное количество - 25 грамм. Вы употребили %s грамм сахара.' % (sum(event['state']['session']['history'].values()))
            norm = 50
        else:
            if event['request']['original_utterance'].lower() in ['помощь', 'что ты умеешь'] or 'умеешь' in event['request']['original_utterance'].lower():
                text = 'В данный момент я определяю, сколько сахара вы съели.'
            else:
                text = 'Простите, я не совсем поняла.'
            text += ' Давайте ещё раз: вы мужчина или женщина?'
            replies = ['Мужчина', 'Женщина']
            question = 'МЖ'
            return {
                'version': event['version'],
                'session': event['session'],
                'session_state': {"question": 'МЖ', "all_sum": event['state']['session']['all_sum'], "history_list": event['state']['session']['history_list'], "way": event['state']['session']['way'], "history": event['state']['session']['history'], "facts": facts_list},
                'response': {
                    'text': text,
                    'buttons': [{'title': suggest, 'hide': True} for suggest in replies],
                    'end_session': 'false'
                },
            }
        if norm // 2 > sum(event['state']['session']['history'].values()):
            text += ' Вы ещё не съели оптимальное количество сахара, это прекрасно. Ваш организм скажет вам спасибо!'
        elif norm // 2 < sum(event['state']['session']['history'].values()) and sum(event['state']['session']['history'].values()) < norm:
            text += ' Оптимальное количество сахара вы уже съели, но не превысили максимально допустимую норму. Советую вам больше не есть сладкого сегодня.'
        else:
            text += ' Увы, вы переели максимально допустимую дневную дозу. Категорически советую завязать со сладким на сегодня .'
        text += ' Ну что, проверим ещё раз?'
        replies = ['Да', 'Нет', 'Хватит', 'Факты']
        ways = ''
        now_history = {}
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {"question": 'Всё', "all_sum": event['state']['session']['all_sum'], "way": ways, "history": now_history, "facts": facts_list},
            'response': {
                'text': text,
                'buttons': [{'title': suggest, 'hide': True} for suggest in replies],
                'end_session': 'false'
            },
        }

    elif event['state']['session']['question'] == 'Молчанка':
        question = 'Проверка'
        text = 'Проверим уровень сахара или послушаем факты о вреде сахара?'
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {"question": question, "way": '', "history": {}, "facts": facts_list},
            'response': {
                'text': text,
                'buttons': [{'title': suggest, 'hide': True} for suggest in ["Проверка", "Факты"]],
                'end_session': 'false'
            },
        }



    return {
        'version': event['version'],
        'session': event['session'],
        'session_state': {"question": event['state']['session']['question'], "facts": facts_list},
        'response': {
            'text': 'Если вы добрались до этого сообщения, то примите мои поздравления - вы сделали невозможное и сломали систему. Напишите, пожалуйста, об этом разработчику в отзывы :)',
            'buttons': [{'title': suggest, 'hide': True} for suggest in ["Мои", "Благодарности"]],
            'end_session': 'false'
        },
    }