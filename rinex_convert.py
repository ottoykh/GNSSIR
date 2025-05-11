import os
import subprocess
from pathlib import Path
import argparse  

def rinex_convert(input_folder: str, gfzrnx_exe: str, doy_start: int, doy_end: int, station_name: str, year: int, output_folder: str = None) -> None:
    """
    Converts RINEX files using the gfzrnx executable.

    This function iterates through a range of day-of-year (DOY) values,
    checks for the existence of a corresponding RINEX file in the specified
    input folder, and converts it to a specified RINEX version using the
    gfzrnx executable.  The function now accepts a station name as a parameter
    to allow for flexible filename construction.

    Args:
        input_folder (str): The path to the folder containing the input RINEX files.
            Filenames are expected to follow the pattern: {station_name}00HKG_R_{year}{doy_str}0000_01D_30S_MO.rnx
        gfzrnx_exe (str): The path to the gfzrnx executable.
        doy_start (int): The starting day-of-year (DOY) for the conversion range.
        doy_end (int): The ending day-of-year (DOY) for the conversion range (inclusive).
        station_name (str): The four-character station name (e.g., HKPC).  This is used
            in the input and output filenames.
        year (int): The year of the RINEX files.
        output_folder (str, optional): The path to the folder where the converted
            RINEX files will be saved. If None, the converted files will be saved
            in the current working directory. Defaults to None.

    Returns:
        None. The function converts files and saves them to the specified output directory.

    Raises:
        FileNotFoundError: If the gfzrnx executable is not found at the specified path.
        subprocess.CalledProcessError: If the gfzrnx command returns a non-zero exit code,
            indicating an error during conversion.
    """

    # Check if gfzrnx_exe exists
    if not os.path.exists(gfzrnx_exe):
        raise FileNotFoundError(f"gfzrnx executable not found at: {gfzrnx_exe}")

    # Determine the output folder
    if output_folder is None:
        output_folder = os.getcwd()  # Current working directory
    else:
        # Create the output directory if it doesn't exist
        Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Iterate through the specified range of DOY values
    for doy in range(doy_start, doy_end + 1):
        doy_str = f"{doy:03d}"  # Format DOY as three digits
        input_file = os.path.join(input_folder, f"{station_name}00HKG_R_{year}{doy_str}0000_01D_30S_MO.rnx")
        year_short = str(year % 100)

        # Check if the input file exists
        if os.path.exists(input_file):
            output_file = os.path.join(output_folder, f"{station_name.lower()}{doy_str}0.{year_short}o")

            # Construct the command
            command = [
                gfzrnx_exe,
                "-finp", input_file,
                "-fout", output_file,
                "-vo", "2.11"
            ]

            try:
                # Execute the command
                subprocess.run(command, check=True)  # Raise exception on non-zero exit code
                print(f"Processed: {input_file} -> {output_file}")
            except subprocess.CalledProcessError as e:
                print(f"Error processing {input_file}: {e}")

        else:
            print(f"Skipping: {input_file} (File not found)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert RINEX files using gfzrnx.")
    parser.add_argument("input_folder", help="Path to the input RINEX files")
    parser.add_argument("gfzrnx_exe", help="Path to the gfzrnx executable")
    parser.add_argument("doy_start", type=int, help="Starting day-of-year")
    parser.add_argument("doy_end", type=int, help="Ending day-of-year")
    parser.add_argument("station_name", help="Four-character station name")
    parser.add_argument("year", type=int, help="Year of the RINEX files")
    parser.add_argument("-output_folder", help="Path to the output folder (optional)", default=None)
    args = parser.parse_args()

    rinex_convert(
        input_folder=args.input_folder,
        gfzrnx_exe=args.gfzrnx_exe,
        doy_start=args.doy_start,
        doy_end=args.doy_end,
        station_name=args.station_name,
        year=args.year,
        output_folder=args.output_folder,
    )
