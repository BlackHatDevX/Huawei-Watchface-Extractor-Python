# Huawei Watchface Extractor Python

The Huawei Watchface Extractor is a Python script that allows you to extract images from HWT or com.huawei.watchface files. It can be useful if you want to extract images from a Huawei watchface for further analysis or customization.

## Prerequisites

- Python 3.x
- Pillow library (for image manipulation)

## Installation

1. Clone this repository or download the `watchface_extractor.py` file.
2. Install the necessary dependencies by running the following command:
```
pip install Pillow
```

## Usage

Run the script from the command line using the following command:
```
python watchface_extractor.py input_file.hwt [output_directory]
```

- input_file.hwt: Path to the HWT or com.huawei.watchface file from which you want to extract images.
- output_directory (optional): Path to the directory where the extracted images will be saved. If not provided, a new directory with the name `<input_file>_extra` will be created in the same location as the input file.

The extracted images will be saved as PNG files in the output directory.

## Example

```
python watchface_extractor.py watchface.hwt extracted_images
```

This will extract the images from watchface.hwt and save them in the extracted_images directory.

## Limitations

Please note that this script might not work correctly with all versions or types of Huawei watchfaces. It has been tested with a range of watchfaces, but there can be variations in the file format or image encoding.

For now it cannot decrypt watchfaces with password encryption, if someone is willing to help for that you are welcome to contribute.

## TODO

Encrypted Watchfaces Fix (Watchface Decrypter)

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any inquiries or questions, you can reach out to the project developer:

- Developer's Portfolio: [bit.ly/jashgro](https://bit.ly/jashgro)
- Telegram: [@developer_x](https://telegram.dog/deveioper_x)
- Support Group: [@huawei_watchfaces](https://telegram.dog/huawei_watchfaces)
