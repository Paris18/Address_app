# python import
import random


def generatePass(self):
	string_ = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	passlen = 6
	randlist = random.sample(string_,passlen)
	otp = "".join(randlist)
	return otp