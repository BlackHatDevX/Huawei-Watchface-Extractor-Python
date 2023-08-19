import os
import zipfile
from PIL import Image

class ImageExtractor:
    def __init__(self):
        self.sign = [85, 85, 85, 85]
        self.current_color = None
        self.current_color_count = 0

    def read(self, bin_file, output_dir):
        data_in = None
        zis = None

        if bin_file.endswith(".hwt"):
            found_entry = False
            zis = zipfile.ZipFile(bin_file, 'r')
            for zip_entry in zis.namelist():
                if zip_entry == "com.huawei.watchface":
                    data_in = zis.open(zip_entry)
                    found_entry = True
                    break
            if not found_entry:
                print(f"The archive {bin_file} doesn't contain com.huawei.watchface file")
                return
        else:
            data_in = open(bin_file, 'rb')

        sign_flag = 0
        file_size = os.path.getsize(bin_file)

        for i in range(file_size):
            tmp = data_in.read(1)[0]
            if self.sign[sign_flag] == tmp:
                sign_flag += 1
            else:
                sign_flag = 0

            if sign_flag >= 4:
                print(f"sign position->{i}")
                break

        data_in.read(4)  # Skip 4 bytes
        output_dir = os.path.abspath(output_dir)
        os.makedirs(output_dir, exist_ok=True)
        ims_list = []
        print("Start parsing pictures")
        err_flag = False

        while not err_flag:
            try:
                img = self.read_img(data_in)
                ims_list.append(img)
            except Exception:
                err_flag = True

        print("Start outputting pictures")

        for i, img in enumerate(ims_list):
            print(f"Start outputting picture {i}")
            img_path = os.path.join(output_dir, f"{i}.png")
            img.save(img_path, "PNG")

        print("End of output pictures")
        if zis is not None:
            zis.close()
        data_in.close()

    def read_img(self, data_in):
        header = f"{data_in.read(1).hex()}{data_in.read(1).hex()}{data_in.read(1).hex()}{data_in.read(1).hex()}"
        width1 = data_in.read(1)[0]
        width2 = data_in.read(1)[0]
        height1 = data_in.read(1)[0]
        height2 = data_in.read(1)[0]
        width = width1 + (width2 << 8)
        height = height1 + (height2 << 8)
        print(f"Width->{width}, Height->{height}")
        img = Image.new("RGBA", (width, height))

        for i in range(height):
            for j in range(width):
                c = self.read_color(data_in)
                img.putpixel((j, i), c)

        return img

    def read_color(self, data_in):
        if self.current_color_count > 0:
            self.current_color_count -= 1
            return self.current_color
        else:
            blue = data_in.read(1)[0]
            green = data_in.read(1)[0]
            red = data_in.read(1)[0]
            alpha = data_in.read(1)[0]
            if blue == 137 and green == 103 and red == 69 and alpha == 35:
                blue = data_in.read(1)[0]
                green = data_in.read(1)[0]
                red = data_in.read(1)[0]
                alpha = data_in.read(1)[0]
                l1 = data_in.read(1)[0]
                l2 = data_in.read(1)[0]
                l3 = data_in.read(1)[0]
                l4 = data_in.read(1)[0]
                count = (l4 << 24) + (l3 << 16) + (l2 << 8) + l1
                self.current_color_count = count - 1
                self.current_color = (red, green, blue, alpha)
                return self.current_color
            else:
                return (red, green, blue, alpha)

def main():
    import sys

    if len(sys.argv) < 2 or "-?" in sys.argv or "/?" in sys.argv:
        show_help()
        sys.exit(0)

    input_file = sys.argv[1]
    output_dir = input_file + "_extra" if len(sys.argv) < 3 else sys.argv[2]

    try:
        extractor = ImageExtractor()
        extractor.read(input_file, output_dir)
    except Exception as e:
        print("An error occurred:", str(e))
        sys.exit(-1)

    sys.exit(0)

def show_help():
    arg_format = "%-10s"
    print("Extract images from HWT or com.huawei.watchface file")
    print("Usage: python watchface_extractor.py input_file.hwt [output_directory]")
    print(f"\t{arg_format}*.hwt or com.huawei.watchface file")
    print(f"\t{arg_format}optional output directory for extracted images. Defaults to <input>_extra")

if __name__ == "__main__":
    main()
