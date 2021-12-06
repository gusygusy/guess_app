from flask import render_template
from flask import request
from flask import session
from flask.views import View


class Quiz(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if request.method == 'GET':
            if session.get('push') is None:
                session['push'] = []
                session['oracle_history'] = {"John Travolta": [], "Tom Cruise": [],
                                             "Salma Hayek": []}
                session['counter'] = 1
                default_oracle_value = self.num_generator()
                session['oracle_value'] = default_oracle_value
                return render_template("index.html")
            else:
                oracle_value = session['oracle_value']  # oracle rating
                user_value_history = session['push']

                oracle_history = session['oracle_history']
                return render_template("index.html", oracle_value=oracle_value,
                                       user_val_history=user_value_history, oracle_history=oracle_history)
        if request.method == 'POST':
            if request.form.get('push'):
                user_turn = request.form['push']
                push = session['push']
                user_turn = int(user_turn)
                push = push + [user_turn]
                session['push'] = push
                user_turn = int(user_turn)
                oracle_value = session['oracle_value']
                oracle_choices = session['oracle_choices']
                oracle_history = session['oracle_history']
                for k, v in oracle_choices.items():
                    res_checker = self.result_checker(user_turn, v)
                    rating = self.rating(res_checker)
                    oracle_value[k] = rating
                    session['oracle_value'] = oracle_value
                    oracle_history[k].append(v)
                session['oracle_history'] = oracle_history

                return render_template("index.html", oracle_value=oracle_value,
                                           user_val=user_turn)

            if request.form.get('ready'):
                oracle_value = session['oracle_value']  # current rating

                oracle_choices = self.num_generator(oracle_value.keys())

                session['oracle_choices'] = oracle_choices
                return render_template("index.html", oracle_choice=oracle_choices, oracle_value=oracle_value)
    @staticmethod
    def num_generator(name_list: list = None) -> dict:
        if not name_list:
            name_list = ["John Travolta", "Tom Cruise", "Salma Hayek"]
            result = {k: 100 for k in name_list}
            return result
        import random
        result = {}
        for i in name_list:
            result.setdefault(i, random.randint(10, 99))
        return result

    @staticmethod
    def result_checker(user_input: int, oracle_input: int) -> int:
        """ checks inputs return positive result or 0 """

        diff = user_input + (- oracle_input)
        if diff < 0:
            diff *= -1
        return diff
    @staticmethod
    def rating(diff: int = None) -> int:
        oracle_data = None
        for v in session['oracle_value'].values():
            oracle_data = int(v) - diff

        return oracle_data

