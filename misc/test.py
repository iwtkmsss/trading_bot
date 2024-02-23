import psycopg2
from datetime import datetime, timedelta

from bot.misc import secure_mentor, BDB, is_name_hidden

# db_name = "mydatabase"
# user = "admin"
# password = "csernijd83JJJ"
# host = "91.239.233.223"
#
# conn = psycopg2.connect(user=user,
#                         password=password,
#                         host=host,
#                         database=db_name)
# cursor = conn.cursor()

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print(data[0:5])


# import json
#
# with open(r"C:\Users\alex\PycharmProjects\marline_team_bot\second_bot\txt.txt", "r") as file:
#     data = file.read()
# with open("photo.json", "r")as file:
#     json_data = json.load(file)
# print(len(json_data))
# data_list = [block.split("\n") for block in data.split("\n\n")]
# for d in data_list:
#     json_data.append(d)
#
# with open("photo1.json", "w") as file:
#     json.dump(json_data, file, indent=2)


# import cv2
# from PIL import Image
# import numpy as np


# def resize_and_replace(input_image_path, image_to_insert_path, output_image_path):
#     input_image = Image.open(input_image_path)
#     image_to_insert = Image.open(image_to_insert_path)
#
#     # Перетворення зображень в масиви numpy
#     input_image_np = np.array(input_image)
#
#     x_coords, y_coords = np.where(np.all(input_image_np == [2, 2, 2], axis=-1))
#
#     min_x = np.min(x_coords)
#     max_x = np.max(x_coords)
#     min_y = np.min(y_coords)
#     max_y = np.max(y_coords)
#     width = max_x - min_x + 1
#     height = max_y - min_y + 1
#
#     image_to_insert = image_to_insert.resize((width, height), Image.LANCZOS)
#     image_to_insert_np = np.array(image_to_insert)
#
#     black_pixels = np.all(input_image_np == [0, 0, 0], axis=-1)
#     x, y = np.where(black_pixels)
#
#     # Отримання розмірів чорного квадрата
#     black_square_height = np.max(x) - np.min(x) + 1
#     black_square_width = np.max(y) - np.min(y) + 1
#
#     # Зміна розміру зображення для заміщення
#     replacement_image_resized = image_to_insert_np.resize((black_square_width, black_square_height), Image.ANTIALIAS)
#     replacement_image_np = np.array(replacement_image_resized)
#
#     # Заміна частини чорного квадрата на вміст заміщувального зображення
#     input_image_np[x, y, :] = replacement_image_np[x, y, :]
#
#     # Перетворення обратно в зображення та збереження
#     result_image = Image.fromarray(input_image_np)
#     result_image.save(output_image_path)
#
#
# resize_and_replace("profile_photo.png", "test.jpg", "output_image.jpg")
#
#
# def i(input_image_path, image_to_insert_path, output_image_path):
#     input_image = Image.open(input_image_path)
#     image_to_insert = Image.open(image_to_insert_path)
#
#     input_image_np = np.array(input_image)
#
#     image_to_insert = image_to_insert.resize(input_image.size, Image.LANCZOS)
#
#     image_to_insert_np = np.array(image_to_insert)
#
#     mask = np.all(input_image_np == [2, 2, 2], axis=-1)
#     input_image_np[mask] = image_to_insert_np[mask]
#
#     result_image = Image.fromarray(input_image_np)
#     result_image.save(output_image_path)
#
#
# # i("profile_photo.png", "test.jpg", "output_image.jpg")

# from PIL import Image, ImageDraw, ImageFont
#
#
# def center(x, y, w, h):
#     text_x = int(x - w // 2)
#     text_y = int(y - h // 2)
#     return text_x, text_y
#
#
# async def profit_image(worker_name: str, user_tg_id: str, days_in_team: str, amount_profits: str, average_profit: str):
#     img = Image.open("profile_photo_with_out_photouser.JPG")
#     draw = ImageDraw.Draw(img)
#     font_path = "Roboto-Black.ttf"
#     font_size = 55
#
#     font = ImageFont.truetype(font_path, font_size)
#
#     draw.text((520, 160), worker_name, fill=(255, 255, 255), font=font)
#     draw.text((520, 220), user_tg_id, fill=(175, 175, 175), font=ImageFont.truetype(font_path, 30))
#
#     days_in_team_w, days_in_team_h = font.getsize(days_in_team)
#     draw.text(center(600, 460, days_in_team_w, days_in_team_h), days_in_team, fill=(255, 255, 255), font=font)
#
#     amount_profits_w, amount_profits_h = font.getsize(amount_profits)
#     draw.text(center(880, 460, amount_profits_w, amount_profits_h), amount_profits, fill=(255, 255, 255), font=font)
#
#     average_profit_w, average_profit_h = ImageFont.truetype(font_path, 45).getsize(average_profit)
#     draw.text(center(1160, 460, average_profit_w, average_profit_h), average_profit, fill=(255, 255, 255), font=ImageFont.truetype(font_path, 45))
#
#     img.save("profile_photo_with_out_photouser2.JPG")
#
#     return "bot/misc/new_profit.png"
