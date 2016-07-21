from math import pow, sqrt
import BrightnessMode as BMode
import Helper
# formulas to calculate brightness

class BrightnessCalculator:
    def __init__(self, R,G,B):
        self.r = R
        self.g = G
        self.b = B

    def standard(self, mode=BMode.BrightnessMode.RAW):
        std = (0.2126*self.r) + (0.7152*self.g) + (0.0722*self.b)
        if mode:
            return std

        # 1 is to 
        return Helper.calculate_percentile(std)

    def perceivedA(self, mode=BMode.BrightnessMode.RAW):
        pA = (0.299*self.r + 0.587*self.g + 0.114*self.b)
        if mode:
            return pA

        return Helper.calculate_percentile(pA)

    def perceivedB(self, mode=BMode.BrightnessMode.RAW):
        pB = sqrt( pow(0.299*self.r,2) + pow(0.587*self.g,2) + pow(0.114*self.b,2) )
        if mode:
            return pB

        return Helper.calculate_percentile(pB)

    def average(self, mode=BMode.BrightnessMode.RAW):
        if mode:
            return (self.standard() + self.perceivedA() + self.perceivedB())/3

        return (self.standard(mode=BMode.BrightnessMode.PERCENTILE) +
                    self.perceivedA(mode=BMode.BrightnessMode.PERCENTILE) +
                    self.perceivedB(mode=BMode.BrightnessMode.PERCENTILE))/3
