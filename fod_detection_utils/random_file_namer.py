# #Python program to rename all file
# #names in your directory
# import os
# import random
#
# os.chdir('/home/jmbalmeida/Desktop/FOD5oct_random/no_FOD/')
# print(os.getcwd())
#
# for count, f in enumerate(os.listdir()):
#      #random_name = random.
#      f_name, f_ext = os.path.splitext(f)
#      f_name = "image" + str(count)
#
#      new_name = f'{f_name}{f_ext}'
#      os.rename(f, new_name)


# import os
# import glob
#
# folder = "/home/jmbalmeida/Desktop/FOD5oct_random/FOD/"
# for count, filename in enumerate(os.listdir(folder)):
#     oldname = folder + filename
#     newname = folder + "image" + str(count) + ".jpg"
#     os.rename(oldname, newname)
#
# printing the changed names
# print(glob.glob(folder + "*.*"))

