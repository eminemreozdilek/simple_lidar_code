import numpy as np
import pandas as pd
import time


class Lidar:
    __minute: np.ndarray
    __second: np.ndarray
    __hour: np.ndarray
    __movement: dict[str, int]
    __lidar_origin_y: np.ndarray
    __lidar_origin_x: np.ndarray
    __y: np.ndarray
    __x: np.ndarray

    def __init__(self, saving_data_option: bool = True):
        self.__saving_data_option = saving_data_option
        self.__setup()

    # Setting initial variables
    def __setup(self):
        self.__x = np.array([])
        self.__y = np.array([])
        self.__lidar_origin_x = np.array([])
        self.__lidar_origin_y = np.array([])
        self.__hour = np.array([])
        self.__minute = np.array([])
        self.__second = np.array([])
        self.__movement = {"X": 0,
                           "Y": 0,
                           "Z": 0,
                           "Yaw": 0,
                           "Pitch": 0,
                           "Roll": 0}
        self.__index = 1

    # Data Reader Function
    def read_data(self, line):
        # Time Controller
        current_time = time.time()
        local_time = time.localtime(current_time)
        hour = int(local_time.tm_hour)
        minute = int(local_time.tm_min)
        second = int(local_time.tm_sec)

        # Pour Data Editting
        pour_data = pd.Series(line.split(";")).str.split(",").tolist()
        pour_data = pd.DataFrame(pour_data[1:-1], columns=pour_data[0])
        pour_data = pour_data.loc[pour_data['Case'] == "True"]

        if self.__saving_data_option:
            current_time = time.time()
            local_time = time.localtime(current_time)
            hour = int(local_time.tm_hour)
            minute = int(local_time.tm_min)
            second = int(local_time.tm_sec)
            pour_data.to_csv(
                "locations\\" + str(self.__index) + "_" + str(hour) + "_" + str(minute) + "_" + str(second) + ".csv",
                index=False)
            self.__index += 1

        # Calculating x,y coordinates
        x = pour_data["Distance"].values.astype(float) * np.cos(
            pour_data["Angle"].values.astype(float) + pour_data["Yaw"].values.astype(
                float)) * np.cos(
            pour_data["Roll"].values.astype(float)) + pour_data["X"].values.astype(float)

        y = pour_data["Distance"].values.astype(float) * np.sin(
            pour_data["Angle"].values.astype(float) + pour_data["Yaw"].values.astype(
                float)) * np.cos(
            pour_data["Pitch"].values.astype(float)) + pour_data["Y"].values.astype(float)

        # Collecting all datas together
        self.__x = np.round(np.concatenate((self.__x, x)), 3)
        self.__y = np.round(np.concatenate((self.__y, y)), 3)
        plan = np.unique(np.vstack((self.__x, self.__y)).transpose(), axis=0)
        self.__x = plan[:, 0]
        self.__y = plan[:, 1]

        # Collecting all timing datas together
        self.__hour = np.concatenate((self.__hour, np.ones(self.__x.shape) * np.array([hour])))
        self.__minute = np.concatenate((self.__minute, np.ones(self.__x.shape) * np.array([minute])))
        self.__second = np.concatenate((self.__second, np.ones(self.__x.shape) * np.array([second])))

        # Saving movements of lidar as variable
        self.__movement = {"X": pour_data["X"].values.astype(float)[0],
                           "Y": pour_data["Y"].values.astype(float)[0],
                           "Z": pour_data["Z"].values.astype(float)[0],
                           "Yaw": pour_data["Yaw"].values.astype(float)[0],
                           "Pitch": pour_data["Pitch"].values.astype(float)[0],
                           "Roll": pour_data["Roll"].values.astype(float)[0]}

    @property
    def movement(self):
        return self.__movement

    @property
    def coordinate_arrays(self):
        return self.__x, self.__y

    @property
    def lidar_origins(self):
        return self.__lidar_origin_x, self.__lidar_origin_y

    @property
    def max_coordinates(self):
        return max([np.max(np.abs(self.__x)), np.max(np.abs(self.__y))]) + 0.5