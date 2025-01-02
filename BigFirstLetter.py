import os
from tkinter import Tk, filedialog, StringVar, Text
from tkinter.ttk import Button, Label, Radiobutton
import ttkbootstrap as tb


def capitalize_words(text):
    """Функция, которая делает первые буквы всех слов заглавными."""
    return text.title()


def capitalize_sentence(text):
    """Функция, которая делает только первую букву текста заглавной."""
    return text.capitalize()


def capitalize_exclude_small(text):
    """Функция, которая делает первые буквы заглавными, исключая предлоги."""
    small_words = {'and', 'of', 'from', 'the', 'a', 'an', 'in', 'on', 'at', 'by', 'for', 'to'}
    words = text.split()
    result = [words[0].capitalize()]  # Первая буква всегда большая
    result += [word if word.lower() in small_words else word.capitalize() for word in words[1:]]
    return " ".join(result)


def process_files_in_folder():
    """Обрабатывает файлы в указанной папке в соответствии с выбранным методом."""
    folder = folder_path.get()
    if not folder:
        result_field.delete("1.0", "end")
        result_field.insert("1.0", "Выберите папку для обработки.")
        return

    try:
        # Преобразуем значение `rename_option` в число
        option = int(rename_option.get())
        
        # Определяем функцию на основе выбранного метода
        if option == 1:
            func = capitalize_sentence
        elif option == 2:
            func = capitalize_words
        elif option == 3:
            func = capitalize_exclude_small
        else:
            result_field.delete("1.0", "end")
            result_field.insert("1.0", "Выберите метод переименования.")
            return

        files = os.listdir(folder)
        renamed_files = []
        for file in files:
            original_path = os.path.join(folder, file)
            if os.path.isfile(original_path):
                name, ext = os.path.splitext(file)
                new_name = func(name) + ext
                new_path = os.path.join(folder, new_name)
                os.rename(original_path, new_path)
                renamed_files.append(f"{file} -> {new_name}")

        if renamed_files:
            result_field.delete("1.0", "end")
            result_field.insert("1.0", "Файлы переименованы:\n" + "\n".join(renamed_files))
        else:
            result_field.delete("1.0", "end")
            result_field.insert("1.0", "В выбранной папке нет файлов для обработки.")
    except Exception as e:
        result_field.delete("1.0", "end")
        result_field.insert("1.0", f"Ошибка: {e}")


# Инициализация основного окна
app = tb.Window(themename="darkly")
app.title("Переименование файлов")
app.geometry("600x500")

folder_path = StringVar()
rename_option = StringVar(value="0")

# Метки и поля
Label(app, text="Выберите папку для обработки:").pack(pady=5)
Button(app, text="Обзор папки", command=lambda: folder_path.set(filedialog.askdirectory())).pack(pady=5)
Label(app, textvariable=folder_path).pack(pady=5)

Label(app, text="Выберите метод переименования:").pack(pady=10)

# Радиокнопки для выбора метода
Radiobutton(app, text="1. Только первая буква заглавная (Wind of fire)", 
            variable=rename_option, value="1").pack(anchor="w", padx=20)
Radiobutton(app, text="2. Все слова с заглавной буквы (Wind Of Fire)", 
            variable=rename_option, value="2").pack(anchor="w", padx=20)
Radiobutton(app, text="3. Исключая предлоги (Wind of Fire)", 
            variable=rename_option, value="3").pack(anchor="w", padx=20)

# Поле для вывода результата
Label(app, text="Результат:").pack(pady=5)
result_field = Text(app, height=10, wrap="word", state="normal")
result_field.pack(pady=5)

# Кнопка для обработки файлов
Button(app, text="Переименовать файлы", command=process_files_in_folder).pack(pady=10)

# Запуск приложения
app.mainloop()
