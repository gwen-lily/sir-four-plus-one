from PIL import Image, ImageFilter
import pathlib

def main():
	LL_dir = pathlib.Path('LL')

	img1 = Image.open(LL_dir.joinpath('LL1.png'))
	img2 = Image.open(LL_dir.joinpath('LL2.png'))
	img3 = Image.open(LL_dir.joinpath('LL3.png'))
	eden = Image.open(LL_dir.joinpath('eden llama.jpg'))

	print(img1.size, img2.size, img3.size, eden.size)  # 191, 191

	img = Image.new('RGBA', (img1.size[0], 3*img1.size[1]), (0, 0, 0, 0))

	img.paste(img1, (0, 0))
	img.paste(img2, (0, img1.size[0] + 1))
	img.paste(img3, (0, 2*img1.size[0] + 2))
	img.save(LL_dir.joinpath('LL.png'), "PNG")
	img.show()


if __name__ == '__main__':
	main()
