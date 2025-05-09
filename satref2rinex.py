import requests
import gzip
import shutil
from pathlib import Path
import os
import sys  
import hatanaka 

def satref2rinex(year: int, doy_start: int, doy_end: int, station_id: str, output_directory: str = None) -> None:
    """
    Downloads, unzips, and converts Satellite Reference (SATREF) RINEX files from the Hong Kong Geodetic Survey.

    This function downloads compressed RINEX observation files (.crx.gz) for a specified year,
    day-of-year (DOY) range, and station ID from the Hong Kong Geodetic Survey's online archive.
    It then unzips the downloaded files and converts the .crx files to standard .rnx RINEX format
    using the `hatanaka.decompress_on_disk` function (assumed to be available in the environment).

    Args:
        year (int): The year for which to download the RINEX files.
        doy_start (int): The starting day-of-year (DOY) for the download range.
        doy_end (int): The ending day-of-year (DOY) for the download range (inclusive).
        station_id (str): The four-character station ID (e.g., 'HKST').  Case-insensitive.
        output_directory (str, optional): The directory where downloaded and converted files will be saved.
            If None, a directory named 'downloaded_rinex_files/{year}' will be created in the current
            working directory. Defaults to None.

    Returns:
        None.  The function downloads and converts files to the specified output directory.

    Raises:
        requests.exceptions.RequestException: If there is an issue downloading a file from the server.
        Exception: For any other errors during file processing (e.g., unzipping, conversion).

    Example:
        satref2rinex(2023, 1, 5, 'HKST', 'path/to/output/directory')
    """

    # Define the base URL
    base_url = "https://rinex.geodetic.gov.hk/rinex3/{year}/{doy}/{stationL}/30s/{stationU}00HKG_R_{year}{doy}0000_01D_30S_MO.crx.gz"

    # Create a directory to save the downloaded files
    if output_directory is None:
        output_dir = Path(f"downloaded_rinex_files/{year}")
    else:
        output_dir = Path(output_directory)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Loop through the specified range of DOY
    for doy in range(doy_start, doy_end + 1):
        # Format the DOY to be three digits
        doy_formatted = f"{doy:03}"
        stationL = station_id.lower()
        stationU = station_id.upper()

        # Construct the URL
        url = base_url.format(year=year, doy=doy_formatted, stationL=stationL, stationU=stationU)

        # Construct file names and paths
        gz_file_name = f"{stationU}00HKG_R_{year}{doy_formatted}0000_01D_30S_MO.crx.gz"
        gz_file_path = output_dir / gz_file_name
        rnx_file_name = gz_file_name.replace('.gz', '')
        rnx_file_path = output_dir / rnx_file_name
        rnx_converted_file_path = rnx_file_path.with_suffix('.rnx')


        try:
            # Check if the final .rnx file already exists
            if rnx_converted_file_path.exists():
                print(f"Skipping {url}: {rnx_converted_file_path} already exists.")
                continue

            # Download the file
            response = requests.get(url, stream=True)  # Use stream=True for large files
            response.raise_for_status()  # Raise an error for bad responses

            # Save the .gz file with the original naming convention
            with open(gz_file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):  # Stream the download
                    file.write(chunk)

            print(f"Downloaded: {gz_file_path}")

            # Unzip the .gz file
            with gzip.open(gz_file_path, 'rb') as f_in:
                with open(rnx_file_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            print(f"Unzipped: {rnx_file_path}")

            # Convert .crx to .rnx
            # Assuming hatanaka.decompress_on_disk correctly handles decompression and renaming
            hatanaka.decompress_on_disk(str(rnx_file_path))

            # Check if the file was correctly decompressed and renamed
            if rnx_converted_file_path.exists():
                 print(f"Converted to .rnx: {rnx_converted_file_path}")
            else:
                print(f"Error: Conversion to .rnx failed for {rnx_file_path}")

        except requests.exceptions.RequestException as e:
            print(f"Failed to download {url}: {e}")
        except Exception as e:
            print(f"Error processing file {gz_file_path}: {e}")
        finally:
            # Clean up .crx and .gz files if conversion was successful
            if rnx_converted_file_path.exists():
                try:
                    os.remove(gz_file_path)
                    os.remove(rnx_file_path)
                    print(f"Cleaned up: {gz_file_path} and {rnx_file_path}")
                except OSError as e:
                    print(f"Error deleting temporary files: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: satref2rinex.py <year> <doy_start> <doy_end> <station_id> <output_directory>")
        sys.exit(1)
    try:
        year = int(sys.argv[1])
        doy_start = int(sys.argv[2])
        doy_end = int(sys.argv[3])
        station_id = sys.argv[4]
        output_directory = sys.argv[5]
    except ValueError:
        print("Error: Year, doy_start, and doy_end must be integers.")
        sys.exit(1)
    except Exception as e:
        print(f"Error parsing arguments: {e}")
        sys.exit(1)
    satref2rinex(year, doy_start, doy_end, station_id, output_directory)