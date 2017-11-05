#!/usr/bin/env python2.7

from telnetlib import Telnet
from optparse import OptionParser
from time import sleep
import time, datetime
import colour.plotting
import colour.io
from colour.plotting import *
# import PIL
import numpy as np
from numpy import array, zeros, linspace, float64, savetxt
from scipy import interpolate, vectorize
from scipy.signal import argrelextrema, argrelmax, savgol_filter, resample
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt
import pylab
from itertools import izip
import csv
import warnings
warnings.filterwarnings("ignore")
import urllib2

# Variables
desired_integration_time = 10000000 # min is 10, max is 85000000
illuminance_multiplier = .000003
#output_filename = "/home/pi/readings.csv"
output_filename = "/home/pi/readings.csv"
spectra_filename = "/home/pi/spectra.csv"
#address = "192.168.42.1"
#address = "localhost"
address = "192.168.1.114"
port = "1865"
wait = 2
use_php = True
debug_mode = False

cmd_set_integration_time_php = "http://%s/cgi-bin/setintegration.php?time=%s"
cmd_get_integration_time_php = "http://%s/cgi-bin/getintegration.php?"
cmd_get_spectrum_php = "http://%s/cgi-bin/getspectrum.php"
cmd_get_wavelengths_php = "http://%s/cgi-bin/getwavelengths.php"

cmd_set_integration_time = "\x00\x01"
cmd_get_integration_time = "\x00\x02"
cmd_set_boxcar_width = "\x00\x03"
cmd_get_boxcar_width = "\x00\x04"
cmd_set_scans_to_average = "\x00\x05"
cmd_get_scans_to_average = "\x00\x06"
cmd_set_target_url = "\x00\x07"
cmd_get_target_url = "\x00\x08"
cmd_get_spectrum = b'\x00\x09'
cmd_get_wavelengths = b'\x00\x0A'
cmd_get_serial_number = "\x00\x0B"
cmd_get_name = "\x00\x0C"
cmd_get_version = "\x00\x0D"
cmd_get_calibration_coefficients_from_buffer = "\x00\x0E"
cmd_set_calibration_coefficients_to_buffer = "\x00\x0F"
cmd_get_calibration_coefficients_from_eeprom = "\x00\x10"
cmd_set_calibration_coefficients_to_eeprom = "\x00\x11"
cmd_get_pixel_binning_factor = "\x00\x12"
cmd_set_pixel_binning_factor = "\x00\x13"
cmd_get_integration_time_minimum = "\x00\x14"
cmd_get_integration_time_maximum = "\x00\x15"
cmd_get_intensity_maximum = "\x00\x16"
cmd_get_electric_dark_correction = "\x00\x17"
cmd_set_electric_dark_correction = "\x00\x18"
cmd_set_tec_enable = "\x00\x1A"
cmd_set_tec_temperature = "\x00\x1B"
cmd_get_tec_temperature = "\x00\x1C"
cmd_set_lamp_enable = "\x00\x1D"

cmd_get_current_status = "\x00\x20"
cmd_get_current_spectrum = "\x00\x21"
cmd_set_max_acquisitions = "\x00\x22"
cmd_get_max_acquisitions = "\x00\x23"
cmd_set_file_save_mode = "\x00\x24"
cmd_get_file_save_mode = "\x00\x25"
cmd_set_file_prefix = "\x00\x26"
cmd_get_file_prefix = "\x00\x27"
cmd_set_sequence_type = "\x00\x28"
cmd_get_sequence_type = "\x00\x29"
cmd_set_sequence_interval = "\x00\x2A"
cmd_get_sequence_interval = "\x00\x2B"
cmd_set_save_directory = "\x00\x2C"
cmd_get_save_directory = "\x00\x2D"
cmd_save_spectrum = "\x00\x2E"
cmd_start_sequence = "\x00\x2F"
cmd_pause_sequence = "\x00\x30"
cmd_resume_sequence = "\x00\x31"
cmd_stop_sequence = "\x00\x32"
cmd_get_sequence_state = "\x00\x33"
cmd_get_current_sequence_number = "\x00\x34"
cmd_set_scope_mode = "\x00\x35"
cmd_get_scope_mode = "\x00\x36"
cmd_set_scope_interval = "\x00\x37"
cmd_get_scope_interval = "\x00\x38"

