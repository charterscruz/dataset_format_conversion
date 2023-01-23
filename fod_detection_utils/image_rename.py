import os
import shutil


# Source_Path = '/home/jmbalmeida/Desktop/datasets/test_images_jetson_test_1/5oct/FOD/loc_C/10/FOD'
# Destination = '/home/jmbalmeida/Desktop/datasets/digits_dataset/FOD'

Source_Path = '/home/jmbalmeida/Desktop/datasets/test_images_rpi'  # I've replaced the original folder by other that will be commited to bitbucket
# TODO: NOTA IMPORTANTE: A ESTRUTURA DAS PASTAS TEM QUE SER SEMPRE IGUAL PARA ISTO FUNCIONAR. SE NÃO ME ENGANO,
#  ATUALMENTE, AS PASTAS FOD TEM ./test_folders_files/FOD/loc_A/1/FOD enquanto que as N_FOD têm /N_FOD/loc_A/1/, ou seja, têm menos um nível.  Confirma esta situação comigo

Destination_Path = '/home/jmbalmeida/Desktop/datasets/test_images_rpi_test_1_no_crop'


def main():
    # list first level of folders (FOD or N_FOD)
    for _, first_level_folder in enumerate(os.listdir(Source_Path)):
        first_level_path = os.path.join(Source_Path, first_level_folder)
        #list second level of folders (loc_A, loc_B, loc_C, ...)
        for _, second_level_folder in enumerate(os.listdir(first_level_path)):
            second_level_path = os.path.join(first_level_path, second_level_folder)

            #list third level of folders (1, 2, 3, 4, ...)
            for _, third_level_folder in enumerate(os.listdir(second_level_path)):
                third_level_path = os.path.join(second_level_path, third_level_folder)

                # list fourth level of folders (FOD, N_FOD)
                for _, fourth_level_folder in enumerate(os.listdir(third_level_path)):
                    fourth_level_path = os.path.join(third_level_path, fourth_level_folder)

                    for _, image_file in enumerate(os.listdir(fourth_level_path)):
                        print('is ' + fourth_level_path + image_file + ' a file?:')
                        print(os.path.isfile(os.path.join(fourth_level_path, image_file)))

                        # The following line builds the name sequentially, from the higher level all the way to the
                        # image number in the folder and the position in the cropping. The reasoning is the following:
                        # image_file[:4] - this should be the default name ("image" or "image")
                        # TODO: confirm
                        print(image_file[:6])
                        # '_base' + first_level_folder[0] - this indicates if is from a set with or without any FOD
                        # TODO: confirm
                        print('_base_' + first_level_folder)
                        # second_level_folder  - this should be loc_A, loc_B, ...
                        # TODO: confirm
                        print(second_level_folder)
                        # third_level_folder - this should be the number of FOD items in the captured image
                        # TODO: confirm
                        print(third_level_folder)
                        # fourth_level_folder - this should be if the cropped image has FOD or not
                        # TODO: confirm
                        print(fourth_level_folder)
                        # image_file[5:] - this should be something similar to "_2_3.jpg", i.e. the position of the
                        #  cropping window
                        # TODO: confirm
                        print(image_file[:6])

                        destination_name = image_file[:5] + '_base_' + first_level_folder[:6] + '_' + second_level_folder\
                                           + '_' + third_level_folder + '_' + fourth_level_folder + '_' + image_file[5:]

                        shutil.copy2(os.path.join(fourth_level_path, image_file),
                                     os.path.join(os.path.join(Destination_Path, fourth_level_folder), destination_name))
                        print(os.path.join(os.path.join(Destination_Path, fourth_level_folder), destination_name))
                        print(destination_name)


#     #last_number is the number of the last image in destination folder plus 1, otherwise it will replace the last image
# # last_number = 1136
# #dst_folder = os.mkdir(Destination)
#
#
#
#
#
#     for count, filename in enumerate(os.listdir(Source_Path)):
#         dst = "image" + str(count+last_number) + ".jpg"
#
#         # copy all files
#         shutil.copy2(os.path.join(Source_Path, filename),  os.path.join(Destination, dst))
#         # rename all the files
#         #os.rename(os.path.join(Source_Path, filename),  os.path.join(Destination, dst))


# Driver Code
if __name__ == '__main__':
     main()