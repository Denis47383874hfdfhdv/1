import tkinter as tk
from tkinter import filedialog, messagebox

def extract_texts_between_markers(source_file, target_file, start_marker, end_marker):
    try:
        with open(source_file, 'r', encoding='utf-8') as source:
            content = source.read()

        start_idx = content.find(start_marker)
        texts = []

        while start_idx != -1:
            end_idx = content.find(end_marker, start_idx + len(start_marker))
            if end_idx != -1:
                extracted_text = content[start_idx + len(start_marker):end_idx]
                texts.append(extracted_text.strip())  # Удаляем лишние пробелы и переводы строк
                start_idx = content.find(start_marker, end_idx + len(end_marker))
            else:
                break

        if texts:
            result_text = "\n\n".join(texts)  # Объединяем тексты в одну большую строку с переводами строк
            show_text_in_modal(result_text)

            # Экспорт результата в txt файл
            with open(target_file, 'w', encoding='utf-8') as target:
                target.write(result_text)

            messagebox.showinfo("Готово", "Тексты успешно извлечены. Результаты экспортированы в файл.")
        else:
            messagebox.showerror("Ошибка", "Не удалось найти маркеры в исходном файле.")
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл не найден.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")


def show_text_in_modal(text):
    modal_window = tk.Toplevel()
    modal_window.title("Результаты извлечения текста")

    text_widget = tk.Text(modal_window, wrap="word", font=("Arial", 12), padx=10, pady=10)
    text_widget.insert(tk.END, text)
    text_widget.config(state=tk.DISABLED)  # Запрещаем редактирование текста
    text_widget.pack()

def browse_files():
    source_file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if source_file_path:
        source_file_entry.delete(0, tk.END)
        source_file_entry.insert(tk.END, source_file_path)

def process_files():
    source_file = source_file_entry.get()
    target_file = target_file_entry.get()
    start_marker = start_marker_entry.get()
    end_marker = end_marker_entry.get()

    extract_texts_between_markers(source_file, target_file, start_marker, end_marker)

# Создание окна
window = tk.Tk()
window.title("Вырезание и вставка текста")

# Метка и поле для выбора исходного файла
source_file_label = tk.Label(window, text="Выберите исходный файл:")
source_file_label.pack(pady=5)
source_file_entry = tk.Entry(window, width=50)
source_file_entry.pack(pady=5)
source_file_button = tk.Button(window, text="Обзор", command=browse_files)
source_file_button.pack(pady=5)

# Метка и поле для ввода маркера начала вырезания
start_marker_label = tk.Label(window, text="Введите маркер начала вырезания:")
start_marker_label.pack(pady=5)
start_marker_entry = tk.Entry(window, width=50)
start_marker_entry.pack(pady=5)

# Метка и поле для ввода маркера конца вырезания
end_marker_label = tk.Label(window, text="Введите маркер конца вырезания:")
end_marker_label.pack(pady=5)
end_marker_entry = tk.Entry(window, width=50)
end_marker_entry.pack(pady=5)

# Метка и поле для выбора целевого файла
target_file_label = tk.Label(window, text="Выберите целевой файл для вставки:")
target_file_label.pack(pady=5)
target_file_entry = tk.Entry(window, width=50)
target_file_entry.pack(pady=5)

# Кнопка для запуска процесса
process_button = tk.Button(window, text="Вырезать и вставить", command=process_files)
process_button.pack(pady=10)

window.mainloop()
