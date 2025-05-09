import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(file_path):
    #Завантажує дані з CSV файлу
    try:
        data_frame = pd.read_csv(file_path, sep=";", parse_dates=['time_stamp', 'reg_date'])
        data_frame['sender_id'] = pd.to_numeric(data_frame['sender_id'], errors='coerce')
        data_frame['platform_id'] = pd.to_numeric(data_frame['platform_id'], errors='coerce')
        return data_frame
    except FileNotFoundError:
        print(f"Помилка: Файл '{file_path}' не знайдено.")
        return None

def calculate_likes_summary(data_frame):
    #Обчислює середню кількість лайків для кожної групи до та після тесту

    data_frame['group'] = data_frame['sender_id'] % 2
    data_frame['group'] = data_frame['group'].map({0: 'base', 1: 'test'})

    test_start = pd.Timestamp('2017-03-24 16:00')
    data_frame['after_test'] = data_frame['time_stamp'] > test_start

    likes_per_user = data_frame.groupby(['group', 'after_test', 'sender_id']).size().reset_index(name='likes')
    likes_summary = likes_per_user.groupby(['group', 'after_test'])['likes'].mean().reset_index()
    return likes_summary

def calculate_daily_likes(data_frame):
    #Обчислює кількість лайків за кожен день для кожної групи

    data_frame['date'] = data_frame['time_stamp'].dt.date
    daily_likes = data_frame.groupby(['group', 'date']).size().reset_index(name='likes')
    return daily_likes

def visualize_likes_summary(likes_summary):
    #Візуалізує середню кількість лайків за допомогою стовпчастої діаграми

    plt.figure(figsize=(10, 6))
    sns.barplot(x='group', y='likes', hue='after_test', data=likes_summary)
    plt.title('Середня кількість лайків до та після тесту')
    plt.xlabel('Група')
    plt.ylabel('Середня кількість лайків')
    plt.legend(title='Після тесту')
    plt.show()

def visualize_daily_likes(daily_likes):
    #Візуалізує динаміку лайків за днями за допомогою лінійного графіка

    plt.figure(figsize=(12, 6))
    sns.lineplot(x='date', y='likes', hue='group', data=daily_likes)
    plt.title('Динаміка лайків за днями')
    plt.xlabel('Дата')
    plt.ylabel('Кількість лайків')
    plt.legend(title='Група')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Основний потік програми
file_path = r"D:/test-tasks/appflame/Test_3.csv"
data_frame = load_data(file_path)

if data_frame is not None:
    likes_summary = calculate_likes_summary(data_frame)
    daily_likes = calculate_daily_likes(data_frame)

    print("Quantity of likes")
    print(likes_summary)

    print("\n Dynamic per day")
    print(daily_likes)

    visualize_likes_summary(likes_summary)
    visualize_daily_likes(daily_likes)