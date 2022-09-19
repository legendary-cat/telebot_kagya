import os
import h5py
import easyocr
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3" #конфликт с видюхой убирает ошибки
from pixellib.instance import instance_segmentation

def object_detection_on_an_image(path):
    segment_image = instance_segmentation() #создаем объект класса
    segment_image.load_model("E:\www\mask_rcnn_coco.h5")

    target_classes = segment_image.select_target_classes(person=True) #выбираем только конкретные типы объектов

    result = segment_image.segmentImage(
    image_path=path,
    output_image_name="output.jpg",
    segment_target_classes=target_classes,
    show_bboxes=True #квадрат вокруг модели
    )

    #print(result[0]["scores"])
    object_count = len(result[0]["scores"])
    print(f"найдено объектов заданного типа: {object_count} ")

def video_segmentation(path):
    segment_video = instance_segmentation()
    segment_video.load_model("mask_rcnn_coco.h5")

    target_classes = segment_video.select_target_classes(person=True)

    segment_video.process_video(
    path,
    frames_per_second=5, #fps
    show_bboxes=True,
    segment_target_classes=target_classes,
    output_video_name="output_video.mp4"
    )

def text_search(path):
    reader = easyocr.Reader(["ru", "en"])
    result = reader.readtext(path, detail=0, paragraph=True)

    with open("translation.txt", "w") as file:
        for line in result:
            file.write(f"{line}\n\n")
    print("текст записан в файл")

    '''for line in result:
        print(f"{line}\n\n")'''

    return result

def main():
    code = input("Введите команду: ") #1 - фото, 2 - видео,3 - text,4 = попугай

    if code == '1':
        path = input("Введите название файла: ")
        object_detection_on_an_image(path)

    if code == '2':
        path = input("Введите название файла: ")
        video_segmentation(path)

    if code == '3':
        path = input("Введите название файла: ")
        print(text_search(path=path))


if __name__ == '__main__': #определяем точку входа так как строга она не задается. чтобы сначала мэин потом все остальное(например импорт)
    main()