no_parameters = "\x00\x00"

baseline = [1731.93736643,1714.97365795,1763.71761325,1720.62950519,1562.5243631,1399.46297286,1744.02042099,1537.77428381,1927.73757584,1429.27951403,1644.17679248,1664.06010033,1781.71039775,1740.97314153,1662.4113413,1752.522206,1512.87480517,1647.93173928,1756.3616143,1700.57131869,1743.92995219,1305.31686613,1578.24502239,1793.56623054,1659.29738619,1816.94100453,1717.15266984,1758.67182453,1500.53548825,1689.3984871,1736.24724302,1799.6742935,1659.40150181,1718.25719768,1650.73082506,1561.87628834,1659.863014,1559.30614705,1680.76715006,1809.76150123,1828.35628813,1870.21645065,1736.51191431,1694.47397268,2007.04265585,1566.51166189,1311.69186101,1893.5966283,1464.84152017,1705.73573077,1440.52953906,1439.74945823,1471.08803152,1374.70415444,1647.94750202,1333.52364688,1711.86751413,1614.47545778,1764.19569876,1509.80119499,1459.10385112,1589.37436043,1610.67033298,1620.5653681,1723.64579452,1876.01190862,1768.23521291,1802.7722379,1718.89705739,1564.83494687,1296.78523656,1863.75325786,1715.30693647,1849.81429581,1691.29027929,1680.93477247,1650.14356118,1818.60157521,1733.23221154,1834.52439206,1636.85023382,1638.09813713,1706.89249671,1701.16995011,1609.12114902,1731.96350134,1393.93967024,1853.61860902,1603.64796935,1814.49487233,1650.78581529,1842.30367539,1583.09810006,1794.05022233,1799.44860273,1810.48530492,1636.26171673,1735.15146158,1580.49131821,1569.33995384,1620.42225831,1591.78725539,1850.96587258,1713.88667431,1625.3191111,1728.83907174,1463.42083855,1745.18245124,1606.21379086,1189.84549226,1615.09031202,1526.52839738,1665.14065429,1719.6661666,1683.40273519,1773.50367908,1746.68785491,1675.05677894,1840.8263813,1734.17433892,1820.23485759,1483.88984639,1459.33733742,1898.40865156,1739.73752008,1881.08382476,1564.57913779,1034.29985225,1989.67283303,1464.2469969,1667.54080803,1600.8463599,1717.35807957,1501.80384236,1750.33095332,1773.56108794,1415.07938966,1837.25293308,1511.08093976,1883.29326827,1681.46573248,1911.13748744,1559.42885297,1728.55803655,1736.616256,1742.3795093,1782.91117253,1709.40594915,1611.78731736,1677.08916724,1403.6361978,1562.06291856,1778.48233438,1637.76577544,1578.26919625,1730.61349207,1740.16078649,1733.880191,1826.85610125,1641.01088582,1666.39839326,1701.1206776,1608.49879371,1824.50990771,1625.17678884,1510.91855721,1654.51035899,1824.38449418,1724.00489067,1814.69242733,1452.57175279,1652.11345144,1750.39459191,1742.98420692,1502.94086953,1506.53064434,1805.08524766,1694.10539611,1693.10623478,1379.30215422,1758.09224825,1755.38629154,1730.25104518,1795.19925087,1864.07829182,1348.38367624,1493.42589312,1602.70022819,1614.54281823,1745.54787978,1245.86175067,1467.61173135,1625.39521399,1807.31972626,1732.82010714,1579.14132067,1452.8026809,1323.31621935,1669.07025417,1880.75759912,1783.13539908,1805.34298567,1386.04734852,1456.25758214,1617.12057331,1684.58146373,1778.33440744,1288.74376836,1636.38019179,1877.37207857,1801.34858607,1937.67678237,1612.62699299,1692.22874567,1510.49297459,1691.70684227,1895.38212661,1453.99797638,1787.05823956,1845.92442444,1723.48876003,1552.05046543,1845.41274663,1726.91706713,1488.97491667,1712.60462254,1112.20077182,1859.02062648,1848.02742893,1609.13294974,1612.49124851,1557.88902748,1820.70148145,1901.11976381,1755.04490798,1782.54437499,1560.92441974,1432.00341278,1740.72790746,1613.95704753,1683.36530259,1919.37008875,1740.11118642,1570.76952811,1699.48801344,1686.53672407,1722.01352808,1577.77084318,1782.02188882,1803.42290919,1565.44103928,1533.91115026,1754.7527278,1577.59842086,1597.51003987,1584.57248028,1673.66710245,1661.14083329,1770.86645399,1506.14214611,1569.19527833,1755.82997787,1697.822407,1872.43813524,1789.89862228,1818.78612841,1775.12970912,1661.88932837,1708.37675169,1589.80614782,1713.01084421,1576.87901111,1749.58913058,1615.47723194,1748.45764299,1766.41054244,1607.67166906,1727.19207837,1387.80365342,1795.91661103,1744.74428295,1644.95099193,1605.78156467,1592.5594298,1906.42710883,1568.59561432,1887.0556964,1347.89512717,1165.17708129,1883.32493014,1647.0389585,1786.31165064,1631.41823598,1691.18800843,1767.98274661,1797.75547091,1600.09288319,1879.27991124,1425.74070401,1800.1819611,1562.55902061,1752.45097186,1636.98389992,1704.79860505,1662.82914956,1825.98656451,1654.01952803,1657.72989108,1814.64454684,1737.08358312,1374.80451157,1592.24387108,1671.87118098,1465.52476704,1890.96034178,1698.22466274,1811.31620174,1618.79182564,1482.31058385,1814.78870193,1448.13847712,1701.93869293,1755.57807773,1757.52271312,1753.74293506,1885.03359696,1757.38402279,1630.90812533,1554.99052426,1800.96705082,1566.76808167,1578.08230677,1743.14067849,1445.77012815,1762.20020907,1452.58752871,1717.59331521,1806.62457592,1587.17528377,1956.40918487,1649.40720068,1601.80729015,1505.54444884,1851.43091328,1628.89073232,1277.73444915,1772.70591864,1473.67524442,1840.97639295,1643.25344049,1802.13227659,1733.57038312,1760.25563034,1359.14671159,1884.67200168,1727.15601331,1464.82280073,1513.3002417,1746.011804,1688.03635152,1582.8147754,1470.76230118,1746.2385999,1504.09756654,1871.53802757,1716.50704098,1675.83081346,1619.45877243,1678.20961663,1914.99430004,1558.09516777,1577.48396853,1819.05076966,1816.59168558,1660.7705668,1603.56107647,1809.99426754,1720.26591698,1539.44839866,1778.52482592,1674.97895471,1758.58174804,1663.41371644,1609.88930782,1888.17062927,1574.46652739,1789.32125223,1636.31311747,1514.06318256,1478.88548084,1811.92308278,1771.54856119,1928.90579678,1643.15661921,1824.5943717,1635.40026663,1894.87893856,1346.72969454,1435.74778258,1705.12807057,1536.91118313,1650.5121905,1633.27415415,1618.32054683,1566.65495642,1608.87890424,1773.00522792,1647.81851372,1463.3790225,1816.15743521,1437.74402128,1656.16793179,1877.65341274,1919.4263821,1661.7798516,1689.93314917,1724.67479434,1921.46636053,1549.3796888,1749.92159198,1533.08849213,1804.14059897,996.22977884,1486.54047396,1904.29942636,1694.20524463,1617.96396675,1615.46676747,1742.32827327,1646.72711566,1884.3574848,1660.28715426,1774.3033923,1901.50600455,1560.39146371,1856.94055706,1511.51850695,1806.11913582,1471.66125993,1533.410371,1656.62839821,1850.5053487,1574.05544415,1788.72808654,1754.76995392,1586.74772784,1757.39471561,1665.98026689,1827.7862282,1845.54618084,1589.98790485,1570.42645199,1708.43113595,1818.54945948,1758.76713881,1553.00334441,1703.08510025,1847.67839902,1576.55106154,1704.41719032,1828.2759452,1633.85024057,1472.32341462,1740.73986565,1761.67533626,1845.75002678,1624.25002502,1634.84342734,1575.13209699,1625.07583412,1672.62067157,1660.11649365,1784.21873037,1848.35180083,1729.03446189,1595.77476544,1556.97730021,1563.92557986,1740.6501929,1688.46872451,1607.65533168]

