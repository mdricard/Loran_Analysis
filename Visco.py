import numpy as np
import matplotlib.pyplot as plt
from BiomechTools import low_pass, zero_crossing, max_min, simpson_nonuniform


class Visco:
    n_reps = 0
    energy_absorbed = np.zeros(20)
    energy_returned = np.zeros(20)
    peak_torque = np.zeros(20)
    stiffness = np.zeros(20)

    def __init__(self, fn):
        with open(fn) as infile:
            temp = infile.readline()
            temp = infile.readline()
            header = temp.split(',')
            self.n = int(header[7]) - 2
            self.sampling_rate = int(header[8])
            self.mass = float(header[9])
            self.ht = float(header[10])
            self.limblen = float(header[11])
            self.attachmentlen = float(header[12])
            self.gender = header[13]

        data = np.genfromtxt(fn, delimiter=',', skip_header=2)
        self.pt = data[:, 0]
        self.tor = data[:, 1]
        self.pos = data[:, 2]
        self.vel = data[:, 3]
        self.MHemg = data[:, 4]
        self.VLemg = data[:, 5]
        self.mmg = data[:, 6]

        self.smooth_tor = []
        self.smooth_pos = []
        self.smooth_vel = []
        self.rep_start = np.zeros(20, dtype=np.int32)
        self.max_loc = np.zeros(20, dtype=np.int32)
        self.rep_end = np.zeros(20, dtype=np.int32)