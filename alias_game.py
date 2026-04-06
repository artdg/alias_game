import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import time
import threading
from dataclasses import dataclass
from typing import List, Dict
import json
import os

@dataclass
class Team:
    name: str
    score: int = 0

class AliasGameGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Alias Game - Игра в слова")
        self.root.geometry("900x700")
        self.root.configure(bg='#2c3e50')
        
        # Настройка стилей
        self.setup_styles()
        
        # Данные игры
        self.teams: List[Team] = []
        self.current_team_index = 0
        self.current_round = 0
        self.total_rounds = 0
        self.current_words = []
        self.current_word_index = 0
        self.score_in_round = 0
        self.time_left = 60
        self.timer_running = False
        self.game_active = False
        
        # Слова для игры
        self.load_words()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Показываем начальный экран
        self.show_setup_screen()
        
    def setup_styles(self):
        """Настройка стилей для виджетов"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Настройка цветов
        self.colors = {
            'bg': '#2c3e50',
            'primary': '#3498db',
            'success': '#2ecc71',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'light': '#ecf0f1',
            'dark': '#34495e'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Стили для кнопок
        style.configure('Primary.TButton', 
                        font=('Arial', 11, 'bold'),
                        padding=10)
        style.configure('Success.TButton',
                        font=('Arial', 11, 'bold'),
                        padding=10)
        
    def load_words(self):
        """Загрузка слов для игры"""
        self.categories = {
            'Животные': ['слон', 'жираф', 'кенгуру', 'дельфин', 'тигр', 'пингвин', 
                        'лев', 'зебра', 'медведь', 'волк', 'лиса', 'заяц'],
            'Профессии': ['врач', 'учитель', 'инженер', 'художник', 'повар', 
                         'строитель', 'пилот', 'юрист', 'программист', 'архитектор'],
            'Спорт': ['футбол', 'баскетбол', 'теннис', 'плавание', 'бокс', 
                     'лыжи', 'хоккей', 'гольф', 'волейбол', 'шахматы'],
            'Еда': ['пицца', 'суши', 'бургер', 'паста', 'салат', 'суп', 
                   'десерт', 'мороженое', 'шоколад', 'пирог'],
            'Предметы': ['стол', 'стул', 'компьютер', 'телефон', 'книга', 
                        'ручка', 'лампа', 'часы', 'зеркало', 'окно']
        }
        
    def create_widgets(self):
        """Создание всех виджетов интерфейса"""
        # Главный контейнер
        self.main_container = tk.Frame(self.root, bg=self.colors['bg'])
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Верхняя панель с заголовком
        self.header_frame = tk.Frame(self.main_container, bg=self.colors['primary'], height=80)
        self.header_frame.pack(fill=tk.X)
        self.header_frame.pack_propagate(False)
        
        title_label = tk.Label(self.header_frame, text="🎲 ALIAS GAME 🎲", 
                               font=('Arial', 24, 'bold'), 
                               bg=self.colors['primary'], 
                               fg='white')
        title_label.pack(expand=True)
        
        # Контейнер для основного контента
        self.content_frame = tk.Frame(self.main_container, bg=self.colors['bg'])
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
    def clear_content(self):
        """Очистка контентной области"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
    def show_setup_screen(self):
        """Экран настройки игры"""
        self.clear_content()
        
        # Заголовок
        title = tk.Label(self.content_frame, text="Настройка игры", 
                        font=('Arial', 18, 'bold'), 
                        bg=self.colors['bg'], 
                        fg=self.colors['light'])
        title.pack(pady=20)
        
        # Количество команд
        teams_frame = tk.Frame(self.content_frame, bg=self.colors['bg'])
        teams_frame.pack(pady=10)
        
        tk.Label(teams_frame, text="Количество команд:", 
                font=('Arial', 12), 
                bg=self.colors['bg'], 
                fg=self.colors['light']).pack(side=tk.LEFT, padx=5)
        
        self.teams_count = tk.Spinbox(teams_frame, from_=2, to=4, width=5, 
                                      font=('Arial', 12))
        self.teams_count.pack(side=tk.LEFT, padx=5)
        
        # Поля для названий команд
        self.team_entries = []
        teams_names_frame = tk.Frame(self.content_frame, bg=self.colors['bg'])
        teams_names_frame.pack(pady=20)
        
        def update_team_entries(*args):
            for widget in teams_names_frame.winfo_children():
                widget.destroy()
            self.team_entries.clear()
            
            count = int(self.teams_count.get())
            for i in range(count):
                frame = tk.Frame(teams_names_frame, bg=self.colors['bg'])
                frame.pack(pady=5)
                
                tk.Label(frame, text=f"Команда {i+1}:", 
                        font=('Arial', 11), 
                        bg=self.colors['bg'], 
                        fg=self.colors['light']).pack(side=tk.LEFT, padx=5)
                
                entry = tk.Entry(frame, font=('Arial', 11), width=20)
                entry.pack(side=tk.LEFT, padx=5)
                self.team_entries.append(entry)
        
        self.teams_count.bind('<KeyRelease>', update_team_entries)
        update_team_entries()
        
        # Количество раундов
        rounds_frame = tk.Frame(self.content_frame, bg=self.colors['bg'])
        rounds_frame.pack(pady=10)
        
        tk.Label(rounds_frame, text="Количество раундов:", 
                font=('Arial', 12), 
                bg=self.colors['bg'], 
                fg=self.colors['light']).pack(side=tk.LEFT, padx=5)
        
        self.rounds_count = tk.Spinbox(rounds_frame, from_=1, to=5, width=5, 
                                       font=('Arial', 12))
        self.rounds_count.pack(side=tk.LEFT, padx=5)
        
        # Кнопка начала игры
        start_btn = tk.Button(self.content_frame, 
                             text="▶ НАЧАТЬ ИГРУ", 
                             command=self.start_game,
                             bg=self.colors['success'],
                             fg='white',
                             font=('Arial', 14, 'bold'),
                             padx=30,
                             pady=10)
        start_btn.pack(pady=30)
        
    def start_game(self):
        """Запуск игры"""
        # Собираем команды
        self.teams.clear()
        for i, entry in enumerate(self.team_entries):
            team_name = entry.get().strip()
            if not team_name:
                team_name = f"Команда {i+1}"
            self.teams.append(Team(team_name))
        
        self.total_rounds = int(self.rounds_count.get())
        self.current_round = 0
        self.current_team_index = 0
        
        self.show_category_selection()
        
    def show_category_selection(self):
        """Выбор категории"""
        self.clear_content()
        
        title = tk.Label(self.content_frame, text="Выберите категорию слов", 
                        font=('Arial', 18, 'bold'), 
                        bg=self.colors['bg'], 
                        fg=self.colors['light'])
        title.pack(pady=20)
        
        # Кнопки категорий
        categories_frame = tk.Frame(self.content_frame, bg=self.colors['bg'])
        categories_frame.pack(pady=20)
        
        for category in self.categories.keys():
            btn = tk.Button(categories_frame, 
                          text=category,
                          command=lambda cat=category: self.start_round(cat),
                          bg=self.colors['primary'],
                          fg='white',
                          font=('Arial', 12, 'bold'),
                          width=15,
                          height=2)
            btn.pack(pady=5)
        
        # Случайная категория
        random_btn = tk.Button(self.content_frame,
                              text="🎲 СЛУЧАЙНАЯ КАТЕГОРИЯ",
                              command=lambda: self.start_round('random'),
                              bg=self.colors['warning'],
                              fg='white',
                              font=('Arial', 12, 'bold'),
                              padx=20,
                              pady=10)
        random_btn.pack(pady=10)
        
    def start_round(self, category):
        """Начало раунда"""
        self.current_round += 1
        
        # Выбираем слова
        if category == 'random':
            all_words = []
            for words in self.categories.values():
                all_words.extend(words)
            self.current_words = random.sample(all_words, min(10, len(all_words)))
        else:
            self.current_words = random.sample(self.categories[category], min(10, len(self.categories[category])))
        
        self.current_word_index = 0
        self.score_in_round = 0
        self.time_left = 60
        self.game_active = True
        
        self.show_game_screen()
        
    def show_game_screen(self):
        """Игровой экран"""
        self.clear_content()
        
        current_team = self.teams[self.current_team_index]
        
        # Информационная панель
        info_frame = tk.Frame(self.content_frame, bg=self.colors['dark'], relief=tk.RAISED, bd=2)
        info_frame.pack(fill=tk.X, pady=10)
        
        # Информация о команде и раунде
        team_label = tk.Label(info_frame, 
                             text=f"Команда: {current_team.name}",
                             font=('Arial', 14, 'bold'),
                             bg=self.colors['dark'],
                             fg=self.colors['light'])
        team_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        round_label = tk.Label(info_frame,
                              text=f"Раунд: {self.current_round}/{self.total_rounds}",
                              font=('Arial', 12),
                              bg=self.colors['dark'],
                              fg=self.colors['light'])
        round_label.pack(side=tk.LEFT, padx=20)
        
        # Таймер
        self.timer_label = tk.Label(info_frame,
                                   text=f"⏱️ {self.time_left} сек",
                                   font=('Arial', 18, 'bold'),
                                   bg=self.colors['dark'],
                                   fg=self.colors['warning'])
        self.timer_label.pack(side=tk.RIGHT, padx=20)
        
        # Счет
        score_label = tk.Label(self.content_frame,
                              text=f"Счет в раунде: {self.score_in_round}",
                              font=('Arial', 14),
                              bg=self.colors['bg'],
                              fg=self.colors['success'])
        score_label.pack(pady=10)
        
        # Карточка со словом
        word_card = tk.Frame(self.content_frame, bg=self.colors['primary'], relief=tk.RAISED, bd=3)
        word_card.pack(pady=30, padx=50, fill=tk.BOTH)
        
        self.word_label = tk.Label(word_card,
                                  text=self.current_words[self.current_word_index],
                                  font=('Arial', 32, 'bold'),
                                  bg=self.colors['primary'],
                                  fg='white',
                                  height=3)
        self.word_label.pack(expand=True)
        
        # Кнопки управления
        buttons_frame = tk.Frame(self.content_frame, bg=self.colors['bg'])
        buttons_frame.pack(pady=20)
        
        # Кнопка "Угадали"
        guess_btn = tk.Button(buttons_frame,
                             text="✅ УГАДАЛИ (+1)",
                             command=self.word_guessed,
                             bg=self.colors['success'],
                             fg='white',
                             font=('Arial', 12, 'bold'),
                             width=15,
                             height=2)
        guess_btn.pack(side=tk.LEFT, padx=10)
        
        # Кнопка "Пропустить"
        skip_btn = tk.Button(buttons_frame,
                            text="⏭️ ПРОПУСТИТЬ",
                            command=self.word_skipped,
                            bg=self.colors['danger'],
                            fg='white',
                            font=('Arial', 12, 'bold'),
                            width=15,
                            height=2)
        skip_btn.pack(side=tk.LEFT, padx=10)
        
        # Запуск таймера
        self.start_timer()
        
    def start_timer(self):
        """Запуск таймера"""
        if self.timer_running:
            return
            
        self.timer_running = True
        
        def update_timer():
            while self.time_left > 0 and self.game_active:
                time.sleep(1)
                self.time_left -= 1
                self.timer_label.config(text=f"⏱️ {self.time_left} сек")
                
                if self.time_left <= 10:
                    self.timer_label.config(fg='red')
                    
            if self.time_left <= 0 and self.game_active:
                self.end_round()
                
        timer_thread = threading.Thread(target=update_timer, daemon=True)
        timer_thread.start()
        
    def word_guessed(self):
        """Слово угадано"""
        if not self.game_active:
            return
            
        self.score_in_round += 1
        self.next_word()
        
    def word_skipped(self):
        """Слово пропущено"""
        if not self.game_active:
            return
        self.next_word()
        
    def next_word(self):
        """Следующее слово"""
        self.current_word_index += 1
        
        if self.current_word_index >= len(self.current_words):
            self.end_round()
        else:
            self.word_label.config(text=self.current_words[self.current_word_index])
            
            # Обновляем счет на экране
            for widget in self.content_frame.winfo_children():
                if isinstance(widget, tk.Label) and "Счет в раунде" in widget.cget("text"):
                    widget.config(text=f"Счет в раунде: {self.score_in_round}")
                    break
                    
    def end_round(self):
        """Завершение раунда"""
        self.game_active = False
        self.timer_running = False
        
        # Добавляем очки команде
        self.teams[self.current_team_index].score += self.score_in_round
        
        # Показываем результаты раунда
        result_text = f"Раунд завершен!\n\n"
        result_text += f"Команда {self.teams[self.current_team_index].name}\n"
        result_text += f"Набрала {self.score_in_round} очков!\n"
        result_text += f"Общий счет: {self.teams[self.current_team_index].score}\n"
        
        messagebox.showinfo("Результаты раунда", result_text)
        
        # Переход к следующей команде или раунду
        self.current_team_index += 1
        
        if self.current_team_index >= len(self.teams):
            self.current_team_index = 0
            
            if self.current_round >= self.total_rounds:
                self.end_game()
            else:
                self.show_category_selection()
        else:
            self.start_round('random')  # Следующая команда играет с теми же словами
            
    def end_game(self):
        """Завершение игры"""
        self.game_active = False
        
        # Сортируем команды по очкам
        sorted_teams = sorted(self.teams, key=lambda x: x.score, reverse=True)
        
        result_text = "ИГРА ЗАВЕРШЕНА!\n\n"
        result_text += "ФИНАЛЬНЫЕ РЕЗУЛЬТАТЫ:\n"
        result_text += "=" * 30 + "\n\n"
        
        for i, team in enumerate(sorted_teams, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "📌"
            result_text += f"{medal} {team.name}: {team.score} очков\n"
        
        result_text += f"\n🎉 ПОБЕДИТЕЛЬ: {sorted_teams[0].name}! 🎉"
        
        messagebox.showinfo("Игра завершена", result_text)
        
        # Предложение сыграть снова
        if messagebox.askyesno("Новая игра", "Хотите сыграть еще раз?"):
            self.show_setup_screen()
        else:
            self.root.quit()
            
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

    def save_settings(self):
        """Сохранение настроек"""
        settings = {
            'last_teams': [team.name for team in self.teams],
            'last_rounds': self.total_rounds
        }
        with open('game_settings.json', 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)

    def load_settings(self):
        """Загрузка настроек"""
        if os.path.exists('game_settings.json'):
            with open('game_settings.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

if __name__ == "__main__":
    app = AliasGameGUI()
    app.run()