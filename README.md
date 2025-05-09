# GNSS-Interferometric Reflectometry Processing pipeline (Hong Kong SatRef)


## Overview
This is an implementation processing pipeline for the GNSS-Interferometric Reflectometry (GNSS-IR) for the LandsD SatRef stations. 

GNSS Interferometric Reflectometry is a technique that utilizes a static GNSS station to estimate the height of a reflective surface by analyzing multipath-induced variations in Signal-to-Noise Ratio (SNR) data. The station placed in an area with significant multipath signals, without any cutoff angle, and collects observations including signal strength (S1, S2, S5). It works by analyzing variations in the strength of GNSS signals (S1, S2, S5) caused by reflections (multipath) and relating these changes in Signal-to-Noise Ratio (SNR) to the height of the reflecting surface relative to the receiver.

![GNSS-IR Diagram](https://ottoyu.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fc4e8033b-5afd-4c51-9316-1fb82594c1c2%2F1ed18e92-0471-4563-aa77-858623db2354%2FUntitled.png?table=block&id=12375a61-ffad-4518-b9c6-fb4e7114241b&spaceId=c4e8033b-5afd-4c51-9316-1fb82594c1c2&width=2000&userId=&cache=v2)

## List of ready to use tools 
* satref2rinex (self-developed in this package, to download and unzip the RINEX3 from LandsD Satref) 
* rinex_convert (self-developed in this package, to convert the RINEX 3 to RINEX2)
* rinex2snr (funtion from gnssrefl)
* gnssir_input (funtion from gnssrefl)
* gnssir (funtion from gnssrefl)
* subdaily (funtion from gnssrefl)
Ongoing developments: 
* tide_ref (ongoing developing, to download the tide data from sea level monitoring station)
* compare_gnss (ongoing developing, to compare the tide data and GNSS IR reflector height) 


## Potential stations can be adopted in Hong Kong 
* Coastal: HKQT, HKPC, KYC1 (not too significant and good result) 
* Hillside: HKWS, HKSS

## Steps

1. Download and derived the signal strength from the RINEX data 
2. Original SMO provide RINEX3 in .crx (compress format) 
3. Unzip the .gz file and decompress the .crx file into RINEX3
4. Convert the data into RINEX2 (more simple to derive and read)
5. Download the precise orbit data from the IGS 
6. Compute the satellite coordinate by the navigation message 
7. Compute the elevation and azimuth angle from the satellite to the station 
8. Create a file stored the SNR, azimuth, elevation and time (per day)
9. Compute the reflector height using LSP and SNR 
10. Assess the reflector height correctness using time series analysis 
11. Compare the tide gauge with the derived reflector height with correlation 