def sts_command(tn, cmd):
	tn.open(address, port)
	sleep(wait)
	print("Connected to address %s / port %s" % (address, port))
	#print("Command %s" % cmd)
	# msg = cmd_get_wavelengths+no_parameters
	# msg = b'%s%s' % (cmd_get_spectrum,no_parameters)
	# msg = b'\x00\x09\x00\x00'
	# msg = cmd
	sleep(wait)
	tn.write(cmd)
	sleep(wait)
	return(tn.read_all())


def main():
	global address
	global port

	# parse for command line variables
	usage = "usage: %prog [options] arg"
	parser = OptionParser(usage)
	parser.add_option("-a","--address", dest="address", help="define IP address of raspberry pi with STS ")
	parser.add_option("-p","--port", dest="port", help="raspberry pi telnet port for communication with STS")

	(options, args) = parser.parse_args()

	if len(args) != 1:
		if options.address != None:
			address = options.address
		if options.port != None:
			port = options.port

	print("OceanOptics Spectrometer")
	print("Raspberry Pi STS address: "+address)
	print("Raspberry Pi STS port: "+port)

	print("Opening datalogging file %s" % output_filename)
	outf = open(output_filename, "a")
	print("Opening spectral output file %s" % spectra_filename)
	spf = open(spectra_filename, "a")

	# open telnet connection to Raspberry Pi with Ocean Optics STS spectrometer
	if not use_php:
		tn = Telnet()
		sleep(wait)

	if use_php:
		# get integration time
		integration_time = urllib2.urlopen(cmd_get_integration_time_php % (address)).read()
		print("original integration time = %s" % integration_time)

		# set integration time
		urllib2.urlopen(cmd_set_integration_time_php % (address, desired_integration_time))
		integration_time = urllib2.urlopen(cmd_get_integration_time_php % (address)).read()
		print("integration time set to = %s" % integration_time)

		# get integration time to check
		integration_time = urllib2.urlopen(cmd_get_integration_time_php % (address)).read()
		print("new integration time = %s" % integration_time)

	# get wavelengths
	if not use_php:
		cmd = b'%s%s' % (cmd_get_wavelengths,no_parameters)
		wavelengths = sts_command(tn, cmd).split()[1:]
	else:
		wavelengths_raw = urllib2.urlopen(cmd_get_wavelengths_php % (address)).read().split()
		print(cmd_get_wavelengths_php % (address))

	# get spectrum
	if not use_php:
		cmd = b'%s%s' % (cmd_get_spectrum,no_parameters)
		spectrum = sts_command(tn, cmd).split()[1:]
	else:
		print(cmd_get_spectrum_php % (address))
		spectrum_raw = urllib2.urlopen(cmd_get_spectrum_php % (address)).read().split()


	# close connection
	if not use_php:
		tn.close()

	#spectrum = spectrum_raw
	#wavelengths = wavelengths_raw
	spectrum = array(spectrum_raw, dtype=float)
	wavelengths = array(wavelengths_raw, dtype=float)

	if debug_mode:
		print(wavelengths[0:10], wavelengths[-10:])
		print(spectrum[0:10], spectrum[-10:])
		print(len(wavelengths),len(spectrum))

	# normalise the spectrum so that the values are between 0 and 1
	normalizedSpectrum = normalize(spectrum,'max').reshape(-1,1)

	# resample the spectrum so that the sampling is every nanometer
	#resampledSpectrum = resample(normalizedSpectrum,824-344+1)
	resampledSpectrum = resample(spectrum,824-344+1)
	offsetSpectrum = resampledSpectrum - baseline

	# create a linear integer space arrangement with x between 380 and 730 nm
	# wavelengths1nm = np.linspace(380,730,730-380+1)
	wavelengths1nm = np.linspace(344,824,824-344+1)

	if debug_mode:
		#print(resampledSpectrum)
		#print(wavelengths1nm[0:10], wavelengths1nm[-10:])
		#print(resampledSpectrum[0:10], resampledSpectrum[-10:])
		print(len(wavelengths1nm),len(offsetSpectrum))

	# plot the new resampled, smoothed spectrum, transposed between 380 and 730 nm
	#plt.plot(xx,resampledSpectrum)

	# create spectral power distribution (SPD)
	spd_data = dict(izip(wavelengths1nm, offsetSpectrum))
	# print(spd_data)
	# plt.plot(spectrum)
	# plt.show()

	# convert numpy array to colour library SPD
	spd = colour.SpectralPowerDistribution('SPD', spd_data)
	#print(dir(spd))
	#print(spd.wavelengths)

	# plot the spectrum using the Colour library
	if debug_mode:
		single_spd_plot(spd)
		#single_cctf_plot(spd)

	# calculate the sample spectral power distribution *CIE XYZ* tristimulus values
	# using the CIE 1931 2 degree standard observer and D65 (daylight) standard illuminant
	cmfs = colour.STANDARD_OBSERVERS_CMFS['CIE 1931 2 Degree Standard Observer']
	illuminant = colour.ILLUMINANTS_RELATIVE_SPDS['D65']
	XYZ = colour.spectral_to_XYZ(spd, cmfs, illuminant)
	print('XYZ = ', XYZ)

	# calculate *xy* chromaticity coordinates for the spectrum
	xy = colour.XYZ_to_xy(XYZ)
	print('xy = ', xy)

	# display the colour coordinate of the spectral sample in the CIE chromaticity diagram

	# plot the *CIE 1931 Chromaticity Diagram* including the Planckian Locus
	# the argument *standalone=False* is passed so that the plot doesn't get displayed
	# and can be used as a basis for other plots
	#CIE_1931_chromaticity_diagram_plot(standalone=False)
	if debug_mode:
		planckian_locus_CIE_1931_chromaticity_diagram_plot(standalone=False)

		# plot the *xy* chromaticity coordinates of the spectrum
		x, y = xy

		pylab.plot(x, y, 'o-', color='white')

		# Annotating the plot.
		pylab.annotate(spd.name.title(),
		               xy=xy,
		               xytext=(-50, 30),
		               textcoords='offset points',
		               arrowprops=dict(arrowstyle='->', connectionstyle='arc3, rad=-0.2'))

		# Displaying the plot.
		display(standalone=True)

	# Get timestamp
	ts = time.time()
	#print(time.time(), prev_time)
	datestr = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

	# Calculate CCT and luminous flux
	CCT = colour.temperature.xy_to_CCT(xy)
	luminous_flux = colour.luminous_flux(spd)*illuminance_multiplier
	output_str = datestr+','+str(xy[0])+','+str(xy[1])+','+str(CCT)+','+str(luminous_flux)
	print(output_str)
	outf.write(output_str+'\n')
	outf.flush()
	outf.close()
	spf.write(datestr+','+','.join(map(str, resampledSpectrum)) +'\n')
	spf.close()


if __name__ == "__main__":
	main()


""" Scrap

	# tn.open(address, port)
	# sleep(wait)
	# print("Connected to address %s / port %s" % (address, port))
	# # msg = cmd_get_wavelengths+no_parameters
	# msg = b'%s%s' % (cmd_get_wavelengths,no_parameters)
	# # msg = b'\x00\x0A\x00\x00'
	# sleep(wait)
	# tn.write(msg)
	# sleep(wait)
	# wavelengths = tn.read_all().split()[1:]

	# tn.open(address, port)
	# sleep(wait)
	# print("Connected to address %s / port %s" % (address, port))
	# # msg = cmd_get_wavelengths+no_parameters
	# msg = b'%s%s' % (cmd_get_spectrum,no_parameters)
	# # msg = b'\x00\x09\x00\x00'
	# sleep(wait)
	# tn.write(msg)
	# sleep(wait)
	# spectrum = tn.read_all().split()[1:]

"""
