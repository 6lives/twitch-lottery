import requests
import csv
import datetime
from random import randint

from kivy.app import App
from kivy.config import Config
Config.set("graphics","resizable","0")
Config.set("graphics","width","800")
Config.set("graphics","height","600")
import os
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color


class TwitchApp(App):
    def build(self):
        self.title = 'Twitch lottery'

        root = BoxLayout(orientation = "horizontal", padding = 5, spacing = 5)

        self.console = TextInput(readonly=True, text='[INFO] Добро пожаловать в TWITCH LOTTERY!\n', background_color = [1,0,1,.85])

        self.left = BoxLayout(orientation='vertical')

        top_grid = GridLayout(cols = 2, spacing = 5)

        self.viewers_counter = Label(text='0', size_hint=[.3,1])
        counter_label = Label(text= 'Количество зрителей на трансляции: ')
        get_viewers = Button(text='Загрузить зрителей')
        get_viewers.bind(on_press = self.get_data)

        top_grid.add_widget(counter_label)
        top_grid.add_widget(self.viewers_counter)

        bottom_grid = GridLayout(cols = 2, spacing = 5)

        self.random_number = Label(text='', size_hint=[.3,1])
        random_number_label = Label(text='Порядковый номер победителя: ')
        get_random = Button(text = 'Ролл числа')
        get_random.bind(on_press = self.random_int)

        bottom_grid.add_widget(random_number_label)
        bottom_grid.add_widget(self.random_number)

        write_viewers_to_file = Button(text='Выгрузить зрителей в файл')
        write_viewers_to_file.bind(on_press=self.writing_to_file)

        start_lottery = Button(text='Выявить победителя!')
        start_lottery.bind(on_press=self.get_winner)

        self.left.add_widget(top_grid)
        self.left.add_widget(get_viewers)
        self.left.add_widget(bottom_grid)
        self.left.add_widget(get_random)
        self.left.add_widget(write_viewers_to_file)
        self.left.add_widget(start_lottery)

        root.add_widget(self.left)
        root.add_widget(self.console)

        return root


    def random_int(self, instance):
        try:
            self.random_number.text = str(randint(1, int(self.viewers_counter.text)))
        except Exception:
            self.console.text += '\n[ERROR] Сначала загрузи зрителей!\n'

    def get_data(self, instance):
        try:
            self.all_viewers = []

            payload = [{"operationName":"ChatViewers","variables":{"channelLogin":"chixpixx"},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"e0761ef5444ee3acccee5cfc5b834cbfd7dc220133aa5fbefe1b66120f506250"}}}]
            headers = {
                'Accept': '*/*',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
                'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko'
                }
            url = 'https://gql.twitch.tv/gql'
            req = requests.post(url, headers = headers, json = payload)

            data = req.json()

            logins = data[0]['data']['channel']['chatters']['viewers']
            vips = data[0]['data']['channel']['chatters']['vips']

            self.viewers_counter.text = str(len(logins) + len(vips))

            for vip in vips:
                self.all_viewers.append(vip['login'])
            for user in logins:
                self.all_viewers.append(user['login'])

            self.console.text += '\n[INFO] Зрители успешно загружены!\n'

        except Exception:
            self.console.text += '\n[ERROR] При загрузке зрителей произошла ошибка!\n'

    def writing_to_file(self, instance):
        try:
            cuttent_time = datetime.datetime.now().strftime('%H-%M-%S')

            for login in self.all_viewers:
                with open(f'{cuttent_time}.csv','a',newline='') as file:
                    writer=csv.writer(file)
                    writer.writerow([login])

        except Exception:
            self.console.text += '\n[ERROR] Сначала загрузи зрителей!\n'

        self.console.text += '\n[INFO] Файл со списком зрителей создан!\n'

    def get_winner(self, instance):
        try:
            self.console.text += f'\nПобедитель: {self.all_viewers[int(self.random_number.text)-1]}!\n'
        except Exception:
            self.console.text += '\n[ERROR] Сначала загрузи зрителей и наролль число!\n'

if __name__ == '__main__':
    TwitchApp().run()
